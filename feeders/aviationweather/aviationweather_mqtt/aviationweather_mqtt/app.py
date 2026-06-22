"""MQTT feeder for AviationWeather.gov."""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

SOURCE_ID = "aviationweather"
PY_MODULE = "aviationweather"

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _fetch_entra_mqtt_token(audience: str, managed_identity_client_id: Optional[str] = None) -> str:
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
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
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props


async def feed(args: argparse.Namespace) -> None:
    """Live acquisition loop: stations -> METARs -> SIGMETs over MQTT."""
    from aviationweather_core import (
        AviationWeatherPoller,
        DEFAULT_STATIONS,
        METAR_POLL_INTERVAL,
        SIGMET_POLL_INTERVAL,
        STATION_REFRESH_HOURS,
    )
    from aviationweather_mqtt_producer_mqtt_client.client import GovNoaaAviationweatherMqttMqttClient

    station_ids = os.getenv("AVIATIONWEATHER_STATIONS", DEFAULT_STATIONS)
    if getattr(args, "stations", None):
        station_ids = args.stations

    state_file = getattr(args, "state_file", None) or os.path.expanduser(f"~/.{PY_MODULE}_mqtt_state.json")

    poller = AviationWeatherPoller(
        last_polled_file=state_file,
        station_ids=station_ids,
        metar_poll_interval=METAR_POLL_INTERVAL,
        sigmet_poll_interval=SIGMET_POLL_INTERVAL,
    )

    parsed_url = urlparse(args.broker_url if "://" in args.broker_url else f"mqtt://{args.broker_url}")
    resolved_client_id, resolved_username, resolved_password, connect_props = _resolve_mqtt_connection_settings(
        username=parsed_url.username or args.username,
        password=parsed_url.password or args.password or "",
        client_id=args.client_id,
        auth_mode=args.auth_mode,
    )
    host = parsed_url.hostname or "localhost"
    port = parsed_url.port or (8883 if parsed_url.scheme in ("mqtts", "ssl") else 1883)
    use_tls = parsed_url.scheme in ("mqtts", "ssl") or args.tls or args.auth_mode == "entra"

    mqtt_client = GovNoaaAviationweatherMqttMqttClient(
        host=host, port=port, client_id=resolved_client_id or None,
        use_tls=use_tls, content_mode=args.content_mode,
    )
    if resolved_username or resolved_password:
        mqtt_client._client.username_pw_set(resolved_username, resolved_password)

    await mqtt_client.connect(properties=connect_props)

    def utcnow_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    try:
        logger.info("Emitting station reference data via MQTT...")
        station_count = 0
        for raw in poller.fetch_station_json(poller.station_ids):
            station = poller.parse_station(raw)
            if station:
                await mqtt_client.publish_gov_noaa_aviationweather_mqtt_station(
                    icao_id=station.icao_id, data=station, _time=utcnow_iso(),
                )
                station_count += 1
        logger.info("Published %d station(s) via MQTT", station_count)

        state = poller.load_state()
        metar_timestamps = state.get("metar_timestamps", {})
        seen_sigmet_keys: set = set(state.get("sigmet_keys", []))
        last_sigmet_poll = 0.0
        last_station_refresh = time.monotonic()

        while True:
            now = time.monotonic()
            metar_count = 0
            for raw in poller.fetch_metar_json(poller.station_ids):
                metar = poller.parse_metar(raw)
                if metar is None:
                    continue
                if metar_timestamps.get(metar.icao_id) == metar.obs_time:
                    continue
                await mqtt_client.publish_gov_noaa_aviationweather_mqtt_metar(
                    icao_id=metar.icao_id, data=metar, _time=metar.obs_time,
                )
                metar_timestamps[metar.icao_id] = metar.obs_time
                metar_count += 1
            if metar_count:
                logger.info("Published %d new METAR(s) via MQTT", metar_count)

            if now - last_sigmet_poll >= SIGMET_POLL_INTERVAL:
                sigmet_count = 0
                current_keys: set = set()
                for raw in poller.fetch_airsigmet_json():
                    sigmet = poller.parse_us_sigmet(raw)
                    if sigmet:
                        key = poller.sigmet_dedup_key(sigmet)
                        current_keys.add(key)
                        if key not in seen_sigmet_keys:
                            await mqtt_client.publish_gov_noaa_aviationweather_mqtt_sigmet(
                                region=sigmet.region, sigmet_id=sigmet.sigmet_id,
                                data=sigmet, _time=sigmet.valid_time_from,
                            )
                            sigmet_count += 1
                for raw in poller.fetch_isigmet_json():
                    sigmet = poller.parse_intl_sigmet(raw)
                    if sigmet:
                        key = poller.sigmet_dedup_key(sigmet)
                        current_keys.add(key)
                        if key not in seen_sigmet_keys:
                            await mqtt_client.publish_gov_noaa_aviationweather_mqtt_sigmet(
                                region=sigmet.region, sigmet_id=sigmet.sigmet_id,
                                data=sigmet, _time=sigmet.valid_time_from,
                            )
                            sigmet_count += 1
                seen_sigmet_keys = current_keys
                if sigmet_count:
                    logger.info("Published %d new SIGMET(s) via MQTT", sigmet_count)
                last_sigmet_poll = now

            if now - last_station_refresh >= STATION_REFRESH_HOURS * 3600:
                refresh_count = 0
                for raw in poller.fetch_station_json(poller.station_ids):
                    station = poller.parse_station(raw)
                    if station:
                        await mqtt_client.publish_gov_noaa_aviationweather_mqtt_station(
                            icao_id=station.icao_id, data=station, _time=utcnow_iso(),
                        )
                        refresh_count += 1
                logger.info("Refreshed %d station(s) via MQTT", refresh_count)
                last_station_refresh = now

            poller.save_state({"metar_timestamps": metar_timestamps, "sigmet_keys": list(seen_sigmet_keys)})

            if args.once:
                break
            await asyncio.sleep(METAR_POLL_INTERVAL)

    finally:
        await mqtt_client.disconnect()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description=f"{SOURCE_ID} MQTT bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--host", default=os.getenv("MQTT_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None)
    parser.add_argument("--tls", action="store_true", default=_env_bool("MQTT_TLS", False))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID"))
    parser.add_argument("--auth-mode", choices=("password", "entra"), default=os.getenv("MQTT_AUTH_MODE", "password"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    parser.add_argument("--stations", default=os.getenv("AVIATIONWEATHER_STATIONS", ""))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_mqtt_state.json")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(feed(args))


if __name__ == "__main__":
    main()
