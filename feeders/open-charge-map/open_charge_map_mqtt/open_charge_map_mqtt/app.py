"""MQTT feeder application for Open Charge Map -> Unified Namespace.

Wraps the Open Charge Map reference and POI pollers from
:mod:`open_charge_map_core` and the generated MQTT clients. The broker is reached
via a plain ``mqtt://host:port`` URL (or ``mqtts://`` for TLS); username/password
are optional, and a Microsoft Entra JWT flow (``--auth-mode entra``) is supported
for Azure Event Grid namespace brokers. CloudEvent semantics are preserved
end-to-end: binary mode maps CE attributes to MQTT 5 user properties so
subscribers can route on ``type``, ``source`` and ``subject`` without cracking
the JSON body. Reference events are published under
``ev-charging/open-charge-map/reference/{reference_type}/{reference_id}`` and
locations under ``ev-charging/open-charge-map/location/{poi_id}``.
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from open_charge_map_core import (
    POI_URL,
    REFERENCE_URL,
    FeedConfig,
    OpenChargeMapAPI,
    ParsedLocation,
    ParsedReference,
    load_state,
    parse_ocm_datetime,
    parse_poi,
    parse_reference_data,
    save_state,
)
from open_charge_map_mqtt_producer_data import (
    ChargerType,
    ChargingLocation,
    Connection,
    ConnectionType,
    Country,
    CurrentType,
    DataProvider,
    Operator,
    StatusType,
    SubmissionStatusType,
    UsageType,
)
from open_charge_map_mqtt_producer_mqtt_client.client import (
    IOOpenChargeMapLocationsMqttMqttClient,
    IOOpenChargeMapReferenceMqttMqttClient,
)

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

logger = logging.getLogger(__name__)

REF_CLASSES = {
    "operator": Operator,
    "connection_type": ConnectionType,
    "current_type": CurrentType,
    "charger_type": ChargerType,
    "country": Country,
    "data_provider": DataProvider,
    "status_type": StatusType,
    "usage_type": UsageType,
    "submission_status_type": SubmissionStatusType,
}


def _build_location(p: ParsedLocation) -> ChargingLocation:
    data = dataclasses.asdict(p)
    connections = data.pop("connections")
    if data.get("latitude") is None:
        data["latitude"] = 0.0
    if data.get("longitude") is None:
        data["longitude"] = 0.0
    return ChargingLocation(
        **data,
        connections=[Connection(**c) for c in connections],
    )


def _build_reference(r: ParsedReference):
    return REF_CLASSES[r.reference_type](**r.fields)


def _initial_watermark(state: Dict[str, Any], modified_since_days: int) -> datetime:
    marker = state.get("watermark")
    parsed = parse_ocm_datetime(marker) if marker else None
    if parsed is not None:
        return parsed
    return datetime.now(timezone.utc) - timedelta(days=modified_since_days)


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple:
    """Acquire a Microsoft Entra JWT for the configured audience."""
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
    """Refresh the Entra JWT before it expires and re-establish the session."""
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


async def feed(
    api: OpenChargeMapAPI,
    broker_host: str,
    broker_port: int,
    cfg: FeedConfig,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    content_mode: str = "binary",
    auth_mode: str = "password",
    entra_audience: str = DEFAULT_ENTRA_AUDIENCE,
    entra_client_id: Optional[str] = None,
) -> None:
    state: Dict[str, Any] = load_state(cfg.state_file)
    poi_sigs: Dict[str, Any] = state.get("pois", {})
    watermark = _initial_watermark(state, cfg.modified_since_days)
    last_ref_emit = 0.0

    # Each generated MQTT client wrapper registers its own paho callbacks
    # (on_connect/on_message/on_disconnect) on the paho client it is given.
    # The locations and reference message groups generate two distinct wrapper
    # classes, so they must each own a dedicated paho client -- sharing one
    # would let the second wrapper's __init__ clobber the first's on_connect
    # callback, and the first wrapper's connect() would hang waiting for a
    # CONNACK that is delivered to the other wrapper. Mirrors usgs-iv.
    loc_client_id = f"{client_id}-loc" if client_id else ""
    ref_client_id = f"{client_id}-ref" if client_id else ""
    loc_paho = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=loc_client_id,
        protocol=MQTTv5,
    )
    ref_paho = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=ref_client_id,
        protocol=MQTTv5,
    )

    refresh_tasks: List[asyncio.Task] = []
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
        loc_paho.username_pw_set(username, password or "")
        ref_paho.username_pw_set(username, password or "")

    if tls or auth_mode == "entra":
        loc_paho.tls_set()
        ref_paho.tls_set()

    loop = asyncio.get_running_loop()
    loc_client = IOOpenChargeMapLocationsMqttMqttClient(
        client=loc_paho,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )
    ref_client = IOOpenChargeMapReferenceMqttMqttClient(
        client=ref_paho,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info(
        "Connecting to MQTT broker %s:%s (tls=%s, auth=%s, country=%s)",
        broker_host,
        broker_port,
        tls or auth_mode == "entra",
        auth_mode,
        cfg.country_code or "<global>",
    )
    if auth_mode == "entra":
        for _paho in (loc_paho, ref_paho):
            _paho.connect(
                broker_host,
                broker_port,
                keepalive=60,
                clean_start=True,
                properties=connect_properties,
            )
            _paho.loop_start()
    else:
        await loc_client.connect(broker_host, broker_port)
        await ref_client.connect(broker_host, broker_port)

    if auth_mode == "entra" and expires_at is not None:
        for _paho in (loc_paho, ref_paho):
            refresh_tasks.append(
                asyncio.create_task(
                    _entra_token_refresh_loop(
                        _paho,
                        broker_host,
                        broker_port,
                        60,
                        entra_audience,
                        entra_client_id,
                        expires_at,
                    )
                )
            )

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                now_ts = time.time()
                reference_due = (now_ts - last_ref_emit) >= cfg.reference_refresh_interval

                ref_count = 0
                if reference_due:
                    references = parse_reference_data(api.list_reference_data())
                    for r in references:
                        try:
                            method = getattr(
                                ref_client,
                                f"publish_io_open_charge_map_mqtt_{r.reference_type}",
                            )
                            await method(
                                feedurl=f"{REFERENCE_URL}#{r.reference_type}/{r.reference_id}",
                                reference_type=r.reference_type,
                                reference_id=str(r.reference_id),
                                data=_build_reference(r),
                            )
                            ref_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error(
                                "Error publishing reference %s/%s: %s",
                                r.reference_type,
                                r.reference_id,
                                e,
                            )
                    last_ref_emit = now_ts

                pois = api.list_pois(
                    modified_since=watermark,
                    country_code=cfg.country_code,
                    max_results=cfg.max_results,
                    opendata=cfg.opendata,
                )
                loc_count = 0
                max_change = watermark
                for raw in pois:
                    p = parse_poi(raw)
                    if p.poi_id == 0:
                        continue
                    signature = p.change_signature()
                    key = str(p.poi_id)
                    if poi_sigs.get(key) != signature:
                        try:
                            await loc_client.publish_io_open_charge_map_mqtt_charging_location(
                                feedurl=f"{POI_URL}#{p.poi_id}",
                                poi_id=key,
                                data=_build_location(p),
                            )
                            loc_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing location %s: %s", p.poi_id, e)
                        poi_sigs[key] = signature
                    latest = p.latest_change()
                    if latest is not None and latest > max_change:
                        max_change = latest

                watermark = max_change
                save_state(cfg.state_file, {"watermark": watermark.isoformat(), "pois": poi_sigs})
                end_time = datetime.now(timezone.utc)
                effective = max(
                    0, cfg.polling_interval - (end_time - start_time).total_seconds()
                )
                logger.info(
                    "Published %s reference + %s location events in %.1fs (watermark=%s). "
                    "Sleeping until %s.",
                    ref_count,
                    loc_count,
                    (end_time - start_time).total_seconds(),
                    watermark.isoformat(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                if cfg.once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                await asyncio.sleep(cfg.polling_interval)
    finally:
        for _task in refresh_tasks:
            _task.cancel()
        await loc_client.disconnect()
        await ref_client.disconnect()


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
    parser = argparse.ArgumentParser(description="Open Charge Map -> MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed", help="Feed Open Charge Map reference and location CloudEvents to MQTT"
    )
    feed_parser.add_argument(
        "--broker-url", type=str, default=os.getenv("MQTT_BROKER_URL"),
        help="MQTT broker URL (e.g. mqtt://localhost:1883 or mqtts://broker:8883)",
    )
    feed_parser.add_argument(
        "--broker-host", type=str, default=os.getenv("MQTT_HOST"),
        help="MQTT broker hostname (alternative to --broker-url)",
    )
    feed_parser.add_argument(
        "--broker-port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None,
        help="MQTT broker port (default 1883, or 8883 with --tls)",
    )
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument(
        "--tls", action="store_true",
        default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"),
    )
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument(
        "--content-mode", type=str, default=os.getenv("MQTT_CONTENT_MODE", "binary"),
        choices=["binary", "structured"],
        help="CloudEvents content mode (default: binary)",
    )
    feed_parser.add_argument(
        "-i", "--polling-interval", type=int,
        default=int(os.getenv("POLLING_INTERVAL", "600")),
        help="Delta polling interval in seconds",
    )
    feed_parser.add_argument(
        "--reference-refresh-interval", type=int,
        default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "86400")),
        help="Seconds between full re-emissions of reference data",
    )
    feed_parser.add_argument(
        "--country-code", type=str, default=os.getenv("OCM_COUNTRYCODE"),
        help="Optional ISO country code to scope the POI query (default: global)",
    )
    feed_parser.add_argument(
        "--modified-since-days", type=int,
        default=int(os.getenv("OCM_MODIFIED_SINCE_DAYS", "1")),
        help="Initial look-back window in days for the first delta poll",
    )
    feed_parser.add_argument(
        "--max-results", type=int, default=int(os.getenv("OCM_MAX_RESULTS", "5000")),
        help="Maximum POI records requested per poll",
    )
    feed_parser.add_argument(
        "--state-file", type=str,
        default=os.getenv("STATE_FILE", os.path.expanduser("~/.open_charge_map_state.json")),
    )
    feed_parser.add_argument(
        "--once", action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle.",
    )
    feed_parser.add_argument(
        "--auth-mode", type=str, default=os.getenv("MQTT_AUTH_MODE", "password"),
        choices=["password", "entra"],
        help="Authentication mode: 'password' (default) for username/password, "
        "or 'entra' for Microsoft Entra JWT via managed identity "
        "(suitable for Azure Event Grid namespace MQTT brokers).",
    )
    feed_parser.add_argument(
        "--entra-audience", type=str,
        default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE),
        help=f"Entra token audience (default: {DEFAULT_ENTRA_AUDIENCE}).",
    )
    feed_parser.add_argument(
        "--entra-client-id", type=str, default=os.getenv("MQTT_ENTRA_CLIENT_ID"),
        help="Optional user-assigned managed identity client id; "
        "defaults to DefaultAzureCredential resolution.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> None:
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

    cfg = FeedConfig.from_env(
        polling_interval=args.polling_interval,
        state_file=args.state_file,
        once=args.once,
        reference_refresh_interval=args.reference_refresh_interval,
        country_code=args.country_code,
        modified_since_days=args.modified_since_days,
        max_results=args.max_results,
    )
    api = OpenChargeMapAPI()
    asyncio.run(
        feed(
            api,
            host,
            port,
            cfg,
            username=username,
            password=password,
            tls=tls,
            client_id=args.client_id,
            content_mode=args.content_mode,
            auth_mode=args.auth_mode,
            entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id,
        )
    )


if __name__ == "__main__":
    main()
