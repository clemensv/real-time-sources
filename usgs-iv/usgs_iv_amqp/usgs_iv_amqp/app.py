"""AMQP feeder application for USGS Instantaneous Values → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Awaitable, Callable, Optional
from urllib.parse import urlparse


from usgs_iv.usgs_iv import USGSDataPoller

from usgs_iv_amqp_producer_amqp_producer.producer import USGSSitesAmqpProducer, USGSSiteTimeseriesAmqpProducer, USGSInstantaneousValuesAmqpProducer

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
        if suffix == "p_h":
            suffix = "ph"
        send_name = f"send_{suffix}"
        target = None
        for producer in self._producers:
            target = getattr(producer, send_name, None)
            if target is not None:
                break
        if target is None:
            raise AttributeError(send_name)

        async def _publish(**kwargs):
            call = {}
            for key, value in kwargs.items():
                if key in ("data", "content_type"):
                    call[key] = value
                elif key == "flush_producer":
                    continue
                else:
                    call["_" + key.lstrip("_")] = value
            target(**call)

        return _publish


def _build_publisher(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username, password, entra_audience: str, entra_client_id, sas_key_name, sas_key):
    producers = []
    for cls in (USGSSitesAmqpProducer, USGSSiteTimeseriesAmqpProducer, USGSInstantaneousValuesAmqpProducer,):
        if auth_mode == "entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
            producer = cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
        elif auth_mode == "sas":
            if not sas_key_name or not sas_key:
                raise RuntimeError("AMQP_AUTH_MODE=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
            producer = cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
        else:
            producer = cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)
        producers.append(producer)
    return _AmqpPublishFacade(producers)



class _MqttProducerAdapter:
    def __init__(self, client: Any, prefix: str):
        self.producer = self
        self._client = client
        self._prefix = prefix
        self._tasks: set[asyncio.Task[None]] = set()
        self._failures: list[BaseException] = []
        self._semaphore = asyncio.Semaphore(64)

    def __getattr__(self, name: str) -> Callable[..., None]:
        if not name.startswith("send_"):
            raise AttributeError(name)
        publish_name = name.replace("send_", "publish_").replace(self._prefix, f"{self._prefix}mqtt_")
        publish: Callable[..., Awaitable[None]] = getattr(self._client, publish_name)

        async def _publish_with_limit(**kwargs: Any) -> None:
            async with self._semaphore:
                await publish(**kwargs)

        def _send(**kwargs: Any) -> None:
            kwargs.pop("flush_producer", None)
            normalized = {key[1:] if key.startswith("_") else key: value for key, value in kwargs.items()}
            task = asyncio.create_task(_publish_with_limit(**normalized))
            self._tasks.add(task)
            task.add_done_callback(self._finish_task)

        return _send

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
            pending = list(self._tasks)
            await asyncio.gather(*pending, return_exceptions=True)
        if self._failures:
            raise RuntimeError("one or more AMQP publishes failed") from self._failures[0]


async def feed(
    poller: USGSDataPoller,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "usgs-iv"),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )
    site_adapter = _MqttProducerAdapter(mqtt_client, "usgs_sites_")
    values_adapter = _MqttProducerAdapter(mqtt_client, "usgs_instantaneous_values_")
    poller.site_producer = site_adapter
    poller.values_producer = values_adapter
    try:
        await poller.poll_and_send()
        await site_adapter.drain()
        await values_adapter.drain()
    finally:
        mqtt_client.close()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="USGS IV AMQP 1.0 bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    parser.add_argument("--last-polled-file", default=os.getenv("USGS_LAST_POLLED_FILE", os.path.expanduser("~/.usgs_last_polled_mqtt.json")))
    parser.add_argument("--state", default=os.getenv("USGS_STATE", ""))
    parser.add_argument("--force-site-refresh", action="store_true", default=os.getenv("USGS_FORCE_SITE_REFRESH", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--force-data-refresh", action="store_true", default=os.getenv("USGS_FORCE_DATA_REFRESH", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    poller = USGSDataPoller(
        last_polled_file=args.last_polled_file,
        state=args.state or None,
        force_site_refresh=args.force_site_refresh,
        force_data_refresh=args.force_data_refresh,
        once=args.once,
    )
    asyncio.run(feed(
        poller,
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        content_mode=args.content_mode,
    ))
