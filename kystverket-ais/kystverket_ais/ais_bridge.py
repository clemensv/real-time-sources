"""Kystverket AIS bridge — Norwegian vessel tracking data to Kafka as CloudEvents."""

import argparse
import logging
import os
import sys
import threading
import time
from typing import Dict, Optional, Set

from confluent_kafka import Producer
from kystverket_ais_producer_data.no.kystverket.ais.positionreportclassa import PositionReportClassA
from kystverket_ais_producer_data.no.kystverket.ais.staticvoyagedata import StaticVoyageData
from kystverket_ais_producer_data.no.kystverket.ais.positionreportclassb import PositionReportClassB
from kystverket_ais_producer_data.no.kystverket.ais.staticdataclassb import StaticDataClassB
from kystverket_ais_producer_data.no.kystverket.ais.aidtonavigation import AidToNavigation
from kystverket_ais_producer_kafka_producer.producer import NOKystverketAISEventProducer

from kystverket_ais.nmea_decoder import NMEADecoder, DecodedAIS, SUPPORTED_TYPES
from kystverket_ais.tcp_source import TCPSource, RawNMEASentence

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').strip().replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"').strip()
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


def _mmsi_key_mapper(event, data) -> str:
    """Use MMSI as the Kafka partition key."""
    return str(getattr(data, 'mmsi', ''))


def _emit_event(event_producer: NOKystverketAISEventProducer, decoded: DecodedAIS) -> None:
    """Send a decoded AIS message through the typed Kafka producer."""
    fields = decoded.fields

    if decoded.event_type == "position_report_class_a":
        event_producer.send_no_kystverket_ais_position_report_class_a(
            data=PositionReportClassA(**fields),
            flush_producer=False,
            key_mapper=_mmsi_key_mapper,
        )
    elif decoded.event_type == "static_voyage_data":
        event_producer.send_no_kystverket_ais_static_voyage_data(
            data=StaticVoyageData(**fields),
            flush_producer=False,
            key_mapper=_mmsi_key_mapper,
        )
    elif decoded.event_type == "position_report_class_b":
        event_producer.send_no_kystverket_ais_position_report_class_b(
            data=PositionReportClassB(**fields),
            flush_producer=False,
            key_mapper=_mmsi_key_mapper,
        )
    elif decoded.event_type == "static_data_class_b":
        event_producer.send_no_kystverket_ais_static_data_class_b(
            data=StaticDataClassB(**fields),
            flush_producer=False,
            key_mapper=_mmsi_key_mapper,
        )
    elif decoded.event_type == "aid_to_navigation":
        event_producer.send_no_kystverket_ais_aid_to_navigation(
            data=AidToNavigation(**fields),
            flush_producer=False,
            key_mapper=_mmsi_key_mapper,
        )


class AISBridge:
    """Connects TCP AIS stream to Kafka via CloudEvents."""

    def __init__(self, tcp_source: TCPSource,
                 kafka_producer: Producer,
                 event_producer: NOKystverketAISEventProducer,
                 decoder: NMEADecoder,
                 mmsi_filter: Optional[Set[int]] = None,
                 ship_type_filter: Optional[Set[int]] = None,
                 flush_interval: int = 1000):
        self._tcp = tcp_source
        self._kafka = kafka_producer
        self._event_producer = event_producer
        self._decoder = decoder
        self._mmsi_filter = mmsi_filter
        self._ship_type_filter = ship_type_filter
        self._flush_interval = flush_interval
        self._count = 0
        self._total = 0
        self._start_time = 0.0

    def run(self) -> None:
        """Start the bridge — blocks forever."""
        self._start_time = time.time()
        logger.info("Starting AIS bridge — streaming from %s:%d",
                     self._tcp.host, self._tcp.port)
        self._tcp.stream(self._on_sentence)

    def _on_sentence(self, sentence: RawNMEASentence) -> None:
        """Handle a single NMEA sentence from the TCP source."""
        decoded = self._decoder.decode_sentence(
            sentence.nmea, sentence.station_id, sentence.receive_time
        )
        if decoded is None:
            return

        # MMSI filter
        if self._mmsi_filter and decoded.mmsi not in self._mmsi_filter:
            return

        try:
            _emit_event(self._event_producer, decoded)
        except Exception as e:
            logger.warning("Failed to emit event for MMSI %d: %s", decoded.mmsi, e)
            return

        self._count += 1
        self._total += 1

        if self._count >= self._flush_interval:
            self._kafka.flush()
            elapsed = time.time() - self._start_time
            rate = self._total / elapsed if elapsed > 0 else 0
            logger.info("Flushed %d events (total: %d, %.1f msg/sec)",
                        self._count, self._total, rate)
            self._count = 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Kystverket AIS bridge — Norwegian vessel tracking to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    # --- stream ---
    stream_p = subparsers.add_parser("stream", help="Stream AIS data to Kafka")
    stream_p.add_argument("--kafka-bootstrap-servers", type=str,
                          default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    stream_p.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"))
    stream_p.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    stream_p.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    stream_p.add_argument("-c", "--connection-string", type=str,
                          default=os.getenv("CONNECTION_STRING"))
    stream_p.add_argument("--tcp-host", type=str,
                          default=os.getenv("AIS_TCP_HOST", "153.44.253.27"))
    stream_p.add_argument("--tcp-port", type=int,
                          default=int(os.getenv("AIS_TCP_PORT", "5631")))
    stream_p.add_argument("--message-types", type=str,
                          default=os.getenv("AIS_MESSAGE_TYPES", "1,2,3,5,18,19,24,21"),
                          help="Comma-separated AIS message type numbers to emit")
    stream_p.add_argument("--mmsi-filter", type=str,
                          default=os.getenv("AIS_FILTER_MMSI"),
                          help="Comma-separated MMSI numbers to include (default: all)")
    stream_p.add_argument("--flush-interval", type=int,
                          default=int(os.getenv("AIS_FLUSH_INTERVAL", "1000")),
                          help="Flush Kafka producer every N events")

    # --- probe ---
    subparsers.add_parser("probe", help="Connect to TCP stream and print decoded messages")

    args = parser.parse_args()

    if args.command == "probe":
        _run_probe()
        return

    if args.command == "stream":
        if args.connection_string:
            cfg = parse_connection_string(args.connection_string)
            bootstrap = cfg.get("bootstrap.servers")
            topic = cfg.get("kafka_topic")
            sasl_user = cfg.get("sasl.username")
            sasl_pw = cfg.get("sasl.password")
        else:
            bootstrap = args.kafka_bootstrap_servers
            topic = args.kafka_topic
            sasl_user = args.sasl_username
            sasl_pw = args.sasl_password

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
            sys.exit(1)
        if not topic:
            print("Error: Kafka topic required (--kafka-topic or -c).")
            sys.exit(1)

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        kafka_config: Dict[str, str] = {"bootstrap.servers": bootstrap}
        if sasl_user and sasl_pw:
            kafka_config.update({
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_user,
                "sasl.password": sasl_pw,
            })
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"

        # Parse message types
        msg_types = set()
        for t in args.message_types.split(","):
            t = t.strip()
            if t:
                msg_types.add(int(t))

        # Parse MMSI filter
        mmsi_filter = None
        if args.mmsi_filter:
            mmsi_filter = set(int(m.strip()) for m in args.mmsi_filter.split(",") if m.strip())

        tcp = TCPSource(host=args.tcp_host, port=args.tcp_port)
        decoder = NMEADecoder(message_types=msg_types)
        kafka_producer = Producer(kafka_config)
        event_producer = NOKystverketAISEventProducer(kafka_producer, topic)

        bridge = AISBridge(
            tcp_source=tcp,
            kafka_producer=kafka_producer,
            event_producer=event_producer,
            decoder=decoder,
            mmsi_filter=mmsi_filter,
            flush_interval=args.flush_interval,
        )

        try:
            bridge.run()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            kafka_producer.flush()
        return

    parser.print_help()


def _run_probe() -> None:
    """Connect to the live AIS TCP stream and print decoded messages for 30 seconds."""
    from collections import Counter
    decoder = NMEADecoder()
    tcp = TCPSource(host="153.44.253.27", port=5631, timeout=35)
    counter = Counter()
    start = time.time()

    def on_sentence(sentence: RawNMEASentence) -> None:
        decoded = decoder.decode_sentence(
            sentence.nmea, sentence.station_id, sentence.receive_time
        )
        if decoded:
            counter[decoded.event_type] += 1
            if counter[decoded.event_type] <= 2:
                print(f"[{decoded.event_type}] MMSI={decoded.mmsi} "
                      f"station={decoded.station_id} "
                      f"time={decoded.receive_time.isoformat()}")
                for k, v in decoded.fields.items():
                    if k not in ("timestamp", "station_id"):
                        print(f"  {k}: {v}")
                print()
        if time.time() - start > 15:
            raise KeyboardInterrupt("Probe timeout")

    try:
        tcp.stream(on_sentence)
    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    print(f"\n--- Probe results ({elapsed:.0f}s) ---")
    for k, v in counter.most_common():
        print(f"  {k}: {v}")
    print(f"  Total: {sum(counter.values())}")
    print(f"  Rate: {sum(counter.values())/elapsed:.1f} msg/sec")


if __name__ == "__main__":
    main()
