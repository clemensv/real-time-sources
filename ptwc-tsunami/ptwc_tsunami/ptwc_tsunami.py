"""PTWC/NTWC tsunami bulletins bridge."""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional

import aiohttp
from confluent_kafka import Producer

from ptwc_tsunami_producer_data.tsunamibulletin import TsunamiBulletin  # pylint: disable=import-error
from ptwc_tsunami_producer_kafka_producer.producer import PTWCBulletinsEventProducer  # pylint: disable=import-error

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

FEEDS = {
    "PAAQ": "https://www.tsunami.gov/events/xml/PAAQAtom.xml",
    "PHEB": "https://www.tsunami.gov/events/xml/PHEBAtom.xml",
}

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "xhtml": "http://www.w3.org/1999/xhtml",
}

DEFAULT_POLL_INTERVAL = 300
DEFAULT_STATE_FILE = os.path.expanduser("~/.ptwc_tsunami_state.json")
DEFAULT_TOPIC = "ptwc-tsunami"


def _safe_str(value: Any) -> Optional[str]:
    """Convert a value to string if not None."""
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


def _text(element: Optional[ET.Element]) -> Optional[str]:
    """Get text content of an XML element."""
    if element is None:
        return None
    return element.text.strip() if element.text else None


def _parse_summary_field(summary_html: str, field_name: str) -> Optional[str]:
    """Parse a field value from the XHTML summary block.

    The summary contains patterns like:
        <strong>Category:</strong> Information<br/>
        <strong>Preliminary Magnitude: </strong>5.2(mb)<br/>
    """
    pattern = re.compile(
        r"<strong>\s*" + re.escape(field_name) + r"\s*:?\s*</strong>\s*(.+?)(?:<br\s*/?>|$)",
        re.IGNORECASE,
    )
    m = pattern.search(summary_html)
    if m:
        value = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return value if value else None
    return None


def _parse_note(summary_html: str) -> Optional[str]:
    """Parse the Note field from the XHTML summary."""
    pattern = re.compile(r"<b>Note:</b>\s*(.+?)(?:<br\s*/?>|<strong>|$)", re.IGNORECASE)
    m = pattern.search(summary_html)
    if m:
        value = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        value = value.rstrip("*").strip()
        return value if value else None
    return None


def _get_summary_html(entry: ET.Element) -> str:
    """Extract the raw summary HTML from an Atom entry."""
    summary_el = entry.find("atom:summary", NS)
    if summary_el is None:
        return ""
    # Serialize the summary content to string and strip XML namespace prefixes
    raw = ET.tostring(summary_el, encoding="unicode", method="html")
    # Remove the outer <summary ...> wrapper
    raw = re.sub(r"^<[^>]+>", "", raw, count=1)
    raw = re.sub(r"</[^>]+>$", "", raw.rstrip(), count=1)
    # Strip namespace prefixes (html:strong -> strong, etc.)
    raw = re.sub(r"<(/?)(?:\w+:)", r"<\1", raw)
    # Remove xmlns declarations
    raw = re.sub(r'\s+xmlns:\w+="[^"]*"', "", raw)
    raw = re.sub(r'\s+xmlns="[^"]*"', "", raw)
    return raw


def parse_entry(entry: ET.Element, feed_name: str, center: Optional[str] = None) -> Optional[TsunamiBulletin]:
    """Parse an Atom entry into a TsunamiBulletin."""
    bulletin_id = _text(entry.find("atom:id", NS))
    if not bulletin_id:
        return None

    title = _text(entry.find("atom:title", NS))
    updated = _text(entry.find("atom:updated", NS))

    if not title or not updated:
        return None

    lat_el = entry.find("geo:lat", NS)
    lon_el = entry.find("geo:long", NS)
    latitude = float(lat_el.text.strip()) if lat_el is not None and lat_el.text else None
    longitude = float(lon_el.text.strip()) if lon_el is not None and lon_el.text else None

    summary_html = _get_summary_html(entry)

    category = _parse_summary_field(summary_html, "Category")
    magnitude = _parse_summary_field(summary_html, "Preliminary Magnitude")
    affected_region = _parse_summary_field(summary_html, "Affected Region")
    note = _parse_note(summary_html)

    bulletin_url = None
    cap_url = None
    for link in entry.findall("atom:link", NS):
        rel = link.get("rel", "")
        link_type = link.get("type", "")
        href = link.get("href", "").strip()
        if rel == "alternate" and href:
            bulletin_url = href
        elif rel == "related" and "cap" in link_type and href:
            cap_url = href

    return TsunamiBulletin(
        bulletin_id=bulletin_id,
        feed=feed_name,
        center=center,
        title=title,
        updated=updated,
        latitude=latitude,
        longitude=longitude,
        category=category,
        magnitude=magnitude,
        affected_region=affected_region,
        note=note,
        bulletin_url=bulletin_url,
        cap_url=cap_url,
    )


class PTWCTsunamiPoller:
    """Polls PTWC/NTWC tsunami Atom feeds and sends bulletins to Kafka."""

    def __init__(self, kafka_config: Optional[Dict[str, str]] = None,
                 kafka_topic: str = DEFAULT_TOPIC,
                 state_file: str = DEFAULT_STATE_FILE,
                 poll_interval: int = DEFAULT_POLL_INTERVAL,
                 feeds: Optional[List[str]] = None):
        self.kafka_topic = kafka_topic
        self.state_file = state_file
        self.poll_interval = poll_interval
        self.feeds = feeds or list(FEEDS.keys())
        self.event_producer: Optional[PTWCBulletinsEventProducer] = None
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.event_producer = PTWCBulletinsEventProducer(producer, kafka_topic)

    async def fetch_feed(self, session: aiohttp.ClientSession, feed_name: str) -> Optional[ET.Element]:
        """Fetch and parse an Atom feed."""
        url = FEEDS.get(feed_name)
        if not url:
            return None
        try:
            async with session.get(url) as response:
                if response.status == 404:
                    return None
                response.raise_for_status()
                data = await response.read()
                return ET.fromstring(data)
        except Exception:
            logger.warning("Failed to fetch feed %s", feed_name, exc_info=True)
            return None

    def load_state(self) -> Dict[str, str]:
        """Load state tracking seen bulletin IDs."""
        if self.state_file and os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def save_state(self, state: Dict[str, str]):
        """Persist state to disk."""
        if self.state_file:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state, f)

    async def poll_and_send(self, once: bool = False):
        """Main poll loop."""
        state = self.load_state()

        while True:
            count_new = 0
            count_updated = 0

            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=60),
                headers={"User-Agent": "ptwc-tsunami-bridge/1.0"}
            ) as session:
                for feed_name in self.feeds:
                    root = await self.fetch_feed(session, feed_name)
                    if root is None:
                        continue

                    # Extract center from feed author
                    author_name = root.find("atom:author/atom:name", NS)
                    center = _text(author_name)

                    entries = root.findall("atom:entry", NS)
                    for entry in entries:
                        bulletin = parse_entry(entry, feed_name, center)
                        if bulletin is None:
                            continue

                        updated_str = bulletin.updated or ""
                        prev_updated = state.get(bulletin.bulletin_id)
                        if prev_updated is not None and prev_updated >= updated_str:
                            continue

                        if prev_updated is None:
                            count_new += 1
                        else:
                            count_updated += 1

                        if self.event_producer:
                            await self.event_producer.send_ptwc_tsunami_bulletin(
                                _bulletin_id=bulletin.bulletin_id,
                                data=bulletin,
                                flush_producer=False,
                            )

                        state[bulletin.bulletin_id] = updated_str

            if self.event_producer:
                self.event_producer.producer.flush()
            self.save_state(state)

            if count_new > 0 or count_updated > 0:
                logger.info("Processed %d new and %d updated bulletins", count_new, count_updated)
            else:
                logger.debug("No new bulletins")

            if once:
                return

            await asyncio.sleep(self.poll_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs or Fabric Event Stream connection string."""
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
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PTWC/NTWC tsunami bulletins bridge")
    parser.add_argument("--connection-string", type=str, help="Event Hubs connection string")
    parser.add_argument("--bootstrap-servers", type=str, help="Kafka bootstrap servers")
    parser.add_argument("--topic", type=str, help="Kafka topic")
    parser.add_argument("--sasl-username", type=str, help="SASL username")
    parser.add_argument("--sasl-password", type=str, help="SASL password")
    parser.add_argument("--state-file", type=str, help="State file path")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Poll interval in seconds")
    parser.add_argument("--feeds", type=str, help="Comma-separated list of feeds (PAAQ, PHEB)")
    parser.add_argument("--once", action="store_true", help="Poll once and exit")
    parser.add_argument("--log-level", type=str, default="INFO", help="Logging level")
    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv("PTWC_TSUNAMI_CONNECTION_STRING") or os.getenv("CONNECTION_STRING")
    if not args.bootstrap_servers:
        args.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    if not args.topic:
        args.topic = os.getenv("KAFKA_TOPIC", DEFAULT_TOPIC)
    if not args.sasl_username:
        args.sasl_username = os.getenv("SASL_USERNAME")
    if not args.sasl_password:
        args.sasl_password = os.getenv("SASL_PASSWORD")
    if not args.state_file:
        args.state_file = os.getenv("PTWC_TSUNAMI_STATE_FILE", DEFAULT_STATE_FILE)
    if os.getenv("LOG_LEVEL"):
        args.log_level = os.getenv("LOG_LEVEL")

    logging.getLogger().setLevel(args.log_level.upper())

    feeds = None
    if args.feeds:
        feeds = [f.strip().upper() for f in args.feeds.split(",")]

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic", args.topic)
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        bootstrap_servers = args.bootstrap_servers
        kafka_topic = args.topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not bootstrap_servers:
        print("Error: Kafka bootstrap servers required via --bootstrap-servers, --connection-string, or KAFKA_BOOTSTRAP_SERVERS.")
        sys.exit(1)
    if not kafka_topic:
        kafka_topic = DEFAULT_TOPIC

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config: Dict[str, str] = {"bootstrap.servers": bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    poller = PTWCTsunamiPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        state_file=args.state_file,
        poll_interval=args.poll_interval,
        feeds=feeds,
    )

    asyncio.run(poller.poll_and_send(once=args.once))


if __name__ == "__main__":
    main()
