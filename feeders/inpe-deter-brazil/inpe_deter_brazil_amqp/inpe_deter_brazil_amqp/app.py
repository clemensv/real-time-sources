"""AMQP feeder application for INPE DETER Brazil → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
from typing import Optional
from urllib.parse import urlparse


from inpe_deter_brazil.inpe_deter_brazil import DEFAULT_PAGE_SIZE, INPEDeterPoller, SOURCE_URI, WFS_ENDPOINTS
from inpe_deter_brazil_amqp_producer_data import DeforestationAlert
from inpe_deter_brazil_amqp_producer_amqp_producer.producer import BRINPEDETERAmqpProducer
from inpe_deter_brazil_amqp_producer_data.br.inpe.deter.biomeenum import BiomeEnum
from inpe_deter_brazil_amqp_producer_data.br.inpe.deter.classslugenum import ClassSlugenum

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
class _AmqpPublishFacade:
    def __init__(self, producer): self._producer=producer
    def close(self): self._producer.close()
    def __getattr__(self,name):
        if not name.startswith("publish_"): raise AttributeError(name)
        suffix=name.split("_mqtt_",1)[1] if "_mqtt_" in name else name[len("publish_"):]
        parts=suffix.split("_")
        target=None
        for start in range(len(parts)):
            send_name="send_"+"_".join(parts[start:])
            target=getattr(self._producer,send_name,None)
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
    if auth_mode=="entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred=ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        p=_retry_producer_init(lambda: BRINPEDETERAmqpProducer(host=host,address=address,port=port,content_mode=content_mode,credential=cred,entra_audience=entra_audience,use_tls=use_tls))
    elif auth_mode=="sas":
        p=_retry_producer_init(lambda: BRINPEDETERAmqpProducer(host=host,address=address,port=port,content_mode=content_mode,sas_key_name=sas_key_name,sas_key=sas_key,use_tls=use_tls))
    else:
        p=_retry_producer_init(lambda: BRINPEDETERAmqpProducer(host=host,address=address,port=port,username=username,password=password,content_mode=content_mode,use_tls=use_tls))
    return _AmqpPublishFacade(p)

logger = logging.getLogger(__name__)


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls


def _parse_biomes(value: str) -> list[str]:
    requested = [item.strip().lower() for item in value.split(",") if item.strip()]
    if not requested:
        return list(WFS_ENDPOINTS.keys())
    invalid = sorted(set(requested) - set(WFS_ENDPOINTS.keys()))
    if invalid:
        raise ValueError(f"Unsupported biomes: {', '.join(invalid)}")
    return requested


async def feed(
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    biomes: str = "",
    page_size: int = DEFAULT_PAGE_SIZE,
    since_date: Optional[str] = None,
    once: bool = False,
    content_mode: str = "binary",
    poll_interval_minutes: int = 10,
) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "inpe-deter-brazil"),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )
    poller = INPEDeterPoller(page_size=page_size, poll_interval_minutes=poll_interval_minutes)
    selected_biomes = _parse_biomes(biomes)
    try:
        if os.getenv("INPE_DETER_MOCK", "").lower() in ("1", "true", "yes"):
            alert = DeforestationAlert(
                alert_id="mock-cerrado-1",
                biome=BiomeEnum("cerrado"),
                classname="DESMATAMENTO_CR",
                view_date="2026-01-01",
                satellite="AMAZONIA-1",
                sensor="WFI",
                area_km2=1.25,
                municipality="Brasília",
                state_code="DF",
                state_slug="df",
                class_slug=ClassSlugenum("desmatamento-cr") if "desmatamento-cr" else None,
                path_row="000/000",
                publish_month="2026-01-01",
                centroid_latitude=-15.78,
                centroid_longitude=-47.93,
            )
            await mqtt_client.publish_br_inpe_deter_mqtt_deforestation_alert(
                source_uri=SOURCE_URI,
                biome=alert.biome,
                alert_id=alert.alert_id,
                view_date=alert.view_date,
                state_slug=alert.state_slug,
                class_slug=alert.class_slug,
                data=alert,
            )
            logger.info("Mock mode: published one INPE DETER alert")
            return
        while True:
            published = 0
            for biome in selected_biomes:
                features = await poller.fetch_biome(biome, since_date=since_date)
                logger.info("Fetched %d INPE DETER features for %s", len(features), biome)
                for feature in features:
                    alert = poller.parse_alert(feature, biome)
                    if alert is None:
                        continue
                    await mqtt_client.publish_br_inpe_deter_mqtt_deforestation_alert(
                        source_uri=SOURCE_URI,
                        biome=alert.biome,
                        alert_id=alert.alert_id,
                        view_date=alert.view_date,
                        state_slug=alert.state_slug,
                        class_slug=alert.class_slug,
                        data=alert,
                    )
                    published += 1
            logger.info("Published %d INPE DETER alerts to AMQP", published)
            if once:
                break
            await asyncio.sleep(max(1, poll_interval_minutes * 60))
    finally:
        mqtt_client.close()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="INPE DETER Brazil AMQP 1.0 bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    parser.add_argument("--biomes", default=os.getenv("INPE_BIOMES", ""))
    parser.add_argument("--page-size", type=int, default=int(os.getenv("PAGE_SIZE", str(DEFAULT_PAGE_SIZE))))
    parser.add_argument("--since-date", default=os.getenv("SINCE_DATE", ""))
    parser.add_argument("--poll-interval-minutes", type=int, default=int(os.getenv("POLL_INTERVAL_MINUTES", "10")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, parsed_tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=parsed_tls,
        client_id=args.client_id or None,
        biomes=args.biomes,
        page_size=args.page_size,
        since_date=args.since_date or None,
        once=args.once,
        content_mode=args.content_mode,
        poll_interval_minutes=args.poll_interval_minutes,
    ))


if __name__ == "__main__":
    main()
