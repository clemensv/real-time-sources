"""US CBP Border Wait Times bridge to Kafka.

Polls the CBP Border Wait Time API for wait times at US land border
crossings with Canada and Mexico and publishes them as CloudEvents.
"""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from confluent_kafka import Producer
from cbp_border_wait_producer_data.gov.cbp.borderwait.port import Port
from cbp_border_wait_producer_data.gov.cbp.borderwait.waittime import WaitTime
from cbp_border_wait_producer_kafka_producer.producer import GovCbpBorderwaitEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

API_URL = "https://bwt.cbp.gov/api/bwtnew"


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as exc:
        logging.warning("Could not load state from %s: %s", state_file, exc)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file."""
    if not state_file:
        return
    try:
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as exc:
        logging.warning("Could not save state to %s: %s", state_file, exc)


def parse_int_or_none(value: str) -> Optional[int]:
    """Parse an integer from a CBP string value.

    Returns None for missing, empty, or non-numeric values such as 'N/A'.

    Args:
        value: The string value from the CBP API.

    Returns:
        The integer value, or None if not parseable.
    """
    if value is None:
        return None
    value = str(value).strip()
    if not value or value.upper() == "N/A":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_delay_minutes(value: str) -> Optional[int]:
    """Parse delay minutes from a CBP lane detail string.

    Handles empty strings, 'N/A', and other non-numeric values by
    returning None. A value of '0' is returned as 0 (no delay).

    Args:
        value: The delay_minutes string from the CBP API.

    Returns:
        Delay in minutes as an integer, or None if not available.
    """
    return parse_int_or_none(value)


def parse_lanes_open(value: str) -> Optional[int]:
    """Parse lanes open count from a CBP lane detail string.

    Args:
        value: The lanes_open string from the CBP API.

    Returns:
        Number of lanes open as an integer, or None if not available.
    """
    return parse_int_or_none(value)


def parse_operational_status(value: str) -> Optional[str]:
    """Normalize an operational status string.

    Returns None for empty strings, otherwise returns the value as-is.
    Known values: 'no delay', 'delay', 'N/A', 'Lanes Closed', 'Update Pending'.

    Args:
        value: The operational_status string from the CBP API.

    Returns:
        The status string, or None if empty.
    """
    if value is None:
        return None
    value = str(value).strip()
    return value if value else None


def _extract_lane(lane_data: dict) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    """Extract delay, lanes_open, and operational_status from a lane dict.

    Args:
        lane_data: A dict like ``{"update_time": ..., "operational_status": ...,
            "delay_minutes": ..., "lanes_open": ...}``.

    Returns:
        Tuple of (delay_minutes, lanes_open, operational_status).
    """
    if not lane_data:
        return None, None, None
    status = parse_operational_status(lane_data.get("operational_status", ""))
    delay = parse_delay_minutes(lane_data.get("delay_minutes", ""))
    lanes = parse_lanes_open(lane_data.get("lanes_open", ""))
    return delay, lanes, status


class CbpBorderWaitAPI:
    """Client for the CBP Border Wait Time API."""

    def __init__(self, api_url: str = API_URL):
        self.api_url = api_url
        self.session = requests.Session()

    def fetch_ports(self) -> List[Dict[str, Any]]:
        """Fetch all port data from the CBP API.

        Returns:
            List of raw port dicts from the API response.
        """
        resp = self.session.get(self.api_url, timeout=60)
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def parse_port(raw: Dict[str, Any]) -> Port:
        """Convert a raw CBP port dict to a Port data class.

        Args:
            raw: A single element from the API array response.

        Returns:
            Port reference data object.
        """
        pv = raw.get("passenger_vehicle_lanes", {})
        cv = raw.get("commercial_vehicle_lanes", {})
        ped = raw.get("pedestrian_lanes", {})
        return Port(
            port_number=raw.get("port_number", ""),
            port_name=raw.get("port_name", ""),
            border=raw.get("border", ""),
            crossing_name=raw.get("crossing_name", ""),
            hours=raw.get("hours", ""),
            passenger_vehicle_max_lanes=parse_int_or_none(pv.get("maximum_lanes", "")),
            commercial_vehicle_max_lanes=parse_int_or_none(cv.get("maximum_lanes", "")),
            pedestrian_max_lanes=parse_int_or_none(ped.get("maximum_lanes", "")),
        )

    @staticmethod
    def parse_wait_time(raw: Dict[str, Any]) -> WaitTime:
        """Convert a raw CBP port dict to a flattened WaitTime data class.

        Extracts lane-level detail from the nested passenger_vehicle_lanes,
        pedestrian_lanes, and commercial_vehicle_lanes structures.

        Args:
            raw: A single element from the API array response.

        Returns:
            WaitTime telemetry data object.
        """
        pv = raw.get("passenger_vehicle_lanes", {})
        ped = raw.get("pedestrian_lanes", {})
        cv = raw.get("commercial_vehicle_lanes", {})

        pv_std_delay, pv_std_lanes, pv_std_status = _extract_lane(pv.get("standard_lanes", {}))
        pv_ns_delay, pv_ns_lanes, pv_ns_status = _extract_lane(pv.get("NEXUS_SENTRI_lanes", {}))
        pv_rd_delay, pv_rd_lanes, pv_rd_status = _extract_lane(pv.get("ready_lanes", {}))

        ped_std_delay, ped_std_lanes, ped_std_status = _extract_lane(ped.get("standard_lanes", {}))
        ped_rd_delay, ped_rd_lanes, ped_rd_status = _extract_lane(ped.get("ready_lanes", {}))

        cv_std_delay, cv_std_lanes, cv_std_status = _extract_lane(cv.get("standard_lanes", {}))
        cv_fast_delay, cv_fast_lanes, cv_fast_status = _extract_lane(cv.get("FAST_lanes", {}))

        return WaitTime(
            port_number=raw.get("port_number", ""),
            port_name=raw.get("port_name", ""),
            border=raw.get("border", ""),
            crossing_name=raw.get("crossing_name", ""),
            port_status=raw.get("port_status", ""),
            date=raw.get("date", ""),
            time=raw.get("time", ""),
            passenger_vehicle_standard_delay=pv_std_delay,
            passenger_vehicle_standard_lanes_open=pv_std_lanes,
            passenger_vehicle_standard_operational_status=pv_std_status,
            passenger_vehicle_nexus_sentri_delay=pv_ns_delay,
            passenger_vehicle_nexus_sentri_lanes_open=pv_ns_lanes,
            passenger_vehicle_nexus_sentri_operational_status=pv_ns_status,
            passenger_vehicle_ready_delay=pv_rd_delay,
            passenger_vehicle_ready_lanes_open=pv_rd_lanes,
            passenger_vehicle_ready_operational_status=pv_rd_status,
            pedestrian_standard_delay=ped_std_delay,
            pedestrian_standard_lanes_open=ped_std_lanes,
            pedestrian_standard_operational_status=ped_std_status,
            pedestrian_ready_delay=ped_rd_delay,
            pedestrian_ready_lanes_open=ped_rd_lanes,
            pedestrian_ready_operational_status=ped_rd_status,
            commercial_vehicle_standard_delay=cv_std_delay,
            commercial_vehicle_standard_lanes_open=cv_std_lanes,
            commercial_vehicle_standard_operational_status=cv_std_status,
            commercial_vehicle_fast_delay=cv_fast_delay,
            commercial_vehicle_fast_lanes_open=cv_fast_lanes,
            commercial_vehicle_fast_operational_status=cv_fast_status,
            construction_notice=raw.get("construction_notice", "") or None,
        )


def _parse_connection_string(connection_string: str):
    """Parse the connection string and extract Kafka config and topic."""
    config_dict = {}
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
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict, kafka_topic


def feed(args):
    """Main feed loop: emit port reference data then poll for wait times."""
    connection_string = args.connection_string or os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logging.error("CONNECTION_STRING is required")
        sys.exit(1)

    kafka_config, kafka_topic = _parse_connection_string(connection_string)

    tls_enabled = os.environ.get("KAFKA_ENABLE_TLS", "true").lower()
    if tls_enabled == "false" and "security.protocol" not in kafka_config:
        kafka_config["security.protocol"] = "PLAINTEXT"

    polling_interval = int(args.polling_interval or os.environ.get("POLLING_INTERVAL", "3600"))
    state_file = args.state_file or os.environ.get("STATE_FILE", "")

    previous_timestamps: Dict[str, str] = _load_state(state_file)

    producer = Producer(kafka_config)
    event_producer = GovCbpBorderwaitEventProducer(producer, kafka_topic)
    api = CbpBorderWaitAPI()

    logging.info(
        "Starting CBP Border Wait Times feed to Kafka topic %s at %s",
        kafka_topic,
        kafka_config.get("bootstrap.servers", "unknown"),
    )

    # Emit port reference data at startup
    try:
        raw_ports = api.fetch_ports()
        for raw in raw_ports:
            try:
                port = api.parse_port(raw)
                event_producer.send_gov_cbp_borderwait_port(
                    _port_number=port.port_number,
                    data=port,
                    flush_producer=False,
                )
            except Exception as exc:
                logging.error("Error sending port %s: %s", raw.get("port_number", "?"), exc)
        producer.flush()
        logging.info("Sent %d port reference records", len(raw_ports))
    except Exception as exc:
        logging.error("Failed to fetch port reference data: %s", exc)

    # Telemetry polling loop
    while True:
        try:
            count = 0
            start_time = datetime.now(timezone.utc)
            raw_ports = api.fetch_ports()
            for raw in raw_ports:
                port_num = raw.get("port_number", "")
                date_val = raw.get("date", "")
                time_val = raw.get("time", "")
                dedup_key = f"{date_val}T{time_val}"
                if port_num in previous_timestamps and previous_timestamps[port_num] == dedup_key:
                    continue
                try:
                    wait_time = api.parse_wait_time(raw)
                    event_producer.send_gov_cbp_borderwait_wait_time(
                        _port_number=wait_time.port_number,
                        data=wait_time,
                        flush_producer=False,
                    )
                    count += 1
                    previous_timestamps[port_num] = dedup_key
                except Exception as exc:
                    logging.error("Error sending wait time for port %s: %s", port_num, exc)
            producer.flush()
            end_time = datetime.now(timezone.utc)
            elapsed = (end_time - start_time).total_seconds()
            effective_interval = max(0, polling_interval - elapsed)
            logging.info(
                "Sent %d wait time updates in %.1f s. Next poll at %s.",
                count,
                elapsed,
                (datetime.now(timezone.utc) + timedelta(seconds=effective_interval)).isoformat(),
            )
            _save_state(state_file, previous_timestamps)
            if effective_interval > 0:
                time.sleep(effective_interval)
        except KeyboardInterrupt:
            logging.info("Exiting...")
            break
        except Exception as exc:
            logging.error("Error occurred: %s", exc)
            logging.info("Retrying in %d seconds...", polling_interval)
            time.sleep(polling_interval)


def main():
    parser = argparse.ArgumentParser(description="US CBP Border Wait Times bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start the feed loop")
    feed_parser.add_argument("--connection-string", help="Kafka connection string")
    feed_parser.add_argument("--polling-interval", type=int, default=3600, help="Polling interval in seconds (default: 3600)")
    feed_parser.add_argument("--state-file", help="Path to state persistence file")

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
