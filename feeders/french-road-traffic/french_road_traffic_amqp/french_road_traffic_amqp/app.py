from __future__ import annotations

import argparse
import logging
import os
import time
from typing import Any
from urllib.parse import urlparse

from french_road_traffic_amqp_producer_amqp_producer.producer import (
    FrGouvTransportBisonFuteRoadEventAmqpProducer,
    FrGouvTransportBisonFuteTrafficFlowAmqpProducer,
)
from french_road_traffic_amqp_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
from french_road_traffic_amqp_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
from french_road_traffic_core.french_road_traffic import (
    DEFAULT_POLL_INTERVAL_SECONDS,
    FEED_SOURCE_EVENTS,
    FEED_SOURCE_FLOW,
    FrenchRoadTrafficSource,
)

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str) -> tuple[str, int, bool, str | None, str | None, str | None]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in {"amqps", "ssl", "tls"}
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _producer_kwargs(args: argparse.Namespace) -> dict[str, Any]:
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_password, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_password
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        address = path or address
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    kwargs: dict[str, Any] = {
        "host": host,
        "address": address,
        "port": port,
        "content_mode": args.content_mode,
        "use_tls": tls,
    }
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        kwargs.update(
            credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(),
            entra_audience=args.entra_audience,
        )
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return kwargs


def _flow_data(record: dict[str, Any]) -> TrafficFlowMeasurement:
    return TrafficFlowMeasurement(**record)


def _event_data(record: dict[str, Any]) -> RoadEvent:
    return RoadEvent(**record)


def _publish_cycle(source: FrenchRoadTrafficSource, flow_producer: FrGouvTransportBisonFuteTrafficFlowAmqpProducer, event_producer: FrGouvTransportBisonFuteRoadEventAmqpProducer) -> None:
    flow_count = 0
    event_count = 0
    for record in source.fetch_traffic_flow():
        flow_producer.send_amqp(data=_flow_data(record), _feedurl=FEED_SOURCE_FLOW, _site_id=record["site_id"])
        flow_count += 1
    for record in source.fetch_road_events():
        event_producer.send_amqp(data=_event_data(record), _feedurl=FEED_SOURCE_EVENTS, _situation_id=record["situation_id"])
        event_count += 1
    logger.info("Published %d flow measurements and %d road events", flow_count, event_count)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="French Road Traffic AMQP bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "french-road-traffic"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", "https://servicebus.azure.net/.default"))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")

    source = FrenchRoadTrafficSource()
    kwargs = _producer_kwargs(args)
    flow_producer = FrGouvTransportBisonFuteTrafficFlowAmqpProducer(**kwargs)
    event_producer = FrGouvTransportBisonFuteRoadEventAmqpProducer(**kwargs)
    try:
        while True:
            _publish_cycle(source, flow_producer, event_producer)
            if args.once:
                break
            time.sleep(args.polling_interval)
    finally:
        flow_producer.close()
        event_producer.close()


if __name__ == "__main__":
    main()
