"""Live USGS water-quality acquisition over MQTT 5."""

import argparse
import asyncio
import json
import logging
import os
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from usgs_nwis_wq.usgs_nwis_wq import USGSWaterQualityPoller
from usgs_nwis_wq.transport import PublisherAdapter
from .delivery import PublishAcknowledgements
from usgs_nwis_wq_mqtt_producer_mqtt_client.client import (
    USGSWaterQualitySitesMqttMqttClient,
    USGSWaterQualityReadingsMqttMqttClient,
)


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
    client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).lower()
    if mode == "password":
        return client_id, username or "", password or "", None
    if mode != "entra":
        raise ValueError("MQTT_AUTH_MODE must be password or entra")
    if not client_id:
        raise ValueError("MQTT_CLIENT_ID is required for MQTT_AUTH_MODE=entra")
    token = _fetch_entra_mqtt_token(
        os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/"),
        os.getenv("MQTT_ENTRA_CLIENT_ID"),
    )
    # WORKAROUND(xregistry/codegen#432): generated connect lacks enhanced authentication properties.
    from paho.mqtt.properties import Properties
    from paho.mqtt.packettypes import PacketTypes
    properties = Properties(PacketTypes.CONNECT)
    properties.AuthenticationMethod = "OAUTH2-JWT"
    properties.AuthenticationData = token.encode("utf-8")
    return client_id, client_id, token, properties


async def feed(host, port, username=None, password=None, tls=False, client_id=None, once=False, content_mode="binary"):
    from usgs_nwis_wq.waterdata import WaterDataFeed, api_mode
    poller = USGSWaterQualityPoller(
        last_polled_file=os.getenv("USGS_WQ_LAST_POLLED_FILE") or os.getenv("STATE_FILE") or os.path.expanduser("~/.usgs_wq_last_polled_mqtt.json"),
        states=os.getenv("USGS_WQ_STATES", "").split(",") if os.getenv("USGS_WQ_STATES") else None,
        sites=os.getenv("USGS_WQ_SITES", "").split(",") if os.getenv("USGS_WQ_SITES") else None,
        parameter_codes=os.getenv("USGS_WQ_PARAMETER_CODES") or None,
    )
    if api_mode() == "waterdata":
        WaterDataFeed(poller)
    identity, user, secret, properties = _resolve_mqtt_connection_settings(
        username=username, password=password, client_id=client_id,
    )
    raw = mqtt.Client(client_id=identity, callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
    if properties is None and (user or secret):
        raw.username_pw_set(user, secret)
    if tls or properties is not None:
        raw.tls_set()
    acknowledgements = PublishAcknowledgements(raw.publish)
    # WORKAROUND(xregistry/codegen#700): generated methods discard PUBACK.
    # Keep the Paho API intact while flush confirms every broker outcome.
    setattr(raw, "publish", acknowledgements.publish)
    setattr(raw, "flush_publishes", acknowledgements.flush_publishes)
    raw.on_publish = acknowledgements.on_publish
    clients = []
    try:
        for suffix, cls in (
            ("sites", USGSWaterQualitySitesMqttMqttClient),
            ("readings", USGSWaterQualityReadingsMqttMqttClient),
        ):
            client = cls(client=raw, content_mode=content_mode, loop=asyncio.get_running_loop())
            clients.append(client)
            adapter = PublisherAdapter(client, "mqtt")
            if suffix == "sites":
                poller.site_producer = adapter
            else:
                poller.readings_producer = adapter
        loop = asyncio.get_running_loop()
        connected = loop.create_future()

        def on_connect(client, userdata, flags, reason, properties=None):
            def complete():
                if connected.done():
                    return
                if reason == 0:
                    connected.set_result(None)
                else:
                    connected.set_exception(RuntimeError(f"MQTT broker rejected CONNECT: {reason}"))
            loop.call_soon_threadsafe(complete)

        def on_disconnect(client, userdata, flags, reason, properties=None):
            def complete():
                if not connected.done():
                    connected.set_exception(RuntimeError(f"MQTT disconnected before CONNACK: {reason}"))
            loop.call_soon_threadsafe(complete)

        # Both generated constructors replace raw callbacks; install the
        # connection owner's callbacks only after constructing both wrappers.
        raw.on_connect = on_connect
        raw.on_disconnect = on_disconnect
        raw.connect(host, port, keepalive=60, clean_start=True, properties=properties)
        raw.loop_start()
        await asyncio.wait_for(connected, timeout=30)
        await poller.poll_and_send(once=once)
    finally:
        raw.disconnect()
        await asyncio.to_thread(raw.loop_stop)


def _parse_broker_url(url):
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    tls = (parsed.scheme or "mqtt").lower() in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls, parsed.username, parsed.password


def main(argv=None):
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    parser = argparse.ArgumentParser(description="USGS NWIS WQ MQTT bridge")
    sub = parser.add_subparsers(dest="command")
    feed_parser = sub.add_parser("feed")
    feed_parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--broker-host", default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--broker-port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true", default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", choices=["binary", "structured"], default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    if args.broker_url:
        host, port, tls, user, secret = _parse_broker_url(args.broker_url)
        user, secret = args.username or user, args.password or secret
        port, tls = args.broker_port or port, tls or args.tls
    else:
        host, tls = args.broker_host or "localhost", args.tls
        port, user, secret = args.broker_port or (8883 if tls else 1883), args.username, args.password
    asyncio.run(feed(host, port, username=user, password=secret, tls=tls, client_id=args.client_id,
                     once=args.once, content_mode=args.content_mode))
