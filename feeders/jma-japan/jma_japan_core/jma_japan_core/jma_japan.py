"""Transport-agnostic acquisition layer for the JMA Japan weather bulletins bridge."""

import hashlib
import json
import os
from typing import Dict, List, Optional
from xml.etree import ElementTree

import requests

from jma_japan_producer_data import WeatherBulletin
from jma_japan_producer_data.feedtypeenum import FeedTypeenum
from datetime import datetime

ATOM_NS = "{http://www.w3.org/2005/Atom}"

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-jma-japan/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

REGULAR_FEED_URL = "https://www.data.jma.go.jp/developer/xml/feed/regular.xml"
EXTRA_FEED_URL = "https://www.data.jma.go.jp/developer/xml/feed/extra.xml"
POLL_INTERVAL_SECONDS = 60

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/xml",
}


def make_bulletin_id(entry_id: str) -> str:
    """Create a stable short ID from an Atom entry ID (typically a long URL)."""
    return hashlib.sha256(entry_id.encode("utf-8")).hexdigest()[:16]


def fetch_feed(url: str) -> Optional[ElementTree.Element]:
    """Fetch and parse an Atom XML feed. Returns the root Element or None on error."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return ElementTree.fromstring(response.content)
    except Exception as err:
        print(f"Error fetching feed {url}: {err}")
        return None


def parse_entries(root: ElementTree.Element, feed_type: str) -> List[WeatherBulletin]:
    """Parse Atom feed entries into WeatherBulletin objects."""
    bulletins = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        entry_id_el = entry.find(f"{ATOM_NS}id")
        title_el = entry.find(f"{ATOM_NS}title")
        updated_el = entry.find(f"{ATOM_NS}updated")
        author_el = entry.find(f"{ATOM_NS}author")
        link_el = entry.find(f"{ATOM_NS}link")
        content_el = entry.find(f"{ATOM_NS}content")

        entry_id = entry_id_el.text if entry_id_el is not None and entry_id_el.text else ""
        if not entry_id:
            continue

        title = title_el.text if title_el is not None and title_el.text else ""
        updated = updated_el.text if updated_el is not None and updated_el.text else ""
        author = None
        if author_el is not None:
            name_el = author_el.find(f"{ATOM_NS}name")
            if name_el is not None and name_el.text:
                author = name_el.text
        link = link_el.get("href") if link_el is not None else None
        content = content_el.text if content_el is not None and content_el.text else None

        bulletin_id = make_bulletin_id(entry_id)
        bulletin = WeatherBulletin(
            bulletin_id=bulletin_id,
            title=title,
            author=author,
            updated=datetime.fromisoformat(updated),
            link=link,
            content=content,
            feed_type=FeedTypeenum(feed_type),
            office=author,
        )
        bulletins.append(bulletin)
    return bulletins


def poll_feeds() -> List[WeatherBulletin]:
    """Fetch both regular and extra feeds and return all parsed bulletins."""
    all_bulletins: List[WeatherBulletin] = []
    for url, feed_type in [
        (REGULAR_FEED_URL, "regular"),
        (EXTRA_FEED_URL, "extra"),
    ]:
        root = fetch_feed(url)
        if root is not None:
            bulletins = parse_entries(root, feed_type)
            all_bulletins.extend(bulletins)
    return all_bulletins


def load_seen_bulletins(state_file: str) -> dict:
    """Load the set of previously seen bulletin IDs from the state file."""
    try:
        if os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {"seen_ids": []}


def save_seen_bulletins(state_file: str, state: dict) -> None:
    """Save the set of seen bulletin IDs to the state file."""
    try:
        os.makedirs(
            os.path.dirname(state_file) if os.path.dirname(state_file) else '.',
            exist_ok=True,
        )
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Error saving state: {e}")


def bulletin_office_segment(bulletin: WeatherBulletin) -> str:
    """Return a safe topic/route segment for the bulletin's office."""
    raw = (bulletin.office or bulletin.author or "unknown").strip()
    if not raw:
        return "unknown"
    for ch in ("/", "+", "#", " "):
        raw = raw.replace(ch, "-")
    return raw or "unknown"
