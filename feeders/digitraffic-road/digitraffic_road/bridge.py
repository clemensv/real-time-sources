"""Digitraffic Road bridge — Finnish road traffic data to Kafka as CloudEvents."""

import argparse
import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional, Set

import requests
from confluent_kafka import Producer
from digitraffic_road_producer_data import (
    MaintenanceTaskType,
    MaintenanceTracking,
    TmsSensorData,
    TmsStation,
    TrafficMessage,
    WeatherSensorData,
    WeatherStation,
)
from digitraffic_road_producer_kafka_producer.producer import (
    FiDigitrafficRoadMaintenanceEventProducer,
    FiDigitrafficRoadMaintenanceTasksEventProducer,
    FiDigitrafficRoadMessagesEventProducer,
    FiDigitrafficRoadSensorsEventProducer,
    FiDigitrafficRoadStationsEventProducer,
)

from digitraffic_road.mqtt_source import MQTTSource

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Maps MQTT situation type values to producer send methods
_SITUATION_TYPE_SENDERS = {
    "TRAFFIC_ANNOUNCEMENT": "send_fi_digitraffic_road_messages_traffic_announcement",
    "ROAD_WORK": "send_fi_digitraffic_road_messages_road_work",
    "WEIGHT_RESTRICTION": "send_fi_digitraffic_road_messages_weight_restriction",
    "EXEMPTED_TRANSPORT": "send_fi_digitraffic_road_messages_exempted_transport",
}

# Maps MQTT situation type to human-readable situation_type field values
_SITUATION_TYPE_LABELS = {
    "TRAFFIC_ANNOUNCEMENT": "traffic announcement",
    "ROAD_WORK": "road work",
    "WEIGHT_RESTRICTION": "weight restriction",
    "EXEMPTED_TRANSPORT": "exempted transport",
}

_TMS_STATIONS_URL = "https://tie.digitraffic.fi/api/tms/v1/stations"
_WEATHER_STATIONS_URL = "https://tie.digitraffic.fi/api/weather/v1/stations"
_MAINTENANCE_TASKS_URL = "https://tie.digitraffic.fi/api/maintenance/v1/tracking/tasks"


def _flatten_station(feature: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten a GeoJSON Feature from the Digitraffic stations REST API into a flat dict."""
    props = feature.get("properties", {})
    coords = feature.get("geometry", {}).get("coordinates", [0.0, 0.0, 0.0])
    names = props.get("names", {})
    road = props.get("roadAddress", {})
    return {
        "station_id": props.get("id", 0),
        "name": props.get("name", ""),
        "tms_number": props.get("tmsNumber"),
        "names_fi": names.get("fi", ""),
        "names_sv": names.get("sv"),
        "names_en": names.get("en"),
        "longitude": coords[0] if len(coords) > 0 else 0.0,
        "latitude": coords[1] if len(coords) > 1 else 0.0,
        "altitude": coords[2] if len(coords) > 2 and coords[2] != 0.0 else None,
        "municipality": props.get("municipality", ""),
        "municipality_code": props.get("municipalityCode", 0),
        "province": props.get("province", ""),
        "province_code": props.get("provinceCode", 0),
        "road_number": road.get("roadNumber", 0),
        "road_section": road.get("roadSection", 0),
        "distance_from_section_start": road.get("distanceFromRoadSectionStart", 0),
        "carriageway": road.get("carriageway"),
        "side": road.get("side"),
        "contract_area": road.get("contractArea"),
        "contract_area_code": road.get("contractAreaCode"),
        "station_type": props.get("stationType", ""),
        "master": props.get("master"),
        "collection_status": props.get("collectionStatus", ""),
        "collection_interval": props.get("collectionInterval"),
        "state": props.get("state"),
        "free_flow_speed_1": props.get("freeFlowSpeed1"),
        "free_flow_speed_2": props.get("freeFlowSpeed2"),
        "bearing": props.get("bearing"),
        "start_time": props.get("startTime", ""),
        "livi_id": props.get("liviId"),
        "sensors": props.get("sensors", []),
        "data_updated_time": props.get("dataUpdatedTime"),
    }


def fetch_and_emit_tms_stations(
    stations_producer: "FiDigitrafficRoadStationsEventProducer",
) -> int:
    """Fetch all TMS stations from the REST API and emit as reference events. Returns count."""
    resp = requests.get(_TMS_STATIONS_URL, timeout=60)
    resp.raise_for_status()
    features = resp.json().get("features", [])
    count = 0
    for feature in features:
        try:
            flat = _flatten_station(feature)
            data = TmsStation.from_serializer_dict(flat)
            stations_producer.send_fi_digitraffic_road_stations_tms_station(
                _station_id=str(flat["station_id"]),
                data=data,
                flush_producer=False,
            )
            count += 1
        except Exception as e:
            logger.warning("Failed to emit TMS station %s: %s", feature.get("id"), e)
    return count


def fetch_and_emit_weather_stations(
    stations_producer: "FiDigitrafficRoadStationsEventProducer",
) -> int:
    """Fetch all weather stations from the REST API and emit as reference events. Returns count."""
    resp = requests.get(_WEATHER_STATIONS_URL, timeout=60)
    resp.raise_for_status()
    features = resp.json().get("features", [])
    count = 0
    for feature in features:
        try:
            flat = _flatten_station(feature)
            data = WeatherStation.from_serializer_dict(flat)
            stations_producer.send_fi_digitraffic_road_stations_weather_station(
                _station_id=str(flat["station_id"]),
                data=data,
                flush_producer=False,
            )
            count += 1
        except Exception as e:
            logger.warning("Failed to emit weather station %s: %s", feature.get("id"), e)
    return count


def fetch_and_emit_maintenance_tasks(
    tasks_producer: "FiDigitrafficRoadMaintenanceTasksEventProducer",
) -> int:
    """Fetch all maintenance task types from the REST API and emit as reference events. Returns count."""
    resp = requests.get(_MAINTENANCE_TASKS_URL, timeout=30)
    resp.raise_for_status()
    tasks = resp.json()
    count = 0
    for task in tasks:
        try:
            flat = {
                "task_id": task.get("id", ""),
                "name_fi": task.get("nameFi", ""),
                "name_en": task.get("nameEn", ""),
                "name_sv": task.get("nameSv", ""),
                "data_updated_time": task.get("dataUpdatedTime"),
            }
            data = MaintenanceTaskType.from_serializer_dict(flat)
            tasks_producer.send_fi_digitraffic_road_maintenance_tasks_maintenance_task_type(
                _task_id=flat["task_id"],
                data=data,
                flush_producer=False,
            )
            count += 1
        except Exception as e:
            logger.warning("Failed to emit maintenance task type %s: %s", task.get("id"), e)
    return count


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=", 1)[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
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
    return config_dict


def _emit_sensor_event(
    event_producer: FiDigitrafficRoadSensorsEventProducer,
    data_type: str,
    station_id: int,
    sensor_id: int,
    payload: Dict[str, Any],
) -> bool:
    """Send a sensor message through the typed Kafka producer. Returns True on success."""
    enriched = dict(payload)
    enriched["station_id"] = station_id
    enriched["sensor_id"] = sensor_id

    try:
        if data_type == "tms":
            if "start" not in enriched:
                enriched["start"] = None
            if "end" not in enriched:
                enriched["end"] = None
            data = TmsSensorData.from_serializer_dict(enriched)
            event_producer.send_fi_digitraffic_road_sensors_tms_sensor_data(
                _station_id=str(station_id),
                _sensor_id=str(sensor_id),
                data=data,
                flush_producer=False,
            )
            return True
        elif data_type == "weather":
            data = WeatherSensorData.from_serializer_dict(enriched)
            event_producer.send_fi_digitraffic_road_sensors_weather_sensor_data(
                _station_id=str(station_id),
                _sensor_id=str(sensor_id),
                data=data,
                flush_producer=False,
            )
            return True
        else:
            return False
    except Exception as e:
        logger.warning("Failed to emit %s for station %d sensor %d: %s", data_type, station_id, sensor_id, e)
        return False


def _flatten_traffic_message(situation_type_mqtt: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten a Digitraffic traffic-message GeoJSON Feature into the TrafficMessage schema."""
    props = payload.get("properties", payload)
    announcement = {}
    announcements = props.get("announcements", [])
    if announcements:
        announcement = announcements[0]

    situation_type_label = _SITUATION_TYPE_LABELS.get(situation_type_mqtt, situation_type_mqtt)

    td = announcement.get("timeAndDuration", {})
    location = announcement.get("location", {})
    contact = props.get("contact", {})
    geometry = payload.get("geometry", {})

    return {
        "situation_id": props.get("situationId", ""),
        "situation_type": situation_type_label,
        "traffic_announcement_type": props.get("trafficAnnouncementType"),
        "version": props.get("version", 0),
        "release_time": props.get("releaseTime", ""),
        "version_time": props.get("versionTime", ""),
        "title": announcement.get("title"),
        "language": announcement.get("language"),
        "sender": announcement.get("sender"),
        "location_description": location.get("description"),
        "start_time": td.get("startTime"),
        "end_time": td.get("endTime"),
        "features_json": json.dumps(announcement.get("features")) if announcement.get("features") else None,
        "road_work_phases_json": json.dumps(announcement.get("roadWorkPhases")) if announcement.get("roadWorkPhases") else None,
        "comment": announcement.get("comment"),
        "additional_information": announcement.get("additionalInformation"),
        "contact_phone": contact.get("phone"),
        "contact_email": contact.get("email"),
        "announcements_json": json.dumps(announcements) if announcements else None,
        "geometry_type": geometry.get("type"),
        "geometry_coordinates_json": json.dumps(geometry.get("coordinates")) if geometry.get("coordinates") else None,
    }


def _emit_traffic_message(
    event_producer: FiDigitrafficRoadMessagesEventProducer,
    situation_type_mqtt: str,
    payload: Dict[str, Any],
) -> bool:
    """Send a traffic message through the typed Kafka producer. Returns True on success."""
    sender_name = _SITUATION_TYPE_SENDERS.get(situation_type_mqtt)
    if not sender_name:
        logger.debug("Unknown situation type for emission: %s", situation_type_mqtt)
        return False
    try:
        flat = _flatten_traffic_message(situation_type_mqtt, payload)
        data = TrafficMessage.from_serializer_dict(flat)
        sender = getattr(event_producer, sender_name)
        sender(
            _situation_id=flat["situation_id"],
            data=data,
            flush_producer=False,
        )
        return True
    except Exception as e:
        logger.warning("Failed to emit traffic message (%s): %s", situation_type_mqtt, e)
        return False


def _emit_maintenance(
    event_producer: FiDigitrafficRoadMaintenanceEventProducer,
    domain: str,
    payload: Dict[str, Any],
) -> bool:
    """Send a maintenance tracking event. Returns True on success."""
    try:
        enriched = dict(payload)
        enriched["domain"] = domain
        if "direction" not in enriched:
            enriched["direction"] = None
        if "source" not in enriched:
            enriched["source"] = None
        data = MaintenanceTracking.from_serializer_dict(enriched)
        event_producer.send_fi_digitraffic_road_maintenance_maintenance_tracking(
            _domain=domain,
            data=data,
            flush_producer=False,
        )
        return True
    except Exception as e:
        logger.warning("Failed to emit maintenance (%s): %s", domain, e)
        return False


class DigitrafficRoadBridge:
    """Connects Digitraffic Road MQTT to Kafka via CloudEvents."""

    def __init__(
        self,
        mqtt_source: MQTTSource,
        kafka_producer: Producer,
        sensors_producer: Optional[FiDigitrafficRoadSensorsEventProducer] = None,
        messages_producer: Optional[FiDigitrafficRoadMessagesEventProducer] = None,
        maintenance_producer: Optional[FiDigitrafficRoadMaintenanceEventProducer] = None,
        stations_producer: Optional[FiDigitrafficRoadStationsEventProducer] = None,
        tasks_producer: Optional[FiDigitrafficRoadMaintenanceTasksEventProducer] = None,
        flush_interval: int = 1000,
    ):
        self._mqtt = mqtt_source
        self._kafka = kafka_producer
        self._sensors_producer = sensors_producer
        self._messages_producer = messages_producer
        self._maintenance_producer = maintenance_producer
        self._stations_producer = stations_producer
        self._tasks_producer = tasks_producer
        self._flush_interval = flush_interval
        self._count = 0
        self._total = 0
        self._skipped = 0
        self._start_time = 0.0

    def run(self) -> None:
        """Start the bridge — emits reference data, then streams telemetry. Blocks forever."""
        self._start_time = time.time()
        self._emit_reference_data()
        logger.info("Starting Digitraffic Road MQTT telemetry stream")
        self._mqtt.stream(self._on_message)

    def _emit_reference_data(self) -> None:
        """Fetch and emit reference data from REST APIs before starting telemetry."""
        ref_total = 0
        if self._stations_producer:
            try:
                n = fetch_and_emit_tms_stations(self._stations_producer)
                ref_total += n
                logger.info("Emitted %d TMS station reference events", n)
            except Exception as e:
                logger.error("Failed to fetch TMS stations: %s", e)
            try:
                n = fetch_and_emit_weather_stations(self._stations_producer)
                ref_total += n
                logger.info("Emitted %d weather station reference events", n)
            except Exception as e:
                logger.error("Failed to fetch weather stations: %s", e)
        if self._tasks_producer:
            try:
                n = fetch_and_emit_maintenance_tasks(self._tasks_producer)
                ref_total += n
                logger.info("Emitted %d maintenance task type reference events", n)
            except Exception as e:
                logger.error("Failed to fetch maintenance task types: %s", e)
        if ref_total > 0:
            self._kafka.flush()
            logger.info("Reference data flush complete (%d events)", ref_total)
            self._total += ref_total

    def _on_message(self, data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        """Handle a single MQTT message."""
        emitted = False

        if data_type in ("tms", "weather") and self._sensors_producer:
            emitted = _emit_sensor_event(
                self._sensors_producer,
                data_type,
                metadata["station_id"],
                metadata["sensor_id"],
                payload,
            )
        elif data_type in ("traffic-announcement", "road-work", "weight-restriction", "exempted-transport") and self._messages_producer:
            emitted = _emit_traffic_message(
                self._messages_producer,
                metadata["situation_type"],
                payload,
            )
        elif data_type == "maintenance" and self._maintenance_producer:
            emitted = _emit_maintenance(
                self._maintenance_producer,
                metadata["domain"],
                payload,
            )

        if emitted:
            self._count += 1
            self._total += 1
        else:
            self._skipped += 1

        if self._count >= self._flush_interval:
            self._kafka.flush()
            elapsed = time.time() - self._start_time
            rate = self._total / elapsed if elapsed > 0 else 0
            logger.info(
                "Flushed %d events (total: %d, skipped: %d, %.1f msg/sec)",
                self._count, self._total, self._skipped, rate,
            )
            self._count = 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Digitraffic Road bridge — Finnish road traffic data to Kafka",
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- stream ---
    stream_p = subparsers.add_parser("stream", help="Stream traffic data to Kafka")
    stream_p.add_argument(
        "--kafka-bootstrap-servers", type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    )
    stream_p.add_argument(
        "--kafka-topic-sensors", type=str,
        default=os.getenv("KAFKA_TOPIC_SENSORS", "digitraffic-road-sensors"),
    )
    stream_p.add_argument(
        "--kafka-topic-messages", type=str,
        default=os.getenv("KAFKA_TOPIC_MESSAGES", "digitraffic-road-messages"),
    )
    stream_p.add_argument(
        "--kafka-topic-maintenance", type=str,
        default=os.getenv("KAFKA_TOPIC_MAINTENANCE", "digitraffic-road-maintenance"),
    )
    stream_p.add_argument(
        "--sasl-username", type=str, default=os.getenv("SASL_USERNAME"),
    )
    stream_p.add_argument(
        "--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"),
    )
    stream_p.add_argument(
        "-c", "--connection-string", type=str,
        default=os.getenv("CONNECTION_STRING"),
    )
    stream_p.add_argument(
        "--subscribe", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather,traffic-messages,maintenance"),
        help="Comma-separated: tms,weather,traffic-messages,maintenance",
    )
    stream_p.add_argument(
        "--station-filter", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"),
        help="Comma-separated station IDs to include (sensors only, default: all)",
    )
    stream_p.add_argument(
        "--flush-interval", type=int,
        default=int(os.getenv("DIGITRAFFIC_ROAD_FLUSH_INTERVAL", "1000")),
        help="Flush Kafka producer every N events",
    )

    # --- probe ---
    probe_p = subparsers.add_parser("probe", help="Connect to MQTT and print messages")
    probe_p.add_argument(
        "--subscribe", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather,traffic-messages,maintenance"),
        help="Comma-separated families to subscribe to",
    )
    probe_p.add_argument(
        "--station-filter", type=str,
        default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"),
        help="Comma-separated station IDs to include (sensors only)",
    )
    probe_p.add_argument(
        "--duration", type=int, default=15,
        help="Probe duration in seconds (default: 15)",
    )

    args = parser.parse_args()

    if args.command == "probe":
        _run_probe(args)
        return

    if args.command == "stream":
        subs = [s.strip() for s in args.subscribe.split(",")]
        sub_tms = "tms" in subs
        sub_weather = "weather" in subs
        sub_messages = "traffic-messages" in subs
        sub_maintenance = "maintenance" in subs

        if args.connection_string:
            cfg = parse_connection_string(args.connection_string)
            bootstrap = cfg.get("bootstrap.servers")
            sasl_user = cfg.get("sasl.username")
            sasl_pw = cfg.get("sasl.password")
        else:
            bootstrap = args.kafka_bootstrap_servers
            sasl_user = args.sasl_username
            sasl_pw = args.sasl_password

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
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

        station_filter_set = None
        if args.station_filter:
            station_filter_set = set(
                int(s.strip()) for s in args.station_filter.split(",") if s.strip()
            )

        mqtt_source = MQTTSource(
            subscribe_tms=sub_tms,
            subscribe_weather=sub_weather,
            subscribe_traffic_messages=sub_messages,
            subscribe_maintenance=sub_maintenance,
            station_filter=station_filter_set,
        )
        kafka_producer = Producer(kafka_config)

        sensors_prod = FiDigitrafficRoadSensorsEventProducer(
            kafka_producer, args.kafka_topic_sensors,
        ) if sub_tms or sub_weather else None

        messages_prod = FiDigitrafficRoadMessagesEventProducer(
            kafka_producer, args.kafka_topic_messages,
        ) if sub_messages else None

        maintenance_prod = FiDigitrafficRoadMaintenanceEventProducer(
            kafka_producer, args.kafka_topic_maintenance,
        ) if sub_maintenance else None

        stations_prod = FiDigitrafficRoadStationsEventProducer(
            kafka_producer, args.kafka_topic_sensors,
        ) if sub_tms or sub_weather else None

        tasks_prod = FiDigitrafficRoadMaintenanceTasksEventProducer(
            kafka_producer, args.kafka_topic_maintenance,
        ) if sub_maintenance else None

        bridge = DigitrafficRoadBridge(
            mqtt_source=mqtt_source,
            kafka_producer=kafka_producer,
            sensors_producer=sensors_prod,
            messages_producer=messages_prod,
            maintenance_producer=maintenance_prod,
            stations_producer=stations_prod,
            tasks_producer=tasks_prod,
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
    sub_tms = "tms" in subs
    sub_weather = "weather" in subs
    sub_messages = "traffic-messages" in subs
    sub_maintenance = "maintenance" in subs

    station_filter_set = None
    if args.station_filter:
        station_filter_set = set(
            int(s.strip()) for s in args.station_filter.split(",") if s.strip()
        )

    mqtt_src = MQTTSource(
        subscribe_tms=sub_tms,
        subscribe_weather=sub_weather,
        subscribe_traffic_messages=sub_messages,
        subscribe_maintenance=sub_maintenance,
        station_filter=station_filter_set,
    )

    counter: Counter = Counter()
    start = time.time()
    sample_count: Dict[str, int] = {}

    def on_message(data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        counter[data_type] += 1

        shown = sample_count.get(data_type, 0)
        if shown < 3:
            sample_count[data_type] = shown + 1
            print(f"[{data_type}] {_json.dumps(metadata)} {_json.dumps(payload)[:200]}")

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
        print(f"  Rate: {total / elapsed:.1f} msg/sec")


if __name__ == "__main__":
    main()
