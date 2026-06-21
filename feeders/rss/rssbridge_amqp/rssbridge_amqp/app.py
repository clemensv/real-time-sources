"""AMQP feeder for RSS/Atom feeds."""
from __future__ import annotations
import argparse, asyncio, logging, os
from urllib.parse import urlparse
from rssbridge.rssbridge import load_feedstore, load_state, poll_feeds, save_feedstore, save_state
import rssbridge.rssbridge as bridge
from rssbridge_amqp_producer_data.microsoft.opendata.rssfeeds.feeditem import FeedItem
from rssbridge_amqp_producer_amqp_producer.producer import MicrosoftOpenDataRssFeedsAmqpProducer
logger=logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _parse_amqp_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))



def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def create_amqp_producer(args: argparse.Namespace, producer_cls):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode in ("entra", "sas")
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, credential=credential, entra_audience=args.entra_audience, use_tls=tls)
    if args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key, use_tls=tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=args.content_mode, use_tls=tls)

class RssAmqpProducer:
    def __init__(self, producer): self.producer=producer
    def send_microsoft_open_data_rss_feeds_feed_item(self, *, _sourceurl: str, _item_id: str, data, flush_producer: bool=False):
        self.producer.send_feed_item(data=data, _sourceurl=_sourceurl, _item_id=_item_id)
async def run():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    p=argparse.ArgumentParser(description='RSS/Atom AMQP bridge'); p.add_argument('process', nargs='?', default='process'); p.add_argument('urls', nargs='*', default=os.getenv('FEED_URLS','').split(',') if os.getenv('FEED_URLS') else []); add_amqp_arguments(p,'rss'); p.add_argument('--state-dir', default=os.getenv('STATE_DIR', os.path.expanduser('~'))); p.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    args=p.parse_args();
    if args.process not in ('process','feed'): p.error("only 'process'/'feed' is supported")
    bridge.USER_DIR=args.state_dir; bridge.STATE_FILE=os.path.join(args.state_dir,'.rss-grabber.json'); bridge.FEEDSTORE_FILE=os.path.join(args.state_dir,'.rss-grabber-feedstore.xml'); os.makedirs(args.state_dir, exist_ok=True)
    producer=_retry_producer_init(lambda: create_amqp_producer(args, MicrosoftOpenDataRssFeedsAmqpProducer)); wrapper=RssAmqpProducer(producer)
    try:
        feed_urls=load_feedstore(); feed_urls.extend([u for u in args.urls if u]);
        if args.urls: save_feedstore(list(dict.fromkeys(feed_urls)))
        if os.getenv('RSS_SAMPLE_MODE','').lower() in ('1','true','yes'):
            wrapper.send_microsoft_open_data_rss_feeds_feed_item(_sourceurl='https://example.invalid/rss.xml', _item_id='sample-item', data=FeedItem(feed_slug='sample-feed', item='sample-item', id='sample-item', author=None, publisher=None, summary=None, title=None, source=None, content=None, enclosures=None, published=None, updated=None, created=None, expired=None, license=None, comments=None, contributors=None, links=None)); return
        state=load_state(); unique=list(dict.fromkeys(feed_urls));
        if args.once:
            for feed_url in unique: bridge.process_feed(feed_url, state, wrapper)
            save_state(state)
        else: await poll_feeds(unique, state, wrapper)
    finally: producer.close()
def main(): asyncio.run(run())
if __name__=='__main__': main()
