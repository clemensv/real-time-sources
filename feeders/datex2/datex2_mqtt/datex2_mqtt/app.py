from __future__ import annotations

import argparse
import asyncio
import logging
import os
import json
import ssl
import urllib.parse
import urllib.request
from typing import Optional

import paho.mqtt.client as mqtt
from datex2_core import collect_batches, load_endpoints
from datex2_mqtt_producer_data import MeasurementSite, SituationRecord, TrafficMeasurement
from datex2_mqtt_producer_mqtt_client.client import OrgDatex2MeasuredMqttMqttClient, OrgDatex2SituationMqttMqttClient
from paho.mqtt.client import CallbackAPIVersion, MQTTv5


def _imds_token(audience: str, client_id: Optional[str]) -> str:
    params = {"api-version": "2018-02-01", "resource": audience}
    if client_id:
        params["client_id"] = client_id
    req = urllib.request.Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urllib.parse.urlencode(params),
        headers={"Metadata": "true"},
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return str(payload.get("access_token") or payload.get("accessToken") or "")


async def feed(args: argparse.Namespace) -> None:
    parsed = urllib.parse.urlparse(args.broker_url if "://" in args.broker_url else "mqtt://" + args.broker_url)
    host = parsed.hostname or args.broker_url.split(":")[0]
    port = parsed.port or (8883 if args.enable_tls or parsed.scheme == "mqtts" else 1883)
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.client_id or "datex2-mqtt", protocol=MQTTv5)
    if args.enable_tls or parsed.scheme == "mqtts":
        client.tls_set(ca_certs=args.ca_file or None, cert_reqs=ssl.CERT_REQUIRED)
    connect_props = None
    if args.auth_mode == "entra":
        from paho.mqtt.packettypes import PacketTypes
        from paho.mqtt.properties import Properties

        token = _imds_token(args.entra_audience, args.entra_client_id)
        client.username_pw_set(args.client_id or args.username or "datex2-mqtt", token)
        connect_props = Properties(PacketTypes.CONNECT)
        connect_props.AuthenticationMethod = "OAUTH2-JWT"
        connect_props.AuthenticationData = token.encode("utf-8")
    elif args.auth_mode in {"userpass", "password"} or args.username or args.password:
        client.username_pw_set(args.username, args.password)
    loop = asyncio.get_running_loop()
    measured = OrgDatex2MeasuredMqttMqttClient(client, content_mode="binary", loop=loop)
    situation = OrgDatex2SituationMqttMqttClient(client, content_mode="binary", loop=loop)
    client.connect(host, port, keepalive=60, properties=connect_props)
    client.loop_start()
    try:
        while True:
            batch = collect_batches(load_endpoints(args.datex2_endpoints, mock=args.mock), mock=args.mock, max_records=args.max_records)
            for row in batch.measurement_sites:
                await measured.publish_org_datex2_measured_measurement_site_mqtt(row["feed_url"], row["supplier_id"], row["measurement_site_id"], row.get("country_code") or "eu", row.get("operator_id") or "datex2", MeasurementSite(**row))
            for row in batch.traffic_measurements:
                await measured.publish_org_datex2_measured_traffic_measurement_mqtt(row["feed_url"], row["supplier_id"], row["measurement_site_id"], row.get("country_code") or "eu", row.get("operator_id") or "datex2", TrafficMeasurement(**row))
            for row in batch.situation_records:
                await situation.publish_org_datex2_situation_situation_record_mqtt(row["feed_url"], row["supplier_id"], row["situation_record_id"], row.get("country_code") or "eu", row.get("operator_id") or "datex2", SituationRecord(**row))
            await asyncio.sleep(1)
            if args.once:
                break
            await asyncio.sleep(args.polling_interval)
    finally:
        client.loop_stop()
        client.disconnect()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DATEX II MQTT feeder")
    sub = parser.add_subparsers(dest="command")
    feed_parser = sub.add_parser("feed")
    feed_parser.add_argument("--datex2-endpoints", default=os.getenv("DATEX2_ENDPOINTS", ""))
    feed_parser.add_argument("--mock", action="store_true", default=os.getenv("DATEX2_MOCK", "").lower() == "true")
    feed_parser.add_argument("--max-records", type=int, default=int(os.getenv("MAX_RECORDS_PER_FAMILY", "25")))
    feed_parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "localhost:1883"))
    feed_parser.add_argument("--enable-tls", action=argparse.BooleanOptionalAction, default=os.getenv("MQTT_ENABLE_TLS", "false").lower() == "true")
    feed_parser.add_argument("--auth-mode", choices=["anonymous", "userpass", "password", "tls-cert", "entra"], default=os.getenv("MQTT_AUTH_MODE", "anonymous"))
    feed_parser.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--ca-file", default=os.getenv("MQTT_CA_FILE"))
    feed_parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/"))
    feed_parser.add_argument("--entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID") or os.getenv("AZURE_CLIENT_ID"))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "false").lower() == "true")
    return parser


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    parser = _parser()
    args = parser.parse_args()
    if args.command != "feed":
        args = parser.parse_args(["feed"])
    asyncio.run(feed(args))
