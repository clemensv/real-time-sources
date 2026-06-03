"""Blitzortung lightning firehose -> AMQP 1.0 bridge.

Connects to the public LightningMaps / Blitzortung WebSocket firehose,
normalizes each batched stroke into a single UNS event family
(``LightningStroke``), and republishes it as a non-retained QoS-0 AMQP 5
binary-mode CloudEvent on the topic family

    weather/intl/blitzortung/blitzortung/{geohash5}/{geohash7}/{stroke_id}/stroke

Each placeholder is a real field on the published dataclass:

* ``geohash5`` — 5-char geohash (~5 km cell) derived in this bridge from
  the upstream ``lat``/``lon``.
* ``geohash7`` — 7-char geohash (~150 m cell) derived likewise.
* ``stroke_id`` — source-scoped stroke identifier from the upstream
  ``id`` field, stringified.

The trailing literal ``stroke`` is baked into the topic template (single
event family). The CloudEvents subject extends the Kafka subject from
``{source_id}/{stroke_id}`` to ``{geohash5}/{geohash7}/{stroke_id}`` so
subject ⊇ topic axes; the Kafka key (``{source_id}/{stroke_id}``) is
untouched on the original endpoint.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse


from blitzortung_amqp_producer_data import (
    DetectorParticipation,
    LightningStroke,
)
from blitzortung_amqp.geohash import geohash5, geohash7
from blitzortung_amqp_producer_amqp_producer.producer import BlitzortungLightningAmqpProducer

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
        send_name = f"send_{suffix}"
        target = None
        for producer in self._producers:
            target = getattr(producer, send_name, None)
            if target is not None:
                break
        if target is None:
            raise AttributeError(send_name)
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
    for cls in (BlitzortungLightningAmqpProducer,):
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


DEFAULT_WS_URLS = (
    "wss://live.lightningmaps.org:443/",
    "wss://live2.lightningmaps.org:443/",
)
DEFAULT_BBOX = (90.0, 180.0, -90.0, -180.0)
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-blitzortung/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)
DEFAULT_USER_AGENT = USER_AGENT


def _iso_from_ms(ts_ms: Any) -> str:
    try:
        ts_int = int(ts_ms)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc).isoformat()
    if ts_int > 10_000_000_000_000:  # ns / us guard
        ts_int = ts_int // 1_000_000 if ts_int > 10_000_000_000_000_000 else ts_int // 1000
    return datetime.fromtimestamp(ts_int / 1000.0, tz=timezone.utc).isoformat()


def _build_stroke(raw: Dict[str, Any], source_id_default: int = 0) -> Optional[LightningStroke]:
    if not isinstance(raw, dict):
        return None
    stroke_id_raw = raw.get("id")
    if stroke_id_raw is None:
        return None
    lat = raw.get("lat")
    lon = raw.get("lon")
    if lat is None or lon is None:
        return None
    src = raw.get("src", source_id_default)
    try:
        src_int = int(src)
    except (TypeError, ValueError):
        src_int = source_id_default
    time_ms = raw.get("time")

    detectors: List[DetectorParticipation] = []
    sta = raw.get("sta")
    if isinstance(sta, dict):
        for key, val in sta.items():
            try:
                detectors.append(DetectorParticipation(
                    station_id=int(key), status=int(val)
                ))
            except (TypeError, ValueError):
                continue
    elif isinstance(sta, list):
        for entry in sta:
            if isinstance(entry, dict) and "station_id" in entry and "status" in entry:
                try:
                    detectors.append(DetectorParticipation(
                        station_id=int(entry["station_id"]),
                        status=int(entry["status"])
                    ))
                except (TypeError, ValueError):
                    continue

    return LightningStroke(
        source_id=src_int,
        stroke_id=str(stroke_id_raw),
        event_time=_iso_from_ms(time_ms),
        event_timestamp_ms=int(time_ms) if time_ms is not None else 0,
        latitude=float(lat),
        longitude=float(lon),
        server_id=(int(raw["srv"]) if raw.get("srv") is not None else None),
        server_delay_ms=(int(raw["del"]) if raw.get("del") is not None else None),
        accuracy_diameter_m=(float(raw["dev"]) if raw.get("dev") is not None else None),
        detector_participations=detectors,
        geohash5=geohash5(lat, lon),
        geohash7=geohash7(lat, lon),
    )


class BlitzortungAmqpBridge:
    def __init__(
        self,
        client: BlitzortungLightningMqttMqttClient,
        *,
        ws_urls: Iterable[str] = DEFAULT_WS_URLS,
        bbox: tuple = DEFAULT_BBOX,
        source_mask: int = 4,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.client = client
        self.ws_urls = list(ws_urls)
        self.bbox = bbox
        self.source_mask = source_mask
        self.user_agent = user_agent
        self._count = 0

    async def run(self, max_events: Optional[int] = None) -> None:
        import websockets
        # north, east, south, west
        bbox_msg = json.dumps({
            "west": self.bbox[3], "east": self.bbox[1],
            "north": self.bbox[0], "south": self.bbox[2],
            "limit": 0,
        })
        retry_delay = 1
        max_retry_delay = 60
        url_idx = 0
        while True:
            url = self.ws_urls[url_idx % len(self.ws_urls)]
            try:
                async with websockets.connect(
                    url,
                    user_agent_header=self.user_agent,
                    max_size=2 ** 22,
                ) as ws:
                    await ws.send(bbox_msg)
                    logger.info("Connected to Blitzortung WS at %s", url)
                    retry_delay = 1
                    async for raw in ws:
                        try:
                            envelope = json.loads(raw)
                        except (TypeError, ValueError):
                            continue
                        await self._dispatch_envelope(envelope)
                        if max_events and self._count >= max_events:
                            logger.info("max_events=%d reached, exiting", max_events)
                            return
            except (asyncio.CancelledError, KeyboardInterrupt):
                raise
            except Exception as exc:
                logger.error("Blitzortung WS error: %s. Retrying in %ds", exc, retry_delay)
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, max_retry_delay)
                url_idx += 1

    async def _dispatch_envelope(self, envelope: Any) -> None:
        # The public live feed sends one stroke object per WS message in
        # current servers; older variants may batch under {"strokes": [...]}.
        if isinstance(envelope, dict) and "strokes" in envelope and isinstance(envelope["strokes"], list):
            for raw in envelope["strokes"]:
                await self._publish_one(raw)
        elif isinstance(envelope, dict):
            await self._publish_one(envelope)
        elif isinstance(envelope, list):
            for raw in envelope:
                await self._publish_one(raw)

    async def _publish_one(self, raw: Dict[str, Any]) -> None:
        data = _build_stroke(raw)
        if data is None:
            return
        await self.client.publish_blitzortung_lightning_mqtt_lightning_stroke(
            source_id=str(data.source_id),
            geohash5=data.geohash5,
            geohash7=data.geohash7,
            stroke_id=data.stroke_id,
            event_time=data.event_time,
            data=data, qos=0, retain=False,
        )
        self._count += 1

    async def emit_mock_corpus(self) -> None:
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        await self._publish_one({
            "id": 123456789,
            "src": 4,
            "time": now_ms,
            "lat": 50.1109,
            "lon": 8.6821,  # Frankfurt
            "srv": 1,
            "del": 12,
            "dev": 1500.0,
            "sta": {"101": 1, "202": 0, "303": 1},
        })


def _parse_broker(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (5671 if scheme == "amqps" else 5672)
    return host, port, scheme == "amqps"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.amqp_broker_url)
    tls = tls or args.amqp_enable_tls

    client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "blitzortung"),
        use_tls=tls, content_mode="binary", auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=args.amqp_username, password=args.amqp_password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )

    bridge = BlitzortungAmqpBridge(client)
    if args.mock:
        logger.info("Mock mode: emitting synthetic Blitzortung corpus and exiting")
        await bridge.emit_mock_corpus()
        await asyncio.sleep(1.0)
        client.close()
        return
    await bridge.run(max_events=args.max_events)


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="Blitzortung -> AMQP 1.0 bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream Blitzortung strokes to AMQP")
    feed.add_argument("--amqp-broker-url",
                      default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    feed.add_argument("--amqp-enable-tls", action="store_true",
                      default=os.getenv("AMQP_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--amqp-username", default=os.getenv("AMQP_USERNAME"))
    feed.add_argument("--amqp-password", default=os.getenv("AMQP_PASSWORD"))
    feed.add_argument("--amqp-client-id", default=os.getenv("AMQP_CLIENT_ID"))
    feed.add_argument("--max-events", type=int,
                      default=int(os.getenv("BLITZORTUNG_MAX_EVENTS", "0")) or None)
    feed.add_argument("--mock", action="store_true",
                      default=os.getenv("BLITZORTUNG_MOCK", "false").lower() in ("true", "1", "yes"),
                      help="Skip live WS, emit one synthetic stroke, then exit")

    args = p.parse_args()
    if args.command != "feed":
        p.print_help()
        sys.exit(1)

    try:
        asyncio.run(_run(args))
    except KeyboardInterrupt:
        logger.info("Shutting down")


if __name__ == "__main__":
    main()
