"""AMQP feeder for Carbon Intensity UK."""
from __future__ import annotations
import argparse, asyncio, logging, os
from urllib.parse import urlparse
from carbon_intensity.carbon_intensity import CarbonIntensityPoller, POLL_INTERVAL_SECONDS
from carbon_intensity_amqp_producer_amqp_producer.producer import UkOrgCarbonintensityAmqpProducer
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

def _ce_timestamp(value): return value.isoformat().replace('+00:00','Z')
class _NoopProducer:
    def flush(self):
        return None

class CarbonIntensityAmqpPoller(CarbonIntensityPoller):
    def __init__(self, producer, last_polled_file: str):
        producer.producer = _NoopProducer()
        self.kafka_topic=''; self.last_polled_file=last_polled_file; self.producer=producer; self.regional_producer=producer
    def emit_intensity(self, intensity): self.producer.send_intensity(data=intensity, _period_from=_ce_timestamp(intensity.period_from), _ce_id=intensity.ce_id)
    def emit_generation_mix(self, gen_mix): self.producer.send_generation_mix(data=gen_mix, _period_from=_ce_timestamp(gen_mix.period_from), _ce_id=gen_mix.ce_id)
    def emit_regional(self, regional): self.producer.send_regional_intensity(data=regional, _region_id=str(regional.region_id), _ce_id=regional.ce_id)
    async def poll_and_send_async(self, once=False):
        state=self.load_state(); last_period=state.get('last_period_from')
        while True:
            emitted_key=self.poll_once()
            if emitted_key and emitted_key != last_period:
                last_period=emitted_key; state['last_period_from']=last_period; self.save_state(state)
            if once: return
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
async def feed(producer, state_file: str, once: bool):
    try:
        await CarbonIntensityAmqpPoller(producer, state_file or os.path.expanduser('~/.carbon_intensity_amqp_last_polled.json')).poll_and_send_async(once=once)
    finally:
        producer.close()
def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    p=argparse.ArgumentParser(description='Carbon Intensity AMQP bridge'); p.add_argument('feed', nargs='?', default='feed'); add_amqp_arguments(p,'carbon-intensity'); p.add_argument('--state-file', default=os.getenv('CARBON_INTENSITY_AMQP_STATE_FILE', os.getenv('STATE_FILE',''))); p.add_argument('--once', action='store_true', default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
    args=p.parse_args();
    if args.feed!='feed': p.error("only the 'feed' command is supported")
    asyncio.run(feed(create_amqp_producer(args, UkOrgCarbonintensityAmqpProducer), args.state_file, args.once))
if __name__=='__main__': main()
