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

from gbfs_bikeshare_core import load_state, parse_bool, parse_feed_configuration, save_state
from gbfs_bikeshare_core.acquisition import (
    GbfsSourceClient,
    FreeBikeStatusRecord,
    StationInformationRecord,
    StationStatusRecord,
    SystemInformationRecord,
    discover_sources,
    should_publish_free_bike_status,
    should_publish_station_status,
)
from gbfs_bikeshare_mqtt_producer_data import FreeBikeStatus, StationInformation, StationStatus, SystemInformation
from gbfs_bikeshare_mqtt_producer_mqtt_client.client import (
    OrgGbfsMqttFreeBikesMqttClient,
    OrgGbfsMqttStationsMqttClient,
    OrgGbfsMqttSystemMqttClient,
)

logger = logging.getLogger(__name__)
DEFAULT_STATE_FILE = os.path.expanduser("~/.gbfs_bikeshare_mqtt_state.json")
DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"


def _build_system_information(record: SystemInformationRecord) -> SystemInformation:
    return SystemInformation(
        system_id=record.system_id,
        name=record.name,
        operator=record.operator,
        url=record.url,
        timezone=record.timezone,
        language=record.language,
        phone_number=record.phone_number,
    )


def _build_station_information(record: StationInformationRecord) -> StationInformation:
    return StationInformation(
        system_id=record.system_id,
        station_id=record.station_id,
        name=record.name,
        short_name=record.short_name,
        lat=record.lat,
        lon=record.lon,
        capacity=record.capacity,
        region_id=record.region_id,
        address=record.address,
        post_code=record.post_code,
    )


def _build_station_status(record: StationStatusRecord) -> StationStatus:
    return StationStatus(
        system_id=record.system_id,
        station_id=record.station_id,
        num_bikes_available=record.num_bikes_available,
        num_docks_available=record.num_docks_available,
        num_ebikes_available=record.num_ebikes_available,
        is_installed=record.is_installed,
        is_renting=record.is_renting,
        is_returning=record.is_returning,
        last_reported=record.last_reported,
    )


def _build_free_bike_status(record: FreeBikeStatusRecord) -> FreeBikeStatus:
    return FreeBikeStatus(
        system_id=record.system_id,
        bike_id=record.bike_id,
        lat=record.lat,
        lon=record.lon,
        is_reserved=record.is_reserved,
        is_disabled=record.is_disabled,
        vehicle_type_id=record.vehicle_type_id,
        current_range_meters=record.current_range_meters,
        last_reported=record.last_reported,
    )


def _parse_broker_settings(args: argparse.Namespace) -> tuple[str, int, bool]:
    broker_url = args.mqtt_broker_url or (f"mqtt://{args.mqtt_host}:{args.mqtt_port}" if args.mqtt_host else None)
    if not broker_url:
        raise SystemExit("MQTT_BROKER_URL or MQTT_HOST/MQTT_PORT must be provided.")
    parsed = urlparse(broker_url if "://" in broker_url else f"mqtt://{broker_url}")
    tls = parse_bool(args.mqtt_tls, default=parsed.scheme.lower() == "mqtts")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple[str, datetime]:
    from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

    credential = ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
    scope = audience if audience.endswith("/.default") else f"{audience}.default" if audience.endswith("/") else f"{audience}/.default"
    token = credential.get_token(scope)
    expires_at = datetime.fromtimestamp(token.expires_on, tz=timezone.utc)
    return token.token, expires_at


async def _entra_token_refresh_loop(client: mqtt.Client, host: str, port: int, audience: str, client_id: Optional[str], expires_at: datetime) -> None:
    while True:
        now = datetime.now(timezone.utc)
        sleep_seconds = max(60.0, (expires_at - now).total_seconds() - 300.0)
        await asyncio.sleep(sleep_seconds)
        token, expires_at = _acquire_entra_token(audience, client_id)
        props = Properties(PacketTypes.CONNECT)
        props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
        props.AuthenticationData = token.encode("utf-8")
        try:
            client.disconnect()
        except Exception:  # pragma: no cover
            pass
        client.connect(host, port, keepalive=60, clean_start=True, properties=props)
        logger.info("Refreshed Entra JWT and reconnected MQTT client")


async def feed(args: argparse.Namespace) -> None:
    configured_feeds = parse_feed_configuration(args.gbfs_feeds, args.gbfs_system_ids)
    host, port, tls = _parse_broker_settings(args)
    state = load_state(args.state_file)
    client = GbfsSourceClient()
    sources = discover_sources(client, configured_feeds)
    if not sources:
        raise SystemExit("No GBFS feeds could be discovered successfully.")

    paho_client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=args.mqtt_client_id or "", protocol=MQTTv5)
    auth_mode = (args.mqtt_auth_mode or "anonymous").lower()
    refresh_task: Optional[asyncio.Task] = None
    if auth_mode == "userpass" and args.mqtt_username:
        paho_client.username_pw_set(args.mqtt_username, args.mqtt_password or "")
    if auth_mode == "tls-cert":
        paho_client.tls_set(ca_certs=args.mqtt_ca_file or None, certfile=args.mqtt_client_cert, keyfile=args.mqtt_client_key)
    elif tls or auth_mode == "entra":
        paho_client.tls_set(ca_certs=args.mqtt_ca_file or None)

    loop = asyncio.get_running_loop()
    system_client = OrgGbfsMqttSystemMqttClient(paho_client, content_mode="binary", loop=loop)
    stations_client = OrgGbfsMqttStationsMqttClient(paho_client, content_mode="binary", loop=loop)
    free_bikes_client = OrgGbfsMqttFreeBikesMqttClient(paho_client, content_mode="binary", loop=loop)

    if auth_mode == "entra":
        token, expires_at = _acquire_entra_token(args.mqtt_entra_audience, args.mqtt_entra_client_id)
        props = Properties(PacketTypes.CONNECT)
        props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
        props.AuthenticationData = token.encode("utf-8")
        if args.mqtt_username:
            paho_client.username_pw_set(args.mqtt_username, "")
        paho_client.connect(host, port, keepalive=60, clean_start=True, properties=props)
        paho_client.loop_start()
        refresh_task = asyncio.create_task(_entra_token_refresh_loop(paho_client, host, port, args.mqtt_entra_audience, args.mqtt_entra_client_id, expires_at))
        logger.info("Using Entra ID MQTT auth (expires %s)", expires_at.isoformat())
    else:
        await system_client.connect(host, port)

    last_reference_refresh = 0.0
    reference_refresh = max(300, args.reference_refresh_interval)
    try:
        while True:
            cycle_started = time.time()
            if last_reference_refresh == 0.0 or cycle_started - last_reference_refresh >= reference_refresh:
                for source in sources:
                    try:
                        system_payload = client.fetch_system_information(source)
                        if system_payload is not None:
                            system_record, feed_url = system_payload
                            await system_client.publish_org_gbfs_mqtt_system_information(feed_url=feed_url, system_id=system_record.system_id, data=_build_system_information(system_record))
                        stations, station_feed_url = client.fetch_station_information(source)
                        if station_feed_url:
                            for station in stations:
                                await stations_client.publish_org_gbfs_mqtt_station_information(feed_url=station_feed_url, system_id=station.system_id, station_id=station.station_id, data=_build_station_information(station))
                    except Exception as exc:  # pylint: disable=broad-except
                        logger.warning("Reference refresh failed for %s: %s", source.autodiscovery_url, exc)
                last_reference_refresh = cycle_started

            for source in sources:
                try:
                    statuses, station_feed_url, _ = client.fetch_station_status(source)
                    if station_feed_url:
                        for status in statuses:
                            if not should_publish_station_status(status, state):
                                continue
                            await stations_client.publish_org_gbfs_mqtt_station_status(feed_url=station_feed_url, system_id=status.system_id, station_id=status.station_id, data=_build_station_status(status))
                    bikes, bike_feed_url, _ = client.fetch_free_bike_status(source)
                    if bike_feed_url:
                        for bike in bikes:
                            if not should_publish_free_bike_status(bike, state):
                                continue
                            await free_bikes_client.publish_org_gbfs_mqtt_free_bike_status(feed_url=bike_feed_url, system_id=bike.system_id, bike_id=bike.bike_id, data=_build_free_bike_status(bike))
                except Exception as exc:  # pylint: disable=broad-except
                    logger.warning("Telemetry poll failed for %s: %s", source.autodiscovery_url, exc)
            save_state(args.state_file, state)
            if args.once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            elapsed = time.time() - cycle_started
            await asyncio.sleep(max(1, args.poll_interval - int(elapsed)))
    finally:
        if refresh_task is not None:
            refresh_task.cancel()
        try:
            await system_client.disconnect()
        except Exception:  # pragma: no cover
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GBFS bikeshare -> MQTT bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll GBFS feeds and publish CloudEvents to MQTT")
    feed_parser.add_argument("--gbfs-feeds", default=os.getenv("GBFS_FEEDS"))
    feed_parser.add_argument("--gbfs-system-ids", default=os.getenv("GBFS_SYSTEM_IDS"))
    feed_parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "60")))
    feed_parser.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--mqtt-host", default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--mqtt-port", type=int, default=int(os.getenv("MQTT_PORT", "1883")))
    feed_parser.add_argument("--mqtt-tls", default=os.getenv("MQTT_TLS", os.getenv("MQTT_ENABLE_TLS", "false")))
    feed_parser.add_argument("--mqtt-auth-mode", default=os.getenv("MQTT_AUTH_MODE", "anonymous"))
    feed_parser.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--mqtt-ca-file", default=os.getenv("MQTT_CA_FILE"))
    feed_parser.add_argument("--mqtt-client-cert", default=os.getenv("MQTT_CLIENT_CERT"))
    feed_parser.add_argument("--mqtt-client-key", default=os.getenv("MQTT_CLIENT_KEY"))
    feed_parser.add_argument("--mqtt-entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--mqtt-entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    try:
        asyncio.run(feed(args))
    except KeyboardInterrupt:
        logger.info("Interrupted, exiting.")
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("GBFS MQTT bridge failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
