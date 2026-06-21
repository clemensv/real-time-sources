from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urlparse

from siri_amqp_producer_amqp_producer import OrgSiriAmqpProducer
from siri_amqp_producer_data import Operator, VehiclePosition
from siri_core import SUPPORTED_PROVIDERS, FeedConfig, SiriClient, load_state, parse_csv_tokens, parse_data_types, save_state

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

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


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def _build_producer(
    *,
    host: str,
    port: int,
    address: str,
    use_tls: bool,
    auth_mode: str,
    username: Optional[str],
    password: Optional[str],
    entra_audience: str,
    entra_client_id: Optional[str],
    sas_key_name: Optional[str],
    sas_key: Optional[str],
) -> OrgSiriAmqpProducer:
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return OrgSiriAmqpProducer(
            host=host,
            address=address,
            port=port,
            credential=credential,
            entra_audience=entra_audience,
            use_tls=use_tls,
            content_mode="binary",
        )
    if auth_mode == "sas":
        return OrgSiriAmqpProducer(
            host=host,
            address=address,
            port=port,
            sas_key_name=sas_key_name,
            sas_key=sas_key,
            use_tls=use_tls,
            content_mode="binary",
        )
    return OrgSiriAmqpProducer(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        use_tls=use_tls,
        content_mode="binary",
    )


def feed(
    api: SiriClient,
    producer: OrgSiriAmqpProducer,
    polling_interval: int,
    *,
    state_file: str = "",
    once: bool = False,
) -> None:
    previous_items = load_state(state_file)
    known_operators: set[str] = set()

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                snapshot = api.load_snapshot()
                operator_set = set(snapshot.operators)
                if not known_operators or operator_set != known_operators:
                    for operator_ref in snapshot.operators:
                        producer.send_operator(
                            data=_build_operator(operator_ref),
                            _feedurl=snapshot.operator_feed_urls[operator_ref],
                            _operator_ref=operator_ref,
                        )
                    known_operators = operator_set
                    logger.info("Published %d operator reference events", len(snapshot.operators))

                    emitted = 0
                else:
                    emitted = 0
                next_items = dict(previous_items)
                for position in snapshot.vehicle_positions:
                    if previous_items.get(position.identity) == position.item_identifier:
                        continue
                    producer.send_vehicle_position(
                        data=_build_vehicle_position(position),
                        _feedurl=position.feedurl,
                        _operator_ref=position.operator_ref,
                        _vehicle_ref=position.vehicle_ref,
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
                    time.sleep(effective)
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", exc)
                if once:
                    raise
                time.sleep(polling_interval)
    finally:
        try:
            producer.close()
        except Exception:  # pylint: disable=broad-except
            pass


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    tls = (parsed.scheme or "amqp").lower() in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SIRI VehicleMonitoring → AMQP bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed operator metadata and vehicle positions as CloudEvents over AMQP 1.0")
    feed_parser.add_argument("--provider", choices=SUPPORTED_PROVIDERS, default=os.getenv("SIRI_PROVIDER", "bods"))
    feed_parser.add_argument("--siri-url", type=str, default=os.getenv("SIRI_URL"))
    feed_parser.add_argument("--api-key", type=str, default=os.getenv("SIRI_API_KEY") or os.getenv("BODS_API_KEY"))
    feed_parser.add_argument("--headers", type=str, default=os.getenv("SIRI_HEADERS"))
    feed_parser.add_argument("--et-client-name", type=str, default=os.getenv("SIRI_ET_CLIENT_NAME"))
    feed_parser.add_argument("--operators", type=str, default=os.getenv("SIRI_OPERATORS") or os.getenv("OPERATORS"))
    feed_parser.add_argument("--data-types", type=str, default=os.getenv("SIRI_DATA_TYPES", "vm"))
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "siri"))
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--auth-mode", choices=["password", "entra", "sas"], default=os.getenv("AMQP_AUTH_MODE", "password"))
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "30")))
    feed_parser.add_argument("--state-file", type=str, default=os.getenv("STATE_FILE", os.path.expanduser("~/.siri_state.json")))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    config = FeedConfig.from_env(
        provider=args.provider,
        siri_url=args.siri_url,
        api_key=args.api_key,
        operators=parse_csv_tokens(args.operators),
        data_types=parse_data_types(args.data_types),
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        request_headers=args.headers,
        et_client_name=args.et_client_name,
    )

    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = args.tls or args.auth_mode in ("entra", "sas")
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password

    producer = _retry_producer_init(lambda: _build_producer(
        host=host,
        port=port,
        address=address,
        use_tls=tls,
        auth_mode=args.auth_mode,
        username=username,
        password=password,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
    ))
    api = SiriClient(
        provider=config.provider,
        siri_url=config.siri_url,
        api_key=config.api_key,
        operators=config.operators,
        data_types=config.data_types,
        request_headers=config.request_headers,
    )
    feed(api, producer, config.polling_interval, state_file=config.state_file, once=config.once)


if __name__ == "__main__":
    main()
