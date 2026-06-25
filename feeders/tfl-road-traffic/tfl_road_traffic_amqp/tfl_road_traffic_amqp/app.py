"""AMQP 1.0 companion feeder for tfl-road-traffic."""

from __future__ import annotations

import argparse
import logging
import os
import time
from urllib.parse import urlparse

from tfl_road_traffic_amqp_producer_amqp_producer.producer import UkGovTflRoadAmqpProducer
from tfl_road_traffic_amqp_producer_data import RoadCorridor, RoadDisruption, RoadStatus
from tfl_road_traffic_core.tfl_road_traffic import TflRoadTrafficSource, build_road_corridor_record, build_road_disruption_record, build_road_status_record

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(args):
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_pwd
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
    kwargs = dict(host=host, address=address, port=port, content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return UkGovTflRoadAmqpProducer(**kwargs)


class TflRoadTrafficAmqpBridge(TflRoadTrafficSource):
    def __init__(self, producer: UkGovTflRoadAmqpProducer, *, polling_interval: int = 60, reference_refresh_interval: int = 3600) -> None:
        super().__init__(polling_interval=polling_interval, reference_refresh_interval=reference_refresh_interval)
        self.producer = producer

    def publish_corridor(self, raw: dict) -> bool:
        record = build_road_corridor_record(raw)
        if record is None:
            return False
        data = RoadCorridor(**record)
        self.producer.send_road_corridor(data=data, _road_id=data.road_id)
        return True

    def publish_status(self, raw: dict) -> bool:
        record = build_road_status_record(raw)
        if record is None:
            return False
        data = RoadStatus(**record)
        self.producer.send_road_status(data=data, _road_id=data.road_id)
        return True

    def publish_disruption(self, raw: dict) -> bool:
        pending, candidate_state = self.pending_disruptions([raw])
        if not pending:
            return False
        for record in pending:
            data = RoadDisruption(**record)
            method = getattr(self.producer, f"send_road_disruption_{data.severity}")
            method(data=data, _road_id=data.road_id, _severity=data.severity, _disruption_id=data.disruption_id)
        self.commit_disruption_state(candidate_state)
        return True

    def publish_cycle(self) -> None:
        if self.reference_due():
            corridors = self.fetch_corridors() or []
            for raw in corridors:
                self.publish_corridor(raw)
            self.remember_reference_fetch(corridors)
        for raw in self.fetch_statuses() or []:
            self.publish_status(raw)
        for raw in self.fetch_disruptions() or []:
            self.publish_disruption(raw)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(description="tfl-road-traffic AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "tfl-road-traffic"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", "https://servicebus.azure.net/.default"))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    parser.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "3600")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")

    producer = _build_amqp_producer(args)
    bridge = TflRoadTrafficAmqpBridge(producer, polling_interval=args.polling_interval, reference_refresh_interval=args.reference_refresh_interval)
    try:
        while True:
            bridge.publish_cycle()
            if args.once:
                break
            time.sleep(args.polling_interval)
    finally:
        producer.close()
