"""AMQP feeder application for USGS Geomagnetism → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from urllib.parse import urlparse


from usgs_geomag.usgs_geomag import DEFAULT_OBSERVATORIES, POLL_INTERVAL_SECONDS, USGSGeomagPoller


from usgs_geomag_amqp_producer_amqp_producer.producer import GovUsgsGeomagAmqpProducer

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
        target = None
        for producer in self._producers:
            target = getattr(producer, f"send_{suffix}", None)
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
    for cls in (GovUsgsGeomagAmqpProducer,):
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


def _load_state(path: str) -> Dict:
    try:
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    data.setdefault("last_timestamps", {})
                    return data
    except Exception as exc:
        logger.warning("Could not load state %s: %s", path, exc)
    return {"last_timestamps": {}}


def _save_state(path: str, state: Dict) -> None:
    if not path:
        return
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f)


async def _publish_observatories(client: GovUsgsGeomagMqttMqttClient, observatories: List[str]) -> None:
    features = USGSGeomagPoller.fetch_observatories()
    wanted = {code.upper() for code in observatories}
    for feature in features:
        obs = USGSGeomagPoller.parse_observatory(feature)
        if wanted and obs.iaga_code.upper() not in wanted:
            continue
        await client.publish_gov_usgs_geomag_mqtt_observatory(
            iaga_code=obs.iaga_code.lower(),
            data=obs,
        )


async def _publish_readings(
    client: GovUsgsGeomagMqttMqttClient,
    observatories: List[str],
    state: Dict,
) -> int:
    last_timestamps = state.setdefault("last_timestamps", {})
    now = datetime.now(timezone.utc)
    end_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    default_start = (now - timedelta(minutes=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    sent = 0
    for code in observatories:
        iaga_code = code.upper()
        start_time = last_timestamps.get(iaga_code, default_start)
        data = USGSGeomagPoller.fetch_variation_data(iaga_code, start_time, end_time)
        if data is None:
            continue
        latest_ts = last_timestamps.get(iaga_code)
        for reading in USGSGeomagPoller.parse_timeseries(iaga_code, data):
            reading_ts = reading.timestamp.isoformat()
            if latest_ts and reading_ts <= latest_ts:
                continue
            await client.publish_gov_usgs_geomag_mqtt_magnetic_field_reading(
                iaga_code=reading.iaga_code.lower(),
                data=reading,
            )
            latest_ts = reading_ts
            sent += 1
        if latest_ts:
            last_timestamps[iaga_code] = latest_ts
    return sent


async def feed(
    broker_host: str,
    broker_port: int,
    observatories: List[str],
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    mqtt_client = _build_publisher(
        host=broker_host, port=broker_port, address=os.getenv("AMQP_ADDRESS", "usgs-geomag"),
        use_tls=tls, content_mode=content_mode, auth_mode=os.getenv("AMQP_AUTH_MODE", "password"),
        username=username, password=password,
        entra_audience=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS),
        entra_client_id=os.getenv("AMQP_ENTRA_CLIENT_ID"),
        sas_key_name=os.getenv("AMQP_SAS_KEY_NAME"), sas_key=os.getenv("AMQP_SAS_KEY"),
    )
    state = _load_state(state_file)
    try:
        await _publish_observatories(mqtt_client, observatories)
        while True:
            sent = await _publish_readings(mqtt_client, observatories, state)
            _save_state(state_file, state)
            logger.info("Published %d magnetic field readings", sent)
            if once:
                break
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
    finally:
        mqtt_client.close()


def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    return parsed.hostname or "localhost", parsed.port or (5671 if scheme in ("amqps", "ssl", "tls") else 5672), scheme in ("amqps", "ssl", "tls")


def _parse_observatories(raw: str) -> List[str]:
    return [part.strip().upper() for part in raw.split(",") if part.strip()] or DEFAULT_OBSERVATORIES


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="USGS Geomagnetism AMQP 1.0 bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL", "amqp://localhost:5672"))
    parser.add_argument("--observatories", default=os.getenv("GEOMAG_OBSERVATORIES", ",".join(DEFAULT_OBSERVATORIES)))
    parser.add_argument("--state-file", default=os.getenv("GEOMAG_LAST_POLLED_FILE", ""))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("AMQP_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        host,
        port,
        _parse_observatories(args.observatories),
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        state_file=args.state_file,
        once=args.once,
        content_mode=args.content_mode,
    ))
