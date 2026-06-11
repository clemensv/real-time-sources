"""MQTT feeder application for NVE Hydrology → Unified Namespace.

Reuses the upstream HydAPI client and station catalog logic from the
existing ``nve_hydro`` Kafka bridge and pushes CloudEvents into MQTT 5.0
using the xrcg-generated :class:`NONVEHydrologyMqttMqttClient`.

Topic tree: ``hydro/no/nve/nve-hydro/{river_name}/{station_id}/{info|water-level}``.
``{river_name}`` is sourced from the NVE HydAPI station catalog
(``riverName`` / Norwegian ``Vassdrag``) and normalized to lowercase
kebab-case by :func:`_uns_slug`.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from nve_hydro.nve_hydro import (
    NVEHydroAPI,
    PARAM_DISCHARGE,
    PARAM_STAGE,
    _load_state,
    _save_state,
    _fetch_station_observations,
    _station_has_parameter,
)
from nve_hydro_mqtt_producer_data import Station, WaterLevelObservation
from nve_hydro_mqtt_producer_mqtt_client.client import NONVEHydrologyMqttMqttClient
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

MAX_WORKERS = 10

_UNS_REPLACEMENTS = str.maketrans({
    "æ": "ae", "ø": "o", "å": "aa", "Æ": "ae", "Ø": "o", "Å": "aa",
    "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u", "ß": "ss",
})

def _uns_slug(value: str) -> str:
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

def _build_station(s: Dict[str, Any]) -> Station:
    return Station(
        station_id=s.get("stationId", ""),
        station_name=s.get("stationName", "") or "",
        river_name=s.get("riverName", "") or "",
        latitude=float(s.get("latitude", 0.0) or 0.0),
        longitude=float(s.get("longitude", 0.0) or 0.0),
        masl=float(s.get("masl") or 0.0),
        council_name=s.get("councilName", "") or "",
        county_name=s.get("countyName", "") or "",
        drainage_basin_area=float(s.get("drainageBasinArea") or 0.0),
    )

async def _publish_stations(
    mqtt_client: NONVEHydrologyMqttMqttClient,
    stations: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    by_id: Dict[str, Dict[str, Any]] = {}
    for s in stations:
        sid = s.get("stationId")
        if not sid:
            continue
        river_slug = _uns_slug(s.get("riverName", ""))
        by_id[sid] = s
        await mqtt_client.publish_no_nve_hydrology_mqtt_station(
            station_id=sid,
            river_name=river_slug,
            data=_build_station(s),
        )
    return by_id

async def _publish_observations(
    api: NVEHydroAPI,
    mqtt_client: NONVEHydrologyMqttMqttClient,
    stations_by_id: Dict[str, Dict[str, Any]],
    previous_readings: Dict[str, Any],
) -> int:
    station_params: Dict[str, List[int]] = {}
    for sid, station in stations_by_id.items():
        params: List[int] = []
        if _station_has_parameter(station, PARAM_STAGE):
            params.append(PARAM_STAGE)
        if _station_has_parameter(station, PARAM_DISCHARGE):
            params.append(PARAM_DISCHARGE)
        if params:
            station_params[sid] = params

    loop = asyncio.get_running_loop()
    sent = 0

    def fetch_one(sid: str):
        return sid, _fetch_station_observations(api, sid, station_params[sid])

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [loop.run_in_executor(executor, fetch_one, sid) for sid in station_params]
        for fut in asyncio.as_completed(futures):
            try:
                sid, obs_by_param = await fut
            except Exception as exc:  # pylint: disable=broad-except
                logger.debug("Error fetching observations: %s", exc)
                continue
            if not obs_by_param:
                continue

            wl_val = None
            wl_ts = ""
            q_val = None
            q_ts = ""
            if PARAM_STAGE in obs_by_param:
                stage = obs_by_param[PARAM_STAGE]
                wl_val = float(stage["value"])
                wl_ts = stage.get("time", "")
            if PARAM_DISCHARGE in obs_by_param:
                discharge = obs_by_param[PARAM_DISCHARGE]
                q_val = float(discharge["value"])
                q_ts = discharge.get("time", "")
            if wl_val is None and q_val is None:
                continue

            reading_key = f"{sid}:{wl_ts}:{q_ts}"
            if reading_key in previous_readings:
                continue

            station = stations_by_id.get(sid) or {}
            river_raw = station.get("riverName", "") or ""
            river_slug = _uns_slug(river_raw)
            try:
                await mqtt_client.publish_no_nve_hydrology_mqtt_water_level_observation(
                    station_id=sid,
                    river_name=river_slug,
                    data=WaterLevelObservation(
                        station_id=sid,
                        river_name=river_raw,
                        water_level=wl_val if wl_val is not None else 0.0,
                        water_level_unit="m",
                        water_level_timestamp=wl_ts,
                        discharge=q_val if q_val is not None else 0.0,
                        discharge_unit="m3/s",
                        discharge_timestamp=q_ts,
                    ),
                )
                sent += 1
                previous_readings[reading_key] = wl_ts or q_ts
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error publishing observation for %s: %s", sid, exc)
    return sent

async def feed(
    api: NVEHydroAPI,
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
    mqtt_client = NONVEHydrologyMqttMqttClient(
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

    stations = api.get_stations()
    logger.info("Publishing %d station info events under hydro/no/nve/nve-hydro/...", len(stations))
    stations_by_id = await _publish_stations(mqtt_client, stations)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = await _publish_observations(api, mqtt_client, stations_by_id, previous_readings)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info("Published %d observations in %.1fs.", count, (end_time - start_time).total_seconds())
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
    parser = argparse.ArgumentParser(description="NVE Hydrology → MQTT/UNS bridge.")
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
    feed_parser.add_argument("--api-key", type=str, default=os.getenv("NVE_API_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.nve_hydro_mqtt_state.json")))
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

    if not args.api_key:
        print("Error: NVE_API_KEY environment variable or --api-key required")
        sys.exit(1)

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

    api = NVEHydroAPI(args.api_key)
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
