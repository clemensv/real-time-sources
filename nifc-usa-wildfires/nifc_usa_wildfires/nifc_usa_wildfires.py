"""
NIFC USA Wildfires Data Poller
Polls the National Interagency Fire Center (NIFC) ArcGIS Feature Service for
active wildfire incident data and sends events to a Kafka topic.
"""

import os
import json
import sys
import asyncio
import aiohttp
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
import argparse
from urllib.parse import quote
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from nifc_usa_wildfires_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident
from nifc_usa_wildfires_producer_kafka_producer.producer import GovNIFCWildfiresEventProducer
# pylint: enable=import-error, line-too-long


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

BASE_URL = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer/0/query"
SOURCE_URI = "https://services9.arcgis.com/RHVPKKiFTONKtxq3/arcgis/rest/services/USA_Wildfires_v1/FeatureServer/0"
MAX_RECORD_COUNT = 2000
POLL_INTERVAL_MINUTES = 5


def epoch_ms_to_iso(epoch_ms: Optional[int]) -> Optional[str]:
    """Convert ArcGIS epoch milliseconds to ISO 8601 string."""
    if epoch_ms is None:
        return None
    return datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc).isoformat()


def build_query_url(where_clause: str = "1=1", result_offset: int = 0,
                    result_record_count: int = MAX_RECORD_COUNT) -> str:
    """Build the ArcGIS Feature Service query URL."""
    return (
        f"{BASE_URL}?"
        f"where={quote(where_clause)}"
        f"&outFields=*"
        f"&f=geojson"
        f"&resultRecordCount={result_record_count}"
        f"&resultOffset={result_offset}"
    )


class NIFCWildfirePoller:
    """Polls the NIFC ArcGIS Feature Service for active wildfire incidents."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: Optional[str] = None,
                 last_polled_file: Optional[str] = None,
                 poll_interval_minutes: int = POLL_INTERVAL_MINUTES):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.poll_interval = timedelta(minutes=poll_interval_minutes)
        self.event_producer: Optional[GovNIFCWildfiresEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = GovNIFCWildfiresEventProducer(producer, kafka_topic)

    async def fetch_incidents(self, where_clause: str = "1=1") -> List[Dict[str, Any]]:
        """Fetch wildfire incidents from the ArcGIS Feature Service, paging through all results."""
        all_features: List[Dict[str, Any]] = []
        offset = 0
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            while True:
                url = build_query_url(where_clause, offset)
                try:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.json()
                except aiohttp.ClientError as e:
                    logger.error("HTTP error fetching incidents: %s", e)
                    break
                except asyncio.TimeoutError:
                    logger.error("Timeout fetching incidents at offset %d", offset)
                    break

                features = data.get("features", [])
                all_features.extend(features)

                exceeded = data.get("properties", {}).get("exceededTransferLimit", False)
                if exceeded and len(features) > 0:
                    offset += len(features)
                else:
                    break

        return all_features

    def parse_incident(self, feature: Dict[str, Any]) -> Optional[WildfireIncident]:
        """Parse a GeoJSON feature into a WildfireIncident dataclass."""
        props = feature.get("properties", {})
        geometry = feature.get("geometry")

        irwin_id = props.get("IrwinID")
        if not irwin_id:
            return None

        incident_name = props.get("IncidentName", "")
        if not incident_name:
            return None

        # Extract coordinates from geometry
        latitude = None
        longitude = None
        if geometry and geometry.get("type") == "Point":
            coords = geometry.get("coordinates", [])
            if len(coords) >= 2:
                longitude = coords[0]
                latitude = coords[1]

        modified_on_ms = props.get("ModifiedOnDateTime")
        modified_on_datetime = epoch_ms_to_iso(modified_on_ms)
        if modified_on_datetime is None:
            modified_on_datetime = datetime.now(timezone.utc).isoformat()

        return WildfireIncident(
            irwin_id=irwin_id,
            incident_name=incident_name,
            unique_fire_identifier=props.get("UniqueFireIdentifier"),
            incident_type_category=props.get("IncidentTypeCategory"),
            incident_type_kind=props.get("IncidentTypeKind"),
            fire_discovery_datetime=epoch_ms_to_iso(props.get("FireDiscoveryDateTime")),
            daily_acres=props.get("DailyAcres"),
            calculated_acres=props.get("CalculatedAcres"),
            discovery_acres=props.get("DiscoveryAcres"),
            percent_contained=props.get("PercentContained"),
            poo_state=props.get("POOState"),
            poo_county=props.get("POOCounty"),
            latitude=latitude,
            longitude=longitude,
            fire_cause=props.get("FireCause"),
            fire_cause_general=props.get("FireCauseGeneral"),
            gacc=props.get("GACC"),
            total_incident_personnel=props.get("TotalIncidentPersonnel"),
            incident_management_organization=props.get("IncidentManagementOrganization"),
            fire_mgmt_complexity=props.get("FireMgmtComplexity"),
            residences_destroyed=props.get("ResidencesDestroyed"),
            other_structures_destroyed=props.get("OtherStructuresDestroyed"),
            injuries=props.get("Injuries"),
            fatalities=props.get("Fatalities"),
            containment_datetime=epoch_ms_to_iso(props.get("ContainmentDateTime")),
            control_datetime=epoch_ms_to_iso(props.get("ControlDateTime")),
            fire_out_datetime=epoch_ms_to_iso(props.get("FireOutDateTime")),
            final_acres=props.get("FinalAcres"),
            modified_on_datetime=modified_on_datetime,
        )

    def load_seen_ids(self) -> Dict[str, str]:
        """Load previously seen incident IDs and their modified timestamps."""
        if self.last_polled_file and os.path.exists(self.last_polled_file):
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error("Error decoding last polled file")
                    return {}
        return {}

    def save_seen_ids(self, seen_ids: Dict[str, str]):
        """Save seen incident IDs and modified timestamps to file."""
        if self.last_polled_file:
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(seen_ids, f)

    async def poll_and_send(self):
        """Continuously poll the NIFC wildfire feed and send new/updated incidents to Kafka."""
        seen_ids = self.load_seen_ids()

        while True:
            start_poll_time = datetime.now(timezone.utc)

            # Build where clause for incremental polling
            where_clause = "1=1"

            features = await self.fetch_incidents(where_clause)
            count_new = 0
            count_updated = 0

            for feature in features:
                incident = self.parse_incident(feature)
                if incident is None:
                    continue

                prev_modified = seen_ids.get(incident.irwin_id)
                if prev_modified == incident.modified_on_datetime:
                    continue

                if prev_modified is None:
                    count_new += 1
                else:
                    count_updated += 1

                self.event_producer.send_gov_nifc_wildfires_wildfire_incident(
                    _source_uri=SOURCE_URI,
                    _irwin_id=incident.irwin_id,
                    _modified_on_datetime=incident.modified_on_datetime,
                    data=incident,
                    flush_producer=False,
                )

                seen_ids[incident.irwin_id] = incident.modified_on_datetime

            self.event_producer.producer.flush()
            self.save_seen_ids(seen_ids)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated wildfire incidents", count_new, count_updated)
            else:
                logger.debug("No new wildfire incidents")

            # Prune seen IDs older than 90 days
            cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
            seen_ids = {k: v for k, v in seen_ids.items() if v >= cutoff}

            elapsed = datetime.now(timezone.utc) - start_poll_time
            remaining = self.poll_interval - elapsed
            if remaining.total_seconds() > 0:
                logger.debug("Sleeping for %s", remaining)
                await asyncio.sleep(remaining.total_seconds())


async def run_recent_incidents():
    """Fetch and print recent wildfire incidents."""
    poller = NIFCWildfirePoller()
    features = await poller.fetch_incidents()
    for feature in features:
        incident = poller.parse_incident(feature)
        if incident:
            acres_str = f"{incident.daily_acres:.0f} acres" if incident.daily_acres is not None else "? acres"
            contained_str = f"{incident.percent_contained:.0f}%" if incident.percent_contained is not None else "?%"
            print(f"{incident.incident_name} - {acres_str} - {contained_str} contained - {incident.poo_state or '?'} [{incident.irwin_id}]")


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse the connection string and extract Kafka configuration."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=', 1)[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def main():
    """Main entry point for the NIFC USA Wildfires bridge."""
    parser = argparse.ArgumentParser(description="NIFC USA Wildfires Data Poller")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    feed_parser = subparsers.add_parser('feed', help="Poll NIFC wildfire data and feed it to Kafka")
    feed_parser.add_argument('--last-polled-file', type=str,
                             help="File to store the last polled incident IDs")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic to send messages to")
    feed_parser.add_argument('--sasl-username', type=str,
                             help="Username for SASL PLAIN authentication")
    feed_parser.add_argument('--sasl-password', type=str,
                             help="Password for SASL PLAIN authentication")
    feed_parser.add_argument('--connection-string', type=str,
                             help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    feed_parser.add_argument('--poll-interval', type=int, default=POLL_INTERVAL_MINUTES,
                             help=f'Poll interval in minutes (default: {POLL_INTERVAL_MINUTES})')
    feed_parser.add_argument('--log-level', type=str,
                             help='Logging level', default='INFO')

    subparsers.add_parser('incidents', help="List recent wildfire incidents")

    args = parser.parse_args()

    if args.subcommand == 'incidents':
        asyncio.run(run_recent_incidents())
    elif args.subcommand == 'feed':
        if not args.connection_string:
            args.connection_string = os.getenv('CONNECTION_STRING')
        if not args.last_polled_file:
            args.last_polled_file = os.getenv('NIFC_LAST_POLLED_FILE')
            if not args.last_polled_file:
                args.last_polled_file = os.path.expanduser('~/.nifc_usa_wildfires_last_polled.json')
        if os.getenv('LOG_LEVEL'):
            args.log_level = os.getenv('LOG_LEVEL')
        if args.log_level:
            logger.setLevel(args.log_level)

        if args.connection_string:
            config_params = parse_connection_string(args.connection_string)
            kafka_bootstrap_servers = config_params.get('bootstrap.servers')
            kafka_topic = config_params.get('kafka_topic')
            sasl_username = config_params.get('sasl.username')
            sasl_password = config_params.get('sasl.password')
        else:
            kafka_bootstrap_servers = args.kafka_bootstrap_servers
            kafka_topic = args.kafka_topic
            sasl_username = args.sasl_username
            sasl_password = args.sasl_password

        if not kafka_bootstrap_servers:
            print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic must be provided either through the command line or connection string.")
            sys.exit(1)

        tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
        kafka_config: Dict[str, str] = {
            'bootstrap.servers': kafka_bootstrap_servers,
        }
        if sasl_username and sasl_password:
            kafka_config.update({
                'sasl.mechanisms': 'PLAIN',
                'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
                'sasl.username': sasl_username,
                'sasl.password': sasl_password
            })
        elif tls_enabled:
            kafka_config['security.protocol'] = 'SSL'

        poller = NIFCWildfirePoller(
            kafka_config=kafka_config,
            kafka_topic=kafka_topic,
            last_polled_file=args.last_polled_file,
            poll_interval_minutes=args.poll_interval,
        )

        asyncio.run(poller.poll_and_send())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
