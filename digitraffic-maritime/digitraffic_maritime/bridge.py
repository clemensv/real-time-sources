"""Digitraffic Marine AIS bridge — Finnish/Baltic vessel tracking to Kafka as CloudEvents."""

import argparse
import logging
import os
import sys
import time
from typing import Any, Dict, Optional, Set

from confluent_kafka import Producer
from digitraffic_maritime_producer_data import VesselLocation, VesselMetadata
from digitraffic_maritime_producer_kafka_producer.producer import FiDigitrafficMarineAisEventProducer

from digitraffic_maritime.mqtt_source import MQTTSource

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Map MQTT topic type to (data class, send method name)
_MESSAGE_MAP: Dict[str, tuple] = {
    "location": (VesselLocation, "send_fi_digitraffic_marine_ais_vessel_location"),
    "metadata": (VesselMetadata, "send_fi_digitraffic_marine_ais_vessel_metadata"),
}


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


def _emit_event(event_producer: FiDigitrafficMarineAisEventProducer,
                topic_type: str, mmsi: int, payload: Dict[str, Any]) -> bool:
    """Send a decoded AIS message through the typed Kafka producer.

    Returns True if emitted, False if the topic type is unknown.
    """
    mapping = _MESSAGE_MAP.get(topic_type)
    if mapping is None:
        logger.debug("Skipping unknown topic type: %s", topic_type)
        return False

    data_class, send_method_name = mapping
    try:
        # Inject MMSI into the payload — the MQTT message doesn't include it,
        # but the topic contains it and the schema expects it.
        enriched = dict(payload)
        enriched["mmsi"] = mmsi
        data = data_class.from_serializer_dict(enriched)
        send_fn = getattr(event_producer, send_method_name)
        send_fn(_mmsi=str(data.mmsi), data=data, flush_producer=False, key_mapper=_mmsi_key_mapper)
        return True
    except Exception as e:
        logger.warning("Failed to emit %s for MMSI %d: %s", topic_type, mmsi, e)
        return False


class DigitraficBridge:
    """Connects Digitraffic Marine MQTT to Kafka via CloudEvents."""

    def __init__(self, mqtt_source: MQTTSource,
                 kafka_producer: Producer,
                 event_producer: FiDigitrafficMarineAisEventProducer,
                 mmsi_filter: Optional[Set[int]] = None,
                 flush_interval: int = 1000):
        self._mqtt = mqtt_source
        self._kafka = kafka_producer
        self._event_producer = event_producer
        self._mmsi_filter = mmsi_filter
        self._flush_interval = flush_interval
        self._count = 0
        self._total = 0
        self._skipped = 0
        self._start_time = 0.0

    def run(self) -> None:
        """Start the bridge — blocks forever."""
        self._start_time = time.time()
        logger.info("Starting Digitraffic Marine bridge")
        self._mqtt.stream(self._on_message)

    def _on_message(self, topic_type: str, mmsi: int, payload: Dict[str, Any]) -> None:
        """Handle a single MQTT message."""
        if self._mmsi_filter and mmsi not in self._mmsi_filter:
            return

        if _emit_event(self._event_producer, topic_type, mmsi, payload):
            self._count += 1
            self._total += 1
        else:
            self._skipped += 1

        if self._count >= self._flush_interval:
            self._kafka.flush()
            elapsed = time.time() - self._start_time
            rate = self._total / elapsed if elapsed > 0 else 0
            logger.info("Flushed %d events (total: %d, skipped: %d, %.1f msg/sec)",
                        self._count, self._total, self._skipped, rate)
            self._count = 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Digitraffic Marine AIS bridge — Finnish/Baltic vessel tracking to Kafka")
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
    stream_p.add_argument("--subscribe", type=str,
                          default=os.getenv("DIGITRAFFIC_SUBSCRIBE", "location,metadata"),
                          help="Comma-separated: location,metadata (default: both)")
    stream_p.add_argument("--mmsi-filter", type=str,
                          default=os.getenv("DIGITRAFFIC_FILTER_MMSI"),
                          help="Comma-separated MMSI numbers to include (default: all)")
    stream_p.add_argument("--flush-interval", type=int,
                          default=int(os.getenv("DIGITRAFFIC_FLUSH_INTERVAL", "1000")),
                          help="Flush Kafka producer every N events")

    # --- probe ---
    probe_p = subparsers.add_parser("probe", help="Connect to MQTT and print messages")
    probe_p.add_argument("--subscribe", type=str,
                         default=os.getenv("DIGITRAFFIC_SUBSCRIBE", "location,metadata"),
                         help="Comma-separated: location,metadata (default: both)")
    probe_p.add_argument("--mmsi-filter", type=str,
                         default=os.getenv("DIGITRAFFIC_FILTER_MMSI"),
                         help="Comma-separated MMSI numbers to include")
    probe_p.add_argument("--duration", type=int, default=15,
                         help="Probe duration in seconds (default: 15)")

    args = parser.parse_args()

    if args.command == "probe":
        _run_probe(args)
        return

    if args.command == "stream":
        subs = [s.strip() for s in args.subscribe.split(",")]
        sub_loc = "location" in subs
        sub_meta = "metadata" in subs

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

        mmsi_filter_set = None
        if args.mmsi_filter:
            mmsi_filter_set = set(int(m.strip()) for m in args.mmsi_filter.split(",") if m.strip())

        mqtt_source = MQTTSource(
            subscribe_locations=sub_loc,
            subscribe_metadata=sub_meta,
            mmsi_filter=mmsi_filter_set,
        )
        kafka_producer = Producer(kafka_config)
        event_producer = FiDigitrafficMarineAisEventProducer(kafka_producer, topic)

        bridge = DigitraficBridge(
            mqtt_source=mqtt_source,
            kafka_producer=kafka_producer,
            event_producer=event_producer,
            mmsi_filter=mmsi_filter_set,
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


def _run_probe(args) -> None:
    """Connect to the live Digitraffic MQTT and print messages for --duration seconds."""
    from collections import Counter
    import json as _json

    subs = [s.strip() for s in args.subscribe.split(",")]
    sub_loc = "location" in subs
    sub_meta = "metadata" in subs

    mmsi_filter_set = None
    if args.mmsi_filter:
        mmsi_filter_set = set(int(m.strip()) for m in args.mmsi_filter.split(",") if m.strip())

    mqtt_src = MQTTSource(
        subscribe_locations=sub_loc,
        subscribe_metadata=sub_meta,
        mmsi_filter=mmsi_filter_set,
    )

    counter: Counter = Counter()
    start = time.time()
    sample_count: Dict[str, int] = {}

    def on_message(topic_type: str, mmsi: int, payload: Dict[str, Any]) -> None:
        counter[topic_type] += 1

        shown = sample_count.get(topic_type, 0)
        if shown < 3:
            sample_count[topic_type] = shown + 1
            print(f"[{topic_type}] MMSI={mmsi} {_json.dumps(payload)[:200]}")

        if time.time() - start > args.duration:
            raise KeyboardInterrupt("Probe timeout")

    try:
        mqtt_src.stream(on_message)
    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    total = sum(counter.values())
    print(f"\n--- Probe results ({elapsed:.0f}s) ---")
    for k, v in counter.most_common():
        print(f"  {k}: {v}")
    print(f"  Total: {total}")
    if elapsed > 0:
        print(f"  Rate: {total/elapsed:.1f} msg/sec")


if __name__ == "__main__":
    main()
