"""MQTT feeder application for PegelOnline → Unified Namespace.

Wraps the upstream poller from :mod:`pegelonline_core` and the generated
:class:`DeWsvPegelonlineMqttMqttClient`. The MQTT broker is reached via a
plain ``mqtt://host:port`` URL (or ``mqtts://`` for TLS); username/password
are optional. CloudEvent semantics are preserved end-to-end: binary mode
maps CE attributes to MQTT 5 user properties so subscribers can route on
``type``, ``source`` and ``subject`` without having to crack the JSON body.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from pegelonline_core import FEED_URL_ROOT, PegelOnlineAPI, load_state, save_state

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"
from pegelonline_mqtt_producer_data.de.wsv.pegelonline.currentmeasurement import CurrentMeasurement
from pegelonline_mqtt_producer_data.de.wsv.pegelonline.station import Station
from pegelonline_mqtt_producer_data.de.wsv.pegelonline.water import Water
from pegelonline_mqtt_producer_mqtt_client.client import DeWsvPegelonlineMqttMqttClient

logger = logging.getLogger(__name__)


def _build_station(raw: Dict[str, Any]) -> Station:
    water = raw.get("water") or {}
    return Station(
        station_id=str(raw.get("uuid")) if raw.get("uuid") is not None else None,
        number=str(raw.get("number")) if raw.get("number") is not None else None,
        shortname=str(raw.get("shortname")) if raw.get("shortname") is not None else None,
        longname=str(raw.get("longname")) if raw.get("longname") is not None else None,
        km=raw.get("km"),
        agency=str(raw.get("agency")) if raw.get("agency") is not None else None,
        longitude=float(raw.get("longitude") if raw.get("longitude") is not None else -1),  # type: ignore[arg-type]
        latitude=float(raw.get("latitude") if raw.get("latitude") is not None else -1),  # type: ignore[arg-type]
        water=Water(shortname=str(water.get("shortname")) if water.get("shortname") is not None else None, longname=str(water.get("longname")) if water.get("longname") is not None else None),
    )


def _build_measurement(station_id: str, raw: Dict[str, Any]) -> CurrentMeasurement:
    return CurrentMeasurement(
        station_id=station_id,
        timestamp=raw["timestamp"],
        value=raw["value"],
        stateMnwMhw=raw.get("stateMnwMhw"),
        stateNswHsw=raw.get("stateNswHsw"),
        trend=raw.get("trend"),
    )


def _water_shortname(raw_station: Dict[str, Any]) -> str:
    """Pick the URL-safe water shortname used in the UNS topic.

    Upstream may report water names with spaces or umlauts. Lowercase ASCII
    is what we want on the wire; anything outside that is replaced with ``-``
    so the topic stays well-formed even on edge cases like
    ``MITTELLANDKANAL / ELBE-SEITENKANAL``.
    """
    water = raw_station.get("water") or {}
    raw = (water.get("shortname") or water.get("longname") or "unknown").strip().lower()
    out_chars = []
    for ch in raw:
        if ch.isalnum():
            out_chars.append(ch)
        elif ch in ("-", "_"):
            out_chars.append(ch)
        else:
            out_chars.append("-")
    safe = "".join(out_chars).strip("-")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe or "unknown"


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple:
    """Acquire a Microsoft Entra JWT for the configured audience.

    Returns ``(token_string, expires_at_datetime)``. The returned token is
    suitable as the MQTT password against an Event Grid namespace MQTT
    broker that is configured with custom JWT authentication issued by
    Microsoft Entra ID.
    """
    try:
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    except ImportError as exc:  # pragma: no cover - import error path
        raise RuntimeError(
            "azure-identity must be installed to use MQTT_AUTH_MODE=entra"
        ) from exc

    credential = (
        ManagedIdentityCredential(client_id=client_id)
        if client_id
        else DefaultAzureCredential()
    )
    scope = audience if audience.endswith("/.default") else f"{audience}/.default"
    token = credential.get_token(scope)
    expires_at = datetime.fromtimestamp(token.expires_on, tz=timezone.utc)
    return token.token, expires_at


async def _entra_token_refresh_loop(
    paho_client: "mqtt.Client",
    broker_host: str,
    broker_port: int,
    keepalive: int,
    audience: str,
    client_id: Optional[str],
    expires_at: datetime,
) -> None:
    """Refresh the Entra JWT before it expires and re-establish the session.

    Event Grid's MQTT broker supports MQTT v5 re-authentication via the AUTH
    packet, but paho-mqtt 2.1 does not expose a ``reauth`` method, so we
    fall back to a clean disconnect + reconnect using a freshly minted JWT
    in the CONNECT packet's enhanced-authentication properties.
    """
    while True:
        now = datetime.now(timezone.utc)
        sleep_seconds = max(60.0, (expires_at - now).total_seconds() - 300.0)
        await asyncio.sleep(sleep_seconds)
        try:
            new_token, expires_at = _acquire_entra_token(audience, client_id)
            props = Properties(PacketTypes.CONNECT)
            props.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
            props.AuthenticationData = new_token.encode("utf-8")
            try:
                paho_client.disconnect()
            except Exception:  # pylint: disable=broad-except
                pass
            try:
                paho_client.connect(
                    broker_host,
                    broker_port,
                    keepalive=keepalive,
                    clean_start=True,
                    properties=props,
                )
                logger.info(
                    "Refreshed Entra JWT and reconnected MQTT client (expires=%s)",
                    expires_at.isoformat(),
                )
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("Reconnect after token refresh failed: %s", exc)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to refresh Entra JWT: %s", exc)
            await asyncio.sleep(60)


async def _publish_stations(
    api: PegelOnlineAPI,
    client: DeWsvPegelonlineMqttMqttClient,
    stations: list,
    station_index: Dict[str, Dict[str, Any]],
) -> None:
    for station in stations:
        station_index[station["uuid"]] = station
        await client.publish_de_wsv_pegelonline_mqtt_station(
            feedurl=f"{FEED_URL_ROOT}/stations/{station['shortname']}",
            station_id=station["uuid"],
            water_shortname=_water_shortname(station),
            data=_build_station(station),
        )


async def feed(
    api: PegelOnlineAPI,
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
    auth_mode: str = "password",
    entra_audience: str = DEFAULT_ENTRA_AUDIENCE,
    entra_client_id: Optional[str] = None,
) -> None:
    previous_readings: Dict[str, Dict[str, Any]] = load_state(state_file)

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )

    refresh_task: Optional[asyncio.Task] = None
    connect_properties: Optional[Properties] = None
    expires_at: Optional[datetime] = None
    if auth_mode == "entra":
        token, expires_at = _acquire_entra_token(entra_audience, entra_client_id)
        connect_properties = Properties(PacketTypes.CONNECT)
        connect_properties.AuthenticationMethod = ENTRA_MQTT_AUTH_METHOD
        connect_properties.AuthenticationData = token.encode("utf-8")
        logger.info(
            "Using Microsoft Entra JWT auth (audience=%s, expires=%s)",
            entra_audience,
            expires_at.isoformat(),
        )
    elif username:
        paho_client.username_pw_set(username, password or "")

    if tls or auth_mode == "entra":
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    mqtt_client = DeWsvPegelonlineMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info(
        "Connecting to MQTT broker %s:%s (tls=%s, auth=%s)",
        broker_host,
        broker_port,
        tls or auth_mode == "entra",
        auth_mode,
    )
    if auth_mode == "entra":
        paho_client.connect(
            broker_host,
            broker_port,
            keepalive=60,
            clean_start=True,
            properties=connect_properties,
        )
        paho_client.loop_start()
    else:
        await mqtt_client.connect(broker_host, broker_port)

    if auth_mode == "entra" and expires_at is not None:
        refresh_task = asyncio.create_task(
            _entra_token_refresh_loop(
                paho_client,
                broker_host,
                broker_port,
                60,
                entra_audience,
                entra_client_id,
                expires_at,
            )
        )

    station_index: Dict[str, Dict[str, Any]] = {}
    stations = api.list_stations()
    logger.info("Publishing %d station info events under hydro/de/wsv/pegelonline/...", len(stations))
    await _publish_stations(api, mqtt_client, stations, station_index)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                count = 0
                start_time = datetime.now(timezone.utc)
                measurements = api.get_water_levels()
                for station_id, measurement in measurements.items():
                    prior = previous_readings.get(station_id)
                    if prior is not None and measurement.get("timestamp") == prior.get("timestamp"):
                        continue
                    count += 1
                    station_meta = station_index.get(station_id) or {}
                    water_shortname = _water_shortname(station_meta)
                    try:
                        await mqtt_client.publish_de_wsv_pegelonline_mqtt_current_measurement(
                            feedurl=f"{FEED_URL_ROOT}/stations/{station_id}/W/currentmeasurement.json",
                            station_id=station_id,
                            water_shortname=water_shortname,
                            data=_build_measurement(station_id, measurement),
                        )
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error publishing measurement for %s: %s", station_id, e)
                    previous_readings[station_id] = measurement
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s current measurements in %s seconds. Sleeping until %s.",
                    count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                await asyncio.sleep(polling_interval)
    finally:
        if refresh_task is not None:
            refresh_task.cancel()
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PegelOnline → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed stations and updates as CloudEvents to MQTT")
    feed_parser.add_argument("--broker-url", type=str,
                             default=os.getenv("MQTT_BROKER_URL"),
                             help="MQTT broker URL (e.g. mqtt://localhost:1883 or mqtts://broker:8883)")
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("MQTT_HOST"),
                             help="MQTT broker hostname (alternative to --broker-url)")
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("MQTT_PORT", "0")) or None,
                             help="MQTT broker port (default 1883, or 8883 with --tls)")
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"],
                             help="CloudEvents content mode (default: binary)")
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=polling_interval_default,
                             help="Polling interval in seconds")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.pegelonline_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle.")
    feed_parser.add_argument("--auth-mode", type=str,
                             default=os.getenv("MQTT_AUTH_MODE", "password"),
                             choices=["password", "entra"],
                             help="Authentication mode: 'password' (default) for username/password, "
                                  "or 'entra' for Microsoft Entra JWT via managed identity "
                                  "(suitable for Azure Event Grid namespace MQTT brokers).")
    feed_parser.add_argument("--entra-audience", type=str,
                             default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE),
                             help=f"Entra token audience (default: {DEFAULT_ENTRA_AUDIENCE}).")
    feed_parser.add_argument("--entra-client-id", type=str,
                             default=os.getenv("MQTT_ENTRA_CLIENT_ID"),
                             help="Optional user-assigned managed identity client id; "
                                  "defaults to DefaultAzureCredential resolution.")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.command != "feed":
        parser.print_help()
        return

    if args.broker_url:
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (8883 if tls else 1883)
        username = args.username
        password = args.password

    api = PegelOnlineAPI()
    asyncio.run(
        feed(
            api,
            host,
            port,
            args.polling_interval,
            username=username,
            password=password,
            tls=tls,
            client_id=args.client_id,
            state_file=args.state_file,
            once=args.once,
            content_mode=args.content_mode,
            auth_mode=args.auth_mode,
            entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id,
        )
    )


if __name__ == "__main__":
    main()
