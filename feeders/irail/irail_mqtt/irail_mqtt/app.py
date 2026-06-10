"""MQTT feeder application for iRail Belgian railway → Unified Namespace."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from irail.irail import IRailAPI, REQUEST_DELAY
from irail_mqtt_producer_mqtt_client.client import BeIrailMqttMqttClient
import json

def _fetch_entra_mqtt_token(audience, managed_identity_client_id=None):
    params = {
        "api-version": "2018-02-01",
        "resource": audience or "https://eventgrid.azure.net/",
    }
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id

    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)

def _resolve_mqtt_connection_settings(*, username=None, password=None, client_id=None, auth_mode=None):
    resolved_client_id = str(client_id or os.getenv("MQTT_CLIENT_ID") or "").strip()
    auth_mode = str(auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).strip().lower() or "password"

    if auth_mode != "entra":
        return resolved_client_id, str(username or ""), str(password or "")

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    return resolved_client_id, resolved_username, resolved_password

logger = logging.getLogger(__name__)

def _parse_broker_url(url: str) -> tuple[str, int, bool]:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (8883 if tls else 1883), tls

def _parse_station_filter(value: str) -> set[str]:
    return {item.strip() for item in value.split(",") if item.strip()}

async def feed(
    api: IRailAPI,
    broker_host: str,
    broker_port: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    station_filter: str = "",
    polling_interval: int = 300,
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
        username=username,
        password=password or "",
        client_id=client_id or "",
        auth_mode=os.getenv("MQTT_AUTH_MODE"),
    )

    paho_client = mqtt.Client(client_id=resolved_client_id or "", 
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if resolved_username or resolved_password:
        paho_client.username_pw_set(resolved_username, resolved_password)
    if tls:
        paho_client.tls_set()

    mqtt_client = BeIrailMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=asyncio.get_running_loop(),
    )
    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)
    try:
        filter_set = _parse_station_filter(station_filter)
        all_stations_raw = api.fetch_stations()
        station_ids: list[str] = []
        station_sent = 0
        for raw in all_stations_raw:
            try:
                station = api.parse_station(raw)
                if filter_set and station.station_id not in filter_set:
                    continue
                station_ids.append(station.station_id)
                await mqtt_client.publish_be_irail_mqtt_station(
                    station_id=station.station_id,
                    data=station,
                )
                station_sent += 1
            except Exception as exc:  # pragma: no cover - defensive around upstream rows
                logger.warning("Skipping malformed station %s: %s", raw.get("id", "?"), exc)
        logger.info("Published %d station reference records", station_sent)

        while True:
            departure_board_count = 0
            arrival_board_count = 0
            start_time = datetime.now(timezone.utc)
            board_specs = (
                ("departure", api.parse_liveboard, mqtt_client.publish_be_irail_mqtt_station_board),
                ("arrival", api.parse_arrivalboard, mqtt_client.publish_be_irail_mqtt_arrival_board),
            )
            for station_id in station_ids:
                for board_kind, parser, sender in board_specs:
                    try:
                        liveboard_raw = api.fetch_liveboard(station_id, arrdep=board_kind)
                        if liveboard_raw is None:
                            continue
                        board = parser(liveboard_raw, station_id)
                        await sender(
                            station_id=station_id,
                            data=board,
                        )
                        if board_kind == "departure":
                            departure_board_count += 1
                        else:
                            arrival_board_count += 1
                    except Exception as exc:
                        logger.error("Error fetching %s board for %s: %s", board_kind, station_id, exc)
                    time.sleep(REQUEST_DELAY)
            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            logger.info(
                "Published %d departure boards and %d arrival boards in %.1f s",
                departure_board_count,
                arrival_board_count,
                elapsed,
            )
            if once:
                break
            await asyncio.sleep(max(0, polling_interval - elapsed))
    finally:
        await mqtt_client.disconnect()

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="iRail MQTT/UNS bridge")
    parser.add_argument("feed", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--station-filter", default=os.getenv("STATION_FILTER", ""))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD", ""))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    args = parser.parse_args()
    if args.feed != "feed":
        parser.error("only the 'feed' command is supported")
    host, port, tls = _parse_broker_url(args.broker_url)
    asyncio.run(feed(
        IRailAPI(),
        host,
        port,
        username=args.username or None,
        password=args.password or None,
        tls=tls,
        client_id=args.client_id or None,
        station_filter=args.station_filter,
        polling_interval=args.polling_interval,
        once=args.once,
        content_mode=args.content_mode,
    ))
