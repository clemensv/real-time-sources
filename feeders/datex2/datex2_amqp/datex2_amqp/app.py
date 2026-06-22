from __future__ import annotations

import argparse
import logging
import os
import time
import urllib.parse

from datex2_amqp_producer_amqp_producer.producer import (
    OrgDatex2MeasuredSiteAmqpProducer,
    OrgDatex2SituationAmqpProducer,
    OrgDatex2TrafficMeasurementAmqpProducer,
)
from datex2_amqp_producer_data import MeasurementSite, SituationRecord, TrafficMeasurement
from datex2_core import collect_batches, load_endpoints


def _producer_args(args: argparse.Namespace) -> dict:
    host = args.host
    port = args.port
    username = args.username
    password = args.password
    use_tls = args.tls
    if args.broker_url:
        parsed = urllib.parse.urlparse(args.broker_url)
        host = parsed.hostname or host
        port = parsed.port or port
        use_tls = use_tls or parsed.scheme == "amqps"
        username = urllib.parse.unquote(parsed.username) if parsed.username else username
        password = urllib.parse.unquote(parsed.password) if parsed.password else password
    kwargs = dict(host=host, address=args.address, port=port, username=username, password=password, use_tls=use_tls, content_mode="binary")
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        kwargs.update(credential=credential, entra_audience=args.entra_audience, username=None, password=None, use_tls=True)
    elif args.auth_mode == "sas":
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key, sas_token_ttl_seconds=args.sas_token_ttl_seconds, username=None, password=None)
    return kwargs


def feed(args: argparse.Namespace) -> None:
    kwargs = _producer_args(args)
    sites = OrgDatex2MeasuredSiteAmqpProducer(**kwargs)
    measured = OrgDatex2TrafficMeasurementAmqpProducer(**kwargs)
    situation = OrgDatex2SituationAmqpProducer(**kwargs)
    try:
        while True:
            batch = collect_batches(load_endpoints(args.datex2_endpoints, mock=args.mock, sources_file=args.datex2_sources_file, selector=args.datex2_sources), mock=args.mock, max_records=args.max_records)
            for row in batch.measurement_sites:
                sites.send_amqp(data=MeasurementSite(**row), _feed_url=row["feed_url"], _supplier_id=row["supplier_id"], _measurement_site_id=row["measurement_site_id"])
            for row in batch.traffic_measurements:
                measured.send_amqp(data=TrafficMeasurement(**row), _feed_url=row["feed_url"], _supplier_id=row["supplier_id"], _measurement_site_id=row["measurement_site_id"])
            for row in batch.situation_records:
                situation.send_amqp(data=SituationRecord(**row), _feed_url=row["feed_url"], _supplier_id=row["supplier_id"], _situation_record_id=row["situation_record_id"])
            if args.once:
                break
            time.sleep(args.polling_interval)
    finally:
        for producer in (sites, measured, situation):
            close = getattr(producer, "close", None)
            if close:
                close()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DATEX II AMQP feeder")
    sub = parser.add_subparsers(dest="command")
    feed_parser = sub.add_parser("feed")
    feed_parser.add_argument("--datex2-endpoints", default=os.getenv("DATEX2_ENDPOINTS", ""))
    feed_parser.add_argument("--datex2-sources-file", default=os.getenv("DATEX2_SOURCES_FILE", ""))
    feed_parser.add_argument("--datex2-sources", default=os.getenv("DATEX2_SOURCES", ""))
    feed_parser.add_argument("--mock", action="store_true", default=os.getenv("DATEX2_MOCK", "").lower() == "true")
    feed_parser.add_argument("--max-records", type=int, default=int(os.getenv("MAX_RECORDS_PER_FAMILY", "25")))
    feed_parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", ""))
    feed_parser.add_argument("--host", default=os.getenv("AMQP_HOST", "localhost"))
    feed_parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "5672")))
    feed_parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "datex2"))
    feed_parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action=argparse.BooleanOptionalAction, default=os.getenv("AMQP_TLS", "false").lower() == "true")
    feed_parser.add_argument("--auth-mode", default=os.getenv("AMQP_AUTH_MODE", "password"))
    feed_parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", "https://servicebus.azure.net/.default"))
    feed_parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID") or os.getenv("AZURE_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("--sas-token-ttl-seconds", type=int, default=int(os.getenv("AMQP_SAS_TOKEN_TTL_SECONDS", "3600")))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "false").lower() == "true")
    return parser


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    parser = _parser()
    args = parser.parse_args()
    if args.command != "feed":
        args = parser.parse_args(["feed"])
    feed(args)
