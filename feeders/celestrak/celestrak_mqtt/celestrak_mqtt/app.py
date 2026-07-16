"""MQTT feeder application for CelesTrak -> Unified Namespace.

Wraps the upstream poller from :mod:`celestrak_core` and the generated
:class:`OrgCelestrakMqttMqttClient`. The MQTT broker is reached via a plain
``mqtt://host:port`` URL (or ``mqtts://`` for TLS); username/password are
optional. CloudEvent semantics are preserved end-to-end: binary mode maps CE
attributes to MQTT 5 user properties so subscribers can route on ``type``,
``source`` and ``subject`` without cracking the JSON body.

Reference data (the SATCAT catalog) is published first and refreshed
periodically; General Perturbations (GP) orbital element sets follow as
telemetry, deduplicated on their ``EPOCH``. Optional Supplemental GP (SupGP)
sources are published only when ``SUPGP_SOURCES`` is set. Each event is
published to ``space/celestrak/{satcat|gp|supgp}/{NORAD_CAT_ID}`` with the
retain flag set, so late subscribers immediately receive the last known state
of every catalogued object.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

from celestrak_core import (
    GP_URL,
    SATCAT_URL,
    SUPGP_URL,
    CelesTrakAPI,
    FeedConfig,
    load_state,
    save_state,
)
from celestrak_mqtt_producer_data.org.celestrak.orbitmeanelements import OrbitMeanElements
from celestrak_mqtt_producer_data.org.celestrak.satellitecatalogentry import SatelliteCatalogEntry
from celestrak_mqtt_producer_data.org.celestrak.supplementalorbitmeanelements import (
    SupplementalOrbitMeanElements,
)
from celestrak_mqtt_producer_mqtt_client.client import OrgCelestrakMqttMqttClient

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

logger = logging.getLogger(__name__)


def _opt_str(raw: Dict[str, Any], key: str) -> Optional[str]:
    value = raw.get(key)
    return value if value not in (None, "") else None


def _opt_float(raw: Dict[str, Any], key: str) -> Optional[float]:
    value = raw.get(key)
    if value is None or value == "":
        return None
    return float(value)


def _opt_int(raw: Dict[str, Any], key: str) -> Optional[int]:
    value = raw.get(key)
    if value is None or value == "":
        return None
    return int(value)


def _build_satcat(raw: Dict[str, Any]) -> SatelliteCatalogEntry:
    return SatelliteCatalogEntry(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        OBJECT_TYPE=_opt_str(raw, "OBJECT_TYPE"),
        OPS_STATUS_CODE=_opt_str(raw, "OPS_STATUS_CODE"),
        OWNER=_opt_str(raw, "OWNER"),
        LAUNCH_DATE=_opt_str(raw, "LAUNCH_DATE"),
        LAUNCH_SITE=_opt_str(raw, "LAUNCH_SITE"),
        DECAY_DATE=_opt_str(raw, "DECAY_DATE"),
        PERIOD=_opt_float(raw, "PERIOD"),
        INCLINATION=_opt_float(raw, "INCLINATION"),
        APOGEE=_opt_int(raw, "APOGEE"),
        PERIGEE=_opt_int(raw, "PERIGEE"),
        RCS=_opt_float(raw, "RCS"),
        DATA_STATUS_CODE=_opt_str(raw, "DATA_STATUS_CODE"),
        ORBIT_CENTER=_opt_str(raw, "ORBIT_CENTER"),
        ORBIT_TYPE=_opt_str(raw, "ORBIT_TYPE"),
    )


def _build_gp(raw: Dict[str, Any]) -> OrbitMeanElements:
    return OrbitMeanElements(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        EPOCH=datetime.fromisoformat(raw["EPOCH"]),
        MEAN_MOTION=float(raw["MEAN_MOTION"]),
        ECCENTRICITY=float(raw["ECCENTRICITY"]),
        INCLINATION=float(raw["INCLINATION"]),
        RA_OF_ASC_NODE=float(raw["RA_OF_ASC_NODE"]),
        ARG_OF_PERICENTER=float(raw["ARG_OF_PERICENTER"]),
        MEAN_ANOMALY=float(raw["MEAN_ANOMALY"]),
        EPHEMERIS_TYPE=int(raw["EPHEMERIS_TYPE"]),
        CLASSIFICATION_TYPE=raw["CLASSIFICATION_TYPE"],
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        ELEMENT_SET_NO=int(raw["ELEMENT_SET_NO"]),
        REV_AT_EPOCH=int(raw["REV_AT_EPOCH"]),
        BSTAR=float(raw["BSTAR"]),
        MEAN_MOTION_DOT=float(raw["MEAN_MOTION_DOT"]),
        MEAN_MOTION_DDOT=float(raw["MEAN_MOTION_DDOT"]),
    )


def _build_supgp(raw: Dict[str, Any]) -> SupplementalOrbitMeanElements:
    return SupplementalOrbitMeanElements(
        OBJECT_NAME=_opt_str(raw, "OBJECT_NAME"),
        OBJECT_ID=_opt_str(raw, "OBJECT_ID"),
        EPOCH=datetime.fromisoformat(raw["EPOCH"]),
        MEAN_MOTION=float(raw["MEAN_MOTION"]),
        ECCENTRICITY=float(raw["ECCENTRICITY"]),
        INCLINATION=float(raw["INCLINATION"]),
        RA_OF_ASC_NODE=float(raw["RA_OF_ASC_NODE"]),
        ARG_OF_PERICENTER=float(raw["ARG_OF_PERICENTER"]),
        MEAN_ANOMALY=float(raw["MEAN_ANOMALY"]),
        EPHEMERIS_TYPE=int(raw["EPHEMERIS_TYPE"]),
        CLASSIFICATION_TYPE=raw["CLASSIFICATION_TYPE"],
        NORAD_CAT_ID=int(raw["NORAD_CAT_ID"]),
        ELEMENT_SET_NO=int(raw["ELEMENT_SET_NO"]),
        REV_AT_EPOCH=int(raw["REV_AT_EPOCH"]),
        BSTAR=float(raw["BSTAR"]),
        MEAN_MOTION_DOT=float(raw["MEAN_MOTION_DOT"]),
        MEAN_MOTION_DDOT=float(raw["MEAN_MOTION_DDOT"]),
        RMS=_opt_float(raw, "RMS"),
        DATA_SOURCE=_opt_str(raw, "DATA_SOURCE"),
    )


def _satcat_source(norad: int) -> str:
    return f"{SATCAT_URL}?CATNR={norad}&FORMAT=json"


def _gp_source(norad: int) -> str:
    return f"{GP_URL}?CATNR={norad}&FORMAT=json"


def _supgp_source(norad: int) -> str:
    return f"{SUPGP_URL}?CATNR={norad}&FORMAT=json"


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple:
    """Acquire a Microsoft Entra JWT for the configured audience.

    Returns ``(token_string, expires_at_datetime)``. The returned token is
    suitable as the MQTT password against an Event Grid namespace MQTT broker
    configured with custom JWT authentication issued by Microsoft Entra ID.
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


async def _publish_reference(
    api: CelesTrakAPI,
    client: OrgCelestrakMqttMqttClient,
    cfg: FeedConfig,
) -> int:
    satcat = api.get_satcat(cfg.groups)
    count = 0
    for row in satcat:
        norad = int(row["NORAD_CAT_ID"])
        try:
            await client.publish_org_celestrak_mqtt_satellite_catalog_entry(
                feedurl=_satcat_source(norad),
                norad_cat_id=str(norad),
                data=_build_satcat(row),
            )
            count += 1
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error publishing SATCAT record %s: %s", norad, e)
    logger.info("Published %d SATCAT reference records", count)
    return count


async def feed(
    api: CelesTrakAPI,
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
    """Publish SATCAT reference data and GP/SupGP telemetry as CloudEvents to MQTT."""

    state: Dict[str, Any] = load_state(cfg.state_file)
    gp_state: Dict[str, str] = state.get("gp", {})
    supgp_state: Dict[str, str] = state.get("supgp", {})

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
    mqtt_client = OrgCelestrakMqttMqttClient(
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

    logger.info(
        "Starting CelesTrak feed to MQTT (groups=%s, supgp=%s)",
        ",".join(cfg.groups),
        ",".join(cfg.supgp_sources) or "<off>",
    )

    last_reference = 0.0
    try:
        while True:
            try:
                cycle_start = datetime.now(timezone.utc)
                now_mono = time.monotonic()

                if last_reference == 0.0 or (now_mono - last_reference) >= cfg.reference_refresh_interval:
                    await _publish_reference(api, mqtt_client, cfg)
                    last_reference = now_mono

                gp_count = 0
                for row in api.get_gp(cfg.groups):
                    norad = int(row["NORAD_CAT_ID"])
                    epoch = str(row.get("EPOCH"))
                    if gp_state.get(str(norad)) == epoch:
                        continue
                    try:
                        await mqtt_client.publish_org_celestrak_mqtt_orbit_mean_elements(
                            feedurl=_gp_source(norad),
                            norad_cat_id=str(norad),
                            data=_build_gp(row),
                        )
                        gp_state[str(norad)] = epoch
                        gp_count += 1
                    except Exception as e:  # pylint: disable=broad-except
                        logger.error("Error publishing GP element set %s: %s", norad, e)

                supgp_count = 0
                if cfg.supgp_sources:
                    for row in api.get_supgp(cfg.supgp_sources):
                        norad = int(row["NORAD_CAT_ID"])
                        dedup_key = f"{norad}|{row.get('DATA_SOURCE')}|{row.get('EPOCH')}"
                        if supgp_state.get(dedup_key):
                            continue
                        try:
                            await mqtt_client.publish_org_celestrak_mqtt_supplemental_orbit_mean_elements(
                                feedurl=_supgp_source(norad),
                                norad_cat_id=str(norad),
                                data=_build_supgp(row),
                            )
                            supgp_state[dedup_key] = str(row.get("EPOCH"))
                            supgp_count += 1
                        except Exception as e:  # pylint: disable=broad-except
                            logger.error("Error publishing SupGP element set %s: %s", norad, e)

                save_state(cfg.state_file, {"gp": gp_state, "supgp": supgp_state})
                elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
                logger.info(
                    "Published %d GP + %d SupGP element sets in %.1fs.",
                    gp_count,
                    supgp_count,
                    elapsed,
                )

                if api.halted:
                    backoff = max(cfg.polling_interval, 3600)
                    logger.error(
                        "CelesTrak usage-policy hard stop hit; backing off %ds before retrying.",
                        backoff,
                    )
                    if cfg.once:
                        break
                    await asyncio.sleep(backoff)
                    api.reset_halt()
                    continue

                if cfg.once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break

                effective = max(0.0, cfg.polling_interval - elapsed)
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as e:  # pylint: disable=broad-except
                logger.error("Error occurred: %s", e)
                await asyncio.sleep(cfg.polling_interval)
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
    parser = argparse.ArgumentParser(description="CelesTrak -> MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Feed SATCAT + GP element sets as CloudEvents to MQTT")
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
    feed_parser.add_argument("--groups", type=str, default=os.getenv("CELESTRAK_GROUPS"),
                             help="Comma-separated CelesTrak GROUP views (default: stations)")
    feed_parser.add_argument("--supgp-sources", type=str, default=os.getenv("SUPGP_SOURCES"),
                             help="Comma-separated Supplemental GP SOURCE views (default: off)")
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "3600")),
                             help="Telemetry polling interval in seconds (default: 3600)")
    feed_parser.add_argument("--reference-refresh-interval", type=int,
                             default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", "86400")),
                             help="SATCAT reference refresh interval in seconds (default: 86400)")
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.celestrak_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"),
                             help="Exit after one polling cycle (also via ONCE_MODE env var).")
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

    groups = [g.strip() for g in args.groups.split(",")] if args.groups else None
    supgp = [s.strip() for s in args.supgp_sources.split(",")] if args.supgp_sources else None
    feed_cfg = FeedConfig.from_env(
        groups=groups,
        supgp_sources=supgp,
        polling_interval=args.polling_interval,
        reference_refresh_interval=args.reference_refresh_interval,
        state_file=args.state_file,
        once=args.once,
    )

    api = CelesTrakAPI()
    asyncio.run(
        feed(
            api,
            host,
            port,
            feed_cfg,
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
