"""MQTT feeder application for kmi-belgium."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from kmi_belgium_core import KMIBelgiumAPI, _format_timestamp, _load_state, _save_state, extract_stations
from kmi_belgium_mqtt_producer_mqtt_client.client import BEGovKMIWeatherMqttMqttClient

logger = logging.getLogger(__name__)

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id
    request = Request("http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params), headers={"Metadata": "true"})
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
    from paho.mqtt.properties import Properties as _Props
    from paho.mqtt.packettypes import PacketTypes as _Types
    props = _Props(_Types.CONNECT)
    props.AuthenticationMethod = "OAUTH2-JWT"
    props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, props

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (8883 if scheme in ("mqtts", "ssl", "tls") else 1883), scheme in ("mqtts", "ssl", "tls")

def _segment(value) -> str:
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"

async def _run_live(args: argparse.Namespace, mqtt_client: BEGovKMIWeatherMqttMqttClient) -> None:
    api = KMIBelgiumAPI(polling_interval=args.polling_interval)
    previous_readings = _load_state(args.state_file)
    stations = extract_stations(api.get_latest_observations())
    for station in stations:
        await mqtt_client.publish_be_gov_kmi_weather_mqtt_station(station_code=station.station_code, region=_segment(station.region or "unknown"), data=station)
    while True:
        last_timestamp = previous_readings.get("__last_timestamp__")
        features = api.get_observations(last_timestamp=last_timestamp) if last_timestamp else api.get_latest_observations()
        sent = 0
        latest_observation_time = None
        for feature in features:
            obs = api.parse_observation(feature)
            if latest_observation_time is None or obs.observation_time > latest_observation_time:
                latest_observation_time = obs.observation_time
            reading_timestamp = _format_timestamp(obs.observation_time)
            reading_key = f"{obs.station_code}:{reading_timestamp}"
            if reading_key in previous_readings:
                continue
            await mqtt_client.publish_be_gov_kmi_weather_mqtt_weather_observation(station_code=obs.station_code, region=_segment(obs.region or "unknown"), data=obs, _time=obs.observation_time.isoformat())
            previous_readings[reading_key] = reading_timestamp
            sent += 1
        if latest_observation_time is not None:
            previous_readings["__last_timestamp__"] = _format_timestamp(latest_observation_time)
        _save_state(args.state_file, previous_readings)
        if args.once:
            break
        await asyncio.sleep(args.polling_interval)

def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="kmi-belgium MQTT bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(r"~/.kmi_belgium_mqtt_state.json")))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "600")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    host, port, tls = _parse_broker_url(args.broker_url)
    cid, user, pwd, props = _resolve_mqtt_connection_settings(username=args.username or None, password=args.password or None, client_id=args.client_id or None, auth_mode=os.getenv("MQTT_AUTH_MODE"))
    async def _runner():
        paho_client = mqtt.Client(client_id=cid or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if props is None and (user or pwd):
            paho_client.username_pw_set(user, pwd)
        if tls or props is not None:
            paho_client.tls_set()
        mqtt_client = BEGovKMIWeatherMqttMqttClient(client=paho_client, content_mode=args.content_mode, loop=asyncio.get_running_loop())
        if props is not None:
            paho_client.connect(host, port, keepalive=60, clean_start=True, properties=props)
            paho_client.loop_start()
        else:
            await mqtt_client.connect(host, port)
        try:
            await _run_live(args, mqtt_client)
        finally:
            await mqtt_client.disconnect()
    asyncio.run(_runner())
