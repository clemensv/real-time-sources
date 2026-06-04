from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from uk_bods_siri_core import BODS_BULK_URL, BodsSiriClient, FeedConfig, load_state, save_state
from uk_bods_siri_mqtt_producer_data import Operator, VehiclePosition
from uk_bods_siri_mqtt_producer_mqtt_client.client import UkGovDftBodsMqttMqttClient

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

logger = logging.getLogger(__name__)


def _build_operator(operator_ref: str) -> Operator:
    return Operator(operator_ref=operator_ref)


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(value) if value else None


def _build_vehicle_position(position) -> VehiclePosition:
    return VehiclePosition(
        operator_ref=position.operator_ref,
        vehicle_ref=position.vehicle_ref,
        line_ref=position.line_ref,
        direction_ref=position.direction_ref,
        published_line_name=position.published_line_name,
        origin_ref=position.origin_ref,
        origin_name=position.origin_name,
        destination_ref=position.destination_ref,
        destination_name=position.destination_name,
        longitude=position.longitude,
        latitude=position.latitude,
        bearing=position.bearing,
        recorded_at_time=_parse_dt(position.recorded_at_time),
        valid_until_time=_parse_dt(position.valid_until_time),
        block_ref=position.block_ref,
        vehicle_journey_ref=position.vehicle_journey_ref,
        origin_aimed_departure_time=_parse_dt(position.origin_aimed_departure_time),
        data_frame_ref=position.data_frame_ref,
        dated_vehicle_journey_ref=position.dated_vehicle_journey_ref,
        item_identifier=position.item_identifier,
    )


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple[str, datetime]:
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

    credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
    scope = audience if audience.endswith("/.default") else f"{audience}/.default"
    token = credential.get_token(scope)
    expires_at = datetime.fromtimestamp(token.expires_on, tz=timezone.utc)
    return token.token, expires_at


async def _entra_token_refresh_loop(
    paho_client: mqtt.Client,
    broker_host: str,
    broker_port: int,
    keepalive: int,
    audience: str,
    client_id: Optional[str],
    expires_at: datetime,
) -> None:
    while True:
        now = datetime.now(timezone.utc)
        sleep_seconds = max(60.0, (expires_at - now).total_seconds() - 300.0)
        await asyncio.sleep(sleep_seconds)
        try:
            new_token, expires_at = _acquire_entra_token(audience, client_id)
            props = Properties(PacketTypes.CONNECT)
            props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
            props.AuthenticationData = new_token.encode("utf-8")
            try:
                paho_client.disconnect()
            except Exception:  # pylint: disable=broad-except
                pass
            paho_client.connect(broker_host, broker_port, keepalive=keepalive, clean_start=True, properties=props)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to refresh Entra JWT: %s", exc)
            await asyncio.sleep(60)


async def feed(
    api: BodsSiriClient,
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
    auth_mode: str = "anonymous",
    entra_audience: str = DEFAULT_ENTRA_AUDIENCE,
    entra_client_id: Optional[str] = None,
) -> None:
    previous_items = load_state(state_file)
    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )

    refresh_task: Optional[asyncio.Task] = None
    connect_properties: Optional[Properties] = None
    expires_at: Optional[datetime] = None
    if auth_mode == "entra":
        token, expires_at = _acquire_entra_token(entra_audience, entra_client_id)
        connect_properties = Properties(PacketTypes.CONNECT)
        connect_properties.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
        connect_properties.AuthenticationData = token.encode("utf-8")
    elif auth_mode == "userpass" and username:
        paho_client.username_pw_set(username, password or "")

    if tls or auth_mode == "entra":
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    bods_client = UkGovDftBodsMqttMqttClient(client=paho_client, content_mode="binary", loop=loop)

    if auth_mode == "entra":
        paho_client.connect(broker_host, broker_port, keepalive=60, clean_start=True, properties=connect_properties)
        paho_client.loop_start()
        refresh_task = asyncio.create_task(
            _entra_token_refresh_loop(paho_client, broker_host, broker_port, 60, entra_audience, entra_client_id, expires_at)
        )
    else:
        await bods_client.connect(broker_host, broker_port)

    known_operators: set[str] = set()
    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                snapshot = api.load_snapshot()
                operator_set = set(snapshot.operators)
                if not known_operators or operator_set != known_operators:
                    for operator_ref in snapshot.operators:
                        await bods_client.publish_uk_gov_dft_bods_mqtt_operator(
                            feedurl=BODS_BULK_URL,
                            operator_ref=operator_ref,
                            data=_build_operator(operator_ref),
                        )
                    known_operators = operator_set
                    logger.info("Published %d operator reference events", len(snapshot.operators))

                emitted = 0
                next_items = dict(previous_items)
                for position in snapshot.vehicle_positions:
                    if previous_items.get(position.identity) == position.item_identifier:
                        continue
                    await bods_client.publish_uk_gov_dft_bods_mqtt_vehicle_position(
                        feedurl=BODS_BULK_URL,
                        operator_ref=position.operator_ref,
                        vehicle_ref=position.vehicle_ref,
                        data=_build_vehicle_position(position),
                    )
                    next_items[position.identity] = position.item_identifier
                    emitted += 1
                previous_items = next_items
                save_state(state_file, previous_items)

                end_time = datetime.now(timezone.utc)
                effective = max(0.0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %d vehicle positions from %d operators in %.2f seconds. Sleeping until %s.",
                    emitted,
                    len(snapshot.operators),
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", exc)
                if once:
                    raise
                await asyncio.sleep(polling_interval)
    finally:
        if refresh_task is not None:
            refresh_task.cancel()
        await bods_client.disconnect()


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    tls = (parsed.scheme or "mqtt").lower() == "mqtts"
    port = parsed.port or (8883 if tls else 1883)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="UK BODS SIRI-VM → MQTT bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed operator metadata and vehicle positions as CloudEvents over MQTT")
    feed_parser.add_argument("--bods-api-key", type=str, default=os.getenv("BODS_API_KEY"))
    feed_parser.add_argument("--operators", type=str, default=os.getenv("OPERATORS"))
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--host", type=str, default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--tls", action="store_true", default=os.getenv("MQTT_ENABLE_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--auth-mode", choices=["anonymous", "userpass", "entra"], default=os.getenv("MQTT_AUTH_MODE", "anonymous"))
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "30")))
    feed_parser.add_argument("--state-file", type=str, default=os.getenv("STATE_FILE", os.path.expanduser("~/.uk_bods_siri_state.json")))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    operators = {token.strip() for token in (args.operators or "").split(",") if token.strip()} or None
    config = FeedConfig.from_env(
        bods_api_key=args.bods_api_key,
        polling_interval=args.polling_interval,
        operators=operators,
        state_file=args.state_file,
        once=args.once,
    )

    if args.broker_url:
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
    else:
        host = args.host or "localhost"
        tls = args.tls
        port = args.port or (8883 if tls else 1883)
        username = args.username
        password = args.password

    api = BodsSiriClient(api_key=config.bods_api_key, operators=config.operators)
    asyncio.run(
        feed(
            api,
            host,
            port,
            config.polling_interval,
            username=username,
            password=password,
            tls=tls,
            client_id=args.client_id,
            state_file=config.state_file,
            once=config.once,
            auth_mode=args.auth_mode,
            entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id,
        )
    )


if __name__ == "__main__":
    main()
