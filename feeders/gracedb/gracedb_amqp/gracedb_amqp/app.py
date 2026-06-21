"""AMQP feeder application for GraceDB → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Any, Awaitable, Optional
from urllib.parse import urlparse


from gracedb.gracedb import BASE_API_URL, DEFAULT_CATEGORIES, DEFAULT_POLL_COUNT, GraceDBPoller


from gracedb_amqp_producer_amqp_producer.producer import OrgLigoGracedbAmqpProducer

logger = logging.getLogger(__name__)
class _MqttProducerAdapter:
    def __init__(self, client: OrgLigoGracedbMqttMqttClient):
        self.producer = self
        self._client = client
        self._tasks: set[asyncio.Task[None]] = set()
        self._failures: list[BaseException] = []
        self._semaphore = asyncio.Semaphore(64)

    def send_org_ligo_gracedb_superevent(self, **kwargs: Any) -> None:
        kwargs.pop("flush_producer", None)
        data = kwargs["data"]
        normalized = {key[1:] if key.startswith("_") else key: value for key, value in kwargs.items()}
        # The Kafka producer takes a uniform CloudEvents ``_time`` override, but
        # the AMQP/MQTT publish method takes the named ``created`` template
        # variable. Translate so the shared bridge call site works everywhere.
        if "time" in normalized and "created" not in normalized:
            normalized["created"] = normalized.pop("time")
        normalized["category"] = data.category
        normalized["group"] = data.group
        task = asyncio.create_task(self._publish(**normalized))
        self._tasks.add(task)
        task.add_done_callback(self._finish_task)

    async def _publish(self, **kwargs: Any) -> None:
        async with self._semaphore:
            await self._client.publish_org_ligo_gracedb_mqtt_superevent(**kwargs)

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


async def feed(
    poller: GraceDBPoller,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
    once: bool = False,
) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "gracedb"),
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

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
class _AmqpPublishFacade:
    def __init__(self, producers): self._producers=list(producers)
    def close(self):
        for p in self._producers:
            c=getattr(p,"close",None)
            if c: c()
    def __getattr__(self,name):
        if not name.startswith("publish_"): raise AttributeError(name)
        suffix=name.split("_mqtt_",1)[1] if "_mqtt_" in name else name[len("publish_"):]
        target=None
        for p in self._producers:
            target=getattr(p,"send_"+suffix,None)
            if target: break
        if target is None: raise AttributeError("send_"+suffix)
        async def _publish(**kwargs):
            accepted=set(target.__code__.co_varnames[:target.__code__.co_argcount])
            call={}
            for k,v in kwargs.items():
                if k in ("data","content_type"): call[k]=v
                elif k in ("flush_producer","qos","retain"): continue
                else:
                    candidate="_"+k.lstrip("_")
                    if candidate in accepted: call[candidate]=v
            target(**call)
        return _publish
def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            import logging; logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def _build_publisher(*, host, port, address, use_tls, content_mode, auth_mode, username, password, entra_audience, entra_client_id, sas_key_name, sas_key):
    out=[]
    for cls in (OrgLigoGracedbAmqpProducer,):
        if auth_mode=="entra":
            from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
            cred=ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
            obj=cls(host=host,address=address,port=port,content_mode=content_mode,credential=cred,entra_audience=entra_audience,use_tls=use_tls)
        elif auth_mode=="sas":
            obj=cls(host=host,address=address,port=port,content_mode=content_mode,sas_key_name=sas_key_name,sas_key=sas_key,use_tls=use_tls)
        else:
            obj=cls(host=host,address=address,port=port,username=username,password=password,content_mode=content_mode,use_tls=use_tls)
        out.append(obj)
    return _AmqpPublishFacade(out)


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="GraceDB AMQP 1.0 bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    parser.add_argument(
        "--last-polled-file",
        default=os.getenv(
            "GRACEDB_AMQP_LAST_POLLED_FILE",
            os.getenv("GRACEDB_LAST_POLLED_FILE", os.getenv("STATE_FILE", os.path.expanduser("~/.gracedb_seen_mqtt.json"))),
        ),
    )
    parser.add_argument("--poll-count", type=int, default=int(os.getenv("GRACEDB_POLL_COUNT", str(DEFAULT_POLL_COUNT))))
    parser.add_argument("--categories", default=os.getenv("GRACEDB_CATEGORIES", DEFAULT_CATEGORIES))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    poller = GraceDBPoller(last_polled_file=args.last_polled_file, poll_count=args.poll_count, categories=args.categories)
    asyncio.run(feed(poller, host, port, username=args.username or None, password=args.password or None, tls=tls, client_id=args.client_id or None, content_mode=args.content_mode, once=args.once))
