"""AMQP feeder for Australian wildfires."""
from __future__ import annotations
import argparse, asyncio, dataclasses, logging, os, re, unicodedata
from typing import Optional
from urllib.parse import urlparse
from australia_wildfires.australia_wildfires import AustraliaWildfiresAPI
from australia_wildfires_amqp_producer_data import FireIncident
from australia_wildfires_amqp_producer_amqp_producer.producer import AUGovEmergencyWildfiresAmqpProducer
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

def topic_slug(value: object, default: str = "unknown") -> str:
    text=str(value or '').strip();
    if not text: return default
    normalized=unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode('ascii')
    return re.sub(r'[^a-zA-Z0-9]+','-',normalized).strip('-').lower() or default
def topic_safe_id(value: object, default: str = "unknown") -> str:
    text=str(value or '').strip();
    if not text: return default
    normalized=unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode('ascii')
    return re.sub(r'[^A-Za-z0-9._-]+','-',normalized).strip('-._') or default
def _to_incident(incident) -> FireIncident:
    payload=dataclasses.asdict(incident); payload['state']=topic_slug(payload.get('state')); payload['status']=topic_slug(payload.get('status')); payload['incident_id']=topic_safe_id(payload.get('incident_id')); return FireIncident(**payload)
async def feed(producer, *, once=False, polling_interval=300):
    api=AustraliaWildfiresAPI(polling_interval=polling_interval)
    try:
        while True:
            if os.getenv('AUSTRALIA_WILDFIRES_SAMPLE_MODE','').lower() in ('1','true','yes'):
                incidents=[FireIncident(incident_id='sample-incident-001',state='nsw',title='Sample Fire Incident',alert_level='Advice',status='under-control',location='Sample Location, NSW',latitude=-33.0,longitude=151.0,size_hectares=10.5,type='Bush Fire',responsible_agency='Rural Fire Service',updated='2026-01-01T00:00:00+00:00',source_url='https://www.rfs.nsw.gov.au/feeds/majorIncidents.json')]
            else:
                incidents=[]; incidents.extend(_to_incident(i) for i in api.fetch_nsw_incidents()); incidents.extend(_to_incident(i) for i in api.fetch_vic_incidents()); incidents.extend(_to_incident(i) for i in api.fetch_qld_incidents())
            for item in incidents:
                producer.send_fire_incident(data=item, _state=item.state, _incident_id=item.incident_id)
            logger.info('Published %d Australian wildfire incidents to AMQP', len(incidents))
            if once: return
            await asyncio.sleep(max(1,polling_interval))
    finally:
        producer.close()
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    p=argparse.ArgumentParser(description='Australian wildfires AMQP bridge'); p.add_argument('feed', nargs='?', default='feed'); add_amqp_arguments(p,'australia-wildfires'); p.add_argument('--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL','300'))); p.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    args=p.parse_args();
    if args.feed!='feed': p.error("only the 'feed' command is supported")
    asyncio.run(feed(create_amqp_producer(args, AUGovEmergencyWildfiresAmqpProducer), once=args.once, polling_interval=args.polling_interval))
if __name__=='__main__': main()
