"""MQTT feeder application for German Waters Hydrology → Unified Namespace.

Reuses the upstream HTTP providers and station catalog logic from the existing
``german_waters`` Kafka bridge and pushes CloudEvents into MQTT 5.0 using the
xrcg-generated :class:`DEWatersHydrologyMqttMqttClient`.

Topic tree: ``hydro/de/wsv/german-waters/{water_body}/{station_id}/{info|water-level}``.
``{water_body}`` is sourced from the per-provider station catalog
(field ``water_body``) and normalized to lowercase kebab-case by
:func:`_uns_slug` so umlauts, spaces and slashes never reach the broker.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from german_waters.german_waters import (
    PROVIDER_CLASSES,
    _load_state,
    _resolve_providers,
    _save_state,
    _station_to_event,
)
from german_waters.providers import BaseProvider, ObservationData, StationData
from german_waters_mqtt_producer_data import Station, WaterLevelObservation
from german_waters_mqtt_producer_mqtt_client.client import DEWatersHydrologyMqttMqttClient
import json
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id

    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)

def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"

    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or "")

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    return resolved_client_id, resolved_username, resolved_password

logger = logging.getLogger(__name__)

_UNS_REPLACEMENTS = str.maketrans({
    "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u", "ß": "ss",
    "à": "a", "á": "a", "â": "a", "è": "e", "é": "e", "ê": "e",
    "ì": "i", "í": "i", "î": "i", "ò": "o", "ó": "o", "ô": "o",
    "ù": "u", "ú": "u", "û": "u", "ç": "c", "ñ": "n",
})

def _uns_slug(value: str) -> str:
    """Normalize an arbitrary upstream label to a UNS-safe lowercase kebab segment."""
    if not value:
        return "unknown"
    raw = value.translate(_UNS_REPLACEMENTS).lower().strip()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in ("-", "_"):
            out.append(ch)
        else:
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"

def _station_to_mqtt_event(s: StationData) -> Station:
    """Convert internal StationData to the MQTT producer dataclass."""
    return Station(
        station_id=s.station_id,
        station_name=s.station_name,
        water_body=s.water_body,
        state=s.state or None,
        region=s.region or None,
        provider=s.provider,
        latitude=s.latitude or None,
        longitude=s.longitude or None,
        river_km=s.river_km or None,
        altitude=s.altitude or None,
        station_type=s.station_type or None,
        warn_level_cm=s.warn_level_cm or None,
        alarm_level_cm=s.alarm_level_cm or None,
        warn_level_m3s=s.warn_level_m3s or None,
        alarm_level_m3s=s.alarm_level_m3s or None,
    )

def _obs_to_mqtt_event(o: ObservationData, water_body: str) -> WaterLevelObservation:
    """Convert internal ObservationData to the MQTT producer dataclass."""
    wl_ts = None
    if o.water_level_timestamp:
        try:
            wl_ts = datetime.fromisoformat(o.water_level_timestamp)
        except (ValueError, TypeError):
            pass
    dis_ts = None
    if o.discharge_timestamp:
        try:
            dis_ts = datetime.fromisoformat(o.discharge_timestamp)
        except (ValueError, TypeError):
            pass
    return WaterLevelObservation(
        station_id=o.station_id,
        provider=o.provider,
        water_body=water_body,
        water_level=o.water_level or None,
        water_level_unit=o.water_level_unit or None,
        water_level_timestamp=wl_ts,
        discharge=o.discharge or None,
        discharge_unit=o.discharge_unit or None,
        discharge_timestamp=dis_ts,
        trend=o.trend or None,
        situation=o.situation or None,
    )

async def _publish_stations(
    mqtt_client: DEWatersHydrologyMqttMqttClient,
    providers: List[BaseProvider],
) -> Dict[str, str]:
    """Publish station info events. Returns station_id → water_body map."""
    station_water_map: Dict[str, str] = {}
    for provider in providers:
        try:
            stations = provider.get_stations()
        except Exception as exc:
            logger.error("Error fetching stations from %s: %s", provider.name, exc)
            continue
        for s in stations:
            water_slug = _uns_slug(s.water_body or "unknown")
            station_water_map[s.station_id] = s.water_body or "unknown"
            await mqtt_client.publish_de_waters_hydrology_mqtt_station(
                station_id=s.station_id,
                water_body=water_slug,
                data=_station_to_mqtt_event(s),
            )
    return station_water_map

async def _publish_observations(
    mqtt_client: DEWatersHydrologyMqttMqttClient,
    providers: List[BaseProvider],
    station_water_map: Dict[str, str],
    previous_readings: Dict[str, str],
) -> int:
    """Publish observation events. Returns count of published messages."""
    sent = 0
    for provider in providers:
        try:
            if hasattr(provider, 'invalidate'):
                provider.invalidate()
            observations = provider.get_observations()
        except Exception as exc:
            logger.error("Error fetching observations from %s: %s", provider.name, exc, exc_info=True)
            continue
        for o in observations:
            ts_key = o.water_level_timestamp or o.discharge_timestamp
            if not ts_key:
                continue
            prev_ts = previous_readings.get(o.station_id)
            if prev_ts == ts_key:
                continue
            water_body_raw = station_water_map.get(o.station_id, "unknown")
            water_slug = _uns_slug(water_body_raw)
            try:
                await mqtt_client.publish_de_waters_hydrology_mqtt_water_level_observation(
                    station_id=o.station_id,
                    water_body=water_slug,
                    data=_obs_to_mqtt_event(o, water_body_raw),
                )
                sent += 1
                previous_readings[o.station_id] = ts_key
            except Exception as exc:
                logger.error("Error publishing observation for %s: %s", o.station_id, exc)
    return sent

async def feed(
    providers: List[BaseProvider],
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    previous_readings = _load_state(state_file)

    resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if resolved_username or resolved_password:
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    mqtt_client = DEWatersHydrologyMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    provider_names = ", ".join(p.name for p in providers)
    logger.info("Publishing station info events for providers: [%s]", provider_names)
    station_water_map = await _publish_stations(mqtt_client, providers)
    logger.info("Published %d station info events", len(station_water_map))

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = await _publish_observations(
                    mqtt_client, providers, station_water_map, previous_readings
                )
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s observations in %.1fs. Sleeping until %s.",
                    count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:
                logger.error("Error during polling cycle: %s", exc, exc_info=True)
                await asyncio.sleep(polling_interval)
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple:
    from urllib.parse import urlparse
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="German Waters Hydrology → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and observations as CloudEvents to MQTT")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "900")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.german_waters_mqtt_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--providers", type=str, default=os.getenv("PROVIDERS"),
                             help="Comma-separated provider keys to include")
    feed_parser.add_argument("--exclude-providers", type=str, default=os.getenv("EXCLUDE_PROVIDERS"),
                             help="Comma-separated provider keys to exclude")
    return parser

def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

    if args.broker_url:
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (8883 if tls else 1883)
        username = args.username
        password = args.password

    providers = _resolve_providers(args.providers, args.exclude_providers)
    asyncio.run(
        feed(
            providers, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
        )
    )

if __name__ == "__main__":
    main()
