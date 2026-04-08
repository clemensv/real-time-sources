"""Bridge for French national non-conceded road network real-time traffic data.

Polls two Bison Futé DATEX II XML endpoints:
  - Traffic flow measurements (vehicle counts and speeds)
  - Road events / situations (incidents, works, closures)

Emits CloudEvents to Kafka via the generated xrcg producers.
"""

import argparse
import json
import logging
import os
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from confluent_kafka import Producer

from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.trafficflowmeasurement import TrafficFlowMeasurement
from french_road_traffic_producer_data.fr.gouv.transport.bison_fute.roadevent import RoadEvent
from french_road_traffic_producer_kafka_producer.producer import (
    FrGouvTransportBisonFuteTrafficFlowEventProducer,
    FrGouvTransportBisonFuteRoadEventEventProducer,
)

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# DATEX II XML namespace
DATEX2_NS = "http://datex2.eu/schema/2/2_0"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"
SOAP_NS = "http://www.w3.org/2003/05/soap-envelope"

TRAFFIC_FLOW_URL = (
    "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/QTV-DIR/qtvDir.xml"
)
ROAD_EVENTS_URL = (
    "http://tipi.bison-fute.gouv.fr/bison-fute-ouvert/publicationsDIR/Evenementiel-DIR/grt/RRN/content.xml"
)

FEED_SOURCE_FLOW = "https://transport.data.gouv.fr/datasets/etat-de-circulation-en-temps-reel-sur-le-reseau-national-routier-non-concede"
FEED_SOURCE_EVENTS = "https://transport.data.gouv.fr/datasets/evenements-routiers-sur-le-reseau-routier-national-non-concede"


def _find(element: ET.Element, path: str, ns: Optional[str] = DATEX2_NS) -> Optional[ET.Element]:
    """Find a child element with namespace."""
    if ns:
        return element.find(path.replace("/", f"/{{{ns}}}").replace("//", f"//{{{ns}}}") if "/" in path else f"{{{ns}}}{path}")
    return element.find(path)


def _findall(element: ET.Element, path: str, ns: Optional[str] = DATEX2_NS) -> List[ET.Element]:
    """Find all child elements with namespace."""
    if ns:
        return element.findall(path.replace("/", f"/{{{ns}}}").replace("//", f"//{{{ns}}}") if "/" in path else f"{{{ns}}}{path}")
    return element.findall(path)


def _text(element: ET.Element, path: str, ns: Optional[str] = DATEX2_NS) -> Optional[str]:
    """Get text content of a child element."""
    el = _find(element, path, ns)
    return el.text if el is not None else None


def parse_traffic_flow_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    """Parse DATEX II MeasuredDataPublication XML into traffic flow records."""
    root = ET.fromstring(xml_bytes)
    results = []

    payload = _find(root, "payloadPublication")
    if payload is None:
        return results

    for site_meas in _findall(payload, "siteMeasurements"):
        site_ref = _find(site_meas, "measurementSiteReference")
        site_id = site_ref.get("id", "") if site_ref is not None else ""
        meas_time = _text(site_meas, "measurementTimeDefault")

        if not site_id or not meas_time:
            continue

        flow_rate = None
        avg_speed = None
        input_flow = None
        input_speed = None

        for mv in _findall(site_meas, "measuredValue"):
            inner = _find(mv, "measuredValue")
            if inner is None:
                continue
            basic_data = _find(inner, "basicData")
            if basic_data is None:
                continue

            xsi_type = basic_data.get(f"{{{XSI_NS}}}type", "")

            if "TrafficFlow" in xsi_type:
                vf = _find(basic_data, "vehicleFlow")
                if vf is not None:
                    rate_text = _text(vf, "vehicleFlowRate")
                    if rate_text is not None:
                        try:
                            flow_rate = int(rate_text)
                        except (ValueError, TypeError):
                            pass
                    niv = vf.get("numberOfInputValuesUsed")
                    if niv is not None:
                        try:
                            input_flow = int(niv)
                        except (ValueError, TypeError):
                            pass

            elif "TrafficSpeed" in xsi_type:
                avs = _find(basic_data, "averageVehicleSpeed")
                if avs is not None:
                    speed_text = _text(avs, "speed")
                    if speed_text is not None:
                        try:
                            avg_speed = float(speed_text)
                        except (ValueError, TypeError):
                            pass
                    niv = avs.get("numberOfInputValuesUsed")
                    if niv is not None:
                        try:
                            input_speed = int(niv)
                        except (ValueError, TypeError):
                            pass

        results.append({
            "site_id": site_id,
            "measurement_time": meas_time,
            "vehicle_flow_rate": flow_rate,
            "average_speed": avg_speed,
            "input_values_flow": input_flow,
            "input_values_speed": input_speed,
        })

    return results


def _extract_ns2_text(element: ET.Element, local_name: str) -> Optional[str]:
    """Extract text from an ns2-prefixed element (road events use ns2: namespace)."""
    el = element.find(f"{{{DATEX2_NS}}}{local_name}")
    return el.text if el is not None else None


def _extract_comments(record: ET.Element) -> Tuple[Optional[str], Optional[str]]:
    """Extract description and location comments from generalPublicComment elements."""
    description = None
    location_parts = []

    for comment_elem in _findall(record, "generalPublicComment"):
        comment_type_el = _find(comment_elem, "commentType")
        comment_type = comment_type_el.text if comment_type_el is not None else ""

        value_el = comment_elem.find(f".//{{{DATEX2_NS}}}value")
        value_text = value_el.text if value_el is not None else None

        if comment_type == "description" and value_text:
            description = value_text
        elif comment_type == "locationDescriptor" and value_text:
            location_parts.append(value_text)

    location_description = " | ".join(location_parts) if location_parts else None
    return description, location_description


def _extract_location(record: ET.Element) -> Tuple[Optional[float], Optional[float], Optional[str], Optional[str], Optional[str]]:
    """Extract lat, lon, road_number, town_name, direction from location elements."""
    latitude = None
    longitude = None
    road_number = None
    town_name = None
    direction = None

    group = _find(record, "groupOfLocations")
    if group is None:
        return latitude, longitude, road_number, town_name, direction

    # Try to find coordinates
    coords = group.find(f".//{{{DATEX2_NS}}}pointCoordinates")
    if coords is not None:
        lat_text = _extract_ns2_text(coords, "latitude")
        lon_text = _extract_ns2_text(coords, "longitude")
        if lat_text:
            try:
                latitude = float(lat_text)
            except (ValueError, TypeError):
                pass
        if lon_text:
            try:
                longitude = float(lon_text)
            except (ValueError, TypeError):
                pass

    # Extract road number from linearElement or tpeg descriptor
    road_el = group.find(f".//{{{DATEX2_NS}}}roadNumber")
    if road_el is not None and road_el.text:
        road_number = road_el.text

    # Extract direction
    dir_el = group.find(f".//{{{DATEX2_NS}}}tpegDirection")
    if dir_el is not None and dir_el.text:
        direction = dir_el.text

    # Extract town name from tpeg descriptors
    for name_el in group.findall(f".//{{{DATEX2_NS}}}name"):
        desc_type_el = _find(name_el, "tpegOtherPointDescriptorType")
        if desc_type_el is not None and desc_type_el.text == "townName":
            value_el = name_el.find(f".//{{{DATEX2_NS}}}value")
            if value_el is not None and value_el.text:
                town_name = value_el.text
                break
        # Also check for linkName if no road_number yet
        if road_number is None and desc_type_el is not None and desc_type_el.text == "linkName":
            value_el = name_el.find(f".//{{{DATEX2_NS}}}value")
            if value_el is not None and value_el.text:
                road_number = value_el.text

    return latitude, longitude, road_number, town_name, direction


def parse_road_events_xml(xml_bytes: bytes) -> List[Dict[str, Any]]:
    """Parse DATEX II SituationPublication XML into road event records."""
    results = []

    root = ET.fromstring(xml_bytes)

    # The road events XML is wrapped in SOAP envelope
    body = root.find(f"{{{SOAP_NS}}}Body")
    if body is not None:
        model = body.find(f"d2LogicalModel")
        if model is None:
            model = body.find(f"{{{DATEX2_NS}}}d2LogicalModel")
            if model is None:
                # Try without namespace prefix
                for child in body:
                    if "d2LogicalModel" in child.tag:
                        model = child
                        break
    else:
        model = root

    if model is None:
        return results

    payload = _find(model, "payloadPublication")
    if payload is None:
        # Try ns2 prefix style
        for child in model:
            if "payloadPublication" in child.tag:
                payload = child
                break
    if payload is None:
        return results

    for situation in _findall(payload, "situation"):
        sit_id = situation.get("id", "")
        sit_version = situation.get("version", "")
        severity = _extract_ns2_text(situation, "overallSeverity")

        for record in _findall(situation, "situationRecord"):
            record_id = record.get("id", "")
            record_version = record.get("version", sit_version)
            record_type_raw = record.get(f"{{{XSI_NS}}}type", "")
            # Strip namespace prefix if present (e.g. "ns2:Accident" -> "Accident")
            record_type = record_type_raw.split(":")[-1] if ":" in record_type_raw else record_type_raw

            creation_time = _extract_ns2_text(record, "situationRecordCreationTime") or ""
            observation_time = _extract_ns2_text(record, "situationRecordObservationTime")
            probability = _extract_ns2_text(record, "probabilityOfOccurrence")

            # Source
            source_el = _find(record, "source")
            source_name = None
            if source_el is not None:
                source_name = _extract_ns2_text(source_el, "sourceIdentification")

            # Validity
            validity_el = _find(record, "validity")
            validity_status = None
            overall_start_time = None
            overall_end_time = None
            if validity_el is not None:
                validity_status = _extract_ns2_text(validity_el, "validityStatus")
                time_spec = _find(validity_el, "validityTimeSpecification")
                if time_spec is not None:
                    overall_start_time = _extract_ns2_text(time_spec, "overallStartTime")
                    overall_end_time = _extract_ns2_text(time_spec, "overallEndTime")

            description, location_description = _extract_comments(record)
            latitude, longitude, road_number, town_name, direction = _extract_location(record)

            if not sit_id or not record_id or not creation_time:
                continue

            results.append({
                "situation_id": sit_id,
                "record_id": record_id,
                "version": sit_version,
                "severity": severity,
                "record_type": record_type,
                "probability": probability,
                "latitude": latitude,
                "longitude": longitude,
                "road_number": road_number,
                "town_name": town_name,
                "direction": direction,
                "description": description,
                "location_description": location_description,
                "source_name": source_name,
                "validity_status": validity_status,
                "overall_start_time": overall_start_time,
                "overall_end_time": overall_end_time,
                "creation_time": creation_time,
                "observation_time": observation_time,
            })

    return results


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse Event Hubs / Fabric / plain Kafka connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                config_dict["kafka_topic"] = part.split("=")[1].strip('"').strip()
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


def fetch_xml(session: requests.Session, url: str, timeout: int = 60) -> bytes:
    """Fetch XML from URL, returning raw bytes."""
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def run_bridge(
    kafka_config: Dict[str, str],
    topic_flow: str,
    topic_events: str,
    polling_interval: int,
    flow_url: str = TRAFFIC_FLOW_URL,
    events_url: str = ROAD_EVENTS_URL,
) -> None:
    """Main polling loop: fetch DATEX II XML, parse, emit CloudEvents."""
    producer = Producer(kafka_config)
    flow_producer = FrGouvTransportBisonFuteTrafficFlowEventProducer(producer, topic_flow)
    event_producer = FrGouvTransportBisonFuteRoadEventEventProducer(producer, topic_events)
    session = requests.Session()

    logger.info(
        "Starting French Road Traffic bridge — flow topic=%s, events topic=%s, interval=%ds",
        topic_flow, topic_events, polling_interval,
    )

    while True:
        try:
            start = datetime.now(timezone.utc)
            flow_count = 0
            event_count = 0

            # --- Traffic flow ---
            try:
                flow_xml = fetch_xml(session, flow_url)
                measurements = parse_traffic_flow_xml(flow_xml)
                for m in measurements:
                    flow_producer.send_fr_gouv_transport_bison_fute_traffic_flow_measurement(
                        _feedurl=FEED_SOURCE_FLOW,
                        _site_id=m["site_id"],
                        data=TrafficFlowMeasurement(
                            site_id=m["site_id"],
                            measurement_time=m["measurement_time"],
                            vehicle_flow_rate=m["vehicle_flow_rate"],
                            average_speed=m["average_speed"],
                            input_values_flow=m["input_values_flow"],
                            input_values_speed=m["input_values_speed"],
                        ),
                        flush_producer=False,
                    )
                    flow_count += 1
            except Exception as exc:
                logger.error("Error fetching/parsing traffic flow: %s", exc)

            # --- Road events ---
            try:
                events_xml = fetch_xml(session, events_url)
                events = parse_road_events_xml(events_xml)
                for ev in events:
                    event_producer.send_fr_gouv_transport_bison_fute_road_event(
                        _feedurl=FEED_SOURCE_EVENTS,
                        _situation_id=ev["situation_id"],
                        data=RoadEvent(
                            situation_id=ev["situation_id"],
                            record_id=ev["record_id"],
                            version=ev["version"],
                            severity=ev["severity"],
                            record_type=ev["record_type"],
                            probability=ev["probability"],
                            latitude=ev["latitude"],
                            longitude=ev["longitude"],
                            road_number=ev["road_number"],
                            town_name=ev["town_name"],
                            direction=ev["direction"],
                            description=ev["description"],
                            location_description=ev["location_description"],
                            source_name=ev["source_name"],
                            validity_status=ev["validity_status"],
                            overall_start_time=ev["overall_start_time"],
                            overall_end_time=ev["overall_end_time"],
                            creation_time=ev["creation_time"],
                            observation_time=ev["observation_time"],
                        ),
                        flush_producer=False,
                    )
                    event_count += 1
            except Exception as exc:
                logger.error("Error fetching/parsing road events: %s", exc)

            producer.flush()
            elapsed = (datetime.now(timezone.utc) - start).total_seconds()
            logger.info(
                "Emitted %d flow measurements + %d road events in %.1fs",
                flow_count, event_count, elapsed,
            )

            remaining = max(0, polling_interval - elapsed)
            if remaining > 0:
                time.sleep(remaining)

        except KeyboardInterrupt:
            logger.info("Shutting down...")
            break
        except Exception as exc:
            logger.error("Unexpected error: %s", exc)
            logger.info("Retrying in %ds...", polling_interval)
            time.sleep(polling_interval)

    producer.flush()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="French Road Traffic bridge — real-time DATEX II data to Kafka"
    )
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start the polling bridge")
    feed_parser.add_argument(
        "--kafka-bootstrap-servers", type=str,
        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    )
    feed_parser.add_argument(
        "--kafka-topic-flow", type=str,
        default=os.getenv("KAFKA_TOPIC_FLOW", "french-road-traffic-flow"),
    )
    feed_parser.add_argument(
        "--kafka-topic-events", type=str,
        default=os.getenv("KAFKA_TOPIC_EVENTS", "french-road-traffic-events"),
    )
    feed_parser.add_argument(
        "--sasl-username", type=str, default=os.getenv("SASL_USERNAME"),
    )
    feed_parser.add_argument(
        "--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"),
    )
    feed_parser.add_argument(
        "-c", "--connection-string", type=str,
        default=os.getenv("CONNECTION_STRING"),
    )
    polling_default = int(os.getenv("POLLING_INTERVAL", "360"))
    feed_parser.add_argument(
        "-i", "--polling-interval", type=int, default=polling_default,
        help="Polling interval in seconds (default: 360)",
    )

    args = parser.parse_args()

    if args.command == "feed":
        if args.connection_string:
            config = parse_connection_string(args.connection_string)
            bootstrap = config.get("bootstrap.servers")
            topic_from_cs = config.get("kafka_topic")
            sasl_user = config.get("sasl.username")
            sasl_pass = config.get("sasl.password")
        else:
            bootstrap = args.kafka_bootstrap_servers
            topic_from_cs = None
            sasl_user = args.sasl_username
            sasl_pass = args.sasl_password

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or CONNECTION_STRING).")
            sys.exit(1)

        topic_flow = args.kafka_topic_flow
        topic_events = args.kafka_topic_events
        # If connection string provided an EntityPath, use it for both topics
        if topic_from_cs:
            topic_flow = topic_from_cs
            topic_events = topic_from_cs

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        kafka_config: Dict[str, str] = {"bootstrap.servers": bootstrap}

        if sasl_user and sasl_pass:
            kafka_config.update({
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_user,
                "sasl.password": sasl_pass,
            })
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"

        run_bridge(kafka_config, topic_flow, topic_events, args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
