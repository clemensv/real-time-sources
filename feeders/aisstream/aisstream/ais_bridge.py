"""AISstream.io bridge — global AIS vessel tracking data to Kafka as CloudEvents."""

import argparse
import logging
import os
import sys
import time
from typing import Any, Dict, Optional, Set

from confluent_kafka import Producer
from aisstream_producer_data import (
    PositionReport, ShipStaticData, StandardClassBPositionReport,
    ExtendedClassBPositionReport, AidsToNavigationReport, StaticDataReport,
    BaseStationReport, SafetyBroadcastMessage,
    StandardSearchAndRescueAircraftReport, LongRangeAisBroadcastMessage,
    AddressedSafetyMessage, AddressedBinaryMessage, AssignedModeCommand,
    BinaryAcknowledge, BinaryBroadcastMessage, ChannelManagement,
    CoordinatedUTCInquiry, DataLinkManagementMessage,
    GnssBroadcastBinaryMessage, GroupAssignmentCommand, Interrogation,
    MultiSlotBinaryMessage, SingleSlotBinaryMessage,
)
from aisstream_producer_kafka_producer.producer import IOAISstreamEventProducer

from aisstream.ws_source import WebSocketSource

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Map AISstream MessageType strings to (data class, send method name)
_MESSAGE_MAP: Dict[str, tuple] = {
    "PositionReport": (PositionReport, "send_io_aisstream_position_report"),
    "ShipStaticData": (ShipStaticData, "send_io_aisstream_ship_static_data"),
    "StandardClassBPositionReport": (StandardClassBPositionReport, "send_io_aisstream_standard_class_bposition_report"),
    "ExtendedClassBPositionReport": (ExtendedClassBPositionReport, "send_io_aisstream_extended_class_bposition_report"),
    "AidsToNavigationReport": (AidsToNavigationReport, "send_io_aisstream_aids_to_navigation_report"),
    "StaticDataReport": (StaticDataReport, "send_io_aisstream_static_data_report"),
    "BaseStationReport": (BaseStationReport, "send_io_aisstream_base_station_report"),
    "SafetyBroadcastMessage": (SafetyBroadcastMessage, "send_io_aisstream_safety_broadcast_message"),
    "StandardSearchAndRescueAircraftReport": (StandardSearchAndRescueAircraftReport, "send_io_aisstream_standard_search_and_rescue_aircraft_report"),
    "LongRangeAisBroadcastMessage": (LongRangeAisBroadcastMessage, "send_io_aisstream_long_range_ais_broadcast_message"),
    "AddressedSafetyMessage": (AddressedSafetyMessage, "send_io_aisstream_addressed_safety_message"),
    "AddressedBinaryMessage": (AddressedBinaryMessage, "send_io_aisstream_addressed_binary_message"),
    "AssignedModeCommand": (AssignedModeCommand, "send_io_aisstream_assigned_mode_command"),
    "BinaryAcknowledge": (BinaryAcknowledge, "send_io_aisstream_binary_acknowledge"),
    "BinaryBroadcastMessage": (BinaryBroadcastMessage, "send_io_aisstream_binary_broadcast_message"),
    "ChannelManagement": (ChannelManagement, "send_io_aisstream_channel_management"),
    "CoordinatedUTCInquiry": (CoordinatedUTCInquiry, "send_io_aisstream_coordinated_utcinquiry"),
    "DataLinkManagementMessage": (DataLinkManagementMessage, "send_io_aisstream_data_link_management_message"),
    "GnssBroadcastBinaryMessage": (GnssBroadcastBinaryMessage, "send_io_aisstream_gnss_broadcast_binary_message"),
    "GroupAssignmentCommand": (GroupAssignmentCommand, "send_io_aisstream_group_assignment_command"),
    "Interrogation": (Interrogation, "send_io_aisstream_interrogation"),
    "MultiSlotBinaryMessage": (MultiSlotBinaryMessage, "send_io_aisstream_multi_slot_binary_message"),
    "SingleSlotBinaryMessage": (SingleSlotBinaryMessage, "send_io_aisstream_single_slot_binary_message"),
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
    """Use MMSI (UserID) as the Kafka partition key."""
    return str(getattr(data, 'UserID', getattr(data, 'user_id', '')))


def _emit_event(event_producer: IOAISstreamEventProducer,
                message_type: str, payload: Dict[str, Any]) -> bool:
    """Send a decoded AIS message through the typed Kafka producer.

    Returns True if the message was emitted, False if the type is unknown.
    """
    mapping = _MESSAGE_MAP.get(message_type)
    if mapping is None:
        logger.debug("Skipping unknown message type: %s", message_type)
        return False

    data_class, send_method_name = mapping
    try:
        data = data_class.from_serializer_dict(payload)
        send_fn = getattr(event_producer, send_method_name)
        mmsi = _mmsi_key_mapper(None, data)
        send_fn(_mmsi=mmsi, data=data, flush_producer=False, key_mapper=_mmsi_key_mapper)
        return True
    except Exception as e:
        logger.warning("Failed to emit %s: %s", message_type, e)
        return False


def _parse_bounding_boxes(bbox_str: str):
    """Parse bounding box string: 'lat1,lon1,lat2,lon2;...' into nested list."""
    boxes = []
    for box_str in bbox_str.split(";"):
        parts = [float(x.strip()) for x in box_str.split(",")]
        if len(parts) != 4:
            raise ValueError(f"Bounding box must have 4 values (lat1,lon1,lat2,lon2), got {len(parts)}")
        boxes.append([[parts[0], parts[1]], [parts[2], parts[3]]])
    return boxes


class AISBridge:
    """Connects AISstream.io WebSocket to Kafka via CloudEvents."""

    def __init__(self, ws_source: WebSocketSource,
                 kafka_producer: Producer,
                 event_producer: IOAISstreamEventProducer,
                 mmsi_filter: Optional[Set[str]] = None,
                 flush_interval: int = 1000):
        self._ws = ws_source
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
        logger.info("Starting AISstream bridge")
        self._ws.stream(self._on_message)

    def _on_message(self, msg: Dict[str, Any]) -> None:
        """Handle a single AISstream JSON message."""
        message_type = msg.get("MessageType")
        if not message_type:
            return

        metadata = msg.get("MetaData", {})
        mmsi = str(metadata.get("MMSI", ""))

        # Client-side MMSI filter (supplements server-side filtering)
        if self._mmsi_filter and mmsi not in self._mmsi_filter:
            return

        # Extract the typed payload from the Message wrapper
        message_wrapper = msg.get("Message", {})
        payload = message_wrapper.get(message_type)
        if payload is None:
            logger.debug("No payload for message type %s", message_type)
            return

        if _emit_event(self._event_producer, message_type, payload):
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
        description="AISstream.io bridge — global AIS vessel tracking to Kafka")
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
    stream_p.add_argument("--api-key", type=str,
                          default=os.getenv("AISSTREAM_API_KEY"),
                          help="AISstream.io API key")
    stream_p.add_argument("--bounding-boxes", type=str,
                          default=os.getenv("AISSTREAM_BOUNDING_BOXES", "-90,-180,90,180"),
                          help="Bounding boxes as 'lat1,lon1,lat2,lon2;...' (default: global)")
    stream_p.add_argument("--message-types", type=str,
                          default=os.getenv("AISSTREAM_MESSAGE_TYPES"),
                          help="Comma-separated AIS message type names to subscribe to (default: all)")
    stream_p.add_argument("--mmsi-filter", type=str,
                          default=os.getenv("AISSTREAM_FILTER_MMSI"),
                          help="Comma-separated MMSI numbers to include (default: all)")
    stream_p.add_argument("--flush-interval", type=int,
                          default=int(os.getenv("AISSTREAM_FLUSH_INTERVAL", "1000")),
                          help="Flush Kafka producer every N events")

    # --- probe ---
    probe_p = subparsers.add_parser("probe", help="Connect to WebSocket and print messages")
    probe_p.add_argument("--api-key", type=str,
                         default=os.getenv("AISSTREAM_API_KEY"),
                         help="AISstream.io API key")
    probe_p.add_argument("--bounding-boxes", type=str,
                         default=os.getenv("AISSTREAM_BOUNDING_BOXES", "-90,-180,90,180"),
                         help="Bounding boxes as 'lat1,lon1,lat2,lon2;...'")
    probe_p.add_argument("--message-types", type=str,
                         default=os.getenv("AISSTREAM_MESSAGE_TYPES"),
                         help="Comma-separated message type names to subscribe to")
    probe_p.add_argument("--duration", type=int, default=15,
                         help="Probe duration in seconds (default: 15)")

    args = parser.parse_args()

    if args.command == "probe":
        _run_probe(args)
        return

    if args.command == "stream":
        if not args.api_key:
            print("Error: AISstream API key required (--api-key or AISSTREAM_API_KEY).")
            sys.exit(1)

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

        bounding_boxes = _parse_bounding_boxes(args.bounding_boxes)
        message_type_filter = None
        if args.message_types:
            message_type_filter = [t.strip() for t in args.message_types.split(",") if t.strip()]

        mmsi_filter = None
        if args.mmsi_filter:
            mmsi_filter = set(m.strip() for m in args.mmsi_filter.split(",") if m.strip())

        ws = WebSocketSource(
            api_key=args.api_key,
            bounding_boxes=bounding_boxes,
            message_type_filter=message_type_filter,
            mmsi_filter=[m for m in mmsi_filter] if mmsi_filter else None,
        )
        kafka_producer = Producer(kafka_config)
        event_producer = IOAISstreamEventProducer(kafka_producer, topic)

        bridge = AISBridge(
            ws_source=ws,
            kafka_producer=kafka_producer,
            event_producer=event_producer,
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


def _run_probe(args) -> None:
    """Connect to the live AISstream and print messages for --duration seconds."""
    from collections import Counter

    if not args.api_key:
        print("Error: AISstream API key required (--api-key or AISSTREAM_API_KEY).")
        sys.exit(1)

    bounding_boxes = _parse_bounding_boxes(args.bounding_boxes)
    message_type_filter = None
    if args.message_types:
        message_type_filter = [t.strip() for t in args.message_types.split(",") if t.strip()]

    ws = WebSocketSource(
        api_key=args.api_key,
        bounding_boxes=bounding_boxes,
        message_type_filter=message_type_filter,
    )

    counter: Counter = Counter()
    start = time.time()
    sample_count: Dict[str, int] = {}

    def on_message(msg: Dict[str, Any]) -> None:
        message_type = msg.get("MessageType", "Unknown")
        counter[message_type] += 1
        metadata = msg.get("MetaData", {})

        # Print first 2 samples of each type
        shown = sample_count.get(message_type, 0)
        if shown < 2:
            sample_count[message_type] = shown + 1
            mmsi = metadata.get("MMSI", "?")
            name = metadata.get("ShipName", "").strip()
            lat = metadata.get("latitude", "?")
            lon = metadata.get("longitude", "?")
            ts = metadata.get("time_utc", "?")
            print(f"[{message_type}] MMSI={mmsi} name={name!r} "
                  f"pos=({lat},{lon}) time={ts}")

        if time.time() - start > args.duration:
            raise KeyboardInterrupt("Probe timeout")

    try:
        ws.stream(on_message)
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
