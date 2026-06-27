from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from openaq_core import OpenAQClient, build_mock_client, load_query_slices, load_state, parse_bool, save_state, should_publish_measurement
from openaq_core.acquisition import LocationRecord, MeasurementRecord, SensorRecord
from openaq_mqtt_producer_data import Location, Measurement, Sensor
from openaq_mqtt_producer_data.org.openaq.parameternameenum import ParameterNameenum
from openaq_mqtt_producer_mqtt_client.client import OrgOpenaqLocationsMqttMqttClient, OrgOpenaqSensorsMqttMqttClient

logger = logging.getLogger(__name__)
DEFAULT_STATE_FILE = os.path.expanduser("~/.openaq_mqtt_state.json")
DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

def _enum(name: str) -> ParameterNameenum: return ParameterNameenum(name)
def build_location(r: LocationRecord) -> Location: return Location(**r.__dict__)
def build_sensor(r: SensorRecord) -> Sensor:
    d=dict(r.__dict__); d["parameter_name"]=_enum(r.parameter_name); return Sensor(**d)
def build_measurement(r: MeasurementRecord) -> Measurement:
    d=dict(r.__dict__); d["parameter_name"]=_enum(r.parameter_name); return Measurement(**d)
def _parse_broker_settings(args: argparse.Namespace) -> tuple[str, int, bool]:
    broker_url = args.mqtt_broker_url or (f"mqtt://{args.mqtt_host}:{args.mqtt_port}" if args.mqtt_host else None)
    if not broker_url: raise SystemExit("MQTT_BROKER_URL or MQTT_HOST/MQTT_PORT must be provided.")
    parsed = urlparse(broker_url if "://" in broker_url else f"mqtt://{broker_url}")
    tls = parse_bool(args.mqtt_tls, default=parsed.scheme.lower() == "mqtts")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple[str, datetime]:
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
    scope = audience if audience.endswith("/.default") else f"{audience}.default" if audience.endswith("/") else f"{audience}/.default"
    token = credential.get_token(scope)
    return token.token, datetime.fromtimestamp(token.expires_on, tz=timezone.utc)

async def feed(args: argparse.Namespace) -> None:
    host, port, tls = _parse_broker_settings(args)
    state = load_state(args.state_file)
    client = build_mock_client() if args.mock else OpenAQClient(args.openaq_api_key)
    if args.mock: args.once = True
    query_slices = load_query_slices(args.openaq_countries, args.openaq_locations, args.openaq_bbox, args.page_limit, args.max_pages, mock=args.mock, sources_file=args.openaq_sources_file, selector=args.openaq_sources)
    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.mqtt_client_id or "", protocol=MQTTv5)
    auth_mode = (args.mqtt_auth_mode or "anonymous").lower()
    if auth_mode == "userpass" and args.mqtt_username: paho_client.username_pw_set(args.mqtt_username, args.mqtt_password or "")
    if auth_mode == "tls-cert": paho_client.tls_set(ca_certs=args.mqtt_ca_file or None, certfile=args.mqtt_client_cert, keyfile=args.mqtt_client_key)
    elif tls or auth_mode == "entra": paho_client.tls_set(ca_certs=args.mqtt_ca_file or None)
    loop = asyncio.get_running_loop()
    loc_client = OrgOpenaqLocationsMqttMqttClient(paho_client, content_mode="binary", loop=loop)
    sensor_client = OrgOpenaqSensorsMqttMqttClient(paho_client, content_mode="binary", loop=loop)
    if auth_mode == "entra":
        token, expires_at = _acquire_entra_token(args.mqtt_entra_audience, args.mqtt_entra_client_id)
        props = Properties(PacketTypes.CONNECT); props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD; props.AuthenticationData = token.encode("utf-8")
        if args.mqtt_username: paho_client.username_pw_set(args.mqtt_username, "")
        paho_client.connect(host, port, keepalive=60, clean_start=True, properties=props); paho_client.loop_start()
        logger.info("Using Entra ID MQTT auth (expires %s)", expires_at.isoformat())
    else:
        # Direct paho connect: multiple generated MqttClient instances sharing one
        # paho client overwrite each other's on_connect, causing connect() timeout.
        import threading as _threading
        _connected = _threading.Event()
        def _on_connack(client, userdata, flags, reason_code, props=None):
            rc = getattr(reason_code, 'value', reason_code) if not isinstance(reason_code, int) else reason_code
            if rc == 0:
                _connected.set()
        paho_client.on_connect = _on_connack
        paho_client.connect(host, port, keepalive=60); paho_client.loop_start()
        if not await asyncio.get_running_loop().run_in_executor(None, lambda: _connected.wait(30)):
            raise RuntimeError('MQTT CONNACK timeout after 30s')
    last_reference_refresh=0.0; reference_refresh=max(300,args.reference_refresh_interval); locations_cache=[]; sensors_cache={}
    try:
        while True:
            cycle_started=time.time()
            if last_reference_refresh == 0.0 or cycle_started-last_reference_refresh >= reference_refresh:
                locs=[]; sens={}
                for query_slice in query_slices:
                    for location in client.iter_locations(query_slice.countries, query_slice.locations, query_slice.bbox, query_slice.page_limit, query_slice.max_pages):
                        locs.append(location)
                        await loc_client.publish_org_openaq_mqtt_location(location_id=str(location.location_id), country_iso=location.country_iso, data=build_location(location))
                        m={}
                        for sensor in client.sensors_for_location(location):
                            m[sensor.sensor_id]=sensor
                            await sensor_client.publish_org_openaq_mqtt_sensor(location_id=str(sensor.location_id), sensor_id=str(sensor.sensor_id), country_iso=sensor.country_iso, parameter_name=sensor.parameter_name, data=build_sensor(sensor))
                        sens[location.location_id]=m
                locations_cache=locs; sensors_cache=sens; last_reference_refresh=cycle_started
            for location in locations_cache:
                for measurement in client.latest_for_location(location, sensors_cache.get(location.location_id, {})):
                    if should_publish_measurement(measurement, state):
                        await sensor_client.publish_org_openaq_mqtt_measurement(location_id=str(measurement.location_id), sensor_id=str(measurement.sensor_id), country_iso=measurement.country_iso, parameter_name=measurement.parameter_name, data=build_measurement(measurement))
            save_state(args.state_file, state)
            if args.once: break
            await asyncio.sleep(max(1, args.poll_interval-int(time.time()-cycle_started)))
    finally:
        try: await sensor_client.disconnect()
        except Exception: pass

def build_parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="OpenAQ global air quality -> MQTT bridge"); sub=parser.add_subparsers(dest="command"); f=sub.add_parser("feed")
    for name, env, default in [("openaq-api-key","OPENAQ_API_KEY",None),("openaq-countries","OPENAQ_COUNTRIES",None),("openaq-locations","OPENAQ_LOCATIONS",None),("openaq-bbox","OPENAQ_BBOX",None)]: f.add_argument("--"+name, default=os.getenv(env, default) if default is not None else os.getenv(env))
    f.add_argument("--openaq-sources-file", default=os.getenv("OPENAQ_SOURCES_FILE", "")); f.add_argument("--openaq-sources", default=os.getenv("OPENAQ_SOURCES", ""))
    f.add_argument("--page-limit", type=int, default=int(os.getenv("OPENAQ_PAGE_LIMIT","25"))); f.add_argument("--max-pages", type=int, default=int(os.getenv("OPENAQ_MAX_PAGES","1")))
    f.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL","900"))); f.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL","21600"))); f.add_argument("--state-file", default=os.getenv("STATE_FILE",DEFAULT_STATE_FILE)); f.add_argument("--once", action="store_true", default=parse_bool(os.getenv("ONCE_MODE"),False)); f.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("OPENAQ_MOCK"),False))
    f.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL")); f.add_argument("--mqtt-host", default=os.getenv("MQTT_HOST")); f.add_argument("--mqtt-port", default=os.getenv("MQTT_PORT","1883")); f.add_argument("--mqtt-tls", default=os.getenv("MQTT_ENABLE_TLS","false")); f.add_argument("--mqtt-auth-mode", default=os.getenv("MQTT_AUTH_MODE","anonymous")); f.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME")); f.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD")); f.add_argument("--mqtt-client-cert", default=os.getenv("MQTT_CLIENT_CERT")); f.add_argument("--mqtt-client-key", default=os.getenv("MQTT_CLIENT_KEY")); f.add_argument("--mqtt-ca-file", default=os.getenv("MQTT_CA_FILE")); f.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID")); f.add_argument("--mqtt-entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID")); f.add_argument("--mqtt-entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    return parser

def main(argv: Optional[list[str]]=None) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO").upper()); parser=build_parser(); args=parser.parse_args(argv)
    if args.command != "feed": parser.print_help(); return
    try: asyncio.run(feed(args))
    except Exception as exc: logger.error("OpenAQ MQTT bridge failed: %s", exc); sys.exit(1)
if __name__ == "__main__": main()
