"""AMQP 1.0 feeder for Seattle Street Closures.

Reuses the upstream HTTP polling logic from the existing
``seattle_street_closures`` Kafka bridge (imported as the transport-agnostic
"core" package) and pushes change-detected ``StreetClosure`` events into
AMQP 1.0 via the xrcg-generated :class:`USWASeattleStreetClosuresAmqpProducer`.

Authentication modes:

* ``password`` -- SASL PLAIN against generic AMQP 1.0 brokers (RabbitMQ,
  Artemis, the local Service Bus emulator with username/password).
* ``entra``    -- AMQP CBS put-token with a JWT acquired from Microsoft
  Entra ID (``DefaultAzureCredential`` or ``ManagedIdentityCredential``
  when ``AMQP_ENTRA_CLIENT_ID`` is provided). Targets Azure Service Bus.
* ``sas``      -- AMQP CBS put-token with a SAS token signed locally from
  ``AMQP_SAS_KEY_NAME``/``AMQP_SAS_KEY``. Targets the Service Bus emulator
  and SAS-only namespaces.
"""

from __future__ import annotations

import argparse
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

from seattle_street_closures.seattle_street_closures import (
    DEFAULT_POLL_INTERVAL_SECONDS,
    SeattleStreetClosuresBridge,
    closure_digest,
)
from seattle_street_closures_amqp_producer_amqp_producer.producer import (
    USWASeattleStreetClosuresAmqpProducer,
)

logger = logging.getLogger("seattle_street_closures_amqp")

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _parse_amqp_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument(
        "--tls",
        action="store_true",
        default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"),
    )
    parser.add_argument(
        "--content-mode",
        choices=("binary", "structured"),
        default=os.getenv("AMQP_CONTENT_MODE", "binary"),
    )
    parser.add_argument(
        "--auth-mode",
        choices=("password", "entra", "sas"),
        default=os.getenv("AMQP_AUTH_MODE", "password"),
    )
    parser.add_argument(
        "--entra-audience",
        default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
    )
    parser.add_argument(
        "--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID")
    )
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(
    args: argparse.Namespace, producer_cls
) -> USWASeattleStreetClosuresAmqpProducer:
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

        credential = (
            ManagedIdentityCredential(client_id=args.entra_client_id)
            if args.entra_client_id
            else DefaultAzureCredential()
        )
        return producer_cls(
            host=host,
            address=address,
            port=port,
            content_mode=args.content_mode,
            credential=credential,
            entra_audience=args.entra_audience,
            use_tls=tls,
        )
    if args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError(
                "AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY"
            )
        return producer_cls(
            host=host,
            address=address,
            port=port,
            content_mode=args.content_mode,
            sas_key_name=args.sas_key_name,
            sas_key=args.sas_key,
            use_tls=tls,
        )
    return producer_cls(
        host=host,
        address=address,
        port=port,
        username=username,
        password=password,
        content_mode=args.content_mode,
        use_tls=tls,
    )


def _publish_mock(producer: USWASeattleStreetClosuresAmqpProducer) -> None:
    """Emit one synthetic record so smoke tests can assert delivery."""
    from seattle_street_closures_amqp_producer_data import StreetClosure

    closure = StreetClosure(
        closure_id="mock-permit|mock-segkey|2026-01-01|2026-01-02",
        permit_number="mock-permit",
        permit_type="utility",
        project_name="Mock project",
        project_description="Mock street closure for emulator smoke test",
        start_date="2026-01-01",
        end_date="2026-01-02",
        sunday=None,
        monday="07:00-19:00",
        tuesday="07:00-19:00",
        wednesday="07:00-19:00",
        thursday="07:00-19:00",
        friday="07:00-19:00",
        saturday=None,
        street_on="Mock Street",
        street_from="Mock Ave",
        street_to="Mock Blvd",
        segkey="mock-segkey",
        geometry_json=None,
    )
    producer.send_amqp(data=closure, _closure_id=closure.closure_id)


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
def feed(
    producer: USWASeattleStreetClosuresAmqpProducer,
    state_file: str,
    polling_interval: int,
    once: bool,
) -> None:
    """Run the AMQP polling loop until ``once`` triggers an early exit."""
    if os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"):
        try:
            _publish_mock(producer)
        finally:
            producer.close()
        return

    bridge = SeattleStreetClosuresBridge(state_file=state_file)
    try:
        while True:
            try:
                start = datetime.now(timezone.utc)
                closures = bridge.fetch_closures()
                current_digests = {}
                sent = 0
                for closure in closures:
                    digest = closure_digest(closure)
                    current_digests[closure.closure_id] = digest
                    if bridge.previous_digests.get(closure.closure_id) == digest:
                        continue
                    producer.send_amqp(data=closure, _closure_id=closure.closure_id)  # type: ignore[arg-type]
                    sent += 1
                bridge.previous_digests = current_digests
                bridge.save_state()
                elapsed = (datetime.now(timezone.utc) - start).total_seconds()
                logger.info(
                    "Fetched %d closures, sent %d new/changed AMQP events in %.1fs",
                    len(closures),
                    sent,
                    elapsed,
                )
            except KeyboardInterrupt:
                logger.info("Interrupt received, exiting")
                break
            except Exception:
                logger.exception("Error during Seattle street closure poll")
            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break
            sleep_for = max(0, polling_interval)
            if sleep_for:
                time.sleep(sleep_for)
    finally:
        producer.close()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Seattle Street Closures -> AMQP 1.0 bridge"
    )
    parser.add_argument("command", nargs="?", default="feed")
    add_amqp_arguments(parser, "seattle-street-closures")
    parser.add_argument(
        "--state-file",
        default=os.getenv(
            "SEATTLE_STREET_CLOSURES_STATE_FILE",
            os.getenv("STATE_FILE", ""),
        ),
    )
    parser.add_argument(
        "--polling-interval",
        type=int,
        default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))),
    )
    parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
    )
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.error("only the 'feed' command is supported")
    producer = _retry_producer_init(lambda: create_amqp_producer(args, USWASeattleStreetClosuresAmqpProducer))
    feed(producer, args.state_file, args.polling_interval, args.once)


if __name__ == "__main__":
    main()
