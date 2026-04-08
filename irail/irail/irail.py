"""iRail Belgian railway real-time bridge to Kafka."""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests
from confluent_kafka import Producer
from irail_producer_data.be.irail.station import Station
from irail_producer_data.be.irail.arrival import Arrival
from irail_producer_data.be.irail.arrivalboard import ArrivalBoard
from irail_producer_data.be.irail.departure import Departure
from irail_producer_data.be.irail.stationboard import StationBoard
from irail_producer_kafka_producer.producer import BeIrailEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

API_BASE = "https://api.irail.be"
FEED_URL = "https://api.irail.be"

# iRail rate limits: 3 requests/sec with 5 burst
REQUEST_DELAY = 0.35  # slightly over 1/3 sec to stay within limits


class IRailAPI:
    """Client for the iRail REST API."""

    def __init__(self, user_agent: str = "real-time-sources/1.0 (github.com/clemensv/real-time-sources)"):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": user_agent,
        })

    def fetch_stations(self) -> List[Dict[str, Any]]:
        """Fetch all Belgian railway stations."""
        resp = self.session.get(f"{API_BASE}/stations/", params={"format": "json", "lang": "en"}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("station", [])

    def fetch_liveboard(self, station_id: str, arrdep: str = "departure") -> Optional[Dict[str, Any]]:
        """Fetch the current departure or arrival board for a station by NMBS id."""
        resp = self.session.get(
            f"{API_BASE}/liveboard/",
            params={
                "id": f"BE.NMBS.{station_id}",
                "format": "json",
                "lang": "en",
                "alerts": "false",
                "arrdep": arrdep,
            },
            timeout=30,
        )
        if resp.status_code == 404:
            return None
        if resp.status_code == 429:
            logging.warning("Rate limited, backing off")
            time.sleep(5)
            return None
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def parse_station(raw: Dict[str, Any]) -> Station:
        """Convert a raw station dict from the iRail stations API to a Station data class."""
        station_id = IRailAPI._parse_station_id(raw.get("id", ""))
        return Station(
            station_id=station_id,
            name=raw.get("name", ""),
            standard_name=raw.get("standardname", ""),
            longitude=float(raw.get("locationX", 0.0)),
            latitude=float(raw.get("locationY", 0.0)),
            uri=raw.get("@id", ""),
        )

    @staticmethod
    def _parse_station_id(raw_id: str) -> str:
        """Normalize an iRail station identifier to the nine-digit NMBS id."""
        return raw_id.replace("BE.NMBS.", "") if raw_id.startswith("BE.NMBS.") else raw_id

    @staticmethod
    def _parse_scheduled_time(raw_unix: str) -> str:
        """Convert an iRail Unix timestamp string to an ISO 8601 UTC datetime."""
        return datetime.fromtimestamp(int(raw_unix), tz=timezone.utc).isoformat()

    @staticmethod
    def _parse_vehicle_details(vehicle_info: Dict[str, Any]) -> tuple[str, str]:
        """Extract vehicle type and number from the liveboard payload."""
        vehicle_type = vehicle_info.get("type", "")
        vehicle_number = vehicle_info.get("number", "")
        if vehicle_type or vehicle_number:
            return vehicle_type, vehicle_number

        shortname = vehicle_info.get("shortname", "")
        parts = shortname.split(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        if parts:
            return parts[0], ""
        return "", ""

    @staticmethod
    def _parse_platform_details(raw: Dict[str, Any]) -> tuple[Optional[str], bool]:
        """Extract the platform and whether it is the scheduled one."""
        platform = raw.get("platform", None)
        if platform in ("", "?"):
            platform = None

        platform_info = raw.get("platforminfo", {})
        is_normal = platform_info.get("normal", "1") == "1"
        return platform, is_normal

    @staticmethod
    def _parse_occupancy(raw: Dict[str, Any]) -> str:
        """Normalize the optional occupancy term emitted by iRail."""
        occupancy_info = raw.get("occupancy", {})
        occupancy = occupancy_info.get("name", "unknown")
        if occupancy not in ("low", "medium", "high", "unknown"):
            return "unknown"
        return occupancy

    @staticmethod
    def _parse_connection_uri(raw: Dict[str, Any], *keys: str) -> str:
        """Return the first non-empty connection URI field from the payload."""
        for key in keys:
            value = raw.get(key)
            if value:
                return str(value)
        return ""

    @staticmethod
    def _normalize_board_entries(raw_entries: Any) -> List[Dict[str, Any]]:
        """Normalize liveboard entry collections to a list."""
        if isinstance(raw_entries, list):
            return raw_entries
        if isinstance(raw_entries, dict):
            return [raw_entries]
        return []

    @staticmethod
    def parse_departure(raw: Dict[str, Any]) -> Departure:
        """Convert a raw departure dict from the iRail liveboard API to a Departure data class."""
        station_info = raw.get("stationinfo", {})
        dest_station_id = IRailAPI._parse_station_id(station_info.get("id", ""))
        scheduled_time = IRailAPI._parse_scheduled_time(raw.get("time", "0"))

        vehicle_info = raw.get("vehicleinfo", {})
        vehicle_type, vehicle_number = IRailAPI._parse_vehicle_details(vehicle_info)
        platform, is_normal = IRailAPI._parse_platform_details(raw)
        occupancy = IRailAPI._parse_occupancy(raw)

        return Departure(
            destination_station_id=dest_station_id,
            destination_name=raw.get("station", station_info.get("name", "")),
            scheduled_time=scheduled_time,
            delay_seconds=int(raw.get("delay", "0")),
            is_canceled=str(raw.get("canceled", "0")) == "1",
            has_left=str(raw.get("left", "0")) == "1",
            is_extra_stop=str(raw.get("isExtra", "0")) == "1",
            vehicle_id=raw.get("vehicle", vehicle_info.get("name", "")),
            vehicle_short_name=vehicle_info.get("shortname", ""),
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            platform=platform,
            is_normal_platform=is_normal,
            occupancy=occupancy,
            departure_connection_uri=IRailAPI._parse_connection_uri(raw, "departureConnection", "connection"),
        )

    @staticmethod
    def parse_arrival(raw: Dict[str, Any]) -> Arrival:
        """Convert a raw arrival dict from the iRail liveboard API to an Arrival data class."""
        station_info = raw.get("stationinfo", {})
        origin_station_id = IRailAPI._parse_station_id(station_info.get("id", ""))
        scheduled_time = IRailAPI._parse_scheduled_time(raw.get("time", "0"))

        vehicle_info = raw.get("vehicleinfo", {})
        vehicle_type, vehicle_number = IRailAPI._parse_vehicle_details(vehicle_info)
        platform, is_normal = IRailAPI._parse_platform_details(raw)
        occupancy = IRailAPI._parse_occupancy(raw)

        return Arrival(
            origin_station_id=origin_station_id,
            origin_name=raw.get("station", station_info.get("name", "")),
            scheduled_time=scheduled_time,
            delay_seconds=int(raw.get("delay", "0")),
            is_canceled=str(raw.get("canceled", "0")) == "1",
            has_arrived=str(raw.get("arrived", "0")) == "1",
            is_extra_stop=str(raw.get("isExtra", "0")) == "1",
            vehicle_id=raw.get("vehicle", vehicle_info.get("name", "")),
            vehicle_short_name=vehicle_info.get("shortname", ""),
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            platform=platform,
            is_normal_platform=is_normal,
            occupancy=occupancy,
            connection_uri=IRailAPI._parse_connection_uri(raw, "arrivalConnection", "departureConnection", "connection"),
        )

    @staticmethod
    def parse_liveboard(raw: Dict[str, Any], station_id: str) -> StationBoard:
        """Convert a raw liveboard response to a StationBoard data class."""
        timestamp_unix = int(raw.get("timestamp", "0"))
        retrieved_at = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc).isoformat()

        departures_obj = raw.get("departures", {})
        raw_departures = IRailAPI._normalize_board_entries(departures_obj.get("departure", []))
        departures = []
        for dep in raw_departures:
            try:
                departures.append(IRailAPI.parse_departure(dep))
            except Exception as e:
                logging.debug("Skipping malformed departure: %s", e)

        station_info_raw = raw.get("stationinfo", {})
        station_name = raw.get("station", station_info_raw.get("name", ""))

        return StationBoard(
            station_id=station_id,
            station_name=station_name,
            retrieved_at=retrieved_at,
            departure_count=len(departures),
            departures=departures,
        )

    @staticmethod
    def parse_arrivalboard(raw: Dict[str, Any], station_id: str) -> ArrivalBoard:
        """Convert a raw liveboard response to an ArrivalBoard data class."""
        timestamp_unix = int(raw.get("timestamp", "0"))
        retrieved_at = datetime.fromtimestamp(timestamp_unix, tz=timezone.utc).isoformat()

        arrivals_obj = raw.get("arrivals", {})
        raw_arrivals = IRailAPI._normalize_board_entries(arrivals_obj.get("arrival", []))
        arrivals = []
        for arr in raw_arrivals:
            try:
                arrivals.append(IRailAPI.parse_arrival(arr))
            except Exception as e:
                logging.debug("Skipping malformed arrival: %s", e)

        station_info_raw = raw.get("stationinfo", {})
        station_name = raw.get("station", station_info_raw.get("name", ""))

        return ArrivalBoard(
            station_id=station_id,
            station_name=station_name,
            retrieved_at=retrieved_at,
            arrival_count=len(arrivals),
            arrivals=arrivals,
        )


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
                _feedurl=FEED_URL,
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
                            _feedurl=FEED_URL,
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

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
