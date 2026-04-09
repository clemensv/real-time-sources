"""Australian State Wildfires Bridge — fetches live bushfire incidents from NSW RFS, VicEmergency, and QLD Fire Department."""

import argparse
import json
import sys
import os
import time
import re
import typing
import logging
import hashlib
import requests
from datetime import datetime, timezone

from confluent_kafka import Producer

from australia_wildfires_producer_kafka_producer.producer import AUGovEmergencyWildfiresEventProducer
from australia_wildfires_producer_data import FireIncident

logger = logging.getLogger(__name__)

NSW_RFS_URL = "https://www.rfs.nsw.gov.au/feeds/majorIncidents.json"
VIC_EMERGENCY_URL = "https://www.emergency.vic.gov.au/public/osom-geojson.json"
QLD_FIRE_URL = "https://publiccontent-gis-psba-qld-gov-au.s3.amazonaws.com/content/Feeds/BushfireCurrentIncidents/bushfireAlert.json"

# Regex to parse key-value pairs from the NSW RFS HTML description field
NSW_DESC_PATTERN = re.compile(
    r"(?:ALERT LEVEL|LOCATION|COUNCIL AREA|STATUS|TYPE|FIRE|SIZE|RESPONSIBLE AGENCY|UPDATED)\s*:\s*([^<]+?)(?:<br\s*/?>|$)",
    re.IGNORECASE,
)
NSW_FIELD_PATTERN = re.compile(
    r"(ALERT LEVEL|LOCATION|COUNCIL AREA|STATUS|TYPE|FIRE|SIZE|RESPONSIBLE AGENCY|UPDATED)\s*:\s*([^<]+?)(?:\s*<br\s*/?>|$)",
    re.IGNORECASE,
)


def _parse_nsw_description(description: str) -> dict[str, str]:
    """Parse structured fields from the NSW RFS HTML description string."""
    fields: dict[str, str] = {}
    for match in NSW_FIELD_PATTERN.finditer(description):
        key = match.group(1).strip().upper()
        value = match.group(2).strip()
        fields[key] = value
    return fields


def _extract_point_from_geometry(geometry: typing.Optional[dict]) -> tuple[typing.Optional[float], typing.Optional[float]]:
    """Extract latitude and longitude from a GeoJSON geometry.

    Handles Point, Polygon, MultiPolygon, and GeometryCollection types.
    Returns (latitude, longitude) or (None, None) if no coordinates found.
    """
    if not geometry:
        return None, None

    geo_type = geometry.get("type", "")
    coordinates = geometry.get("coordinates")

    if geo_type == "Point" and coordinates and len(coordinates) >= 2:
        return coordinates[1], coordinates[0]

    if geo_type == "Polygon" and coordinates and len(coordinates) > 0:
        return _polygon_centroid(coordinates[0])

    if geo_type == "MultiPolygon" and coordinates and len(coordinates) > 0:
        # Use the first polygon's outer ring
        return _polygon_centroid(coordinates[0][0])

    if geo_type == "GeometryCollection":
        geometries = geometry.get("geometries", [])
        # Prefer Point geometry
        for g in geometries:
            if g.get("type") == "Point":
                coords = g.get("coordinates", [])
                if len(coords) >= 2:
                    return coords[1], coords[0]
        # Fall back to first polygon
        for g in geometries:
            lat, lon = _extract_point_from_geometry(g)
            if lat is not None:
                return lat, lon

    return None, None


def _polygon_centroid(ring: list[list[float]]) -> tuple[typing.Optional[float], typing.Optional[float]]:
    """Compute the centroid of a polygon ring as the average of its vertices."""
    if not ring:
        return None, None
    lats = [p[1] for p in ring if len(p) >= 2]
    lons = [p[0] for p in ring if len(p) >= 2]
    if not lats or not lons:
        return None, None
    return sum(lats) / len(lats), sum(lons) / len(lons)


def _incident_id_from_guid(guid: str) -> str:
    """Extract a numeric incident ID from an NSW RFS GUID URL."""
    # e.g. https://incidents.rfs.nsw.gov.au/api/v1/incidents/653509
    parts = guid.rstrip("/").split("/")
    if parts:
        return parts[-1]
    return hashlib.md5(guid.encode()).hexdigest()[:12]


def _parse_size_hectares(size_str: str) -> typing.Optional[float]:
    """Parse a size string like '150 ha' into a float."""
    if not size_str:
        return None
    cleaned = size_str.lower().replace("ha", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def _parse_nsw_updated(updated_str: str) -> str:
    """Parse the NSW UPDATED field (e.g. '9 Apr 2026 00:08') to ISO 8601 UTC."""
    for fmt in ("%d %b %Y %H:%M", "%d/%m/%Y %I:%M:%S %p", "%d %b %Y %H:%M:%S"):
        try:
            dt = datetime.strptime(updated_str.strip(), fmt)
            return dt.replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return datetime.now(timezone.utc).isoformat()


class AustraliaWildfiresAPI:
    """Client for fetching bushfire incident data from Australian state fire services."""

    def __init__(self, polling_interval: int = 300):
        self.polling_interval = polling_interval
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "real-time-sources-australia-wildfires-bridge/1.0"})

    def fetch_nsw_incidents(self) -> list[FireIncident]:
        """Fetch and parse fire incidents from NSW Rural Fire Service."""
        try:
            response = self.session.get(NSW_RFS_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.warning("Failed to fetch NSW RFS data: %s", e)
            return []

        incidents: list[FireIncident] = []
        for feature in data.get("features", []):
            try:
                incident = self._parse_nsw_feature(feature)
                if incident:
                    incidents.append(incident)
            except Exception as e:
                logger.debug("Failed to parse NSW feature: %s", e)
        return incidents

    def fetch_vic_incidents(self) -> list[FireIncident]:
        """Fetch and parse fire incidents from VicEmergency."""
        try:
            response = self.session.get(VIC_EMERGENCY_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.warning("Failed to fetch VicEmergency data: %s", e)
            return []

        incidents: list[FireIncident] = []
        for feature in data.get("features", []):
            try:
                props = feature.get("properties", {})
                # Filter for fire events
                category2 = (props.get("category2") or "").lower()
                cap = props.get("cap", {}) or {}
                cap_category = (cap.get("category") or "").lower()
                if "fire" not in category2 and "fire" not in cap_category:
                    continue
                incident = self._parse_vic_feature(feature)
                if incident:
                    incidents.append(incident)
            except Exception as e:
                logger.debug("Failed to parse VIC feature: %s", e)
        return incidents

    def fetch_qld_incidents(self) -> list[FireIncident]:
        """Fetch and parse fire incidents from Queensland Fire Department."""
        try:
            response = self.session.get(QLD_FIRE_URL, timeout=30)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.warning("Failed to fetch QLD Fire data: %s", e)
            return []

        incidents: list[FireIncident] = []
        for feature in data.get("features", []):
            try:
                incident = self._parse_qld_feature(feature)
                if incident:
                    incidents.append(incident)
            except Exception as e:
                logger.debug("Failed to parse QLD feature: %s", e)
        return incidents

    @staticmethod
    def _parse_nsw_feature(feature: dict) -> typing.Optional[FireIncident]:
        """Parse a single NSW RFS GeoJSON feature into a FireIncident."""
        props = feature.get("properties", {})
        geometry = feature.get("geometry")

        title = props.get("title", "")
        guid = props.get("guid", "")
        if not guid:
            return None

        incident_id = _incident_id_from_guid(guid)
        desc_fields = _parse_nsw_description(props.get("description", ""))
        lat, lon = _extract_point_from_geometry(geometry)

        alert_level = props.get("category", desc_fields.get("ALERT LEVEL", "Unknown"))
        status = desc_fields.get("STATUS")
        location = desc_fields.get("LOCATION")
        fire_type = desc_fields.get("TYPE")
        responsible_agency = desc_fields.get("RESPONSIBLE AGENCY")
        size_str = desc_fields.get("SIZE", "")
        size_hectares = _parse_size_hectares(size_str)

        updated_str = desc_fields.get("UPDATED", "")
        updated = _parse_nsw_updated(updated_str) if updated_str else datetime.now(timezone.utc).isoformat()

        source_url = guid if guid.startswith("http") else f"https://www.rfs.nsw.gov.au/fire-information/fires-near-me"

        return FireIncident(
            incident_id=incident_id,
            state="NSW",
            title=title,
            alert_level=alert_level,
            status=status,
            location=location,
            latitude=lat,
            longitude=lon,
            size_hectares=size_hectares,
            type=fire_type,
            responsible_agency=responsible_agency,
            updated=updated,
            source_url=source_url,
        )

    @staticmethod
    def _parse_vic_feature(feature: dict) -> typing.Optional[FireIncident]:
        """Parse a single VicEmergency GeoJSON feature into a FireIncident."""
        props = feature.get("properties", {})
        geometry = feature.get("geometry")

        source_id = props.get("sourceId") or props.get("id")
        if not source_id:
            return None

        cap = props.get("cap", {}) or {}
        lat, lon = _extract_point_from_geometry(geometry)

        name = props.get("sourceTitle") or props.get("name") or ""
        alert_level = props.get("category1") or props.get("action") or "Unknown"
        status = props.get("status")
        location = props.get("location")
        fire_type = cap.get("event")
        responsible_agency = cap.get("senderName")

        size_hectares = None
        size_fmt = props.get("sizeFmt")
        if size_fmt:
            size_hectares = _parse_size_hectares(size_fmt)

        updated_str = props.get("updated") or props.get("created", "")
        if updated_str:
            try:
                updated = datetime.fromisoformat(updated_str).astimezone(timezone.utc).isoformat()
            except (ValueError, TypeError):
                updated = datetime.now(timezone.utc).isoformat()
        else:
            updated = datetime.now(timezone.utc).isoformat()

        source_url = f"http://emergency.vic.gov.au/respond/#!/warning/{source_id}/moreinfo"

        return FireIncident(
            incident_id=str(source_id),
            state="VIC",
            title=name,
            alert_level=alert_level,
            status=status,
            location=location,
            latitude=lat,
            longitude=lon,
            size_hectares=size_hectares,
            type=fire_type,
            responsible_agency=responsible_agency,
            updated=updated,
            source_url=source_url,
        )

    @staticmethod
    def _parse_qld_feature(feature: dict) -> typing.Optional[FireIncident]:
        """Parse a single QLD Fire Department GeoJSON feature into a FireIncident."""
        props = feature.get("properties", {})
        geometry = feature.get("geometry")

        unique_id = props.get("UniqueID")
        if not unique_id:
            return None

        lat, lon = _extract_point_from_geometry(geometry)

        title = props.get("WarningTitle", "")
        alert_level = props.get("WarningLevel", "Unknown")
        header = props.get("Header", "")
        call_to_action = props.get("CallToAction", "")

        # Derive location from the header or title
        location = header if header else None

        # Derive fire type from CallToAction
        fire_type = None
        if call_to_action:
            cta_lower = call_to_action.lower()
            if "hazard reduction" in cta_lower:
                fire_type = "Hazard Reduction"
            elif "bushfire" in cta_lower or "bush fire" in cta_lower:
                fire_type = "Bush Fire"
            elif "grass fire" in cta_lower:
                fire_type = "Grass Fire"
            elif "structure fire" in cta_lower:
                fire_type = "Structure Fire"
            elif "smoke" in cta_lower:
                fire_type = "Smoke Alert"
            else:
                fire_type = call_to_action

        updated = datetime.now(timezone.utc).isoformat()

        return FireIncident(
            incident_id=str(unique_id),
            state="QLD",
            title=title,
            alert_level=alert_level,
            status=None,
            location=location,
            latitude=lat,
            longitude=lon,
            size_hectares=None,
            type=fire_type,
            responsible_agency="Queensland Fire Department",
            updated=updated,
            source_url=QLD_FIRE_URL,
        )


def parse_connection_string(connection_string: str) -> dict:
    """Parse a Kafka connection string into a config dict."""
    config: dict[str, str] = {}
    for part in connection_string.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key == "Endpoint":
                config["bootstrap.servers"] = value.replace("sb://", "").rstrip("/") + ":9093"
            elif key == "SharedAccessKeyName":
                config["sasl.username"] = "$ConnectionString"
            elif key == "SharedAccessKey":
                config["sasl.password"] = connection_string
            elif key == "BootstrapServer":
                config["bootstrap.servers"] = value
            elif key == "EntityPath":
                config["_entity_path"] = value
    if "sasl.username" in config:
        config["security.protocol"] = "SASL_SSL"
        config["sasl.mechanism"] = "PLAIN"
    return config


def _load_state(state_file: str) -> dict[str, str]:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict[str, str]) -> None:
    """Save dedup state to a JSON file, keeping at most 50000 entries."""
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


def feed_incidents(
    api: AustraliaWildfiresAPI,
    producer: AUGovEmergencyWildfiresEventProducer,
    previous: dict[str, str],
) -> int:
    """Fetch incidents from all three states and emit new or updated ones."""
    all_incidents: list[FireIncident] = []
    all_incidents.extend(api.fetch_nsw_incidents())
    all_incidents.extend(api.fetch_vic_incidents())
    all_incidents.extend(api.fetch_qld_incidents())

    sent = 0
    for incident in all_incidents:
        dedup_key = f"{incident.state}/{incident.incident_id}"
        if previous.get(dedup_key) == incident.updated:
            continue
        producer.send_au_gov_emergency_wildfires_fire_incident(
            incident.state,
            incident.incident_id,
            incident,
            flush_producer=False,
        )
        previous[dedup_key] = incident.updated
        sent += 1

    producer.producer.flush()
    return sent


def main():
    """Main entry point for the Australian Wildfires bridge."""
    parser = argparse.ArgumentParser(description="Australian State Wildfires Bridge")
    parser.add_argument("--connection-string", required=False,
                        help="Kafka/Event Hubs connection string",
                        default=os.environ.get("KAFKA_CONNECTION_STRING") or os.environ.get("CONNECTION_STRING"))
    parser.add_argument("--topic", required=False,
                        help="Kafka topic",
                        default=os.environ.get("KAFKA_TOPIC") or None)
    parser.add_argument("--polling-interval", type=int,
                        default=int(os.environ.get("POLLING_INTERVAL", "300")),
                        help="Polling interval in seconds (default: 300)")
    parser.add_argument("--state-file", type=str,
                        default=os.environ.get("STATE_FILE",
                                               os.path.expanduser("~/.australia_wildfires_state.json")))
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("list", help="List current incidents")
    subparsers.add_parser("feed", help="Feed data to Kafka")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    api = AustraliaWildfiresAPI(polling_interval=args.polling_interval)

    if args.command == "list":
        for state_name, fetch_fn in [("NSW", api.fetch_nsw_incidents),
                                      ("VIC", api.fetch_vic_incidents),
                                      ("QLD", api.fetch_qld_incidents)]:
            incidents = fetch_fn()
            print(f"\n--- {state_name}: {len(incidents)} incidents ---")
            for inc in incidents:
                print(f"  {inc.incident_id}: {inc.title} [{inc.alert_level}] ({inc.location})")
    elif args.command == "feed":
        if not args.connection_string:
            if not os.environ.get("KAFKA_BROKER"):
                print("Error: --connection-string or KAFKA_BROKER environment variable required for feed mode")
                sys.exit(1)
            kafka_config: dict[str, str] = {"bootstrap.servers": os.environ["KAFKA_BROKER"]}
        else:
            kafka_config = parse_connection_string(args.connection_string)
        if "_entity_path" in kafka_config and not args.topic:
            args.topic = kafka_config.pop("_entity_path")
        elif "_entity_path" in kafka_config:
            kafka_config.pop("_entity_path")
        if not args.topic:
            args.topic = "australia-wildfires"
        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        if "sasl.username" in kafka_config:
            kafka_config["security.protocol"] = "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT"
        kafka_config["client.id"] = "australia-wildfires-bridge"
        kafka_producer = Producer(kafka_config)
        event_producer = AUGovEmergencyWildfiresEventProducer(kafka_producer, args.topic)
        logger.info("Starting Australian Wildfires bridge, polling every %d seconds", args.polling_interval)
        state = _load_state(args.state_file)
        while True:
            try:
                count = feed_incidents(api, event_producer, state)
                _save_state(args.state_file, state)
                logger.info("Sent %d fire incident events", count)
            except Exception as e:
                logger.error("Error fetching/sending data: %s", e)
            time.sleep(args.polling_interval)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
