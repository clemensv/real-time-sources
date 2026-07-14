"""MQTT feeder application for TfL Santander Cycles -> Unified Namespace.

Wraps the upstream BikePoint poller from :mod:`tfl_cycles_core` and the
generated :class:`UKGovTfLCyclesMqttStationsMqttClient`. The MQTT broker is
reached via a plain ``mqtt://host:port`` URL (or ``mqtts://`` for TLS);
username/password are optional. CloudEvent semantics are preserved end-to-end:
binary mode maps CE attributes to MQTT 5 user properties so subscribers can
route on ``type``, ``source`` and ``subject`` without cracking the JSON body.
Station info is published under ``mobility/tfl-cycles/{station_id}/info`` and
availability under ``.../status``.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from tfl_cycles_core import (
    FEED_URL_ROOT,
    ParsedStation,
    TfLCyclesAPI,
    load_state,
    parse_bikepoint,
    save_state,
)
from tfl_cycles_mqtt_producer_data import StationInformation, StationStatus
from tfl_cycles_mqtt_producer_mqtt_client.client import UKGovTfLCyclesMqttStationsMqttClient

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

logger = logging.getLogger(__name__)


def _build_info(p: ParsedStation) -> StationInformation:
    return StationInformation(
        station_id=p.station_id,
        name=p.name,
        lat=float(p.lat) if p.lat is not None else 0.0,
        lon=float(p.lon) if p.lon is not None else 0.0,
        terminal_name=p.terminal_name,
        capacity=p.capacity,
        temporary=p.temporary,
        install_date=p.install_date,
        removal_date=p.removal_date,
    )


def _build_status(p: ParsedStation) -> StationStatus:
    return StationStatus(
        station_id=p.station_id,
        num_bikes_available=p.num_bikes_available if p.num_bikes_available is not None else 0,
        num_standard_bikes_available=p.num_standard_bikes_available,
        num_ebikes_available=p.num_ebikes_available,
        num_empty_docks=p.num_empty_docks if p.num_empty_docks is not None else 0,
        num_docks=p.num_docks,
        is_installed=p.is_installed if p.is_installed is not None else False,
        is_locked=p.is_locked if p.is_locked is not None else False,
        modified=p.modified,
    )


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple:
    """Acquire a Microsoft Entra JWT for the configured audience."""
    try:
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    except ImportError as exc:  # pragma: no cover - import error path
        raise RuntimeError(
            "azure-identity must be installed to use MQTT_AUTH_MODE=entra"
        ) from exc

    credential = (
        ManagedIdentityCredential(client_id=client_id)
        if client_id
        else DefaultAzureCredential()
    )
    scope = audience if audience.endswith("/.default") else f"{audience}/.default"
    token = credential.get_token(scope)
    expires_at = datetime.fromtimestamp(token.expires_on, tz=timezone.utc)
    return token.token, expires_at


async def _entra_token_refresh_loop(
    paho_client: "mqtt.Client",
    broker_host: str,
    broker_port: int,
    keepalive: int,
    audience: str,
    client_id: Optional[str],
    expires_at: datetime,
) -> None:
    """Refresh the Entra JWT before it expires and re-establish the session."""
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
            try:
                paho_client.connect(
                    broker_host,
                    broker_port,
                    keepalive=keepalive,
                    clean_start=True,
                    properties=props,
                )
                logger.info(
                    "Refreshed Entra JWT and reconnected MQTT client (expires=%s)",
                    expires_at.isoformat(),
                )
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("Reconnect after token refresh failed: %s", exc)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to refresh Entra JWT: %s", exc)
            await asyncio.sleep(60)


async def feed(
    api: TfLCyclesAPI,
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
    auth_mode: str = "password",
    entra_audience: str = DEFAULT_ENTRA_AUDIENCE,
    entra_client_id: Optional[str] = None,
    reference_refresh_interval: int = 3600,
) -> None:
    previous_status: Dict[str, Any] = load_state(state_file)
    previous_info: Dict[str, Any] = {}
    last_ref_emit = 0.0

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
        logger.info(
            "Using Microsoft Entra JWT auth (audience=%s, expires=%s)",
            entra_audience,
            expires_at.isoformat(),
        )
    elif username:
        paho_client.username_pw_set(username, password or "")

    if tls or auth_mode == "entra":
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    mqtt_client = UKGovTfLCyclesMqttStationsMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info(
        "Connecting to MQTT broker %s:%s (tls=%s, auth=%s)",
        broker_host,
        broker_port,
        tls or auth_mode == "entra",
        auth_mode,
    )
    if auth_mode == "entra":
        paho_client.connect(
            broker_host,
            broker_port,
            keepalive=60,
            clean_start=True,
            properties=connect_properties,
        )
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)

    if auth_mode == "entra" and expires_at is not None:
        refresh_task = asyncio.create_task(
            _entra_token_refresh_loop(
                paho_client,
                broker_host,
                broker_port,
                60,
                entra_audience,
                entra_client_id,
                expires_at,
            )
        )

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                bikepoints = api.list_bikepoints()
                parsed = [parse_bikepoint(bp) for bp in bikepoints]
                now_ts = time.time()
                reference_due = (now_ts - last_ref_emit) >= reference_refresh_interval

                info_count = 0
                for p in parsed:
                    signature = p.info_signature()
                    if reference_due or previous_info.get(p.station_id) != signature:
                        try:
                            await mqtt_client.publish_uk_gov_tf_l_cycles_mqtt_station_information(
                                feedurl=f"{FEED_URL_ROOT}/BikePoint/{p.station_id}",
                                station_id=p.station_id,
                                data=_build_info(p),
                            )
                            info_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing station info for %s: %s", p.station_id, e)
                        previous_info[p.station_id] = signature
                if reference_due:
                    last_ref_emit = now_ts

                status_count = 0
                for p in parsed:
                    signature = p.status_signature()
                    if previous_status.get(p.station_id) != signature:
                        try:
                            await mqtt_client.publish_uk_gov_tf_l_cycles_mqtt_station_status(
                                feedurl=f"{FEED_URL_ROOT}/BikePoint/{p.station_id}",
                                station_id=p.station_id,
                                data=_build_status(p),
                            )
                            status_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing station status for %s: %s", p.station_id, e)
                        previous_status[p.station_id] = signature

                save_state(state_file, previous_status)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s station info + %s status events in %.1fs. Sleeping until %s.",
                    info_count,
                    status_count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                await asyncio.sleep(polling_interval)
    finally:
        if refresh_task is not None:
            refresh_task.cancel()
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
    parser = argparse.ArgumentParser(description="TfL Santander Cycles -> MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed BikePoint reference and availability CloudEvents to MQTT")
    feed_parser.add_argument("--broker-url", type=str,
                             default=os.getenv("MQTT_BROKER_URL"),
                             help="MQTT broker URL (e.g. mqtt://localhost:1883 or mqtts://broker:8883)")
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("MQTT_HOST"),
                             help="MQTT broker hostname (alternative to --broker-url)")
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("MQTT_PORT", "0")) or None,
                             help="MQTT broker port (default 1883, or 8883 with --tls)")
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"],
                             help="CloudEvents content mode (default: binary)")
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=polling_interval_default,
                             help="Polling interval in seconds")
    feed_parser.add_argument("--reference-refresh-interval", type=int,
                             default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")),
                             help="Seconds between full re-emissions of station reference data")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.tfl_cycles_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle.")
    feed_parser.add_argument("--auth-mode", type=str,
                             default=os.getenv("MQTT_AUTH_MODE", "password"),
                             choices=["password", "entra"],
                             help="Authentication mode: 'password' (default) for username/password, "
                                  "or 'entra' for Microsoft Entra JWT via managed identity "
                                  "(suitable for Azure Event Grid namespace MQTT brokers).")
    feed_parser.add_argument("--entra-audience", type=str,
                             default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE),
                             help=f"Entra token audience (default: {DEFAULT_ENTRA_AUDIENCE}).")
    feed_parser.add_argument("--entra-client-id", type=str,
                             default=os.getenv("MQTT_ENTRA_CLIENT_ID"),
                             help="Optional user-assigned managed identity client id; "
                                  "defaults to DefaultAzureCredential resolution.")
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

    api = TfLCyclesAPI()
    asyncio.run(
        feed(
            api,
            host,
            port,
            args.polling_interval,
            username=username,
            password=password,
            tls=tls,
            client_id=args.client_id,
            state_file=args.state_file,
            once=args.once,
            content_mode=args.content_mode,
            auth_mode=args.auth_mode,
            entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id,
            reference_refresh_interval=args.reference_refresh_interval,
        )
    )


if __name__ == "__main__":
    main()
