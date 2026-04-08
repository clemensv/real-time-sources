"""Digitraffic Marine AIS bridge — Finnish/Baltic vessel tracking to Kafka as CloudEvents."""

import argparse
import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional, Set

from confluent_kafka import Producer
import requests
from digitraffic_maritime_producer_data import PortCall, PortCallAgent, PortCallAreaDetail, VesselLocation, VesselMetadata
from digitraffic_maritime_producer_kafka_producer.producer import (
    FiDigitrafficMarineAisEventProducer,
    FiDigitrafficMarinePortcallEventProducer,
)

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

_PORT_CALLS_URL = "https://meri.digitraffic.fi/api/port-call/v1/port-calls"


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


def _port_call_key_mapper(event, data) -> str:
    """Use the Digitraffic port call identifier as the Kafka partition key."""
    return str(getattr(data, 'port_call_id', ''))


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


class DigitrafficPortCallPoller:
    """Polls Digitraffic Portnet port calls and emits them as CloudEvents."""

    def __init__(self,
                 kafka_producer: Producer,
                 event_producer: FiDigitrafficMarinePortcallEventProducer,
                 state_file: str,
                 poll_interval: int = 300,
                 session: Optional[requests.Session] = None):
        self._kafka = kafka_producer
        self._event_producer = event_producer
        self._state_file = state_file
        self._poll_interval = poll_interval
        self._session = session or requests.Session()
        self._session.headers.update({"User-Agent": "real-time-sources-digitraffic-maritime/1.0"})

    @staticmethod
    def _normalize_optional_text(value: Any) -> Optional[str]:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _normalize_optional_int(value: Any) -> Optional[int]:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _normalize_float(value: Any, default: float = 0.0) -> float:
        if value is None or value == "":
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @classmethod
    def parse_port_call(cls, payload: Dict[str, Any]) -> Optional[PortCall]:
        """Normalize one raw Digitraffic port call payload into the generated PortCall type."""
        port_call_id = cls._normalize_optional_int(payload.get("portCallId"))
        updated_at = cls._normalize_optional_text(payload.get("portCallTimestamp"))
        port_to_visit = cls._normalize_optional_text(payload.get("portToVisit"))
        vessel_name = cls._normalize_optional_text(payload.get("vesselName"))
        if port_call_id is None or updated_at is None or port_to_visit is None or vessel_name is None:
            return None

        agents = []
        for agent in payload.get("agentInfo", []) or []:
            name = cls._normalize_optional_text(agent.get("name"))
            port_call_direction = cls._normalize_optional_text(agent.get("portCallDirection"))
            role = cls._normalize_optional_int(agent.get("role"))
            if name is None or port_call_direction is None or role is None:
                continue
            agents.append(PortCallAgent.from_serializer_dict({
                "name": name,
                "port_call_direction": port_call_direction,
                "role": role,
            }))

        port_areas = []
        for detail in payload.get("portAreaDetails", []) or []:
            port_areas.append(PortCallAreaDetail.from_serializer_dict({
                "port_area_code": cls._normalize_optional_text(detail.get("portAreaCode")),
                "port_area_name": cls._normalize_optional_text(detail.get("portAreaName")),
                "berth_code": cls._normalize_optional_text(detail.get("berthCode")),
                "berth_name": cls._normalize_optional_text(detail.get("berthName")),
                "eta": cls._normalize_optional_text(detail.get("eta")),
                "eta_source": cls._normalize_optional_text(detail.get("etaSource")),
                "etd": cls._normalize_optional_text(detail.get("etd")),
                "etd_source": cls._normalize_optional_text(detail.get("etdSource")),
                "ata": cls._normalize_optional_text(detail.get("ata")),
                "ata_source": cls._normalize_optional_text(detail.get("ataSource")),
                "atd": cls._normalize_optional_text(detail.get("atd")),
                "atd_source": cls._normalize_optional_text(detail.get("atdSource")),
                "arrival_draught": cls._normalize_float(detail.get("arrivalDraught"), 0.0),
                "departure_draught": cls._normalize_float(detail.get("departureDraught"), 0.0),
            }))

        return PortCall.from_serializer_dict({
            "port_call_id": port_call_id,
            "updated_at": updated_at,
            "customs_reference": cls._normalize_optional_text(payload.get("customsReference")),
            "port_to_visit": port_to_visit,
            "previous_port": cls._normalize_optional_text(payload.get("prevPort")),
            "next_port": cls._normalize_optional_text(payload.get("nextPort")),
            "mmsi": cls._normalize_optional_int(payload.get("mmsi")),
            "imo_lloyds": cls._normalize_optional_int(payload.get("imoLloyds")),
            "vessel_name": vessel_name,
            "vessel_name_prefix": cls._normalize_optional_text(payload.get("vesselNamePrefix")),
            "radio_call_sign": cls._normalize_optional_text(payload.get("radioCallSign")),
            "nationality": cls._normalize_optional_text(payload.get("nationality")),
            "vessel_type_code": cls._normalize_optional_int(payload.get("vesselTypeCode")),
            "domestic_traffic_arrival": bool(payload.get("domesticTrafficArrival", False)),
            "domestic_traffic_departure": bool(payload.get("domesticTrafficDeparture", False)),
            "arrival_with_cargo": bool(payload.get("arrivalWithCargo", False)),
            "not_loading": bool(payload.get("notLoading", False)),
            "discharge": cls._normalize_optional_int(payload.get("discharge")),
            "current_security_level": cls._normalize_optional_int(payload.get("currentSecurityLevel")),
            "agents": agents,
            "port_areas": port_areas,
        })

    def load_state(self) -> Dict[str, Dict[str, str]]:
        """Load deduplication state for port calls."""
        try:
            if self._state_file and os.path.exists(self._state_file):
                with open(self._state_file, "r", encoding="utf-8") as file_handle:
                    state = json.load(file_handle)
                    if isinstance(state, dict) and isinstance(state.get("port_calls"), dict):
                        return state
        except Exception as exc:
            logger.warning("Failed to load port call state from %s: %s", self._state_file, exc)
        return {"port_calls": {}}

    def save_state(self, state: Dict[str, Dict[str, str]]) -> None:
        """Persist port-call deduplication state."""
        try:
            directory = os.path.dirname(self._state_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self._state_file, "w", encoding="utf-8") as file_handle:
                json.dump(state, file_handle, indent=2)
        except Exception as exc:
            logger.warning("Failed to save port call state to %s: %s", self._state_file, exc)

    def poll_port_calls(self) -> list[PortCall]:
        """Fetch and normalize current Digitraffic port calls."""
        response = self._session.get(_PORT_CALLS_URL, timeout=60)
        response.raise_for_status()
        payload = response.json()
        port_calls = []
        for raw_port_call in payload.get("portCalls", []):
            port_call = self.parse_port_call(raw_port_call)
            if port_call is not None:
                port_calls.append(port_call)
        return port_calls

    def poll_and_send(self, once: bool = False) -> None:
        """Poll and emit new or updated port calls."""
        while True:
            try:
                state = self.load_state()
                last_seen = state.get("port_calls", {})
                port_calls = self.poll_port_calls()

                sent = 0
                for port_call in port_calls:
                    key = str(port_call.port_call_id)
                    if last_seen.get(key) == port_call.updated_at:
                        continue
                    self._event_producer.send_fi_digitraffic_marine_portcall_port_call(
                        _port_call_id=key,
                        data=port_call,
                        flush_producer=False,
                        key_mapper=_port_call_key_mapper,
                    )
                    last_seen[key] = port_call.updated_at
                    sent += 1

                if sent:
                    self._kafka.flush()
                    logger.info("Sent %d new or updated port call event(s)", sent)

                state["port_calls"] = {str(port_call.port_call_id): port_call.updated_at for port_call in port_calls}
                self.save_state(state)
            except Exception as exc:
                logger.warning("Port call polling cycle failed: %s", exc)

            if once:
                break

            time.sleep(self._poll_interval)


def _resolve_kafka_args(args):
    """Resolve Kafka connectivity settings from direct arguments or a connection string."""
    if args.connection_string:
        cfg = parse_connection_string(args.connection_string)
        return (
            cfg.get("bootstrap.servers"),
            cfg.get("kafka_topic"),
            cfg.get("sasl.username"),
            cfg.get("sasl.password"),
        )
    return (
        args.kafka_bootstrap_servers,
        args.kafka_topic,
        args.sasl_username,
        args.sasl_password,
    )


def _build_kafka_config(bootstrap: str, sasl_user: Optional[str], sasl_pw: Optional[str]) -> Dict[str, str]:
    """Build Kafka client configuration for either direct Kafka or Event Hubs connectivity."""
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
    return kafka_config


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

    # --- port-calls ---
    port_calls_p = subparsers.add_parser("port-calls", help="Poll Portnet-backed Digitraffic port calls to Kafka")
    port_calls_p.add_argument("--kafka-bootstrap-servers", type=str,
                              default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    port_calls_p.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"))
    port_calls_p.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    port_calls_p.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    port_calls_p.add_argument("-c", "--connection-string", type=str,
                              default=os.getenv("CONNECTION_STRING"))
    port_calls_p.add_argument("--poll-interval", type=int,
                              default=int(os.getenv("DIGITRAFFIC_PORTCALL_POLL_INTERVAL", "300")),
                              help="Poll interval in seconds for the port call REST feed")
    port_calls_p.add_argument("--state-file", type=str,
                              default=os.getenv("DIGITRAFFIC_PORTCALL_STATE_FILE",
                                                os.path.expanduser("~/.digitraffic_portcalls_state.json")),
                              help="JSON file used to persist last-seen port call timestamps")

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

    if args.command == "port-calls":
        bootstrap, topic, sasl_user, sasl_pw = _resolve_kafka_args(args)

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
            sys.exit(1)
        if not topic:
            print("Error: Kafka topic required (--kafka-topic or -c).")
            sys.exit(1)

        kafka_config = _build_kafka_config(bootstrap, sasl_user, sasl_pw)
        kafka_producer = Producer(kafka_config)
        event_producer = FiDigitrafficMarinePortcallEventProducer(kafka_producer, topic)
        poller = DigitrafficPortCallPoller(
            kafka_producer=kafka_producer,
            event_producer=event_producer,
            state_file=args.state_file,
            poll_interval=args.poll_interval,
        )

        try:
            poller.poll_and_send()
        except KeyboardInterrupt:
            logger.info("Shutting down port call poller...")
        finally:
            kafka_producer.flush()
        return

    if args.command == "stream":
        subs = [s.strip() for s in args.subscribe.split(",")]
        sub_loc = "location" in subs
        sub_meta = "metadata" in subs

        bootstrap, topic, sasl_user, sasl_pw = _resolve_kafka_args(args)

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
            sys.exit(1)
        if not topic:
            print("Error: Kafka topic required (--kafka-topic or -c).")
            sys.exit(1)

        kafka_config = _build_kafka_config(bootstrap, sasl_user, sasl_pw)

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
