"""iRail Belgian railway real-time bridge to Kafka."""

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Dict, List

from confluent_kafka import Producer
from irail_core import (
    IRailAPI,
    REQUEST_DELAY,
    USER_AGENT,
    API_BASE,
    FEED_URL,
    create_retrying_session,
)

try:
    from irail_producer_kafka_producer.producer import BeIrailEventProducer
except ModuleNotFoundError:
    BeIrailEventProducer = None  # type: ignore[assignment,misc]

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def _parse_connection_string(connection_string: str):
    """Parse the connection string and extract Kafka config and topic."""
    config_dict: Dict[str, str] = {}
    kafka_topic = None
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                kafka_topic = part.split("=")[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict, kafka_topic


def feed(args):
    """Main feed loop: emit stations then poll liveboards."""
    connection_string = args.connection_string or os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logging.error("CONNECTION_STRING is required")
        sys.exit(1)

    kafka_config, kafka_topic = _parse_connection_string(connection_string)

    tls_enabled = os.environ.get("KAFKA_ENABLE_TLS", "true").lower()
    if tls_enabled == "false" and "security.protocol" not in kafka_config:
        kafka_config["security.protocol"] = "PLAINTEXT"

    polling_interval = int(args.polling_interval or os.environ.get("POLLING_INTERVAL", "300"))
    station_filter = args.station_filter or os.environ.get("STATION_FILTER", "")
    once = bool(getattr(args, "once", False))

    producer = Producer(kafka_config)
    event_producer = BeIrailEventProducer(producer, kafka_topic)
    api = IRailAPI()

    logging.info(
        "Starting iRail feed to Kafka topic %s at %s",
        kafka_topic,
        kafka_config.get("bootstrap.servers", "?"),
    )

    # Fetch and emit station reference data
    all_stations_raw = api.fetch_stations()
    station_ids: List[str] = []
    for raw in all_stations_raw:
        try:
            station = api.parse_station(raw)
            station_ids.append(station.station_id)
            event_producer.send_be_irail_station(
                _station_id=station.station_id,
                data=station,
                flush_producer=False,
            )
        except Exception as e:
            logging.error("Error sending station %s: %s", raw.get("id", "?"), e)
    producer.flush()
    logging.info("Sent %d station records", len(station_ids))

    # Apply station filter if provided
    if station_filter:
        filter_set = set(s.strip() for s in station_filter.split(",") if s.strip())
        station_ids = [sid for sid in station_ids if sid in filter_set]
        logging.info("Filtered to %d stations", len(station_ids))

    # Liveboard polling loop
    while True:
        try:
            departure_board_count = 0
            departure_count = 0
            arrival_board_count = 0
            arrival_count = 0
            start_time = datetime.now(timezone.utc)
            board_specs = (
                ("departure", api.parse_liveboard, event_producer.send_be_irail_station_board, "departure_count"),
                ("arrival", api.parse_arrivalboard, event_producer.send_be_irail_arrival_board, "arrival_count"),
            )
            for station_id in station_ids:
                for board_kind, parser, sender, count_attr in board_specs:
                    try:
                        liveboard_raw = api.fetch_liveboard(station_id, arrdep=board_kind)
                        if liveboard_raw is None:
                            continue

                        board = parser(liveboard_raw, station_id)
                        sender(
                            _station_id=station_id,
                            data=board,
                            flush_producer=False,
                        )

                        if board_kind == "departure":
                            departure_board_count += 1
                            departure_count += getattr(board, count_attr)
                        else:
                            arrival_board_count += 1
                            arrival_count += getattr(board, count_attr)
                    except Exception as e:
                        logging.error("Error fetching %s board for %s: %s", board_kind, station_id, e)
                    time.sleep(REQUEST_DELAY)
            producer.flush()
            end_time = datetime.now(timezone.utc)
            elapsed = (end_time - start_time).total_seconds()
            effective_interval = max(0, polling_interval - elapsed)
            logging.info(
                "Sent %d departure boards (%d departures) and %d arrival boards (%d arrivals) in %.1f s. Next poll at %s.",
                departure_board_count,
                departure_count,
                arrival_board_count,
                arrival_count,
                elapsed,
                (datetime.now(timezone.utc) + timedelta(seconds=effective_interval)).isoformat(),
            )
            if once:
                logging.info("--once mode: exiting after first polling cycle")
                break
            if effective_interval > 0:
                time.sleep(effective_interval)
        except KeyboardInterrupt:
            logging.info("Exiting...")
            break
        except Exception as e:
            logging.error("Error occurred: %s", e)
            logging.info("Retrying in %d seconds...", polling_interval)
            time.sleep(polling_interval)


def main():
    parser = argparse.ArgumentParser(description="iRail Belgian railway bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start the feed loop")
    feed_parser.add_argument("--connection-string", help="Kafka connection string")
    feed_parser.add_argument("--polling-interval", type=int, default=300, help="Polling interval in seconds (default: 300)")
    feed_parser.add_argument("--station-filter", help="Comma-separated station IDs to poll (default: all)")
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var). Useful for scheduled execution in Fabric notebooks.",
    )

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
