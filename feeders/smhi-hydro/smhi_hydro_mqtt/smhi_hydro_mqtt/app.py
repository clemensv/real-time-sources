"""MQTT feeder application for SMHI Hydrology → Unified Namespace.

Reuses the upstream HTTP client and station catalog logic from the existing
``smhi_hydro`` Kafka bridge (imported as the transport-agnostic "core"
package) and pushes CloudEvents into MQTT 5.0 using the xrcg-generated
:class:`SEGovSMHIHydroMqttMqttClient`.

Topic tree: ``hydro/se/smhi/smhi-hydro/{catchment_name}/{station_id}/{info|discharge}``.
``{catchment_name}`` is sourced from the SMHI station catalog
(field ``catchmentName``) and normalized to lowercase kebab-case by
:func:`_uns_slug` so umlauts, spaces and slashes never reach the broker.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from smhi_hydro.smhi_hydro import SMHIHydroAPI, _load_state, _save_state
from smhi_hydro_mqtt_producer_data import Station, DischargeObservation
from smhi_hydro_mqtt_producer_mqtt_client.client import SEGovSMHIHydroMqttMqttClient
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
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

logger = logging.getLogger(__name__)

_UNS_REPLACEMENTS = str.maketrans({
    "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u", "ß": "ss",
    "à": "a", "á": "a", "â": "a", "è": "e", "é": "e", "ê": "e",
    "ì": "i", "í": "i", "î": "i", "ò": "o", "ó": "o", "ô": "o",
    "ù": "u", "ú": "u", "û": "u", "ç": "c", "ñ": "n",
    "å": "a",
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

_CATCHMENT_UNKNOWN = "unknown"

def _catchment_value(station_data: dict) -> str:
    """Return the raw catchmentName, substituting the lowercase 'unknown'
    sentinel when the SMHI catalog has no value for the station. The sentinel
    is applied BEFORE the record is handed to the generated MQTT producer so
    the on-wire payload, schema-required field, and {catchment_name} topic
    segment all stay populated and non-null."""
    value = station_data.get("catchmentName")
    if value is None:
        return _CATCHMENT_UNKNOWN
    value = str(value).strip()
    return value or _CATCHMENT_UNKNOWN

def _build_station(station_data: dict) -> Station:
    """Build an MQTT-producer Station from raw SMHI bulk API station dict."""
    return Station(
        station_id=str(station_data["key"]),
        name=station_data.get("name", "") or "",
        owner=station_data.get("owner", "") or "",
        measuring_stations=station_data.get("measuringStations", "") or "",
        region=int(station_data.get("region", 0) or 0),
        catchment_name=_catchment_value(station_data),
        catchment_number=int(station_data.get("catchmentNumber", 0) or 0),
        catchment_size=float(station_data.get("catchmentSize", 0.0) or 0.0),
        latitude=float(station_data["latitude"]),
        longitude=float(station_data["longitude"]),
    )

def _build_observation(station_data: dict, catchment_name: str) -> Optional[DischargeObservation]:
    """Build a DischargeObservation from raw SMHI station entry, or None."""
    values = station_data.get("value", [])
    if not values:
        return None
    latest = values[-1]
    value = latest.get("value")
    if value is None:
        return None
    epoch_ms = latest["date"]
    ts = datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc)
    return DischargeObservation(
        station_id=str(station_data["key"]),
        station_name=station_data.get("name", "") or "",
        catchment_name=catchment_name or _CATCHMENT_UNKNOWN,
        timestamp=ts,
        discharge=float(value),
        quality=latest.get("quality", "") or "",
    )

async def _publish_stations(
    mqtt_client: SEGovSMHIHydroMqttMqttClient,
    stations: list,
) -> None:
    for station_data in stations:
        catchment_value = _catchment_value(station_data)
        catchment_slug = _uns_slug(catchment_value)
        station_id = str(station_data["key"])
        await mqtt_client.publish_se_gov_smhi_hydro_mqtt_station(
            station_id=station_id,
            catchment_name=catchment_slug,
            data=_build_station(station_data),
        )

async def _publish_observations(
    mqtt_client: SEGovSMHIHydroMqttMqttClient,
    stations: list,
    previous_readings: Dict[str, Any],
) -> int:
    sent = 0
    for station_data in stations:
        catchment_raw = _catchment_value(station_data)
        catchment_slug = _uns_slug(catchment_raw)
        obs = _build_observation(station_data, catchment_raw)
        if obs is None:
            continue
        reading_key = f"{obs.station_id}:{obs.timestamp.isoformat()}"
        if reading_key in previous_readings:
            continue
        try:
            await mqtt_client.publish_se_gov_smhi_hydro_mqtt_discharge_observation(
                station_id=obs.station_id,
                catchment_name=catchment_slug,
                data=obs,
            )
            sent += 1
            previous_readings[reading_key] = obs.timestamp.isoformat()
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Error publishing observation for %s: %s", obs.station_id, exc)
    return sent

async def feed(
    api: SMHIHydroAPI,
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

    resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if _entra_props is None and (resolved_username or resolved_password):
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls or _entra_props is not None:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    mqtt_client = SEGovSMHIHydroMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    if _entra_props is not None:
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=_entra_props)
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)

    bulk_data = api.get_bulk_discharge_data()
    stations = bulk_data.get("station", [])
    logger.info("Publishing %d station info events under hydro/se/smhi/smhi-hydro/...", len(stations))
    await _publish_stations(mqtt_client, stations)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                bulk_data = api.get_bulk_discharge_data()
                stations = bulk_data.get("station", [])
                count = await _publish_observations(mqtt_client, stations, previous_readings)
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
    parser = argparse.ArgumentParser(description="SMHI Hydrology → MQTT/UNS bridge.")
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
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.smhi_hydro_mqtt_state.json")))
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

    api = SMHIHydroAPI(polling_interval=args.polling_interval)
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
