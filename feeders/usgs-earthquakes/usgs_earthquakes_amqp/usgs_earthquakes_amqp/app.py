"""AMQP feeder application for USGS Earthquakes → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import urlparse


from usgs_earthquakes.usgs_earthquakes import DEFAULT_FEED, USGSEarthquakePoller


from usgs_earthquakes_amqp_producer_amqp_producer.producer import USGSEarthquakesAmqpProducer

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


class _AmqpPublishFacade:
    def __init__(self, producers):
        self._producers = list(producers)

    def close(self):
        for producer in self._producers:
            close = getattr(producer, "close", None)
            if close is not None:
                close()

    def __getattr__(self, name: str):
        if not name.startswith("publish_"):
            raise AttributeError(name)
        suffix = name.split("_mqtt_", 1)[1] if "_mqtt_" in name else name[len("publish_"):]
        parts = suffix.split("_")
        target = None
        for start in range(len(parts)):
            send_name = "send_" + "_".join(parts[start:])
            for producer in self._producers:
                target = getattr(producer, send_name, None)
                if target is not None:
                    break
            if target is not None:
                break
        if target is None:
            raise AttributeError(f"send_{suffix}")

        async def _publish(**kwargs):
            accepted = set(target.__code__.co_varnames[:target.__code__.co_argcount])
            call = {}
            for key, value in kwargs.items():
                if key in ("data", "content_type"):
                    call[key] = value
                elif key in ("flush_producer", "qos", "retain"):
                    continue
                else:
                    candidate = "_" + key.lstrip("_")
                    if candidate in accepted:
                        call[candidate] = value
            target(**call)

        return _publish


def _build_publisher(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username, password, entra_audience: str, entra_client_id, sas_key_name, sas_key):
    producers = []
    for cls in (USGSEarthquakesAmqpProducer,):
        if auth_mode == "entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
            producer = _retry_producer_init(lambda: cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls))  # type: ignore[arg-type]
        elif auth_mode == "sas":
            if not sas_key_name or not sas_key:
                raise RuntimeError("AMQP_AUTH_MODE=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
            producer = cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)  # type: ignore[arg-type]
        else:
            producer = cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)  # type: ignore[arg-type]
        producers.append(producer)
    return _AmqpPublishFacade(producers)


class _MqttProducerAdapter:
    def __init__(self, client: Any):
        self.producer = self
        self._client = client
        self._tasks: set[asyncio.Task[None]] = set()
        self._failures: list[BaseException] = []
        self._semaphore = asyncio.Semaphore(64)

    def send_usgs_earthquakes_event(self, **kwargs: Any) -> None:
        kwargs.pop("flush_producer", None)
        data = kwargs["data"]
        normalized = {key[1:] if key.startswith("_") else key: value for key, value in kwargs.items()}
        normalized["magnitude_bucket"] = data.magnitude_bucket
        task = asyncio.create_task(self._publish(**normalized))
        self._tasks.add(task)
        task.add_done_callback(self._finish_task)

    async def _publish(self, **kwargs: Any) -> None:
        async with self._semaphore:
            await self._client.publish_usgs_earthquakes_event(**kwargs)

    def _finish_task(self, task: asyncio.Task[None]) -> None:
        self._tasks.discard(task)
        try:
            task.result()
        except BaseException as exc:  # pylint: disable=broad-except
            self._failures.append(exc)
            logger.exception("AMQP publish failed", exc_info=exc)

    def flush(self) -> Awaitable[None]:
        return self.drain()

    async def drain(self) -> None:
        while self._tasks:
            await asyncio.gather(*list(self._tasks), return_exceptions=True)
        if self._failures:
            raise RuntimeError("one or more AMQP publishes failed") from self._failures[0]


async def feed(poller: USGSEarthquakePoller, broker_host: str, broker_port: int, *, username: Optional[str] = None, password: Optional[str] = None, tls: bool = False, client_id: Optional[str] = None, content_mode: str = "binary", once: bool = False) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "usgs-earthquakes"),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )
    adapter = _MqttProducerAdapter(mqtt_client)
    poller.event_producer = adapter
    try:
        await poller.poll_and_send(once=once)
        await adapter.drain()
    finally:
        mqtt_client.close()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls


def _resolve_broker_endpoint(broker_url: Optional[str], broker_host: Optional[str], broker_port: Optional[int], tls: bool) -> tuple[str, int, bool]:
    if broker_url:
        return _parse_broker_url(broker_url)
    return broker_host or "localhost", broker_port or (5671 if tls else 5672), tls



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
    parser = argparse.ArgumentParser(description="USGS Earthquakes AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--broker-host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--broker-port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument(
        "--last-polled-file",
        default=os.getenv("USGS_EARTHQUAKES_LAST_POLLED_FILE", os.path.expanduser("~/.usgs_earthquakes_seen_amqp.json")),
        help="Path to the persisted checkpoint and dedupe state file for the USGS Earthquakes AMQP bridge.",
    )
    parser.add_argument(
        "--feed",
        default=os.getenv("USGS_EARTHQUAKES_FEED", DEFAULT_FEED),
        help="USGS GeoJSON summary feed to poll, for example all_hour, all_day, or significant_month.",
    )
    parser.add_argument(
        "--min-magnitude",
        type=float,
        default=float(os.getenv("USGS_EARTHQUAKES_MIN_MAGNITUDE", "0")) if os.getenv("USGS_EARTHQUAKES_MIN_MAGNITUDE") else None,
        help="Optional minimum magnitude filter applied before publishing events.",
    )
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _resolve_broker_endpoint(args.broker_url, args.broker_host, args.broker_port, args.tls)
    poller = USGSEarthquakePoller(last_polled_file=args.last_polled_file, feed=args.feed, min_magnitude=args.min_magnitude)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
