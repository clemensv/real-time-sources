"""Kafka feeder for AviationWeather.gov."""
from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Dict, Set

from aviationweather_core import (
    API_BASE,
    DEFAULT_STATIONS,
    METAR_POLL_INTERVAL,
    SIGMET_POLL_INTERVAL,
    STATION_REFRESH_HOURS,
    USER_AGENT,
    AviationWeatherPoller as CoreAviationWeatherPoller,
)
from aviationweather_producer_kafka_producer.producer import GovNoaaAviationweatherEventProducer


class AviationWeatherPoller(CoreAviationWeatherPoller):
    """Kafka-specific AviationWeather.gov poller."""

    def __init__(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        last_polled_file: str,
        station_ids: str = DEFAULT_STATIONS,
        metar_poll_interval: int = METAR_POLL_INTERVAL,
        sigmet_poll_interval: int = SIGMET_POLL_INTERVAL,
    ):
        self.kafka_topic = kafka_topic
        super().__init__(last_polled_file, station_ids, metar_poll_interval, sigmet_poll_interval)
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = GovNoaaAviationweatherEventProducer(kafka_producer, kafka_topic)

    def emit_stations(self) -> int:
        """Fetch and emit station reference data to Kafka."""
        count = 0
        for raw in self.fetch_station_json(self.station_ids):
            station = self.parse_station(raw)
            if station:
                self.producer.send_gov_noaa_aviationweather_station(
                    station.icao_id, station, flush_producer=False)
                count += 1
        if count > 0:
            self.producer.producer.flush()
        return count

    def emit_metars(self, metar_timestamps: Dict[str, str]):
        """Fetch, deduplicate, and emit METAR observations to Kafka."""
        count = 0
        for raw in self.fetch_metar_json(self.station_ids):
            metar = self.parse_metar(raw)
            if metar is None:
                continue
            if metar_timestamps.get(metar.icao_id) == metar.obs_time:
                continue
            self.producer.send_gov_noaa_aviationweather_metar(
                metar.icao_id, metar, flush_producer=False)
            metar_timestamps[metar.icao_id] = metar.obs_time
            count += 1
        if count > 0:
            self.producer.producer.flush()
        return count, metar_timestamps

    def emit_sigmets(self, seen_keys: Set[str]):
        """Fetch, deduplicate, and emit SIGMETs (US + international) to Kafka."""
        all_sigmets = []
        for raw in self.fetch_airsigmet_json():
            s = self.parse_us_sigmet(raw)
            if s:
                all_sigmets.append(s)
        for raw in self.fetch_isigmet_json():
            s = self.parse_intl_sigmet(raw)
            if s:
                all_sigmets.append(s)

        count = 0
        current_keys: Set[str] = set()
        for sigmet in all_sigmets:
            key = self.sigmet_dedup_key(sigmet)
            current_keys.add(key)
            if key in seen_keys:
                continue
            self.producer.send_gov_noaa_aviationweather_sigmet(
                sigmet.icao_id, sigmet, flush_producer=False)
            count += 1
        if count > 0:
            self.producer.producer.flush()
        return count, current_keys

    def poll_and_send(self, once: bool = False) -> None:
        """Main polling loop."""
        print(f"Starting AviationWeather.gov poller")
        print(f"  Stations: {self.station_ids}")
        print(f"  METAR poll interval: {self.metar_poll_interval}s")
        print(f"  SIGMET poll interval: {self.sigmet_poll_interval}s")
        print(f"  Kafka topic: {self.kafka_topic}")

        print("Fetching and sending station reference data...")
        station_count = self.emit_stations()
        print(f"Sent {station_count} station(s) as reference data")

        state = self.load_state()
        metar_timestamps = state.get("metar_timestamps", {})
        seen_sigmet_keys: Set[str] = set(state.get("sigmet_keys", []))
        last_sigmet_poll = 0.0
        last_station_refresh = time.time()

        while True:
            try:
                now = time.time()
                metar_count, metar_timestamps = self.emit_metars(metar_timestamps)
                if metar_count > 0:
                    print(f"Sent {metar_count} new METAR(s)")
                if now - last_sigmet_poll >= self.sigmet_poll_interval:
                    sigmet_count, seen_sigmet_keys = self.emit_sigmets(seen_sigmet_keys)
                    if sigmet_count > 0:
                        print(f"Sent {sigmet_count} new SIGMET(s)")
                    last_sigmet_poll = now
                if now - last_station_refresh >= STATION_REFRESH_HOURS * 3600:
                    print("Refreshing station reference data...")
                    refresh_count = self.emit_stations()
                    print(f"Refreshed {refresh_count} station(s)")
                    last_station_refresh = now
                self.save_state({
                    "metar_timestamps": metar_timestamps,
                    "sigmet_keys": list(seen_sigmet_keys),
                })
            except Exception as e:
                print(f"Error in polling loop: {e}")
            if once:
                break
            time.sleep(self.metar_poll_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs-style connection string into Kafka config."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"')
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
    return config_dict


def main() -> None:
    """Parse arguments and start the AviationWeather.gov poller."""
    parser = argparse.ArgumentParser(description="AviationWeather.gov METAR/SIGMET Bridge")
    parser.add_argument("--last-polled-file", type=str)
    parser.add_argument("--kafka-bootstrap-servers", type=str)
    parser.add_argument("--kafka-topic", type=str)
    parser.add_argument("--sasl-username", type=str)
    parser.add_argument("--sasl-password", type=str)
    parser.add_argument("--connection-string", type=str)
    parser.add_argument("--stations", type=str)
    parser.add_argument("--metar-poll-interval", type=int, default=METAR_POLL_INTERVAL)
    parser.add_argument("--sigmet-poll-interval", type=int, default=SIGMET_POLL_INTERVAL)
    parser.add_argument("--once", action="store_true",
                        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))

    _argv = sys.argv[1:]
    if _argv and _argv[0] == "feed":
        _argv = _argv[1:]
    args = parser.parse_args(_argv)

    if not args.connection_string:
        args.connection_string = os.getenv("CONNECTION_STRING")
    if not args.last_polled_file:
        args.last_polled_file = os.getenv("AVIATIONWEATHER_LAST_POLLED_FILE") or os.path.expanduser("~/.aviationweather_last_polled.json")
    if not args.stations:
        args.stations = os.getenv("AVIATIONWEATHER_STATIONS", DEFAULT_STATIONS)

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic")
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: Dict[str, str] = {"bootstrap.servers": kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    poller = AviationWeatherPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        station_ids=args.stations,
        metar_poll_interval=args.metar_poll_interval,
        sigmet_poll_interval=args.sigmet_poll_interval,
    )
    poller.poll_and_send(once=args.once)


if __name__ == "__main__":
    main()
