"""Blitzortung lightning firehose -> MQTT/UNS bridge.

Connects to the public LightningMaps / Blitzortung WebSocket firehose,
normalizes each batched stroke into a single UNS event family
(``LightningStroke``), and republishes it as a non-retained QoS-0 MQTT 5
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

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from blitzortung_mqtt_producer_data import (
    DetectorParticipation,
    LightningStroke,
)
from blitzortung_mqtt_producer_mqtt_client.client import BlitzortungLightningMqttMqttClient

from blitzortung_mqtt.geohash import geohash5, geohash7

logger = logging.getLogger("blitzortung_mqtt")


DEFAULT_WS_URLS = (
    "wss://live.lightningmaps.org:443/",
    "wss://live2.lightningmaps.org:443/",
)
DEFAULT_BBOX = (90.0, 180.0, -90.0, -180.0)
DEFAULT_USER_AGENT = (
    "real-time-sources-blitzortung-mqtt/0.1 "
    "(https://github.com/clemensv/real-time-sources)"
)


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


class BlitzortungMqttBridge:
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
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if scheme == "mqtts" else 1883)
    return host, port, scheme == "mqtts"


async def _run(args: argparse.Namespace) -> None:
    broker_host, broker_port, tls = _parse_broker(args.mqtt_broker_url)
    tls = tls or args.mqtt_enable_tls

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=args.mqtt_client_id or "",
        protocol=MQTTv5,
    )
    if args.mqtt_username:
        paho_client.username_pw_set(args.mqtt_username, args.mqtt_password or "")
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    client = BlitzortungLightningMqttMqttClient(
        client=paho_client,
        content_mode="binary",
        loop=loop,
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await client.connect(broker_host, broker_port)

    bridge = BlitzortungMqttBridge(client)
    if args.mock:
        logger.info("Mock mode: emitting synthetic Blitzortung corpus and exiting")
        await bridge.emit_mock_corpus()
        await asyncio.sleep(1.0)
        await client.disconnect()
        return
    await bridge.run(max_events=args.max_events)


def main() -> None:
    if sys.gettrace() is not None:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    p = argparse.ArgumentParser(description="Blitzortung -> MQTT/UNS bridge")
    sub = p.add_subparsers(dest="command")

    feed = sub.add_parser("feed", help="Stream Blitzortung strokes to MQTT")
    feed.add_argument("--mqtt-broker-url",
                      default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    feed.add_argument("--mqtt-enable-tls", action="store_true",
                      default=os.getenv("MQTT_ENABLE_TLS", "false").lower() in ("true", "1", "yes"))
    feed.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME"))
    feed.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD"))
    feed.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID"))
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
