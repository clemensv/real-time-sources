"""MQTT feeder application for geosphere-austria."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import time
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from geosphere_austria_core import (
    create_retrying_session, fetch_station_metadata, parse_station,
    fetch_observations, parse_observation, observation_fingerprint,
    load_state, save_state, station_bundesland_segment,
    DEFAULT_POLLING_INTERVAL, DEFAULT_STATION_REFRESH_INTERVAL,
)
from geosphere_austria_mqtt_producer_mqtt_client.client import AtGeosphereTawesMqttMqttClient

logger = logging.getLogger(__name__)


def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
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
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    props = _MqttConnProps(_MqttPktTypes.CONNECT)
    props.AuthenticationMethod = "OAUTH2-JWT"
    props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, props


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme in ("mqtts", "ssl", "tls") else 1883), scheme in ("mqtts", "ssl", "tls")


async def _run_live(args: argparse.Namespace, mqtt_client: AtGeosphereTawesMqttMqttClient) -> None:
    session = create_retrying_session()
    state = load_state(args.state_file)
    cached_stations = []
    station_map = {}
    last_station_refresh = 0.0
    while True:
        now = time.time()
        station_refresh_due = (now - last_station_refresh) >= args.station_refresh_interval
        try:
            stations_raw = fetch_station_metadata(session)
            stations = [parse_station(s) for s in stations_raw]
            station_map = {s.station_id: s for s in stations}
            cached_stations = stations
        except Exception as exc:
            if not cached_stations:
                raise
            logger.warning("Station metadata refresh failed; using cached: %s", exc)
            stations = cached_stations
        if station_refresh_due:
            for station in stations:
                await mqtt_client.publish_at_geosphere_tawes_mqtt_weather_station(
                    station_id=station.station_id,
                    bundesland=station_bundesland_segment(station),
                    data=station,  # type: ignore[arg-type]
                )
            logger.info("Published %d station reference events via MQTT", len(stations))
            last_station_refresh = now
        station_ids = [s.station_id for s in stations]
        features, timestamp = fetch_observations(session, station_ids)
        fingerprints = state.get("fingerprints", {})
        sent = 0
        for feat in features:
            obs = parse_observation(feat, timestamp)
            if obs is None:
                continue
            fp = observation_fingerprint(obs)
            if fingerprints.get(obs.station_id) == fp:
                continue
            st = station_map.get(obs.station_id)
            bl = station_bundesland_segment(st) if st is not None else "unknown"
            await mqtt_client.publish_at_geosphere_tawes_mqtt_weather_observation(
                station_id=obs.station_id,
                bundesland=bl,
                data=obs,  # type: ignore[arg-type]
            )
            fingerprints[obs.station_id] = fp
            sent += 1
        state["fingerprints"] = fingerprints
        save_state(args.state_file, state)
        logger.info("Published %d observation events via MQTT", sent)
        if args.once:
            break
        await asyncio.sleep(args.polling_interval)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="geosphere-austria MQTT bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.geosphere_austria_mqtt_state.json")))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLLING_INTERVAL))))
    parser.add_argument("--station-refresh-interval", type=int, default=int(os.getenv("STATION_REFRESH_INTERVAL", str(DEFAULT_STATION_REFRESH_INTERVAL))))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    resolved_client_id, resolved_username, resolved_password, entra_props = _resolve_mqtt_connection_settings(
        username=args.username or None,
        password=args.password or None,
        client_id=args.client_id or None,
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    async def _runner():
        paho_client = mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if entra_props is None and (resolved_username or resolved_password):
            paho_client.username_pw_set(resolved_username, resolved_password)
        if tls or entra_props is not None:
            paho_client.tls_set()
        mqtt_cl = AtGeosphereTawesMqttMqttClient(client=paho_client, content_mode=args.content_mode, loop=asyncio.get_running_loop())
        if entra_props is not None:
            paho_client.connect(host, port, keepalive=60, clean_start=True, properties=entra_props)
            paho_client.loop_start()
        else:
            await mqtt_cl.connect(host, port)
        try:
            await _run_live(args, mqtt_cl)
        finally:
            await mqtt_cl.disconnect()

    asyncio.run(_runner())


if __name__ == "__main__":
    main()
