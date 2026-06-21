"""AMQP 1.0 feeder application for NASA FIRMS active fires."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Optional
from urllib.parse import urlparse

from nasa_firms.nasa_firms import DEFAULT_SOURCES, DEFAULT_AREA, DEFAULT_DAY_RANGE, FirmsPoller
from nasa_firms_amqp_producer_amqp_producer.producer import NASAFIRMSAmqpProducer

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


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
def _build_producer(*, host: str, port: int, address: str, use_tls: bool, content_mode: str,
                    auth_mode: str, username, password, entra_audience: str, entra_client_id,
                    sas_key_name, sas_key) -> NASAFIRMSAmqpProducer:
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return NASAFIRMSAmqpProducer(host=host, address=address, port=port, content_mode=content_mode,
                                     credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP_AUTH_MODE=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return NASAFIRMSAmqpProducer(host=host, address=address, port=port, content_mode=content_mode,
                                     sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return NASAFIRMSAmqpProducer(host=host, address=address, port=port, username=username,
                                 password=password, content_mode=content_mode, use_tls=use_tls)


class _AmqpProducerAdapter:
    """Exposes the generated Kafka producer's ``send_*`` surface but routes to AMQP."""

    def __init__(self, producer: NASAFIRMSAmqpProducer):
        self.producer = self
        self._producer = producer
        self._failures: list[BaseException] = []

    def send_nasa_firms_fire_detection(self, **kwargs: Any) -> None:
        self._send(self._producer.send_fire_detection, kwargs)

    def send_nasa_firms_data_availability(self, **kwargs: Any) -> None:
        self._send(self._producer.send_data_availability, kwargs)

    def _send(self, send_fn: Any, kwargs: dict[str, Any]) -> None:
        kwargs.pop("flush_producer", None)
        call = {
            "data": kwargs["data"],
            "_source_uri": kwargs["_source_uri"],
            "_source": kwargs["_source"],
            "_record_id": kwargs["_record_id"],
        }
        if "_time" in kwargs:
            call["_time"] = kwargs["_time"]
        if "content_type" in kwargs:
            call["content_type"] = kwargs["content_type"]
        try:
            send_fn(**call)
        except BaseException as exc:  # pylint: disable=broad-except
            self._failures.append(exc)
            logger.exception("AMQP publish failed", exc_info=exc)

    def flush(self) -> None:
        if self._failures:
            raise RuntimeError("one or more AMQP publishes failed") from self._failures[0]

    def close(self) -> None:
        close = getattr(self._producer, "close", None)
        if close is not None:
            close()


async def feed(poller: FirmsPoller, broker_host: str, broker_port: int, *,
               username: Optional[str] = None, password: Optional[str] = None,
               tls: bool = False, content_mode: str = "binary", once: bool = False) -> None:
    producer = _retry_producer_init(lambda: _build_producer(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "nasa-firms")),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )
    adapter = _AmqpProducerAdapter(producer)
    poller.event_producer = adapter
    try:
        await poller.poll_and_send(once=once)
        adapter.flush()
    finally:
        adapter.close()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="NASA FIRMS AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    parser.add_argument("--map-key", default=os.getenv("FIRMS_MAP_KEY"))
    parser.add_argument("--last-polled-file", default=os.getenv("FIRMS_LAST_POLLED_FILE", os.path.expanduser("~/.nasa_firms_seen_amqp.json")))
    parser.add_argument("--sources", default=os.getenv("FIRMS_SOURCES"))
    parser.add_argument("--area", default=os.getenv("FIRMS_AREA", DEFAULT_AREA))
    parser.add_argument("--day-range", type=int, default=int(os.getenv("FIRMS_DAY_RANGE", str(DEFAULT_DAY_RANGE))))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    if not args.map_key:
        parser.error("a FIRMS MAP_KEY is required (--map-key or FIRMS_MAP_KEY)")
    host, port, tls = _parse_broker_url(args.broker_url)
    sources = args.sources.split(",") if args.sources else list(DEFAULT_SOURCES)
    poller = FirmsPoller(map_key=args.map_key, last_polled_file=args.last_polled_file,
                         sources=sources, area=args.area, day_range=args.day_range)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None,
                     tls=tls, content_mode=args.content_mode, once=args.once))


if __name__ == "__main__":
    main()
