"""AMQP feeder application for USGS Instantaneous Values → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Awaitable, Callable, Dict, List, Optional
from urllib.parse import urlparse


from usgs_iv.usgs_iv import USGSDataPoller, Site

from usgs_iv_amqp_producer_amqp_producer.producer import USGSSitesAmqpProducer, USGSSiteTimeseriesAmqpProducer, USGSInstantaneousValuesAmqpProducer

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"


def _truthy_env(name: str) -> bool:
    return os.getenv(name, "").lower() in ("1", "true", "yes")


class _MockUSGSDataPoller(USGSDataPoller):
    async def get_sites_in_state(self, state_code: str) -> AsyncIterator[Site]:
        yield Site(
            agency_cd="USGS",
            site_no="01477120",
            station_nm="Mock Delaware Streamgage",
            site_tp_cd="ST",
            lat_va="394500",
            long_va="0753000",
            dec_lat_va=39.75,
            dec_long_va=-75.5,
            coord_meth_cd="M",
            coord_acy_cd="S",
            coord_datum_cd="NAD83",
            dec_coord_datum_cd="NAD83",
            district_cd="10",
            state_cd=state_code or "DE",
            county_cd="003",
            country_cd="US",
            land_net_ds="",
            map_nm="",
            map_scale_fc=None,
            alt_va=None,
            alt_meth_cd="",
            alt_acy_va=None,
            alt_datum_cd="",
            huc_cd="02040205",
            basin_cd="",
            topo_cd="",
            instruments_cd="Y",
            construction_dt=None,
            inventory_dt=None,
            drain_area_va=None,
            contrib_drain_area_va=None,
            tz_cd="EST",
            local_time_fg=True,
            reliability_cd="",
            gw_file_cd="",
            nat_aqfr_cd="",
            aqfr_cd="",
            aqfr_type_cd="",
            well_depth_va=None,
            hole_depth_va=None,
            depth_src_cd="",
            project_no="",
        )

    async def get_data_by_state(self, state_code: str) -> AsyncIterator[List[Dict[str, Any]]]:
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        yield [{
            "agency_cd": "USGS",
            "site_no": "01477120",
            "datetime": timestamp,
            "tz_cd": "EST",
            "123456_00060": "42.1",
            "123456_00060_cd": "A",
        }]


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
        if suffix.endswith("_p_h"):
            suffix = suffix[:-4] + "_ph"
        elif suffix == "p_h":
            suffix = "ph"
        parts = suffix.split("_")
        target = None
        for start in range(len(parts)):
            send_name = f"send_{'_'.join(parts[start:])}"
            for producer in self._producers:
                target = getattr(producer, send_name, None)
                if target is not None:
                    break
            if target is not None:
                break
        if target is None:
            raise AttributeError(f"send_{suffix}")

        async def _publish(**kwargs):
            call = {}
            for key, value in kwargs.items():
                if key in ("data", "content_type"):
                    call[key] = value
                elif key in ("flush_producer", "time", "_time"):
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
        publish_name = name.replace("send_", "publish_")
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
    address: str = "usgs-iv",
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
    auth_mode: str = "password",
    entra_audience: str = DEFAULT_ENTRA_AUDIENCE_SERVICEBUS,
    entra_client_id: Optional[str] = None,
    sas_key_name: Optional[str] = None,
    sas_key: Optional[str] = None,
) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=address,
        use_tls=tls, content_mode=content_mode, auth_mode=auth_mode,
        username=username, password=password,
        entra_audience=entra_audience,
        entra_client_id=entra_client_id,
        sas_key_name=sas_key_name, sas_key=sas_key,
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


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    path = (parsed.path or "").lstrip("/") or None
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, path



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
    parser = argparse.ArgumentParser(description="USGS IV AMQP 1.0 bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", "usgs-iv"))
    parser.add_argument("--last-polled-file", default=os.getenv("USGS_LAST_POLLED_FILE", os.path.expanduser("~/.usgs_last_polled_amqp.json")))
    parser.add_argument("--state", default=os.getenv("USGS_STATE", ""))
    parser.add_argument("--force-site-refresh", action="store_true", default=_truthy_env("USGS_FORCE_SITE_REFRESH"))
    parser.add_argument("--force-data-refresh", action="store_true", default=_truthy_env("USGS_FORCE_DATA_REFRESH"))
    parser.add_argument("--once", action="store_true", default=_truthy_env("ONCE_MODE"))
    parser.add_argument("--mock", action="store_true", default=_truthy_env("USGS_IV_MOCK"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--tls", action="store_true", default=_truthy_env("AMQP_TLS"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")

    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_password, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_password
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        tls = args.tls or args.auth_mode == "entra"
        host = args.host or "localhost"
        port = args.port or (5671 if tls else 5672)
        username = args.username or None
        password = args.password or None

    poller_cls = _MockUSGSDataPoller if args.mock else USGSDataPoller
    poller = poller_cls(
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
        address=address,
        username=username or None,
        password=password or None,
        tls=tls,
        client_id=args.client_id or None,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
        sas_key_name=args.sas_key_name,
        sas_key=args.sas_key,
    ))
