"""
RSS Bridge
"""

import argparse
import asyncio
from datetime import datetime, timedelta, timezone
import json
import logging
import os
import sys
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import feedparser
import listparser
from confluent_kafka import Producer
import requests

from requests import RequestException

from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemauthor import FeedItemAuthor
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemcontent import FeedItemContent
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsource import FeedItemSource
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemtitle import FeedItemTitle
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemenclosure import FeedItemEnclosure
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditempublisher import FeedItemPublisher
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditemsummary import FeedItemSummary
from rssbridge_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem
from rssbridge_producer_data.microsoft.opendata.rssfeeds.link import Link
from rssbridge_producer_kafka_producer.producer import MicrosoftOpenDataRssFeedsEventProducer

# Logging configuration
if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


USER_DIR = os.path.expanduser("~")
STATE_FILE = os.path.join(USER_DIR, ".rss-grabber.json")
FEEDSTORE_FILE = os.path.join(USER_DIR, ".rss-grabber-feedstore.xml")
__version__ = "1.0.0"

USER_AGENT = f"Event Stream RSS Agent {__version__}"


def load_state():
    """
    Load the state from the state file.

    Returns:
        dict: The loaded state.
    """
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                logging.info("Loading state from %s", STATE_FILE)
                return json.load(f)
    except Exception as e:
        logging.error("Failed to load state: %s", e)
    return {}


def save_state(state):
    """
    Save the state to the state file.

    Args:
        state (dict): The state to save.
    """
    try:
        if not os.path.exists(os.path.dirname(STATE_FILE)):
            os.makedirs(os.path.dirname(STATE_FILE))
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            logging.info("Saving state to %s", STATE_FILE)
            json.dump(state, f)
    except Exception as e:
        logging.error("Failed to save state: %s", e)
    


def load_feedstore() -> List[str]:
    """
    Load the feed URLs from the feedstore file.

    Returns:
        List[str]: The list of feed URLs.
    """
    if not os.path.exists(FEEDSTORE_FILE):
        return []

    logging.info("Loading feedstore from %s", FEEDSTORE_FILE)
    tree = ET.parse(FEEDSTORE_FILE)
    root = tree.getroot()
    return [outline.get('xmlUrl') for outline in root.iter('outline')]


def save_feedstore(feed_urls: List[str]):
    """
    Save the feed URLs to the feedstore file.

    Args:
        feed_urls (List[str]): The list of feed URLs.
    """
    root = ET.Element("opml")
    head = ET.SubElement(root, "head")
    title = ET.SubElement(head, "title")
    title.text = "RSS Feeds"

    body = ET.SubElement(root, "body")
    for url in feed_urls:
        ET.SubElement(body, "outline", type="rss", xmlUrl=url)

    tree = ET.ElementTree(root)
    logging.info("Saving feedstore to %s", FEEDSTORE_FILE)
    tree.write(FEEDSTORE_FILE)


def extract_feed_urls_from_webpage(url: str) -> List[str]:
    """
    Extract RSS/Atom feed URLs from a web page's alternate links metadata.

    Args:
        url (str): The URL of the web page.

    Returns:
        List[str]: A list of extracted feed URLs.
    """
    response = requests.get(url, headers={'User-Agent': USER_AGENT}, timeout=10)
    if response.status_code != 200:
        logging.error("Failed to fetch %s: %s", url, response.status_code)
        response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    feed_urls = []
    for link in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
        feed_url = link.get('href')
        if feed_url:
            parsedurl = urlparse(feed_url)
            if parsedurl.scheme == '' or parsedurl.netloc == '':  # relative URL
                feed_url = urljoin(url, feed_url)
            if feed_url:
                feed_urls.append(feed_url)
    return feed_urls


def add_feed(url: str):
    """
    Add a feed URL or URLs from an OPML file to the feedstore.

    Args:
        url (str): The feed URL or OPML file URL to add.
    """
    feed_urls = load_feedstore()
    headers = {'User-Agent': USER_AGENT}

    urlparsed = urlparse(url)
    if urlparsed.scheme == '' or urlparsed.netloc == '':
        url = f"https://{url}"

    if url.endswith(".opml"):
        opml_content = requests.get(url, headers=headers, timeout=10).content
        opml_tree = listparser.parse(opml_content)
        feed_urls.extend([outline.url for outline in opml_tree.feeds])
    else:
        try:
            response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()
        except requests.RequestException:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            response.raise_for_status()

        content_type = response.headers.get('Content-Type', '').lower()

        try:
            if 'text/html' in content_type:
                extracted_urls = extract_feed_urls_from_webpage(url)
                if not extracted_urls:
                    logging.debug(f"No feeds found at {url}")
                else:
                    feed_urls.extend(extracted_urls)
                    logging.debug(f"Added feed(s) from {url}: {extracted_urls}")
            elif 'application/rss+xml' in content_type or 'application/atom+xml' in content_type or 'application/xml' in content_type or 'text/xml' in content_type:
                feed_urls.append(url)
                logging.debug(f"Added feed {url}")
            else:
                logging.debug(f"Unsupported content type {content_type} at {url}")
        except Exception as e:
            logging.error("Error processing %s: %s", url, e)

    save_feedstore(list(set(feed_urls)))


def remove_feed(url: str):
    """
    Remove a feed URL from the feedstore.

    Args:
        url (str): The feed URL to remove.
    """
    feed_urls = load_feedstore()
    if url in feed_urls:
        feed_urls.remove(url)
    save_feedstore(feed_urls)


def feeditem_from_feedparser_entry(feed, entry) -> FeedItem:
    """
    Create a FeedItem instance from a feedparser entry.

    Args:
        entry: The feedparser entry.

    Returns:
        FeedItem: The created FeedItem instance.
    """
    def parse_author_detail(detail):
        if detail:
            return FeedItemAuthor(
                name=detail.get('name'),
                href=detail.get('href'),
                email=detail.get('email')
            )
        if 'author' in entry:
            return FeedItemAuthor(name=entry.get('author'), href=None, email=None)

        return None

    def parse_publisher_detail(detail):
        if detail:
            return FeedItemPublisher(
                name=detail.get('name'),
                href=detail.get('href'),
                email=detail.get('email')
            )
        if 'publisher' in entry:
            return FeedItemPublisher(name=entry.get('publisher'), href=None, email=None)
        return None

    def parse_summary_detail(detail):
        if detail:
            return FeedItemSummary(
                value=detail.get('value'),
                type=detail.get('type'),
                language=detail.get('language'),
                base=detail.get('base')
            )
        if 'summary' in entry:
            return FeedItemSummary(value=entry.get('summary'), type=None, language=None, base=None)
        return None

    def parse_title_detail(detail):
        if detail:
            return FeedItemTitle(
                value=detail.get('value'),
                type=detail.get('type'),
                language=detail.get('language'),
                base=detail.get('base')
            )
        if 'title' in entry:
            return FeedItemTitle(value=entry.get('title'), type=None, language=None, base=None)
        return None

    def parse_content_detail(content):
        return [FeedItemContent(
            value=item.get('value'),
            type=item.get('type'),
            language=item.get('language'),
            base=item.get('base')
        ) for item in content] if content else None

    def parse_enclosure_detail(enclosures):
        return [FeedItemEnclosure(
            href=enclosure.get('href'),
            length=enclosure.get('length'),
            type=enclosure.get('type')
        ) for enclosure in enclosures] if enclosures else None

    def parse_source_detail(source):
        if source:
            return FeedItemSource(
                author=source.get('author'),
                author_detail=parse_author_detail(source.get('author_detail')),
                contributors=[parse_author_detail(contrib) for contrib in source.get('contributors', [])],
                icon=source.get('icon'),
                id=source.get('id'),
                link=source.get('link'),
                links=source.get('links'),
                logo=source.get('logo'),
                rights=source.get('rights'),
                subtitle=source.get('subtitle'),
                title=source.get('title'),
                updated=parse_date(source.get('updated_parsed'))
            )
        return None

    def parse_date(parsed_date_value) -> datetime|None:
        if isinstance(parsed_date_value, time.struct_time):
            st: time.struct_time = parsed_date_value
            return datetime(st.tm_year, st.tm_mon, st.tm_mday, st.tm_hour, st.tm_min, st.tm_sec, tzinfo=timezone.utc)
        if isinstance(parsed_date_value, datetime):
            return parsed_date_value.astimezone(timezone.utc)
        if isinstance(parsed_date_value,str):
            return datetime.fromisoformat(parsed_date_value).astimezone(timezone.utc)
        return None

    feed_item = FeedItem(
        author=parse_author_detail(entry.get('author_detail')),
        publisher=parse_publisher_detail(entry.get('publisher_detail')),
        summary=parse_summary_detail(entry.get('summary_detail')),
        title=parse_title_detail(entry.get('title_detail')),
        source=None,
        content=parse_content_detail(entry.get('content')),
        enclosures=parse_enclosure_detail(entry.get('enclosures')),
        published=parse_date(entry.get('published_parsed')),
        updated=parse_date(entry.get('updated_parsed')),
        created=parse_date(entry.get('created_parsed')),
        expired=parse_date(entry.get('expired_parsed')),
        id=entry.get('id'),
        license=entry.get('license'),
        comments=entry.get('comments'),
        contributors=[parse_author_detail(contrib) for contrib in entry.get('contributors', [])],
        links=entry.get('links')
    )
    if not feed_item.source:
        feed_item.source = FeedItemSource(
            author=entry.get('author'),
            author_detail=parse_author_detail(entry.get('author_detail')),
            contributors=[parse_author_detail(contrib) for contrib in entry.get('contributors', [])],
            icon=feed.feed.get('image').get('href') if feed.feed.get('image') else None,
            id=entry.get('id'),
            link=feed.feed.get('link'),
            links=[],
            logo=feed.feed.get('image').get('href') if feed.feed.get('image') else None,
            rights=feed.feed.get('rights'),
            subtitle=feed.feed.get('subtitle'),
            title=feed.feed.get('title'),
            updated=parse_date(feed.feed.get('updated_parsed'))
        )
    for link in feed.feed.get('links'):
        feed_item.source.links.append(Link(title=link.get('title'), href=link.get('href'), rel=link.get('rel'), type=link.get('type'))) 
    return feed_item


def fetch_feed(url: str, etag: Optional[str] = None) -> requests.Response:
    """
    Fetch the RSS feed.

    Args:
        url (str): The URL of the RSS feed.
        etag (Optional[str]): The ETag for caching purposes.

    Returns:
        requests.Response: The HTTP response object.
    """

    try:
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'application/atom+xml, application/rss+xml, application/xml, text/xml',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,de;q=0.7,de-DE;q=0.6,ko;q=0.5',
        }
        if etag:
            headers['If-None-Match'] = etag

        response = requests.get(url, headers=headers, timeout=10)
        logging.info("%s: Response status code: %s", url, response.status_code)
        if response.status_code == 304:
            return response
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error("Failed to fetch %s: %s", url, e)
        raise e


async def process_feed(feed_url: str, state: dict, producer_instance: MicrosoftOpenDataRssFeedsEventProducer):
    """
    Process the feed and update the state.

    Args:
        feed_url (str): The URL of the feed.
        state (dict): The current state.
    """
    try:
        # Handle backoff
        if state.get(feed_url) and not isinstance(state[feed_url], dict):
            state[feed_url] = {}
        next_check_time = state.get(feed_url, {}).get("next_check_time")
        if next_check_time and datetime.now(timezone.utc) < datetime.fromisoformat(next_check_time).astimezone(timezone.utc):
            logging.debug(f"Backoff until {next_check_time} for {feed_url}")
            return

        # Handle skip
        if state.get(feed_url, {}).get("skip", False):
            logging.debug(f"Skipping {feed_url}")
            return

        # Fetch the feed with ETag
        etag = state.get(feed_url, {}).get("etag")
        response = fetch_feed(feed_url, etag)

        if response.status_code == 304:
            state[feed_url] = {
                **state.get(feed_url, {}),
                "last_checked": datetime.now(timezone.utc).isoformat(),
                "next_check_time": (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat()
            }
            return

        feed = feedparser.parse(response.content)
        # Check for redirection
        actual_url = response.url

        new_items = []
        last_checked = state.get(feed_url, {}).get("last_checked", 0)
        last_checked_datetime = datetime.fromisoformat(last_checked).astimezone(timezone.utc) if isinstance(
            last_checked, str) else datetime.fromtimestamp(last_checked, tz=timezone.utc)

        for entry in feed.entries:
            if 'published_parsed' in entry and entry.published_parsed:  # won't handle entries without pub date
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if pub_date > last_checked_datetime:
                    item: FeedItem = feeditem_from_feedparser_entry(feed, entry)
                    try:
                        new_items.append(item)
                    except Exception as e:
                        logging.error("Error processing item: %s", e)

        # Handle cache headers
        cache_control = response.headers.get('Cache-Control', '')
        max_age = None
        if 'max-age' in cache_control:
            try:
                max_age = int(cache_control.split('max-age=')[1].split(',')[0])
            except (IndexError, ValueError):
                pass

        expires = response.headers.get('Expires')
        expires_datetime = None
        if expires:
            try:
                expires_datetime = datetime.strptime(expires, '%a, %d %b %Y %H:%M:%S %Z').astimezone(timezone.utc)
            except ValueError:
                pass

        # next check time is the minimum of the max age, expires, or 12 hours from now, plus 5 seconds to align multiple fgeeds
        next_check_time = min([
            datetime.now(timezone.utc) + timedelta(seconds=max_age) if max_age else datetime.now(timezone.utc) + timedelta(minutes=1),
            expires_datetime if expires_datetime else datetime.now(timezone.utc) + timedelta(minutes=1)
        ]) + timedelta(seconds=5)
        if next_check_time < datetime.now(timezone.utc):
            next_check_time = datetime.now(timezone.utc) + timedelta(minutes=1)
        if next_check_time > datetime.now(timezone.utc) + timedelta(hours=12):
            next_check_time = datetime.now(timezone.utc) + timedelta(hours=12)

        state[feed_url] = {
            "last_checked": datetime.now(timezone.utc).isoformat(),
            "skip": False,
            "actual_url": actual_url,
            "etag": response.headers.get('ETag'),
            "next_check_time": next_check_time.isoformat()
        }

        if new_items:
            for item in new_items:
                logging.info("Sending item %s for feed %s", item.id, feed_url)
                await producer_instance.send_microsoft_open_data_rss_feeds_feed_item(_sourceurl=feed_url, _item_id=item.id, data=item, flush_producer=False)
        producer_instance.producer.flush()

    except RequestException as e:
        if e.response is not None:
            if e.response.status_code == 429:  # Too many requests
                if not 'feed_url' in state:
                    state[feed_url] = {}
                state[feed_url]["next_check_time"] = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
                logging.debug(f"Backoff set for {feed_url} due to 429 response")
            elif e.response.status_code == 404 or e.response.status_code == 403:
                if not 'feed_url' in state:
                    state[feed_url] = {}
                state[feed_url]["skip"] = True
                logging.debug(f"Skipping {feed_url} due to 404/403 response")
            else:
                logging.debug(f"Error processing feed {feed_url}: {e}")
        else:
            logging.debug(f"Error processing feed {feed_url}: {e}")


async def poll_feeds(feed_urls: List[str], state, producer_instance: MicrosoftOpenDataRssFeedsEventProducer):
    """
    Poll the feeds periodically and update the state.

    Args:
        feed_urls (List[str]): The list of feed URLs.
        state (dict): The current state.
        scheduler (sched.scheduler): The scheduler instance.
    """
    while True:
        for feed_url in feed_urls:
            await process_feed(feed_url, state, producer_instance)
        save_state(state)
        next_poll = min([
            (datetime.fromisoformat(state.get(feed_url, {}).get("next_check_time", datetime.now(timezone.utc).isoformat())).astimezone(timezone.utc)-datetime.now(timezone.utc)).total_seconds()
            for feed_url in feed_urls if not state.get(feed_url, {}).get("skip", False)
        ])
        logging.debug(f"Next poll in {next_poll} seconds")
        await asyncio.sleep(next_poll)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string (str): The connection string.

    Returns:
        Dict[str, str]: Extracted connection parameters.
    """
    config_dict = {
        'sasl.username': '$ConnectionString',
        'sasl.password': connection_string.strip(),
    }
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '')+':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    return config_dict


async def run():
    """
    Main function to handle argparse commands.
    """
        
    global USER_DIR
    global STATE_FILE
    global FEEDSTORE_FILE

    parser = argparse.ArgumentParser(description="RSS/Atom Feed Poller")
    subparsers = parser.add_subparsers(dest="command")
    # Subparser for "process" command
    process_parser = subparsers.add_parser("process", help="Process feeds")
    process_parser.add_argument('--kafka-bootstrap-servers', type=str,
                                help="Comma separated list of Kafka bootstrap servers", default=os.environ.get('KAFKA_BOOTSTRAP_SERVERS') if os.environ.get('KAFKA_BOOTSTRAP_SERVERS') else None)
    process_parser.add_argument('--kafka-topic', type=str, help="Kafka topic to send messages to", default=os.environ.get('KAFKA_TOPIC') if os.environ.get('KAFKA_TOPIC') else None)
    process_parser.add_argument('--sasl-username', type=str, help="Username for SASL PLAIN authentication", default=os.environ.get('SASL_USERNAME') if os.environ.get('SASL_USERNAME') else None)
    process_parser.add_argument('--sasl-password', type=str, help="Password for SASL PLAIN authentication", default=os.environ.get('SASL_PASSWORD') if os.environ.get('SASL_PASSWORD') else None)
    process_parser.add_argument('-c', '--connection-string', type=str,
                                help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string', default=os.environ.get('CONNECTION_STRING') if os.environ.get('CONNECTION_STRING') else None)
    process_parser.add_argument('-l', '--log-level', type=str, help='Log level', default='INFO')
    process_parser.add_argument("urls", metavar="URL", type=str, nargs="*", help="URLs of RSS/Atom or OPML files", default=os.environ.get('FEED_URLS').split(',') if os.environ.get('FEED_URLS') else None)
    process_parser.add_argument('--state-dir', type=str, help="Directory to store state", default=os.environ.get('STATE_DIR') if os.environ.get('STATE_DIR') else USER_DIR)
    # Subparser for "add" command
    add_parser = subparsers.add_parser("add", help="Add feeds to the feed store")
    add_parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="URLs of RSS/Atom or OPML files to add")
    add_parser.add_argument('--state-dir', type=str, help="Directory to store state", default=os.environ.get('STATE_DIR') if os.environ.get('STATE_DIR') else USER_DIR)
    # Subparser for "remove" command
    remove_parser = subparsers.add_parser("remove", help="Remove feeds from the feed store")
    remove_parser.add_argument("urls", metavar="URL", type=str, nargs="+", help="URLs of RSS/Atom files to remove")
    remove_parser.add_argument('--state-dir', type=str, help="Directory to store state", default=os.environ.get('STATE_DIR') if os.environ.get('STATE_DIR') else USER_DIR)

    show_parser = subparsers.add_parser("show", help="Show feeds in the feed store")
    show_parser.add_argument('--state-dir', type=str, help="Directory to store state", default=os.environ.get('STATE_DIR') if os.environ.get('STATE_DIR') else USER_DIR)

    args = parser.parse_args()

    if 'state_dir' in args and args.state_dir:
        USER_DIR = args.state_dir
        STATE_FILE = os.path.join(USER_DIR, ".rss-grabber.json")
        FEEDSTORE_FILE = os.path.join(USER_DIR, ".rss-grabber-feedstore.xml")
        if not os.path.exists(USER_DIR):
            os.makedirs(USER_DIR)
    if args.command == "process":
        if args.log_level:
            logging.getLogger().setLevel(args.log_level)
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

        # Check if required parameters are provided
        if not kafka_bootstrap_servers:
            logging.debug("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
            sys.exit(1)
        if not kafka_topic:
            logging.debug("Error: Kafka topic must be provided either through the command line or connection string.")
            sys.exit(1)
        if not sasl_username or not sasl_password:
            logging.debug("Error: SASL username and password must be provided either through the command line or connection string.")
            sys.exit(1)

        kafka_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        }

        kafka_producer = Producer(kafka_config)
        producer_instance = MicrosoftOpenDataRssFeedsEventProducer(kafka_producer, kafka_topic, 'structured')

        state = load_state()
        feed_urls = load_feedstore()

        for url in args.urls:
            if url.endswith(".opml"):
                opml_content = requests.get(url, timeout=10).content
                opml_tree = listparser.parse(opml_content)
                feed_urls.extend([outline.url for outline in opml_tree.feeds])
            else:
                feed_urls.append(url)

        await poll_feeds(feed_urls, state, producer_instance)
    elif args.command == "add":
        for url in args.urls:
            add_feed(url)
    elif args.command == "remove":
        for url in args.urls:
            remove_feed(url)
    elif args.command == "show":
        feed_urls = load_feedstore()
        for url in feed_urls:
            logging.debug(url)
    else:
        parser.print_help()

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()
