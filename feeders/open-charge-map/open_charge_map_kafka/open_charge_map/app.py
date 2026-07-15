"""Kafka feeder application for Open Charge Map.

Drives the Open Charge Map reference-data and POI pollers from
:mod:`open_charge_map_core` and emits CloudEvents through the generated Kafka
producers. Reference events (operators, connection types, current types, charger
types, countries, data providers, status types, usage types, submission-status
types) are emitted first -- as a full snapshot on startup and on a periodic
refresh -- then ChargingLocation telemetry is emitted for locations that changed
since the last ``DateLastStatusUpdate`` high-water mark. Locations are keyed by
the stable Open Charge Map ``poi_id``; reference records by
``{reference_type}/{reference_id}``. Both event families share one Kafka topic.
"""

from __future__ import annotations

import argparse
import dataclasses
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from confluent_kafka import Producer

from open_charge_map_core import (
    POI_URL,
    REFERENCE_URL,
    FeedConfig,
    OpenChargeMapAPI,
    ParsedLocation,
    ParsedReference,
    build_kafka_config,
    load_state,
    parse_kafka_connection_string,
    parse_poi,
    parse_ocm_datetime,
    parse_reference_data,
    save_state,
)
from open_charge_map_producer_data import (
    ChargerType,
    ChargingLocation,
    Connection,
    ConnectionType,
    Country,
    CurrentType,
    DataProvider,
    Operator,
    StatusType,
    SubmissionStatusType,
    UsageType,
)
from open_charge_map_producer_kafka_producer.producer import (
    IOOpenChargeMapLocationsEventProducer,
    IOOpenChargeMapReferenceEventProducer,
)

logger = logging.getLogger(__name__)

# Reference discriminator -> generated data class. The discriminator doubles as
# the send-method suffix (``send_io_open_charge_map_<reference_type>``).
REF_CLASSES = {
    "operator": Operator,
    "connection_type": ConnectionType,
    "current_type": CurrentType,
    "charger_type": ChargerType,
    "country": Country,
    "data_provider": DataProvider,
    "status_type": StatusType,
    "usage_type": UsageType,
    "submission_status_type": SubmissionStatusType,
}


def _build_location(p: ParsedLocation) -> ChargingLocation:
    """Build a generated ``ChargingLocation`` from a parsed location.

    ``ParsedLocation`` and ``ChargingLocation`` share field names by
    construction, so the parsed record is spread straight in; the required
    ``latitude`` / ``longitude`` fall back to ``0.0`` on the rare coordinate-less
    record, and the nested connections are rebuilt as ``Connection`` instances.
    """
    data = dataclasses.asdict(p)
    connections = data.pop("connections")
    if data.get("latitude") is None:
        data["latitude"] = 0.0
    if data.get("longitude") is None:
        data["longitude"] = 0.0
    # asdict already turned each nested ParsedConnection into a kwargs dict.
    return ChargingLocation(
        **data,
        connections=[Connection(**c) for c in connections],
    )


def _build_reference(r: ParsedReference):
    return REF_CLASSES[r.reference_type](**r.fields)


def _initial_watermark(state: Dict[str, Any], modified_since_days: int) -> datetime:
    marker = state.get("watermark")
    parsed = parse_ocm_datetime(marker) if marker else None
    if parsed is not None:
        return parsed
    return datetime.now(timezone.utc) - timedelta(days=modified_since_days)


def feed(
    api: OpenChargeMapAPI,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    cfg: FeedConfig,
) -> None:
    """Feed Open Charge Map reference and location CloudEvents to Kafka."""

    state: Dict[str, Any] = load_state(cfg.state_file)
    poi_sigs: Dict[str, Any] = state.get("pois", {})
    watermark = _initial_watermark(state, cfg.modified_since_days)
    last_ref_emit = 0.0

    raw_producer = Producer(kafka_config)
    loc_producer = IOOpenChargeMapLocationsEventProducer(raw_producer, kafka_topic)
    ref_producer = IOOpenChargeMapReferenceEventProducer(raw_producer, kafka_topic)

    logger.info(
        "Starting Open Charge Map feed to Kafka topic %s at bootstrap servers %s "
        "(country=%s, watermark=%s)",
        kafka_topic,
        kafka_config.get("bootstrap.servers"),
        cfg.country_code or "<global>",
        watermark.isoformat(),
    )

    while True:
        try:
            start_time = datetime.now(timezone.utc)
            now_ts = time.time()
            reference_due = (now_ts - last_ref_emit) >= cfg.reference_refresh_interval

            ref_count = 0
            if reference_due:
                references = parse_reference_data(api.list_reference_data())
                for r in references:
                    try:
                        method = getattr(
                            ref_producer,
                            f"send_io_open_charge_map_{r.reference_type}",
                        )
                        method(
                            _feedurl=f"{REFERENCE_URL}#{r.reference_type}/{r.reference_id}",
                            _reference_type=r.reference_type,
                            _reference_id=str(r.reference_id),
                            data=_build_reference(r),
                            flush_producer=False,
                        )
                        ref_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error(
                            "Error sending reference %s/%s: %s",
                            r.reference_type,
                            r.reference_id,
                            e,
                        )
                last_ref_emit = now_ts

            pois = api.list_pois(
                modified_since=watermark,
                country_code=cfg.country_code,
                max_results=cfg.max_results,
                opendata=cfg.opendata,
            )
            loc_count = 0
            max_change = watermark
            for raw in pois:
                p = parse_poi(raw)
                if p.poi_id == 0:
                    continue
                signature = p.change_signature()
                key = str(p.poi_id)
                if poi_sigs.get(key) != signature:
                    try:
                        loc_producer.send_io_open_charge_map_charging_location(
                            _feedurl=f"{POI_URL}#{p.poi_id}",
                            _poi_id=key,
                            data=_build_location(p),
                            flush_producer=False,
                        )
                        loc_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending location %s: %s", p.poi_id, e)
                    poi_sigs[key] = signature
                latest = p.latest_change()
                if latest is not None and latest > max_change:
                    max_change = latest

            watermark = max_change
            raw_producer.flush()
            state = {"watermark": watermark.isoformat(), "pois": poi_sigs}
            save_state(cfg.state_file, state)

            end_time = datetime.now(timezone.utc)
            effective = max(
                0, cfg.polling_interval - (end_time - start_time).total_seconds()
            )
            logger.info(
                "Sent %s reference + %s location events in %.1fs (watermark=%s). "
                "Waiting until %s.",
                ref_count,
                loc_count,
                (end_time - start_time).total_seconds(),
                watermark.isoformat(),
                (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
            )
            if cfg.once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            if effective > 0:
                time.sleep(effective)
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error occurred: %s", e)
            logger.info("Retrying in %d seconds...", cfg.polling_interval)
            time.sleep(cfg.polling_interval)
    raw_producer.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open Charge Map -> Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed", help="Feed Open Charge Map reference and location CloudEvents to Kafka"
    )
    feed_parser.add_argument(
        "--kafka-bootstrap-servers",
        type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        help="Comma separated list of Kafka bootstrap servers",
    )
    feed_parser.add_argument(
        "--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"),
        help="Kafka topic to send messages to",
    )
    feed_parser.add_argument(
        "--sasl-username", type=str, default=os.getenv("SASL_USERNAME"),
        help="Username for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"),
        help="Password for SASL PLAIN authentication",
    )
    feed_parser.add_argument(
        "-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"),
        help="Microsoft Event Hubs or Fabric Event Stream connection string",
    )
    feed_parser.add_argument(
        "-i", "--polling-interval", type=int,
        default=int(os.getenv("POLLING_INTERVAL", "600")),
        help="Delta polling interval in seconds",
    )
    feed_parser.add_argument(
        "--reference-refresh-interval", type=int,
        default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "86400")),
        help="Seconds between full re-emissions of reference data",
    )
    feed_parser.add_argument(
        "--country-code", type=str, default=os.getenv("OCM_COUNTRYCODE"),
        help="Optional ISO country code to scope the POI query (default: global)",
    )
    feed_parser.add_argument(
        "--modified-since-days", type=int,
        default=int(os.getenv("OCM_MODIFIED_SINCE_DAYS", "1")),
        help="Initial look-back window in days for the first delta poll",
    )
    feed_parser.add_argument(
        "--max-results", type=int, default=int(os.getenv("OCM_MAX_RESULTS", "5000")),
        help="Maximum POI records requested per poll",
    )
    feed_parser.add_argument(
        "--state-file", type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.open_charge_map_state.json")),
    )
    feed_parser.add_argument(
        "--once", action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var).",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    if args.connection_string:
        conn = parse_kafka_connection_string(args.connection_string)
        bootstrap = conn.get("bootstrap.servers")
        topic = conn.get("kafka_topic") or args.kafka_topic
        user = conn.get("sasl.username")
        pwd = conn.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic
        user = args.sasl_username
        pwd = args.sasl_password

    if not bootstrap:
        print("Error: Kafka bootstrap servers must be provided either through CLI or connection string.")
        sys.exit(1)
    if not topic:
        print("Error: Kafka topic must be provided either through CLI or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = build_kafka_config(
        bootstrap_servers=bootstrap,
        sasl_username=user,
        sasl_password=pwd,
        tls_enabled=tls_enabled,
    )

    cfg = FeedConfig.from_env(
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        reference_refresh_interval=args.reference_refresh_interval,
        country_code=args.country_code,
        modified_since_days=args.modified_since_days,
        max_results=args.max_results,
    )
    api = OpenChargeMapAPI()
    feed(api, kafka_config, topic, cfg)


if __name__ == "__main__":
    main()
