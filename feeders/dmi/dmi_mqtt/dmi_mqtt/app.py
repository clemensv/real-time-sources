"""MQTT/UNS feeder application for the DMI observation triad.

Publishes metObs and oceanObs reference and telemetry events into a Unified
Namespace topic tree on an MQTT 5 broker as retained QoS-1 last-known-value
messages. Lightning strikes are intentionally excluded — per-strike events
do not fit LKV semantics, and the UNS subscribers are interested in current
state, not a firehose. CloudEvent metadata travels in MQTT 5 user properties
(binary content mode by default).
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

from dmi_core import (
    DmiApiKeys,
    DmiMetObsAPI,
    DmiOceanObsAPI,
    METOBS_FEED_ROOT,
    OCEANOBS_FEED_ROOT,
    load_state,
    save_state,
)
from dmi_mqtt_producer_data import (
    MetObsObservation,
    MetObsStation,
    OceanObservation,
    OceanStation,
    TidewaterPrediction,
    TidewaterStation,
)
from dmi_mqtt_producer_mqtt_client.client import (
    DkDmiMetObsMqttMqttClient,
    DkDmiOceanObsMqttMqttClient,
)
from dmi_amqp_producer_data.countryenum import CountryEnum
from dmi_amqp_producer_data.parameteridenum import ParameterIdenum

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"
ENTRA_MQTT_AUTH_METHOD = "OAUTH2-JWT"

logger = logging.getLogger(__name__)

_REFERENCE_REFRESH_SECONDS = 6 * 3600


def _opt_float(value: Any) -> Optional[float]:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _opt_str(value: Any) -> Optional[str]:
    return None if value is None else str(value)


def _build_met_station(raw: Dict[str, Any]) -> MetObsStation:
    return MetObsStation(
        station_id=str(raw.get("stationId") or raw.get("id") or ""),
        wmo_station_id=_opt_str(raw.get("wmoStationId")),
        wmo_country_code=_opt_str(raw.get("wmoCountryCode")),
        name=str(raw.get("name") or ""),
        country=CountryEnum(str(raw.get("country") or "")),  # type: ignore[arg-type]
        owner=_opt_str(raw.get("owner")),
        region_id=_opt_str(raw.get("regionId")),
        type=_opt_str(raw.get("type")),
        status=_opt_str(raw.get("status")),
        parameter_id=list(raw.get("parameterId") or []) or None,
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        station_height=_opt_float(raw.get("stationHeight")),
        barometer_height=_opt_float(raw.get("barometerHeight")),
        anemometer_height=_opt_float(raw.get("anemometerHeight")),
        valid_from=datetime.fromisoformat(_opt_str(raw.get("validFrom".replace("Z", "+00:00")))) if _opt_str(raw.get("validFrom")) else None,  # type: ignore[arg-type]
        valid_to=datetime.fromisoformat(_opt_str(raw.get("validTo".replace("Z", "+00:00")))) if _opt_str(raw.get("validTo")) else None,  # type: ignore[arg-type]
        operation_from=datetime.fromisoformat(_opt_str(raw.get("operationFrom".replace("Z", "+00:00")))) if _opt_str(raw.get("operationFrom")) else None,  # type: ignore[arg-type]
        operation_to=datetime.fromisoformat(_opt_str(raw.get("operationTo".replace("Z", "+00:00")))) if _opt_str(raw.get("operationTo")) else None,  # type: ignore[arg-type]
        created=datetime.fromisoformat(_opt_str(raw.get("created".replace("Z", "+00:00")))) if _opt_str(raw.get("created")) else None,  # type: ignore[arg-type]
        updated=datetime.fromisoformat(_opt_str(raw.get("updated".replace("Z", "+00:00")))) if _opt_str(raw.get("updated")) else None,  # type: ignore[arg-type]
    )


def _build_met_observation(raw: Dict[str, Any]) -> MetObsObservation:
    return MetObsObservation(
        observation_id=_opt_str(raw.get("id") or raw.get("observationId")),
        station_id=str(raw.get("stationId") or ""),
        parameter_id=ParameterIdenum(str(raw.get("parameterId") or "")),  # type: ignore[arg-type]
        observed=datetime.fromisoformat(str(raw.get("observed".replace("Z", "+00:00")) or "")),
        value=float(raw.get("value") or 0.0),
        latitude=_opt_float(raw.get("latitude")),
        longitude=_opt_float(raw.get("longitude")),
    )


def _build_ocean_station(raw: Dict[str, Any]) -> OceanStation:
    return OceanStation(
        station_id=str(raw.get("stationId") or raw.get("id") or ""),
        name=str(raw.get("name") or ""),
        country=CountryEnum(str(raw.get("country") or "")) if str(raw.get("country") or "") else None,  # type: ignore[arg-type]
        owner=_opt_str(raw.get("owner")),
        type=_opt_str(raw.get("type")),
        status=_opt_str(raw.get("status")),
        parameter_id=list(raw.get("parameterId") or []) or None,
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        valid_from=datetime.fromisoformat(_opt_str(raw.get("validFrom".replace("Z", "+00:00")))) if _opt_str(raw.get("validFrom")) else None,  # type: ignore[arg-type]
        valid_to=datetime.fromisoformat(_opt_str(raw.get("validTo".replace("Z", "+00:00")))) if _opt_str(raw.get("validTo")) else None,  # type: ignore[arg-type]
        operation_from=datetime.fromisoformat(_opt_str(raw.get("operationFrom".replace("Z", "+00:00")))) if _opt_str(raw.get("operationFrom")) else None,  # type: ignore[arg-type]
        operation_to=datetime.fromisoformat(_opt_str(raw.get("operationTo".replace("Z", "+00:00")))) if _opt_str(raw.get("operationTo")) else None,  # type: ignore[arg-type]
        created=datetime.fromisoformat(_opt_str(raw.get("created".replace("Z", "+00:00")))) if _opt_str(raw.get("created")) else None,  # type: ignore[arg-type]
        updated=datetime.fromisoformat(_opt_str(raw.get("updated".replace("Z", "+00:00")))) if _opt_str(raw.get("updated")) else None,  # type: ignore[arg-type]
    )


def _build_tidewater_station(raw: Dict[str, Any]) -> TidewaterStation:
    return TidewaterStation(
        station_id=str(raw.get("stationId") or raw.get("id") or ""),
        name=str(raw.get("name") or ""),
        country=CountryEnum(str(raw.get("country") or "")) if str(raw.get("country") or "") else None,  # type: ignore[arg-type]
        owner=_opt_str(raw.get("owner")),
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        valid_from=datetime.fromisoformat(_opt_str(raw.get("validFrom".replace("Z", "+00:00")))) if _opt_str(raw.get("validFrom")) else None,  # type: ignore[arg-type]
        valid_to=datetime.fromisoformat(_opt_str(raw.get("validTo".replace("Z", "+00:00")))) if _opt_str(raw.get("validTo")) else None,  # type: ignore[arg-type]
    )


def _build_ocean_observation(raw: Dict[str, Any]) -> OceanObservation:
    return OceanObservation(
        observation_id=_opt_str(raw.get("id") or raw.get("observationId")),
        station_id=str(raw.get("stationId") or ""),
        parameter_id=ParameterIdenum(str(raw.get("parameterId") or "")),  # type: ignore[arg-type]
        observed=datetime.fromisoformat(str(raw.get("observed".replace("Z", "+00:00")) or "")),
        value=float(raw.get("value") or 0.0),
        latitude=_opt_float(raw.get("latitude")),
        longitude=_opt_float(raw.get("longitude")),
    )


def _build_tidewater_prediction(raw: Dict[str, Any]) -> TidewaterPrediction:
    return TidewaterPrediction(
        prediction_id=_opt_str(raw.get("id") or raw.get("predictionId")),
        station_id=str(raw.get("stationId") or ""),
        prediction_type=_opt_str(raw.get("predictionType")),
        prediction_time=datetime.fromisoformat(str(raw.get("predictionTime".replace("Z", "+00:00")) or raw.get("observed") or "")),
        value=float(raw.get("value") or 0.0),
        latitude=_opt_float(raw.get("latitude")),
        longitude=_opt_float(raw.get("longitude")),
    )


def _acquire_entra_token(audience: str, client_id: Optional[str]) -> tuple:
    try:
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
    except ImportError as exc:  # pragma: no cover - import error path
        raise RuntimeError(
            "azure-identity must be installed to use MQTT_AUTH_MODE=entra"
        ) from exc
    credential = (
        ManagedIdentityCredential(client_id=client_id) if client_id else DefaultAzureCredential()
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
    met_api: Optional[DmiMetObsAPI],
    ocean_api: Optional[DmiOceanObsAPI],
    met_client: DkDmiMetObsMqttMqttClient,
    ocean_client: DkDmiOceanObsMqttMqttClient,
) -> int:
    count = 0
    if met_api is not None:
        for station in met_api.list_stations():
            sid = str(station.get("stationId") or station.get("id") or "")
            if not sid:
                continue
            await met_client.publish_dk_dmi_met_obs_mqtt_station(
                feedurl=f"{METOBS_FEED_ROOT}/collections/station/items/{sid}",
                station_id=sid,
                data=_build_met_station(station),
            )
            count += 1
    if ocean_api is not None:
        for station in ocean_api.list_stations():
            sid = str(station.get("stationId") or station.get("id") or "")
            if not sid:
                continue
            await ocean_client.publish_dk_dmi_ocean_obs_mqtt_station(
                feedurl=f"{OCEANOBS_FEED_ROOT}/collections/station/items/{sid}",
                station_id=sid,
                data=_build_ocean_station(station),
            )
            count += 1
        for station in ocean_api.list_tidewater_stations():
            sid = str(station.get("stationId") or station.get("id") or "")
            if not sid:
                continue
            await ocean_client.publish_dk_dmi_ocean_obs_mqtt_tidewater_station(
                feedurl=f"{OCEANOBS_FEED_ROOT}/collections/tidewaterstation/items/{sid}",
                station_id=sid,
                data=_build_tidewater_station(station),
            )
            count += 1
    return count


async def feed(
    api_keys: DmiApiKeys,
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
    state = load_state(state_file)
    seen_met: Dict[str, str] = state.setdefault("metObs_latest", {})
    seen_ocean: Dict[str, str] = state.setdefault("oceanObs_latest", {})
    seen_tide: Dict[str, str] = state.setdefault("tidewater_latest", {})

    met_api = DmiMetObsAPI(api_keys.met_obs)
    ocean_api = DmiOceanObsAPI(api_keys.ocean_obs)

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )

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
    met_client = DkDmiMetObsMqttMqttClient(
        client=paho_client, content_mode=content_mode, loop=loop  # type: ignore[arg-type]
    )
    ocean_client = DkDmiOceanObsMqttMqttClient(
        client=paho_client, content_mode=content_mode, loop=loop  # type: ignore[arg-type]
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
        await met_client.connect(broker_host, broker_port)

    refresh_task: Optional[asyncio.Task] = None
    if auth_mode == "entra" and expires_at is not None:
        refresh_task = asyncio.create_task(
            _entra_token_refresh_loop(
                paho_client, broker_host, broker_port, 60,
                entra_audience, entra_client_id, expires_at,
            )
        )

    logger.info("Publishing reference data under weather/dk/dmi and ocean/dk/dmi ...")
    ref_count = await _publish_reference(met_api, ocean_api, met_client, ocean_client)
    logger.info("Reference data published: %d retained events", ref_count)
    last_reference_refresh = time.monotonic()

    period = os.getenv("DMI_OBSERVATION_PERIOD", "latest-hour")

    try:
        while True:
            try:
                cycle_start = datetime.now(timezone.utc)
                telemetry_count = 0
                if met_api is not None:
                    for obs in met_api.iter_observations(period=period):
                        sid = str(obs.get("stationId") or "")
                        pid = str(obs.get("parameterId") or "")
                        observed = str(obs.get("observed") or "")
                        if not sid or not pid or not observed:
                            continue
                        key = f"{sid}|{pid}"
                        if seen_met.get(key) == observed:
                            continue
                        seen_met[key] = observed
                        try:
                            await met_client.publish_dk_dmi_met_obs_mqtt_observation(
                                feedurl=f"{METOBS_FEED_ROOT}/collections/observation/items?stationId={sid}&parameterId={pid}",
                                station_id=sid,
                                parameter_id=pid,
                                data=_build_met_observation(obs),
                            )
                            telemetry_count += 1
                        except Exception as exc:  # pylint: disable=broad-except
                            logger.error("MQTT publish failed for metObs %s/%s: %s", sid, pid, exc)
                if ocean_api is not None:
                    for obs in ocean_api.iter_observations(period=period):
                        sid = str(obs.get("stationId") or "")
                        pid = str(obs.get("parameterId") or "")
                        observed = str(obs.get("observed") or "")
                        if not sid or not pid or not observed:
                            continue
                        key = f"{sid}|{pid}"
                        if seen_ocean.get(key) == observed:
                            continue
                        seen_ocean[key] = observed
                        try:
                            await ocean_client.publish_dk_dmi_ocean_obs_mqtt_observation(
                                feedurl=f"{OCEANOBS_FEED_ROOT}/collections/observation/items?stationId={sid}&parameterId={pid}",
                                station_id=sid,
                                parameter_id=pid,
                                data=_build_ocean_observation(obs),
                            )
                            telemetry_count += 1
                        except Exception as exc:  # pylint: disable=broad-except
                            logger.error("MQTT publish failed for oceanObs %s/%s: %s", sid, pid, exc)
                    for pred in ocean_api.iter_tidewater(period=period):
                        sid = str(pred.get("stationId") or "")
                        when = str(pred.get("predictionTime") or pred.get("observed") or "")
                        if not sid or not when:
                            continue
                        if seen_tide.get(sid) == when:
                            continue
                        seen_tide[sid] = when
                        try:
                            await ocean_client.publish_dk_dmi_ocean_obs_mqtt_tidewater_prediction(
                                feedurl=f"{OCEANOBS_FEED_ROOT}/collections/tidewater/items?stationId={sid}",
                                station_id=sid,
                                data=_build_tidewater_prediction(pred),
                            )
                            telemetry_count += 1
                        except Exception as exc:  # pylint: disable=broad-except
                            logger.error("MQTT publish failed for tidewater %s: %s", sid, exc)
                cycle_end = datetime.now(timezone.utc)
                elapsed = (cycle_end - cycle_start).total_seconds()
                effective = max(0.0, polling_interval - elapsed)
                logger.info(
                    "Published %d telemetry events in %.2fs; sleeping until %s",
                    telemetry_count,
                    elapsed,
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                save_state(state_file, state)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if time.monotonic() - last_reference_refresh >= _REFERENCE_REFRESH_SECONDS:
                    ref_count = await _publish_reference(met_api, ocean_api, met_client, ocean_client)
                    logger.info("Reference data refreshed: %d retained events", ref_count)
                    last_reference_refresh = time.monotonic()
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting on keyboard interrupt")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("DMI polling cycle failed: %s", exc)
                await asyncio.sleep(polling_interval)
    finally:
        if refresh_task is not None:
            refresh_task.cancel()
        try:
            await met_client.disconnect()
        except Exception:  # pylint: disable=broad-except
            pass


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
    parser = argparse.ArgumentParser(description="DMI observation triad → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed DMI observations as CloudEvents to MQTT/UNS")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("MQTT_TLS", os.getenv("MQTT_ENABLE_TLS", "")).lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str,
                             default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("--metobs-api-key", type=str, default=None)
    feed_parser.add_argument("--oceanobs-api-key", type=str, default=None)
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.dmi_mqtt_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--auth-mode", type=str,
                             default=os.getenv("MQTT_AUTH_MODE", "password"),
                             choices=["password", "entra"])
    feed_parser.add_argument("--entra-audience", type=str,
                             default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    feed_parser.add_argument("--entra-client-id", type=str,
                             default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
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

    api_keys = DmiApiKeys.from_env(
        met_obs=args.metobs_api_key,
        ocean_obs=args.oceanobs_api_key,
    )

    asyncio.run(
        feed(
            api_keys,
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
