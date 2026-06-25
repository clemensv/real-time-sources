"""AMQP 1.0 companion feeder for eaws-albina."""
from __future__ import annotations
import argparse, asyncio, datetime, importlib, inspect, logging, os, time
from urllib.parse import urlparse
from eaws_albina_core import DEFAULT_LANG, DEFAULT_REGIONS
try:
    from proton import symbol
except Exception:
    symbol = lambda value: value  # type: ignore
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "eaws-albina"
PY_MODULE = "eaws_albina"
logger = logging.getLogger(__name__)
def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name); return default if value is None else value.lower() in {"1", "true", "yes", "on"}
def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}"); scheme = (parsed.scheme or "amqp").lower(); tls = scheme in ("amqps", "ssl", "tls"); return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None
def _producer_class():
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer"); classes = [obj for _, obj in vars(mod).items() if inspect.isclass(obj) and any(name.startswith("send_") for name in dir(obj))]
    if not classes: raise RuntimeError(f"No AMQP producer class found in {mod.__name__}")
    classes.sort(key=lambda cls: (len([name for name in dir(cls) if name.startswith("send_")]), cls.__name__), reverse=True); return classes[0]
def _apply_partition_key_workaround(producer):
    def stamp(msg):
        props = dict(getattr(msg, "properties", None) or {}); ce_subject = props.get("cloudEvents:subject") or getattr(msg, "subject", None)
        if ce_subject:
            annotations = dict(getattr(msg, "annotations", None) or {}); annotations[symbol("x-opt-partition-key")] = str(ce_subject); msg.annotations = annotations
        return msg
    if getattr(producer, "_sender", None) is not None:
        original_send = producer._sender.send; producer._sender.send = lambda msg, *a, **kw: original_send(stamp(msg), *a, **kw)
    if getattr(producer, "_send_queue", None) is not None:
        original_reactor_send = producer._send_via_reactor; producer._send_via_reactor = lambda msg: original_reactor_send(stamp(msg))
    return producer
def _build_amqp_producer(args):
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url); username = args.username or url_user; password = args.password or url_pwd
        if args.port: port = args.port
        if args.tls: tls = True
        address = path or address
    else:
        host = args.host or "localhost"; tls = bool(args.tls) or args.auth_mode == "entra"; port = args.port or (5671 if tls else 5672); username = args.username; password = args.password
    kwargs = dict(host=host, address=address, port=port, content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key: raise RuntimeError('AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY')
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(_producer_class()(**kwargs))
def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    for attempt in range(max_attempts):
        try: return factory()
        except Exception as exc:
            if attempt == max_attempts - 1: raise
            delay = initial_delay * (2 ** attempt); logger.warning('Producer init attempt %d/%d failed: %s. Retrying in %ds...', attempt + 1, max_attempts, exc, delay); time.sleep(delay)
async def _run_live(args: argparse.Namespace, producer) -> None:
    from eaws_albina_core import AlbinaPoller
    regions = [part.strip() for part in args.regions.split(',') if part.strip()]
    poller = AlbinaPoller(last_polled_file=args.last_polled_file, regions=regions, lang=args.lang)
    while True:
        total = 0; today = datetime.date.today()
        for d in [today, today - datetime.timedelta(days=1)]:
            for event in poller.fetch_for_date(d.isoformat()): producer.send_avalanche_bulletin(data=event, _region_id=event.region_id, _country=event.country, _danger_level=event.danger_level); total += 1
        if total: logger.info('Published %d avalanche bulletin(s) via AMQP', total)
        if args.once: break
        await asyncio.sleep(args.polling_interval)
def _add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument('feed_command', nargs='?', default='feed'); parser.add_argument('--broker-url', default=os.getenv('AMQP_BROKER_URL')); parser.add_argument('--host', default=os.getenv('AMQP_HOST')); parser.add_argument('--port', type=int, default=int(os.getenv('AMQP_PORT', '0')) or None); parser.add_argument('--address', default=os.getenv('AMQP_ADDRESS', SOURCE_ID)); parser.add_argument('--username', default=os.getenv('AMQP_USERNAME')); parser.add_argument('--password', default=os.getenv('AMQP_PASSWORD')); parser.add_argument('--tls', action='store_true', default=_env_bool('AMQP_TLS', False)); parser.add_argument('--content-mode', choices=('binary', 'structured'), default=os.getenv('AMQP_CONTENT_MODE', 'binary')); parser.add_argument('--auth-mode', choices=('password', 'entra', 'sas'), default=os.getenv('AMQP_AUTH_MODE', 'password')); parser.add_argument('--entra-audience', default=os.getenv('AMQP_ENTRA_AUDIENCE', DEFAULT_ENTRA_AUDIENCE_SERVICEBUS)); parser.add_argument('--entra-client-id', default=os.getenv('AMQP_ENTRA_CLIENT_ID')); parser.add_argument('--sas-key-name', default=os.getenv('AMQP_SAS_KEY_NAME')); parser.add_argument('--sas-key', default=os.getenv('AMQP_SAS_KEY')); parser.add_argument('--polling-interval', type=int, default=int(os.getenv('POLLING_INTERVAL', '3600'))); parser.add_argument('--last-polled-file', default=os.getenv('STATE_FILE', os.path.expanduser('~/.eaws_albina_amqp_state.json'))); parser.add_argument('--once', action='store_true', default=_env_bool('ONCE_MODE', False)); parser.add_argument('--regions', default=os.getenv('EAWS_ALBINA_REGIONS', ','.join(DEFAULT_REGIONS))); parser.add_argument('--lang', default=os.getenv('EAWS_ALBINA_LANG', DEFAULT_LANG)); return parser
async def _async_main(args: argparse.Namespace) -> None:
    producer = _retry_producer_init(lambda: _build_amqp_producer(args))
    try: await _run_live(args, producer)
    finally:
        close = getattr(producer, 'close', None)
        if close: close()
def main() -> None:
    logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO').upper(), format='%(asctime)s %(levelname)s %(name)s: %(message)s'); parser = _add_common_args(argparse.ArgumentParser(description=f'{SOURCE_ID} AMQP 1.0 bridge')); args = parser.parse_args();
    if args.feed_command != 'feed': parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))
if __name__ == '__main__': main()
