
import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(producer_cls, *, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)


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
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)

import asyncio
import dataclasses
import logging
import time

from vatsim.vatsim import VatsimBridge, _load_state, _save_state
from vatsim_amqp_producer_data import ControllerPosition, NetworkStatus, PilotPosition
from vatsim_amqp_producer_amqp_producer.producer import NetVatsimAmqpProducer

logger = logging.getLogger(__name__)


def _pilot(obj) -> PilotPosition: return PilotPosition(**dataclasses.asdict(obj))
def _controller(obj) -> ControllerPosition: return ControllerPosition(**dataclasses.asdict(obj))
def _status(obj) -> NetworkStatus: return NetworkStatus(**dataclasses.asdict(obj))


async def _publish_poll_cycle(bridge: VatsimBridge, producer: NetVatsimAmqpProducer, previous_pilots: dict[str, str], previous_controllers: dict[str, str]) -> tuple[int, int]:
    data = await asyncio.to_thread(bridge.fetch_data)
    general = data.get("general", {})
    pilots = data.get("pilots", [])
    controllers = data.get("controllers", [])
    status = _status(bridge.build_network_status(general, len(pilots), len(controllers)))
    producer.send_facility_status(data=status, _callsign=status.callsign, _facility=status.facility)
    pilot_count = 0
    for raw_pilot in pilots:
        callsign = raw_pilot.get("callsign", "")
        if not callsign: continue
        fingerprint = bridge.pilot_fingerprint(raw_pilot)
        if previous_pilots.get(callsign) == fingerprint: continue
        try:
            pilot = _pilot(bridge.parse_pilot(raw_pilot))
            producer.send_pilot_position(data=pilot, _callsign=pilot.callsign)
            pilot_count += 1
        except Exception as exc:
            logger.error("Error publishing pilot %s: %s", callsign, exc)
        previous_pilots[callsign] = fingerprint
    controller_count = 0
    for raw_controller in controllers:
        callsign = raw_controller.get("callsign", "")
        if not callsign: continue
        fingerprint = bridge.controller_fingerprint(raw_controller)
        if previous_controllers.get(callsign) == fingerprint: continue
        try:
            controller = _controller(bridge.parse_controller(raw_controller))
            producer.send_controller_position(data=controller, _callsign=controller.callsign)
            controller_count += 1
        except Exception as exc:
            logger.error("Error publishing controller %s: %s", callsign, exc)
        previous_controllers[callsign] = fingerprint
    return pilot_count, controller_count


def _publish_sample(producer: NetVatsimAmqpProducer) -> None:
    status = NetworkStatus(callsign="status", facility="network", update_timestamp="2026-01-01T00:00:00.000000Z", connected_clients=2, unique_users=2, pilot_count=1, controller_count=1)
    pilot = PilotPosition(cid=1001, callsign="SAMPLE1", latitude=47.45, longitude=-122.31, altitude=12000, groundspeed=310, heading=90, transponder="7000", qnh_mb=1013, flight_rules="I", aircraft_short="B738", departure="KSEA", arrival="KPDX", route="DCT", cruise_altitude="12000", pilot_rating=1, last_updated="2026-01-01T00:00:00.000000Z")
    controller = ControllerPosition(cid=2001, callsign="SEA_CTR", frequency="124.850", facility=6, rating=8, text_atis="sample", last_updated="2026-01-01T00:00:00.000000Z")
    producer.send_facility_status(data=status, _callsign=status.callsign, _facility=status.facility)
    producer.send_pilot_position(data=pilot, _callsign=pilot.callsign)
    producer.send_controller_position(data=controller, _callsign=controller.callsign)


async def feed(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args, NetVatsimAmqpProducer)
    if args.sample_mode:
        try:
            _publish_sample(producer)
            return
        finally:
            producer.close()
    bridge = VatsimBridge()
    state = _load_state(args.state_file)
    previous_pilots = state.get("pilots", {})
    previous_controllers = state.get("controllers", {})
    try:
        while True:
            started = time.monotonic()
            pilot_count, controller_count = await _publish_poll_cycle(bridge, producer, previous_pilots, previous_controllers)
            _save_state(args.state_file, {"pilots": previous_pilots, "controllers": previous_controllers})
            elapsed = time.monotonic() - started
            logger.info("Published VATSIM status, %d pilots, %d controllers to AMQP in %.1fs", pilot_count, controller_count, elapsed)
            if args.once: break
            await asyncio.sleep(max(0, args.polling_interval - elapsed))
    finally:
        producer.close()


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
def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="VATSIM AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    add_amqp_arguments(parser, "vatsim")
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "60")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser("~/.vatsim_amqp_state.json")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1","true","yes"))
    parser.add_argument("--sample-mode", action="store_true", default=os.getenv("VATSIM_SAMPLE_MODE", "").lower() in ("1","true","yes"))
    args = parser.parse_args()
    if args.feed_command != "feed": parser.error("only the 'feed' command is supported")
    asyncio.run(feed(args))

if __name__ == "__main__": main()
