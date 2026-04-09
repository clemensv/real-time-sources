"""
INPE TerraBrasilis DETER Deforestation Alert Poller

Polls the INPE DETER OGC WFS endpoints for Amazon and Cerrado deforestation
alerts and sends events to a Kafka topic using SASL PLAIN authentication.
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
from urllib.parse import urlencode
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from inpe_deter_brazil_producer_data.br.inpe.deter.deforestationalert import DeforestationAlert
from inpe_deter_brazil_producer_kafka_producer.producer import BRINPEDETEREventProducer
# pylint: enable=import-error, line-too-long


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

WFS_ENDPOINTS = {
    "amazon": {
        "base_url": "http://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/ows",
        "type_name": "deter-amz:deter_amz",
    },
    "cerrado": {
        "base_url": "http://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/ows",
        "type_name": "deter-cerrado:deter_cerrado",
    },
}

DEFAULT_POLL_INTERVAL_MINUTES = 10
DEFAULT_PAGE_SIZE = 1000
SOURCE_URI = "http://terrabrasilis.dpi.inpe.br"


def compute_centroid(geometry: Dict[str, Any]) -> tuple:
    """
    Compute the centroid of a GeoJSON MultiPolygon or Polygon geometry
    by averaging all coordinate points.

    Args:
        geometry: GeoJSON geometry dict with 'type' and 'coordinates'.

    Returns:
        Tuple of (latitude, longitude).
    """
    coords = geometry.get("coordinates", [])
    geo_type = geometry.get("type", "")

    all_points = []
    if geo_type == "MultiPolygon":
        for polygon in coords:
            for ring in polygon:
                all_points.extend(ring)
    elif geo_type == "Polygon":
        for ring in coords:
            all_points.extend(ring)
    else:
        return (0.0, 0.0)

    if not all_points:
        return (0.0, 0.0)

    sum_lon = sum(p[0] for p in all_points)
    sum_lat = sum(p[1] for p in all_points)
    n = len(all_points)
    return (sum_lat / n, sum_lon / n)


def build_wfs_url(biome: str, cql_filter: Optional[str] = None,
                  count: int = DEFAULT_PAGE_SIZE, start_index: int = 0) -> str:
    """
    Build a WFS GetFeature URL for the given biome.

    Args:
        biome: 'amazon' or 'cerrado'.
        cql_filter: Optional CQL filter expression.
        count: Maximum number of features to return.
        start_index: Start index for pagination.

    Returns:
        The fully constructed WFS URL.
    """
    endpoint = WFS_ENDPOINTS[biome]
    params = {
        "service": "WFS",
        "version": "2.0.0",
        "request": "GetFeature",
        "typeName": endpoint["type_name"],
        "outputFormat": "application/json",
        "count": str(count),
        "startIndex": str(start_index),
    }
    if cql_filter:
        params["CQL_FILTER"] = cql_filter

    return endpoint["base_url"] + "?" + urlencode(params)


class INPEDeterPoller:
    """
    Polls INPE DETER WFS endpoints for deforestation alerts and sends events to Kafka.
    """

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: Optional[str] = None,
                 last_polled_file: Optional[str] = None,
                 poll_interval_minutes: int = DEFAULT_POLL_INTERVAL_MINUTES,
                 page_size: int = DEFAULT_PAGE_SIZE):
        """
        Initialize the poller.

        Args:
            kafka_config: Kafka configuration settings.
            kafka_topic: Kafka topic to send messages to.
            last_polled_file: File to store the last polled state.
            poll_interval_minutes: How often to poll in minutes.
            page_size: Number of features per WFS request page.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.poll_interval_minutes = poll_interval_minutes
        self.page_size = page_size
        self.event_producer: Optional[BRINPEDETEREventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = BRINPEDETEREventProducer(producer, kafka_topic)

    async def fetch_biome(self, biome: str, since_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch deforestation alerts from the WFS endpoint for a given biome.

        Args:
            biome: 'amazon' or 'cerrado'.
            since_date: Optional date string (YYYY-MM-DD) for temporal filtering.

        Returns:
            List of GeoJSON feature dictionaries.
        """
        cql_filter = f"view_date>='{since_date}'" if since_date else None
        all_features: List[Dict[str, Any]] = []
        start_index = 0

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            while True:
                url = build_wfs_url(biome, cql_filter=cql_filter,
                                    count=self.page_size, start_index=start_index)
                try:
                    async with asyncio.timeout(60):
                        async with session.get(url) as response:
                            response.raise_for_status()
                            data = await response.json(content_type=None)
                except asyncio.TimeoutError:
                    logger.error("Request timed out for biome %s at startIndex %d", biome, start_index)
                    break
                except aiohttp.ClientError as e:
                    logger.error("HTTP error for biome %s: %s", biome, e)
                    break

                features = data.get("features", [])
                if not features:
                    break

                all_features.extend(features)
                if len(features) < self.page_size:
                    break
                start_index += len(features)

        return all_features

    def parse_alert(self, feature: Dict[str, Any], biome: str) -> Optional[DeforestationAlert]:
        """
        Parse a GeoJSON feature into a DeforestationAlert dataclass.

        Args:
            feature: A GeoJSON feature dictionary from the WFS API.
            biome: The biome name ('amazon' or 'cerrado').

        Returns:
            A DeforestationAlert instance, or None if the feature cannot be parsed.
        """
        props = feature.get("properties", {})
        geometry = feature.get("geometry")

        gid = props.get("gid")
        if not gid:
            return None

        view_date = props.get("view_date")
        if not view_date:
            return None

        classname = props.get("classname", "")
        satellite = props.get("satellite", "")
        sensor = props.get("sensor", "")
        area_km2 = props.get("areamunkm", 0.0)
        municipality = props.get("municipality")
        state_code = props.get("uf")
        path_row = props.get("path_row")
        publish_month = props.get("publish_month")

        if geometry:
            centroid_lat, centroid_lon = compute_centroid(geometry)
        else:
            centroid_lat, centroid_lon = 0.0, 0.0

        return DeforestationAlert(
            alert_id=str(gid),
            biome=biome,
            classname=classname,
            view_date=view_date,
            satellite=satellite,
            sensor=sensor,
            area_km2=float(area_km2) if area_km2 is not None else 0.0,
            municipality=municipality,
            state_code=state_code,
            path_row=path_row,
            publish_month=publish_month,
            centroid_latitude=centroid_lat,
            centroid_longitude=centroid_lon,
        )

    def load_state(self) -> Dict[str, Any]:
        """
        Load previously stored polling state from file.

        Returns:
            Dict with 'seen_ids' and 'last_view_date' per biome.
        """
        if self.last_polled_file and os.path.exists(self.last_polled_file):
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error("Error decoding state file")
                    return {}
        return {}

    def save_state(self, state: Dict[str, Any]):
        """
        Save polling state to file.

        Args:
            state: Dict with 'seen_ids' and 'last_view_date' per biome.
        """
        if self.last_polled_file:
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)

    async def poll_and_send(self):
        """
        Continuously poll both Amazon and Cerrado WFS endpoints and send new alerts to Kafka.
        """
        state = self.load_state()
        poll_interval = timedelta(minutes=self.poll_interval_minutes)

        while True:
            start_poll_time = datetime.now(timezone.utc)
            total_new = 0

            for biome in WFS_ENDPOINTS:
                biome_state = state.get(biome, {})
                seen_ids = set(biome_state.get("seen_ids", []))
                last_view_date = biome_state.get("last_view_date")

                if not last_view_date:
                    last_view_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")

                features = await self.fetch_biome(biome, since_date=last_view_date)
                max_view_date = last_view_date
                count_new = 0

                for feature in features:
                    alert = self.parse_alert(feature, biome)
                    if alert is None:
                        continue

                    if alert.alert_id in seen_ids:
                        continue

                    if self.event_producer:
                        self.event_producer.send_br_inpe_deter_deforestation_alert(
                            _source_uri=SOURCE_URI,
                            _biome=alert.biome,
                            _alert_id=alert.alert_id,
                            _view_date=alert.view_date,
                            data=alert,
                            flush_producer=False
                        )

                    seen_ids.add(alert.alert_id)
                    count_new += 1

                    if alert.view_date > max_view_date:
                        max_view_date = alert.view_date

                # Prune old IDs - keep last 10000 max
                if len(seen_ids) > 10000:
                    seen_ids = set(list(seen_ids)[-10000:])

                state[biome] = {
                    "seen_ids": list(seen_ids),
                    "last_view_date": max_view_date,
                }
                total_new += count_new

            if self.event_producer:
                self.event_producer.producer.flush()
            self.save_state(state)

            if total_new > 0:
                logger.info("Processed %d new deforestation alerts", total_new)
            else:
                logger.debug("No new deforestation alerts")

            elapsed = datetime.now(timezone.utc) - start_poll_time
            remaining = poll_interval - elapsed
            if remaining.total_seconds() > 0:
                logger.debug("Sleeping for %s", remaining)
                await asyncio.sleep(remaining.total_seconds())


async def run_recent_alerts(biome: Optional[str] = None, days: int = 7):
    """Fetch and print recent deforestation alerts."""
    poller = INPEDeterPoller()
    since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    biomes = [biome] if biome else list(WFS_ENDPOINTS.keys())

    for b in biomes:
        features = await poller.fetch_biome(b, since_date=since_date)
        for feature in features:
            alert = poller.parse_alert(feature, b)
            if alert:
                print(f"[{alert.biome.upper()}] {alert.classname} - {alert.municipality or 'Unknown'}, "
                      f"{alert.state_code or '??'} ({alert.view_date}) "
                      f"[{alert.area_km2:.4f} km²] [{alert.alert_id}]")


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string: The connection string.

    Returns:
        Dict with extracted connection parameters.
    """
    config_dict = {}
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
    """
    Main function to parse arguments and start the INPE DETER poller.
    """
    parser = argparse.ArgumentParser(description="INPE DETER Deforestation Alert Poller")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    feed_parser = subparsers.add_parser('feed', help="Poll INPE DETER data and feed it to Kafka")
    feed_parser.add_argument('--last-polled-file', type=str,
                             help="File to store the last polled state")
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
    feed_parser.add_argument('--poll-interval', type=int, default=DEFAULT_POLL_INTERVAL_MINUTES,
                             help=f'Poll interval in minutes (default: {DEFAULT_POLL_INTERVAL_MINUTES})')
    feed_parser.add_argument('--log-level', type=str,
                             help='Logging level', default='INFO')

    events_parser = subparsers.add_parser('events', help="List recent deforestation alerts")
    events_parser.add_argument('--biome', type=str, choices=['amazon', 'cerrado'],
                               help='Biome to query (default: both)')
    events_parser.add_argument('--days', type=int, default=7,
                               help='Number of days to look back (default: 7)')

    subparsers.add_parser('biomes', help="List available biomes")

    args = parser.parse_args()

    if args.subcommand == 'events':
        asyncio.run(run_recent_alerts(args.biome, args.days))
    elif args.subcommand == 'biomes':
        for name, config in WFS_ENDPOINTS.items():
            print(f"{name}: {config['base_url']} ({config['type_name']})")
    elif args.subcommand == 'feed':

        if not args.connection_string:
            args.connection_string = os.getenv('CONNECTION_STRING')
        if not args.last_polled_file:
            args.last_polled_file = os.getenv('INPE_DETER_LAST_POLLED_FILE')
            if not args.last_polled_file:
                args.last_polled_file = os.path.expanduser('~/.inpe_deter_brazil_last_polled.json')
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
        kafka_config = {
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

        poller = INPEDeterPoller(
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
