"""MQTT feeder for NOAA SWPC L1 → Unified Namespace.

Publishes one retained QoS-1 message per new propagated-solar-wind row to a
single LKV topic per spacecraft:

    space-weather/us/noaa-swpc/l1/{spacecraft}/propagated-solar-wind

Supports anonymous, username/password, TLS, and Microsoft Entra JWT
(Event Grid namespace MQTT) authentication. CloudEvent metadata is carried
in MQTT v5 user properties (binary content mode).
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from noaa_swpc_l1_core import (
    FEED_URL,
    PropagatedSolarWindRow,
    SwpcL1API,
    load_state,
    save_state,
)
from noaa_swpc_l1_mqtt_producer_data.gov.noaa.swpc.l1.propagatedsolarwind import (
    PropagatedSolarWind,
)
from noaa_swpc_l1_mqtt_producer_data.gov.noaa.swpc.l1.spacecraftenum import (
    SpacecraftEnum,
)
from noaa_swpc_l1_mqtt_producer_mqtt_client.client import (
    GovNoaaSwpcL1MqttMqttClient,
)

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

logger = logging.getLogger(__name__)


def _row_to_data(row: PropagatedSolarWindRow) -> PropagatedSolarWind:
    return PropagatedSolarWind(
        spacecraft=SpacecraftEnum(row.spacecraft),
        time_tag=row.time_tag,
        propagated_time_tag=row.propagated_time_tag,
        speed=row.speed,
        density=row.density,
        temperature=row.temperature,
        bx=row.bx,
        by=row.by,
        bz=row.bz,
        bt=row.bt,
        vx=row.vx,
        vy=row.vy,
        vz=row.vz,
    )


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple:
    """Acquire an Entra JWT for the configured audience; returns (token, expires_at)."""
    try:
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    except ImportError as exc:  # pragma: no cover
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
    """Disconnect + reconnect with a fresh JWT ~5 minutes before expiry."""
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
                    "Refreshed Entra JWT (next expiry=%s)",
                    expires_at.isoformat(),
                )
            except Exception as exc:  # pylint: disable=broad-except
                logger.warning("Reconnect after token refresh failed: %s", exc)
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to refresh Entra JWT: %s", exc)
            await asyncio.sleep(60)


async def feed(
    api: SwpcL1API,
    broker_host: str,
    broker_port: int,
    *,
    spacecraft: str,
    polling_interval: int,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    backfill_minutes: int = 5,
    content_mode: str = "binary",
    auth_mode: str = "password",
    entra_audience: str = DEFAULT_ENTRA_AUDIENCE,
    entra_client_id: Optional[str] = None,
) -> None:
    state = load_state(state_file)
    last_seen_iso: Optional[str] = state.get("last_time_tag")
    last_seen: Optional[datetime]
    if last_seen_iso:
        try:
            last_seen = datetime.fromisoformat(last_seen_iso.replace("Z", "+00:00"))
        except ValueError:
            last_seen = None
    else:
        last_seen = None
    if last_seen is None:
        last_seen = datetime.now(timezone.utc) - timedelta(minutes=backfill_minutes)
        logger.info(
            "No prior state; starting from %s (last %d minutes)",
            last_seen.isoformat(),
            backfill_minutes,
        )

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
    mqtt_client = GovNoaaSwpcL1MqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info(
        "Connecting to MQTT broker %s:%s (tls=%s, auth=%s, spacecraft=%s)",
        broker_host,
        broker_port,
        tls or auth_mode == "entra",
        auth_mode,
        spacecraft,
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

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                new_rows = list(api.fetch_new_rows(spacecraft, since=last_seen))
                count = 0
                for row in new_rows:
                    try:
                        await mqtt_client.publish_gov_noaa_swpc_l1_mqtt_propagated_solar_wind(
                            feedurl=FEED_URL,
                            spacecraft=row.spacecraft,
                            _time=row.time_tag.isoformat(),
                            data=_row_to_data(row),
                        )
                        count += 1
                        last_seen = row.time_tag
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error publishing row %s: %s", row.time_tag, e)
                if last_seen is not None:
                    save_state(
                        state_file, {"last_time_tag": last_seen.isoformat()}
                    )
                end_time = datetime.now(timezone.utc)
                effective = max(
                    0,
                    polling_interval - (end_time - start_time).total_seconds(),
                )
                logger.info(
                    "Published %s rows in %.2fs (last_time_tag=%s). Sleeping %.1fs.",
                    count,
                    (end_time - start_time).total_seconds(),
                    last_seen.isoformat() if last_seen else "<none>",
                    effective,
                )
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Polling error: %s — retrying in %ds", e, polling_interval)
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
    parser = argparse.ArgumentParser(
        description="NOAA SWPC L1 propagated solar wind → MQTT/UNS bridge."
    )
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser(
        "feed", help="Feed rows as retained CloudEvents to MQTT"
    )
    feed_parser.add_argument(
        "--broker-url",
        type=str,
        default=os.getenv("MQTT_BROKER_URL"),
        help="MQTT broker URL (mqtt://host:1883 or mqtts://host:8883)",
    )
    feed_parser.add_argument(
        "--broker-host", type=str, default=os.getenv("MQTT_HOST")
    )
    feed_parser.add_argument(
        "--broker-port",
        type=int,
        default=int(os.getenv("MQTT_PORT", "0")) or None,
    )
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument(
        "--tls",
        action="store_true",
        default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"),
    )
    feed_parser.add_argument(
        "--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID")
    )
    feed_parser.add_argument(
        "--content-mode",
        type=str,
        default=os.getenv("MQTT_CONTENT_MODE", "binary"),
        choices=["binary", "structured"],
    )
    polling_interval_default = int(os.getenv("POLLING_INTERVAL", "60"))
    feed_parser.add_argument(
        "-i", "--polling-interval", type=int, default=polling_interval_default
    )
    feed_parser.add_argument(
        "--spacecraft",
        type=str,
        default=os.getenv("SPACECRAFT", "dscovr"),
        choices=["dscovr", "ace"],
    )
    feed_parser.add_argument(
        "--backfill-minutes",
        type=int,
        default=int(os.getenv("BACKFILL_MINUTES", "5")),
    )
    feed_parser.add_argument(
        "--state-file",
        type=str,
        default=os.getenv(
            "STATE_FILE", os.path.expanduser("~/.noaa_swpc_l1_state.json")
        ),
    )
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
    )
    feed_parser.add_argument(
        "--auth-mode",
        type=str,
        default=os.getenv("MQTT_AUTH_MODE", "password"),
        choices=["password", "entra"],
    )
    feed_parser.add_argument(
        "--entra-audience",
        type=str,
        default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE),
    )
    feed_parser.add_argument(
        "--entra-client-id", type=str, default=os.getenv("MQTT_ENTRA_CLIENT_ID")
    )
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

    api = SwpcL1API()
    asyncio.run(
        feed(
            api,
            host,
            port,
            spacecraft=args.spacecraft,
            polling_interval=args.polling_interval,
            username=username,
            password=password,
            tls=tls,
            client_id=args.client_id,
            state_file=args.state_file,
            once=args.once,
            backfill_minutes=args.backfill_minutes,
            content_mode=args.content_mode,
            auth_mode=args.auth_mode,
            entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id,
        )
    )


if __name__ == "__main__":
    main()
