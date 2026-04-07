"""
GDACS Disaster Alert Poller
Polls the Global Disaster Alert and Coordination System RSS feed and sends
disaster alert events to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import sys
import asyncio
import aiohttp
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, Optional
import argparse
from confluent_kafka import Producer

from gdacs_producer_data.disasteralert import DisasterAlert  # pylint: disable=import-error
from gdacs_producer_kafka_producer.producer import GDACSAlertsEventProducer  # pylint: disable=import-error


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

GDACS_RSS_URL = "https://www.gdacs.org/xml/rss.xml"

NAMESPACES = {
    'gdacs': 'http://www.gdacs.org',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'georss': 'http://www.georss.org/georss',
}


def _text(element: ET.Element, tag: str, ns: Optional[str] = None) -> Optional[str]:
    """Extract text content from an XML child element."""
    if ns:
        child = element.find(f'{{{NAMESPACES[ns]}}}{tag}')
    else:
        child = element.find(tag)
    if child is not None and child.text:
        return child.text.strip()
    return None


def _attr(element: ET.Element, tag: str, ns: str, attr: str) -> Optional[str]:
    """Extract an attribute value from an XML child element."""
    child = element.find(f'{{{NAMESPACES[ns]}}}{tag}')
    if child is not None:
        return child.get(attr)
    return None


def _parse_float(value: Optional[str]) -> Optional[float]:
    """Safely parse a string to float, returning None on failure."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _parse_int(value: Optional[str]) -> Optional[int]:
    """Safely parse a string to int, returning None on failure."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def _parse_bool(value: Optional[str]) -> Optional[bool]:
    """Parse a GDACS boolean string ('true'/'false'/'1'/'0') to bool."""
    if value is None:
        return None
    return value.lower() in ('true', '1', 'yes')


def _parse_datetime(value: Optional[str]) -> Optional[str]:
    """Parse a date string into ISO-8601 format. Returns None if unparseable."""
    if value is None:
        return None
    # GDACS dates are often in RFC 2822 or ISO-like formats
    for fmt in (
        '%a, %d %b %Y %H:%M:%S %Z',
        '%a, %d %b %Y %H:%M:%S %z',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
    ):
        try:
            dt = datetime.strptime(value.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except ValueError:
            continue
    return value.strip()


def _parse_bbox(value: Optional[str]):
    """Parse a GDACS bounding box string into (min_lon, max_lon, min_lat, max_lat)."""
    if not value:
        return None, None, None, None
    parts = value.replace(',', ' ').split()
    floats = []
    for p in parts:
        try:
            floats.append(float(p))
        except ValueError:
            pass
    if len(floats) == 4:
        return floats[0], floats[1], floats[2], floats[3]
    return None, None, None, None


def parse_rss_item(item: ET.Element) -> Optional[DisasterAlert]:
    """Parse a single RSS item element into a DisasterAlert data class."""
    event_type = _text(item, 'eventtype', 'gdacs')
    event_id = _text(item, 'eventid', 'gdacs')
    alert_level = _text(item, 'alertlevel', 'gdacs')
    lat_str = _text(item, 'lat', 'geo')
    lon_str = _text(item, 'long', 'geo')
    from_date_str = _text(item, 'fromdate', 'gdacs')
    severity_value_str = _attr(item, 'severity', 'gdacs', 'value')
    severity_unit = _attr(item, 'severity', 'gdacs', 'unit')

    latitude = _parse_float(lat_str)
    longitude = _parse_float(lon_str)
    severity_value = _parse_float(severity_value_str)

    if not event_type or not event_id or not alert_level:
        return None
    if latitude is None or longitude is None:
        return None
    if severity_value is None or severity_unit is None:
        return None

    from_date = _parse_datetime(from_date_str)
    if from_date is None:
        return None

    episode_id = _text(item, 'episodeid', 'gdacs')
    alert_score = _parse_float(_text(item, 'alertscore', 'gdacs'))
    episode_alert_level = _text(item, 'episodealertlevel', 'gdacs')
    episode_alert_score = _parse_float(_text(item, 'episodealertscore', 'gdacs'))
    event_name = _text(item, 'eventname', 'gdacs')
    country = _text(item, 'country', 'gdacs')
    iso3 = _text(item, 'iso3', 'gdacs')
    to_date = _parse_datetime(_text(item, 'todate', 'gdacs'))
    vulnerability = _parse_float(_text(item, 'vulnerability', 'gdacs'))
    is_current = _parse_bool(_text(item, 'iscurrent', 'gdacs'))
    version = _parse_int(_text(item, 'version', 'gdacs'))
    description_text = _text(item, 'description')
    link = _text(item, 'link')
    pub_date = _parse_datetime(_text(item, 'pubDate'))

    # Parse population (has value and unit attributes like severity)
    population_value = _parse_float(_attr(item, 'population', 'gdacs', 'value'))
    population_unit = _attr(item, 'population', 'gdacs', 'unit')

    # Parse severity text from element text
    severity_elem = item.find(f'{{{NAMESPACES["gdacs"]}}}severity')
    severity_text = severity_elem.text.strip() if severity_elem is not None and severity_elem.text else None

    # Parse bounding box
    bbox_str = _text(item, 'bbox', 'gdacs')
    bbox_min_lon, bbox_max_lon, bbox_min_lat, bbox_max_lat = _parse_bbox(bbox_str)

    return DisasterAlert(
        event_type=event_type,
        event_id=event_id,
        alert_level=alert_level,
        latitude=latitude,
        longitude=longitude,
        from_date=from_date,
        severity_value=severity_value,
        severity_unit=severity_unit,
        episode_id=episode_id,
        alert_score=alert_score,
        episode_alert_level=episode_alert_level,
        episode_alert_score=episode_alert_score,
        event_name=event_name,
        country=country,
        iso3=iso3,
        to_date=to_date,
        population_value=population_value,
        population_unit=population_unit,
        vulnerability=vulnerability,
        bbox_min_lon=bbox_min_lon,
        bbox_max_lon=bbox_max_lon,
        bbox_min_lat=bbox_min_lat,
        bbox_max_lat=bbox_max_lat,
        severity_text=severity_text,
        is_current=is_current,
        version=version,
        description=description_text,
        link=link,
        pub_date=pub_date,
    )


class GDACSPoller:
    """Polls the GDACS RSS feed and sends disaster alert events to Kafka."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: Optional[str] = None,
                 state_file: Optional[str] = None,
                 poll_interval: int = 300):
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        self.poll_interval = poll_interval
        self.event_producer: Optional[GDACSAlertsEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = GDACSAlertsEventProducer(producer, kafka_topic)

    async def fetch_feed(self) -> str:
        """Download the GDACS RSS feed XML."""
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(GDACS_RSS_URL) as response:
                response.raise_for_status()
                return await response.text()

    def parse_feed(self, xml_text: str):
        """Parse the RSS XML and return a list of DisasterAlert objects."""
        root = ET.fromstring(xml_text)
        channel = root.find('channel')
        if channel is None:
            return []
        items = channel.findall('item')
        alerts = []
        for item in items:
            alert = parse_rss_item(item)
            if alert is not None:
                alerts.append(alert)
        return alerts

    def load_state(self) -> Dict[str, int]:
        """Load the state file tracking seen event+episode combinations and their versions."""
        if self.state_file and os.path.exists(self.state_file):
            with open(self.state_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error("Error decoding state file")
                    return {}
        return {}

    def save_state(self, state: Dict[str, int]):
        """Persist the state dict to disk."""
        if self.state_file:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f)

    @staticmethod
    def _state_key(alert: DisasterAlert) -> str:
        """Build a state key from event_type, event_id, and episode_id."""
        episode = alert.episode_id or '0'
        return f"{alert.event_type}_{alert.event_id}_{episode}"

    async def poll_and_send(self, once: bool = False):
        """Main poll loop. Downloads the feed, detects new/updated episodes, and emits events."""
        state = self.load_state()

        while True:
            try:
                xml_text = await self.fetch_feed()
                alerts = self.parse_feed(xml_text)
            except Exception:
                logger.exception("Error fetching or parsing GDACS feed")
                if once:
                    return
                await asyncio.sleep(self.poll_interval)
                continue

            count_new = 0
            count_updated = 0

            for alert in alerts:
                key = self._state_key(alert)
                prev_version = state.get(key)
                current_version = alert.version if alert.version is not None else 0

                if prev_version is not None and prev_version >= current_version:
                    continue

                if prev_version is None:
                    count_new += 1
                else:
                    count_updated += 1

                if self.event_producer:
                    await self.event_producer.send_gdacs_disaster_alert(
                        _event_type=alert.event_type,
                        _event_id=alert.event_id,
                        data=alert,
                        flush_producer=False,
                    )

                state[key] = current_version

            if self.event_producer:
                self.event_producer.producer.flush()
            self.save_state(state)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated disaster alerts", count_new, count_updated)
            else:
                logger.debug("No new disaster alerts")

            if once:
                return

            await asyncio.sleep(self.poll_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse an Azure Event Hubs or Fabric Event Stream connection string and
    extract bootstrap server, topic name, username, and password.
    """
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
    """Main entry point — parse arguments and start the GDACS poller."""
    parser = argparse.ArgumentParser(description="GDACS Disaster Alert Poller")
    parser.add_argument('--connection-string', type=str,
                        help='Azure Event Hubs or Fabric Event Stream connection string')
    parser.add_argument('--bootstrap-servers', type=str,
                        help='Comma-separated list of Kafka bootstrap servers')
    parser.add_argument('--topic', type=str,
                        help='Kafka topic to send messages to')
    parser.add_argument('--sasl-username', type=str,
                        help='SASL PLAIN username')
    parser.add_argument('--sasl-password', type=str,
                        help='SASL PLAIN password')
    parser.add_argument('--state-file', type=str,
                        help='File to persist seen event state across restarts')
    parser.add_argument('--poll-interval', type=int, default=300,
                        help='Polling interval in seconds (default: 300)')
    parser.add_argument('--once', action='store_true',
                        help='Poll once and exit')
    parser.add_argument('--log-level', type=str, default='INFO',
                        help='Logging level (default: INFO)')
    args = parser.parse_args()

    # Environment variable fallbacks
    if not args.connection_string:
        args.connection_string = os.getenv('GDACS_CONNECTION_STRING') or os.getenv('CONNECTION_STRING')
    if not args.bootstrap_servers:
        args.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    if not args.topic:
        args.topic = os.getenv('KAFKA_TOPIC')
    if not args.sasl_username:
        args.sasl_username = os.getenv('SASL_USERNAME')
    if not args.sasl_password:
        args.sasl_password = os.getenv('SASL_PASSWORD')
    if not args.state_file:
        args.state_file = os.getenv('GDACS_STATE_FILE')
        if not args.state_file:
            args.state_file = os.path.expanduser('~/.gdacs_state.json')
    if os.getenv('LOG_LEVEL'):
        args.log_level = os.getenv('LOG_LEVEL')

    logging.getLogger().setLevel(args.log_level.upper())

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        bootstrap_servers = args.bootstrap_servers
        kafka_topic = args.topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided via --bootstrap-servers, --connection-string, or KAFKA_BOOTSTRAP_SERVERS.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided via --topic, --connection-string, or KAFKA_TOPIC.")
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config: Dict[str, str] = {
        'bootstrap.servers': bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = GDACSPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
    )

    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
