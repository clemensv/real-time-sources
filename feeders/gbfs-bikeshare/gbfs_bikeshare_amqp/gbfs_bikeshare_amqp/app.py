from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Optional
from urllib.parse import urlparse

from gbfs_bikeshare_amqp_producer_amqp_producer.producer import (
    OrgGbfsAmqpFreeBikesProducer,
    OrgGbfsAmqpStationsProducer,
    OrgGbfsAmqpSystemProducer,
)
from gbfs_bikeshare_amqp_producer_data import FreeBikeStatus, StationInformation, StationStatus, SystemInformation
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

logger = logging.getLogger(__name__)
DEFAULT_STATE_FILE = os.path.expanduser("~/.gbfs_bikeshare_amqp_state.json")
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


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


def _parse_broker_url(url: Optional[str]) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    if not url:
        return "", 5672, False, None, None
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in {"amqps", "ssl", "tls"}
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password


def _build_producers(args: argparse.Namespace) -> tuple[OrgGbfsAmqpSystemProducer, OrgGbfsAmqpStationsProducer, OrgGbfsAmqpFreeBikesProducer]:
    host, port, tls_from_url, user_from_url, password_from_url = _parse_broker_url(args.amqp_broker_url)
    host = args.amqp_host or host
    port = args.amqp_port if args.amqp_port is not None else port
    use_tls = parse_bool(args.amqp_tls, default=tls_from_url)
    address = args.amqp_address or "gbfs-bikeshare"
    auth_mode = (args.amqp_auth_mode or "password").lower()
    username = args.amqp_username or user_from_url
    password = args.amqp_password or password_from_url
    common_kwargs = {"host": host, "port": port, "address": address, "content_mode": args.amqp_content_mode, "use_tls": use_tls}
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.amqp_entra_client_id) if args.amqp_entra_client_id else DefaultAzureCredential()
        audience = args.amqp_entra_audience or (DEFAULT_ENTRA_AUDIENCE_SERVICEBUS if use_tls else DEFAULT_ENTRA_AUDIENCE_EVENTHUBS)
        return (
            OrgGbfsAmqpSystemProducer(credential=credential, entra_audience=audience, **common_kwargs),
            OrgGbfsAmqpStationsProducer(credential=credential, entra_audience=audience, **common_kwargs),
            OrgGbfsAmqpFreeBikesProducer(credential=credential, entra_audience=audience, **common_kwargs),
        )
    if auth_mode == "sas":
        return (
            OrgGbfsAmqpSystemProducer(sas_key_name=args.amqp_sas_key_name, sas_key=args.amqp_sas_key, **common_kwargs),
            OrgGbfsAmqpStationsProducer(sas_key_name=args.amqp_sas_key_name, sas_key=args.amqp_sas_key, **common_kwargs),
            OrgGbfsAmqpFreeBikesProducer(sas_key_name=args.amqp_sas_key_name, sas_key=args.amqp_sas_key, **common_kwargs),
        )
    return (
        OrgGbfsAmqpSystemProducer(username=username, password=password, **common_kwargs),
        OrgGbfsAmqpStationsProducer(username=username, password=password, **common_kwargs),
        OrgGbfsAmqpFreeBikesProducer(username=username, password=password, **common_kwargs),
    )


def feed(args: argparse.Namespace) -> None:
    configured_feeds = parse_feed_configuration(args.gbfs_feeds, args.gbfs_system_ids)
    system_producer, stations_producer, free_bikes_producer = _build_producers(args)
    state = load_state(args.state_file)
    client = GbfsSourceClient()
    sources = discover_sources(client, configured_feeds)
    if not sources:
        raise SystemExit("No GBFS feeds could be discovered successfully.")
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
                            system_producer.send_system_information(data=_build_system_information(system_record), _feed_url=feed_url, _system_id=system_record.system_id)
                        stations, station_feed_url = client.fetch_station_information(source)
                        if station_feed_url:
                            for station in stations:
                                stations_producer.send_station_information(data=_build_station_information(station), _feed_url=station_feed_url, _system_id=station.system_id, _station_id=station.station_id)
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
                            stations_producer.send_station_status(data=_build_station_status(status), _feed_url=station_feed_url, _system_id=status.system_id, _station_id=status.station_id)
                    bikes, bike_feed_url, _ = client.fetch_free_bike_status(source)
                    if bike_feed_url:
                        for bike in bikes:
                            if not should_publish_free_bike_status(bike, state):
                                continue
                            free_bikes_producer.send_free_bike_status(data=_build_free_bike_status(bike), _feed_url=bike_feed_url, _system_id=bike.system_id, _bike_id=bike.bike_id)
                except Exception as exc:  # pylint: disable=broad-except
                    logger.warning("Telemetry poll failed for %s: %s", source.autodiscovery_url, exc)
            save_state(args.state_file, state)
            if args.once:
                logger.info("--once mode: exiting after first polling cycle")
                return
            elapsed = time.time() - cycle_started
            time.sleep(max(1, args.poll_interval - int(elapsed)))
    finally:
        for producer in (system_producer, stations_producer, free_bikes_producer):
            try:
                producer.close()
            except Exception:  # pragma: no cover
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GBFS bikeshare -> AMQP bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Poll GBFS feeds and publish CloudEvents to AMQP")
    feed_parser.add_argument("--gbfs-feeds", default=os.getenv("GBFS_FEEDS"))
    feed_parser.add_argument("--gbfs-system-ids", default=os.getenv("GBFS_SYSTEM_IDS"))
    feed_parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL", "60")))
    feed_parser.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")))
    feed_parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--amqp-broker-url", default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--amqp-host", default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--amqp-port", type=int, default=int(os.getenv("AMQP_PORT")) if os.getenv("AMQP_PORT") else None)
    feed_parser.add_argument("--amqp-address", default=os.getenv("AMQP_ADDRESS", "gbfs-bikeshare"))
    feed_parser.add_argument("--amqp-username", default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--amqp-password", default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--amqp-auth-mode", default=os.getenv("AMQP_AUTH_MODE", "password"))
    feed_parser.add_argument("--amqp-tls", default=os.getenv("AMQP_TLS", "false"))
    feed_parser.add_argument("--amqp-content-mode", default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    feed_parser.add_argument("--amqp-entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--amqp-entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--amqp-sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--amqp-sas-key", default=os.getenv("AMQP_SAS_KEY"))
    return parser


def main(argv: Optional[list[str]] = None) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return
    try:
        feed(args)
    except KeyboardInterrupt:
        logger.info("Interrupted, exiting.")
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("GBFS AMQP bridge failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
