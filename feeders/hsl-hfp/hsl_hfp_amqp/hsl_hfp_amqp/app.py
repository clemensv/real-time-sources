"""HSL HFP -> AMQP 1.0 bridge.

Re-publishes the HSL HFP firehose as AMQP 1.0 CloudEvents. Reference (GTFS) and
telemetry events are written to a single AMQP address; the CloudEvents type,
source, and subject travel as AMQP message properties (binary mode) or in the
JSON body (structured mode), and the upstream ``transport_mode`` / ``route_id``
topic levels are carried as AMQP application-properties for broker-side routing.

Three auth modes, selected at runtime:

* **Generic AMQP 1.0** (RabbitMQ AMQP 1.0 plugin, ActiveMQ Artemis, Qpid
  Dispatch, ...): SASL PLAIN over ``amqp://`` (5672) or ``amqps://`` (5671).
* **Azure Service Bus / Event Hubs** with Entra ID: ``--auth-mode entra`` uses
  ``DefaultAzureCredential`` and the AMQP CBS ``$cbs`` link (``put-token``).
* **SAS** (``--auth-mode sas``): AMQP CBS with a Shared Access Signature, for
  SAS-only namespaces or the Service Bus emulator.

The generated AMQP producers send synchronously; a lock serializes the
telemetry thread and the periodic reference-refresh thread onto each producer's
proton connection.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import threading
import time
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlparse

from hsl_hfp.config import HFP_FEED_URL, FeedConfig
from hsl_hfp.runner import BridgeRunner
from hsl_hfp_amqp_producer_data import (
    DriverBlockEvent,
    Operator,
    Route,
    Stop,
    TrafficLightEvent,
    VehicleEvent,
)
from hsl_hfp_amqp_producer_amqp_producer.producer import (
    FiHslGtfsOperatorAmqpProducer,
    FiHslGtfsRouteAmqpProducer,
    FiHslGtfsStopAmqpProducer,
    FiHslHfpAmqpProducer,
)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

logger = logging.getLogger(__name__)


class AmqpSink:
    """Publishes HFP reference + telemetry events as AMQP 1.0 CloudEvents.

    The manifest splits the four event identities into four AMQP producers
    (vehicle telemetry plus operator / route / stop reference), each carrying its
    own subject template. They all publish to the same AMQP address; a shared
    lock serializes the telemetry thread and the periodic reference-refresh
    thread across every proton connection.
    """

    def __init__(self, tele: FiHslHfpAmqpProducer,
                 operator: FiHslGtfsOperatorAmqpProducer,
                 route: FiHslGtfsRouteAmqpProducer,
                 stop: FiHslGtfsStopAmqpProducer,
                 feed_url: str) -> None:
        self._tele = tele
        self._operator = operator
        self._route = route
        self._stop = stop
        self._feed = feed_url
        self._lock = threading.Lock()

    # -- reference ----------------------------------------------------------

    def send_operator(self, operator_id: str, kwargs: Dict[str, Any]) -> None:
        with self._lock:
            self._operator.send_operator(
                data=Operator(**kwargs), _feedurl=self._feed, _operator_id=operator_id)

    def send_route(self, route_id: str, kwargs: Dict[str, Any]) -> None:
        with self._lock:
            self._route.send_route(
                data=Route(**kwargs), _feedurl=self._feed, _route_id=route_id)

    def send_stop(self, stop_id: str, kwargs: Dict[str, Any]) -> None:
        with self._lock:
            self._stop.send_stop(
                data=Stop(**kwargs), _feedurl=self._feed, _stop_id=stop_id)

    # -- telemetry ----------------------------------------------------------

    def _send_telemetry(self, event_type: str, params: Dict[str, Any], data: Any) -> None:
        method = getattr(self._tele, f"send_{event_type}")
        with self._lock:
            method(
                data=data, _feedurl=self._feed,
                _operator_id=params["operator_id"],
                _vehicle_number=params["vehicle_number"],
                _transport_mode=str(params.get("transport_mode", "")),
                _route_id=str(params.get("route_id", "")))

    def send_vehicle(self, event_type: str, params: Dict[str, Any],
                     kwargs: Dict[str, Any]) -> None:
        self._send_telemetry(event_type, params, VehicleEvent(**kwargs))

    def send_traffic_light(self, event_type: str, params: Dict[str, Any],
                           kwargs: Dict[str, Any]) -> None:
        self._send_telemetry(event_type, params, TrafficLightEvent(**kwargs))

    def send_driver_block(self, event_type: str, params: Dict[str, Any],
                          kwargs: Dict[str, Any]) -> None:
        self._send_telemetry(event_type, params, DriverBlockEvent(**kwargs))

    def flush(self) -> None:
        return

    def poll(self) -> None:
        return

    def close(self) -> None:
        for producer in (self._tele, self._operator, self._route, self._stop):
            try:
                producer.close()
            except Exception:  # pylint: disable=broad-except
                pass


def _retry_producer_init(factory, max_attempts: int = 5, initial_delay: int = 10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as exc:  # pylint: disable=broad-except
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                           attempt + 1, max_attempts, exc, delay)
            time.sleep(delay)


def _build_producer(
    cls,
    *,
    host: str,
    port: int,
    address: str,
    use_tls: bool,
    content_mode: str,
    auth_mode: str,
    username: Optional[str],
    password: Optional[str],
    entra_audience: str,
    entra_client_id: Optional[str],
    sas_key_name: Optional[str],
    sas_key: Optional[str],
):
    if auth_mode == "entra":
        try:
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "auth-mode=entra requires azure-identity. Reinstall the package."
            ) from exc
        credential = (ManagedIdentityCredential(client_id=entra_client_id)
                      if entra_client_id else DefaultAzureCredential())
        logger.info("Using Entra ID auth via CBS (host=%s, address=%s, audience=%s)",
                    host, address, entra_audience)
        return cls(host=host, address=address, port=port,
                   content_mode=content_mode,  # type: ignore[arg-type]
                   credential=credential, entra_audience=entra_audience, use_tls=use_tls)

    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError(
                "auth-mode=sas requires --sas-key-name and --sas-key "
                "(or AMQP_SAS_KEY_NAME / AMQP_SAS_KEY env vars).")
        logger.info("Using SAS auth via CBS (host=%s, address=%s, tls=%s, key_name=%s)",
                    host, address, use_tls, sas_key_name)
        return cls(host=host, address=address, port=port,
                   content_mode=content_mode,  # type: ignore[arg-type]
                   sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)

    logger.info("Using SASL PLAIN auth (host=%s:%s, address=%s, tls=%s, user=%s)",
                host, port, address, use_tls, username or "<anonymous>")
    return cls(host=host, address=address, port=port,
               username=username, password=password,
               content_mode=content_mode,  # type: ignore[arg-type]
               use_tls=use_tls)


def _parse_broker_url(url: str) -> Tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HSL HFP -> AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Stream HFP telemetry as CloudEvents over AMQP 1.0")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"),
                             help="AMQP broker URL (e.g. amqp://localhost:5672/hsl-hfp, "
                                  "amqps://ns.servicebus.windows.net:5671/hsl-hfp)")
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"),
                             help="AMQP broker hostname (alternative to --broker-url)")
    feed_parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None,
                             help="AMQP broker port (default 5672, or 5671 with --tls)")
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "hsl-hfp"),
                             help="AMQP address (queue or topic name). Default: hsl-hfp")
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--content-mode", type=str,
                             default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"],
                             help="CloudEvents content mode (default: binary)")
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Emit reference data and a bounded telemetry sample, then exit.")
    feed_parser.add_argument("--auth-mode", type=str,
                             default=os.getenv("AMQP_AUTH_MODE", "password"),
                             choices=["password", "entra", "sas"],
                             help="Authentication mode: 'password' (SASL PLAIN), 'entra' (AMQP CBS "
                                  "with Azure Entra ID), or 'sas' (AMQP CBS with a Shared Access "
                                  "Signature).")
    feed_parser.add_argument("--entra-audience", type=str,
                             default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
                             help=f"Entra token audience. Default: {DEFAULT_ENTRA_AUDIENCE_SERVICEBUS} "
                                  f"(Service Bus). Use {DEFAULT_ENTRA_AUDIENCE_EVENTHUBS} for Event Hubs.")
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"),
                             help="Optional user-assigned managed identity client id.")
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"),
                             help="SAS policy / key name. Required with --auth-mode=sas.")
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"),
                             help="SAS key value (base64). Required with --auth-mode=sas.")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
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
        parser.error("--address is required (or include it in --broker-url path)")

    build_kwargs = dict(
        host=host, port=port, address=address, use_tls=tls,
        content_mode=args.content_mode, auth_mode=args.auth_mode,
        username=username, password=password,
        entra_audience=args.entra_audience, entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name, sas_key=args.sas_key,
    )
    tele = _retry_producer_init(lambda: _build_producer(FiHslHfpAmqpProducer, **build_kwargs))
    operator = _retry_producer_init(lambda: _build_producer(FiHslGtfsOperatorAmqpProducer, **build_kwargs))
    route = _retry_producer_init(lambda: _build_producer(FiHslGtfsRouteAmqpProducer, **build_kwargs))
    stop = _retry_producer_init(lambda: _build_producer(FiHslGtfsStopAmqpProducer, **build_kwargs))
    sink = AmqpSink(tele, operator, route, stop, HFP_FEED_URL)

    config = FeedConfig.from_env()
    if args.once:
        config.once = True

    runner = BridgeRunner(config, feed_url=HFP_FEED_URL)
    logger.info("Starting HSL HFP -> AMQP bridge (address=%s, auth=%s, content_mode=%s)",
                address, args.auth_mode, args.content_mode)
    try:
        runner.run(sink)
    finally:
        sink.close()


if __name__ == "__main__":
    main()
