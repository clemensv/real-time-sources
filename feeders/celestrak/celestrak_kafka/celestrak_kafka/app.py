"""Kafka feeder application for CelesTrak.

Drives the upstream CelesTrak poller from :mod:`celestrak_core` and emits
CloudEvents through the generated Kafka producer. Reference data (the SATCAT
catalog) is emitted first and refreshed periodically; the General Perturbations
(GP) orbital element sets follow as telemetry, deduplicated on their ``EPOCH``
so unchanged element sets are not re-sent. Optional Supplemental GP (SupGP)
sources are emitted only when ``SUPGP_SOURCES`` is set.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from confluent_kafka import Producer

from celestrak_core import (
    GP_URL,
    SATCAT_URL,
    SUPGP_URL,
    CelesTrakAPI,
    FeedConfig,
    build_kafka_config,
    load_state,
    parse_kafka_connection_string,
    save_state,
)
from celestrak_producer_data.org.celestrak.orbitmeanelements import OrbitMeanElements
from celestrak_producer_data.org.celestrak.satellitecatalogentry import SatelliteCatalogEntry
from celestrak_producer_data.org.celestrak.supplementalorbitmeanelements import (
    SupplementalOrbitMeanElements,
)
from celestrak_producer_kafka_producer.producer import OrgCelestrakKafkaEventProducer

logger = logging.getLogger(__name__)


def _opt_str(raw: Dict[str, Any], key: str) -> Optional[str]:
    value = raw.get(key)
    return value if value not in (None, "") else None


def _opt_float(raw: Dict[str, Any], key: str) -> Optional[float]:
    value = raw.get(key)
    if value is None or value == "":
        return None
    return float(value)


def _opt_int(raw: Dict[str, Any], key: str) -> Optional[int]:
    value = raw.get(key)
    if value is None or value == "":
        return None
    return int(value)


def _build_satcat(raw: Dict[str, Any]) -> SatelliteCatalogEntry:
    return SatelliteCatalogEntry(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        OBJECT_TYPE=_opt_str(raw, "OBJECT_TYPE"),
        OPS_STATUS_CODE=_opt_str(raw, "OPS_STATUS_CODE"),
        OWNER=_opt_str(raw, "OWNER"),
        LAUNCH_DATE=_opt_str(raw, "LAUNCH_DATE"),
        LAUNCH_SITE=_opt_str(raw, "LAUNCH_SITE"),
        DECAY_DATE=_opt_str(raw, "DECAY_DATE"),
        PERIOD=_opt_float(raw, "PERIOD"),
        INCLINATION=_opt_float(raw, "INCLINATION"),
        APOGEE=_opt_int(raw, "APOGEE"),
        PERIGEE=_opt_int(raw, "PERIGEE"),
        RCS=_opt_float(raw, "RCS"),
        DATA_STATUS_CODE=_opt_str(raw, "DATA_STATUS_CODE"),
        ORBIT_CENTER=_opt_str(raw, "ORBIT_CENTER"),
        ORBIT_TYPE=_opt_str(raw, "ORBIT_TYPE"),
    )


def _build_gp(raw: Dict[str, Any]) -> OrbitMeanElements:
    return OrbitMeanElements(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        EPOCH=datetime.fromisoformat(raw["EPOCH"]),
        MEAN_MOTION=float(raw["MEAN_MOTION"]),
        ECCENTRICITY=float(raw["ECCENTRICITY"]),
        INCLINATION=float(raw["INCLINATION"]),
        RA_OF_ASC_NODE=float(raw["RA_OF_ASC_NODE"]),
        ARG_OF_PERICENTER=float(raw["ARG_OF_PERICENTER"]),
        MEAN_ANOMALY=float(raw["MEAN_ANOMALY"]),
        EPHEMERIS_TYPE=int(raw["EPHEMERIS_TYPE"]),
        CLASSIFICATION_TYPE=raw["CLASSIFICATION_TYPE"],
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        ELEMENT_SET_NO=int(raw["ELEMENT_SET_NO"]),
        REV_AT_EPOCH=int(raw["REV_AT_EPOCH"]),
        BSTAR=float(raw["BSTAR"]),
        MEAN_MOTION_DOT=float(raw["MEAN_MOTION_DOT"]),
        MEAN_MOTION_DDOT=float(raw["MEAN_MOTION_DDOT"]),
    )


def _build_supgp(raw: Dict[str, Any]) -> SupplementalOrbitMeanElements:
    return SupplementalOrbitMeanElements(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        EPOCH=datetime.fromisoformat(raw["EPOCH"]),
        MEAN_MOTION=float(raw["MEAN_MOTION"]),
        ECCENTRICITY=float(raw["ECCENTRICITY"]),
        INCLINATION=float(raw["INCLINATION"]),
        RA_OF_ASC_NODE=float(raw["RA_OF_ASC_NODE"]),
        ARG_OF_PERICENTER=float(raw["ARG_OF_PERICENTER"]),
        MEAN_ANOMALY=float(raw["MEAN_ANOMALY"]),
        EPHEMERIS_TYPE=int(raw["EPHEMERIS_TYPE"]),
        CLASSIFICATION_TYPE=raw["CLASSIFICATION_TYPE"],
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        ELEMENT_SET_NO=int(raw["ELEMENT_SET_NO"]),
        REV_AT_EPOCH=int(raw["REV_AT_EPOCH"]),
        BSTAR=float(raw["BSTAR"]),
        MEAN_MOTION_DOT=float(raw["MEAN_MOTION_DOT"]),
        MEAN_MOTION_DDOT=float(raw["MEAN_MOTION_DDOT"]),
        RMS=_opt_float(raw, "RMS"),
        DATA_SOURCE=_opt_str(raw, "DATA_SOURCE"),
    )


def _satcat_source(norad: int) -> str:
    return f"{SATCAT_URL}?CATNR={norad}&FORMAT=json"


def _gp_source(norad: int) -> str:
    return f"{GP_URL}?CATNR={norad}&FORMAT=json"


def _supgp_source(norad: int) -> str:
    return f"{SUPGP_URL}?CATNR={norad}&FORMAT=json"


def _emit_reference(
    api: CelesTrakAPI,
    producer: Producer,
    ce: OrgCelestrakKafkaEventProducer,
    cfg: FeedConfig,
) -> int:
    satcat = api.get_satcat(cfg.groups)
    count = 0
    for row in satcat:
        norad = int(row["NORAD_CAT_ID"])
        try:
            ce.send_org_celestrak_kafka_satellite_catalog_entry(
                _feedurl=_satcat_source(norad),
                _norad_cat_id=str(norad),
                data=_build_satcat(row),
                flush_producer=False,
            )
            count += 1
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error sending SATCAT record %s: %s", norad, e)
    producer.flush()
    logger.info("Emitted %d SATCAT reference records", count)
    return count


async def feed(
    api: CelesTrakAPI,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    cfg: FeedConfig,
) -> None:
    """Feed SATCAT reference data and GP/SupGP telemetry as CloudEvents to Kafka."""

    state: Dict[str, Any] = load_state(cfg.state_file)
    gp_state: Dict[str, str] = state.get("gp", {})
    supgp_state: Dict[str, str] = state.get("supgp", {})

    producer = Producer(kafka_config)
    ce = OrgCelestrakKafkaEventProducer(producer, kafka_topic)

    logger.info(
        "Starting CelesTrak feed to Kafka topic %s (groups=%s, supgp=%s)",
        kafka_topic,
        ",".join(cfg.groups),
        ",".join(cfg.supgp_sources) or "<off>",
    )

    last_reference = 0.0
    while True:
        try:
            cycle_start = datetime.now(timezone.utc)
            now_mono = time.monotonic()

            if last_reference == 0.0 or (now_mono - last_reference) >= cfg.reference_refresh_interval:
                _emit_reference(api, producer, ce, cfg)
                last_reference = now_mono

            gp_count = 0
            for row in api.get_gp(cfg.groups):
                norad = int(row["NORAD_CAT_ID"])
                epoch = str(row.get("EPOCH"))
                if gp_state.get(str(norad)) == epoch:
                    continue
                try:
                    ce.send_org_celestrak_kafka_orbit_mean_elements(
                        _feedurl=_gp_source(norad),
                        _norad_cat_id=str(norad),
                        data=_build_gp(row),
                        flush_producer=False,
                    )
                    gp_state[str(norad)] = epoch
                    gp_count += 1
                except Exception as e:  # pylint: disable=broad-except
                    logger.error("Error sending GP element set %s: %s", norad, e)
            producer.flush()

            supgp_count = 0
            if cfg.supgp_sources:
                for row in api.get_supgp(cfg.supgp_sources):
                    norad = int(row["NORAD_CAT_ID"])
                    dedup_key = f"{norad}|{row.get('DATA_SOURCE')}|{row.get('EPOCH')}"
                    if supgp_state.get(dedup_key):
                        continue
                    try:
                        ce.send_org_celestrak_kafka_supplemental_orbit_mean_elements(
                            _feedurl=_supgp_source(norad),
                            _norad_cat_id=str(norad),
                            data=_build_supgp(row),
                            flush_producer=False,
                        )
                        supgp_state[dedup_key] = str(row.get("EPOCH"))
                        supgp_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error sending SupGP element set %s: %s", norad, e)
                producer.flush()

            save_state(cfg.state_file, {"gp": gp_state, "supgp": supgp_state})
            elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
            logger.info(
                "Sent %d GP + %d SupGP element sets in %.1fs.",
                gp_count,
                supgp_count,
                elapsed,
            )

            if api.halted:
                backoff = max(cfg.polling_interval, 3600)
                logger.error(
                    "CelesTrak usage-policy hard stop hit; backing off %ds before retrying.",
                    backoff,
                )
                if cfg.once:
                    break
                time.sleep(backoff)
                api.reset_halt()
                continue

            if cfg.once:
                logger.info("--once mode: exiting after first polling cycle")
                break

            effective = max(0.0, cfg.polling_interval - elapsed)
            if effective > 0:
                time.sleep(effective)
        except KeyboardInterrupt:
            logger.info("Exiting...")
            break
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error occurred: %s", e)
            logger.info("Retrying in %d seconds...", cfg.polling_interval)
            time.sleep(cfg.polling_interval)
    producer.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CelesTrak -> Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed SATCAT + GP element sets as CloudEvents to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str,
                             default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
                             help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"),
                             help="Kafka topic to send messages to")
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"),
                             help="Username for SASL PLAIN authentication")
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"),
                             help="Password for SASL PLAIN authentication")
    feed_parser.add_argument("-c", "--connection-string", type=str, default=os.getenv("CONNECTION_STRING"),
                             help="Microsoft Event Hubs or Fabric Event Stream connection string")
    feed_parser.add_argument("--groups", type=str, default=os.getenv("CELESTRAK_GROUPS"),
                             help="Comma-separated CelesTrak GROUP views (default: stations)")
    feed_parser.add_argument("--supgp-sources", type=str, default=os.getenv("SUPGP_SOURCES"),
                             help="Comma-separated Supplemental GP SOURCE views (default: off)")
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "3600")),
                             help="Telemetry polling interval in seconds (default: 3600)")
    feed_parser.add_argument("--reference-refresh-interval", type=int,
                             default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "86400")),
                             help="SATCAT reference refresh interval in seconds (default: 86400)")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.celestrak_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var).")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    if args.connection_string:
        cfg_kafka = parse_kafka_connection_string(args.connection_string)
        bootstrap = cfg_kafka.get("bootstrap.servers")
        topic = cfg_kafka.get("kafka_topic") or args.kafka_topic
        user = cfg_kafka.get("sasl.username")
        pwd = cfg_kafka.get("sasl.password")
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

    groups = [g.strip() for g in args.groups.split(",")] if args.groups else None
    supgp = [s.strip() for s in args.supgp_sources.split(",")] if args.supgp_sources else None
    feed_cfg = FeedConfig.from_env(
        groups=groups,
        supgp_sources=supgp,
        polling_interval=args.polling_interval,
        reference_refresh_interval=args.reference_refresh_interval,
        state_file=args.state_file,
        once=args.once,
    )

    api = CelesTrakAPI()
    asyncio.run(feed(api, kafka_config, topic, feed_cfg))


if __name__ == "__main__":
    main()
