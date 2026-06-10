"""MQTT feeder application for RWS Waterwebservices → Unified Namespace.

Reuses the upstream HTTP client and station catalog logic from the existing
``rws_waterwebservices`` Kafka bridge (imported as the transport-agnostic "core"
package) and pushes CloudEvents into MQTT 5.0 using the xrcg-generated
:class:`NLRWSWaterwebservicesMqttMqttClient`.

Topic tree: ``hydro/nl/rws/rws-waterwebservices/{station_code}/{info|water-level}``.
RWS Waterwebservices does not expose a stable shared water-body axis in the
station catalog, so the MQTT tree uses station code as the stable subscriber axis.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from rws_waterwebservices.rws_waterwebservices import RWSWaterwebservicesAPI, _load_state, _save_state
from rws_waterwebservices_mqtt_producer_data import Station, WaterLevelObservation
from rws_waterwebservices_mqtt_producer_mqtt_client.client import NLRWSWaterwebservicesMqttMqttClient
import json

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

def _build_station_map(locations: List[Dict[str, Any]]) -> Dict[str, str]:
    """Build station_code → location display name map from catalog locations."""
    mapping: Dict[str, str] = {}
    for loc in locations:
        code = loc.get("Code", "")
        naam = loc.get("Naam", "")
        if code:
            mapping[code] = naam
    return mapping

async def _publish_stations(
    mqtt_client: NLRWSWaterwebservicesMqttMqttClient,
    locations: List[Dict[str, Any]],
    station_map: Dict[str, str],
) -> None:
    for loc in locations:
        code = loc.get("Code", "")
        if not code:
            continue
        naam = station_map.get(code, "")
        station = Station(
            station_code=code,
            name=naam,
            latitude=float(loc.get("Lat", 0) or 0),
            longitude=float(loc.get("Lon", 0) or 0),
            coordinate_system=loc.get("Coordinatenstelsel") or None,
        )
        await mqtt_client.publish_nl_rws_waterwebservices_mqtt_station(
            station_code=code,
            data=station,
        )

async def _publish_observations(
    api: RWSWaterwebservicesAPI,
    mqtt_client: NLRWSWaterwebservicesMqttMqttClient,
    station_codes: List[str],
    station_map: Dict[str, str],
    previous_readings: Dict[str, str],
) -> int:
    observations = api.get_latest_observations(station_codes)
    sent = 0
    for entry in observations:
        locatie = entry.get("Locatie", {})
        aquo = entry.get("AquoMetadata", {})
        unit = aquo.get("Eenheid", {}).get("Code", "cm")
        metingen_lijst = entry.get("MetingenLijst", [])

        for meting in metingen_lijst:
            tijdstip = meting.get("Tijdstip")
            meetwaarde = meting.get("Meetwaarde", {})
            waarde = meetwaarde.get("Waarde_Numeriek")

            if waarde is None or tijdstip is None:
                continue

            location_code = locatie.get("Code", "")
            reading_key = f"{location_code}:{tijdstip}"
            if reading_key in previous_readings:
                continue

            naam = station_map.get(location_code, locatie.get("Naam", ""))
            metadata = meting.get("WaarnemingMetadata", {})

            observation = WaterLevelObservation(
                station_code=location_code,
                location_name=naam or None,
                timestamp=tijdstip,
                value=float(waarde),
                unit=unit,
                quality_code=metadata.get("Kwaliteitswaardecode") or None,
                status=metadata.get("Statuswaarde") or None,
                compartment=api.COMPARTIMENT_CODE,
                parameter=api.GROOTHEID_CODE,
            )

            try:
                await mqtt_client.publish_nl_rws_waterwebservices_mqtt_water_level_observation(
                    station_code=location_code,
                    data=observation,
                )
                sent += 1
                previous_readings[reading_key] = tijdstip
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error publishing observation for %s: %s", location_code, exc)

    return sent

async def feed(
    api: RWSWaterwebservicesAPI,
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
    mqtt_client = NLRWSWaterwebservicesMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    # Fetch station catalog and build station display-name map
    locations = api.get_water_level_stations()
    station_map = _build_station_map(locations)
    station_codes = [loc.get("Code", "") for loc in locations if loc.get("Code")]

    logger.info("Publishing %d station info events under hydro/nl/rws/rws-waterwebservices/...", len(locations))
    await _publish_stations(mqtt_client, locations, station_map)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = await _publish_observations(api, mqtt_client, station_codes, station_map, previous_readings)
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
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                await asyncio.sleep(polling_interval)
    finally:
        await mqtt_client.disconnect()

def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RWS Waterwebservices → MQTT/UNS bridge.")
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
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.rws_waterwebservices_mqtt_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
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

    api = RWSWaterwebservicesAPI()
    asyncio.run(
        feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
        )
    )

if __name__ == "__main__":
    main()
