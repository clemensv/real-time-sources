"""MQTT companion feeder for bom-australia — real acquisition loop."""
from __future__ import annotations

import argparse
import asyncio
import logging
import os
import time
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from bom_australia_core import (  # type: ignore[attr-defined]
    BOMAustraliaAPI,
    WARNING_FEEDS,
    _load_state,
    _save_state,
    _parse_station_list,
    _parse_warning_feed_list,
    fetch_stations_parallel,
    fetch_latest_observations_parallel,
    fetch_new_warnings,
)
from bom_australia_mqtt_producer_mqtt_client.client import (
    AUGovBOMWeatherMqttMqttClient,
    AUGovBOMWarningMqttMqttClient,
)
from bom_australia_mqtt_producer_data import (
    Station as MqttStation,
    WeatherObservation as MqttWeatherObservation,
    WarningBulletin as MqttWarningBulletin,
)

logger = logging.getLogger(__name__)
SOURCE_ID = "bom-australia"
PY_MODULE = "bom_australia"


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _fetch_entra_mqtt_token(audience: str, managed_identity_client_id: str | None = None) -> str:
    params = {"api-version": "2018-02-01", "resource": audience or "https://eventgrid.azure.net/"}
    if managed_identity_client_id:
        params["client_id"] = managed_identity_client_id
    request = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(request, timeout=30) as response:
        payload = __import__("json").loads(response.read().decode("utf-8"))
    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS token response did not contain an access token")
    return str(token)


async def _run_live(args: argparse.Namespace) -> None:
    """Connect to the MQTT broker and run the real BOM acquisition loop."""
    parsed = urlparse(args.broker_url if "://" in args.broker_url else "mqtt://" + args.broker_url)
    broker = parsed.hostname or "localhost"
    port = parsed.port or (8883 if (parsed.scheme or "mqtt") in ("mqtts", "ssl", "tls") else 1883)
    use_tls = (parsed.scheme or "mqtt") in ("mqtts", "ssl", "tls") or args.tls
    username = parsed.username or ""
    password = parsed.password or ""

    auth_mode = os.getenv("MQTT_AUTH_MODE", "password").strip().lower()
    client_id = str(args.client_id or os.getenv("MQTT_CLIENT_ID", "")).strip()
    connect_props = None
    if auth_mode == "entra":
        audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
        mi_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
        resolved_username = client_id or username
        if not resolved_username:
            raise ValueError("MQTT_CLIENT_ID is required for MQTT_AUTH_MODE=entra")
        token = _fetch_entra_mqtt_token(audience, mi_client_id)
        from paho.mqtt.properties import Properties as _MqttConnProps
        from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
        connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
        connect_props.AuthenticationMethod = "OAUTH2-JWT"
        connect_props.AuthenticationData = token.encode("utf-8")
        use_tls = True
        username = resolved_username
        password = token

    raw_client = mqtt.Client(
        client_id=client_id or "",
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )
    if use_tls:
        raw_client.tls_set()
    if connect_props is None and (username or password):
        raw_client.username_pw_set(username, password)

    weather_client = AUGovBOMWeatherMqttMqttClient(
        raw_client, content_mode=args.content_mode
    )
    warning_client = AUGovBOMWarningMqttMqttClient(
        raw_client, content_mode=args.content_mode
    )

    await weather_client.connect(broker, port, properties=connect_props)

    api = BOMAustraliaAPI(polling_interval=args.polling_interval, fetch_workers=args.fetch_workers)

    if args.stations:
        station_list = _parse_station_list(args.stations)
    else:
        station_list = api.discover_stations(args.state_filter or None)
    warning_feeds = _parse_warning_feed_list(args.warning_feeds) if args.warning_feeds else list(WARNING_FEEDS)

    state = _load_state(args.state_file)
    previous_observations: dict = state.get("observations", {})
    previous_warnings: dict = state.get("warnings", {})

    logger.info("Emitting station reference data via MQTT (%d stations)…", len(station_list))
    stations = fetch_stations_parallel(api, station_list)
    for core_station, _ in stations:
        mqtt_station = MqttStation(
            station_wmo=core_station.station_wmo,
            name=core_station.name,
            product_id=core_station.product_id,
            state=core_station.state,
            time_zone=core_station.time_zone,
            latitude=core_station.latitude,
            longitude=core_station.longitude,
        )
        await weather_client.publish_au_gov_bom_weather_mqtt_station(
            station_wmo=core_station.station_wmo,
            state=core_station.state or "unknown",
            data=mqtt_station,
        )
    logger.info("Sent %d station record(s) via MQTT", len(stations))

    while True:
        logger.info("Polling observations for %d stations…", len(station_list))
        new_obs = fetch_latest_observations_parallel(api, station_list, previous_observations)
        for core_obs, _ in new_obs:
            mqtt_obs = MqttWeatherObservation(
                station_wmo=core_obs.station_wmo,
                station_name=core_obs.station_name,
                observation_time_utc=core_obs.observation_time_utc,  # type: ignore[arg-type]
                local_time=core_obs.local_time,
                air_temp=core_obs.air_temp,
                apparent_temp=core_obs.apparent_temp,
                dewpt=core_obs.dewpt,
                rel_hum=core_obs.rel_hum,
                delta_t=core_obs.delta_t,
                wind_dir=core_obs.wind_dir,
                wind_spd_kmh=core_obs.wind_spd_kmh,
                wind_spd_kt=core_obs.wind_spd_kt,
                gust_kmh=core_obs.gust_kmh,
                gust_kt=core_obs.gust_kt,
                press=core_obs.press,
                press_qnh=core_obs.press_qnh,
                press_msl=core_obs.press_msl,
                press_tend=core_obs.press_tend,
                rain_trace=core_obs.rain_trace,
                cloud=core_obs.cloud,
                cloud_oktas=core_obs.cloud_oktas,
                cloud_base_m=core_obs.cloud_base_m,
                cloud_type=core_obs.cloud_type,
                vis_km=core_obs.vis_km,
                weather=core_obs.weather,
                sea_state=core_obs.sea_state,
                swell_dir_worded=core_obs.swell_dir_worded,
                swell_height=core_obs.swell_height,
                swell_period=core_obs.swell_period,
                latitude=core_obs.latitude,
                longitude=core_obs.longitude,
                state=core_obs.state,
            )
            await weather_client.publish_au_gov_bom_weather_mqtt_weather_observation(
                station_wmo=core_obs.station_wmo,
                state=core_obs.state or "unknown",
                data=mqtt_obs,
            )
        logger.info("Sent %d new observation(s) via MQTT", len(new_obs))

        new_bulletins = fetch_new_warnings(api, warning_feeds, previous_warnings)
        for bulletin in new_bulletins:
            mqtt_bulletin = MqttWarningBulletin(
                warning_id=bulletin.warning_id,
                warning_url=bulletin.warning_url,
                feed_url=bulletin.feed_url,
                feed_title=bulletin.feed_title,
                title=bulletin.title,
                published_at=bulletin.published_at,  # type: ignore[arg-type]
                issued_local_time_text=bulletin.issued_local_time_text,
                warning_type=bulletin.warning_type,
                affected_area_text=bulletin.affected_area_text,
                severity=bulletin.severity,
                state=bulletin.state,
            )
            await warning_client.publish_au_gov_bom_warning_mqtt_warning_bulletin(
                state=bulletin.state or "unknown",
                severity=bulletin.severity or "unknown",
                warning_id=bulletin.warning_id,
                data=mqtt_bulletin,
            )
        logger.info("Sent %d new warning(s) via MQTT", len(new_bulletins))

        _save_state(args.state_file, {"observations": previous_observations, "warnings": previous_warnings})

        if args.once:
            break
        await asyncio.sleep(args.polling_interval)

    await weather_client.disconnect()


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = argparse.ArgumentParser(description=f"{SOURCE_ID} MQTT bridge")
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL", "mqtt://localhost:1883"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("MQTT_TLS", False))
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--content-mode", choices=("binary", "structured"),
                        default=os.getenv("MQTT_CONTENT_MODE", "binary"))
    parser.add_argument("--polling-interval", type=int,
                        default=int(os.getenv("POLLING_INTERVAL", "600")))
    parser.add_argument("--fetch-workers", type=int,
                        default=int(os.getenv("BOM_FETCH_WORKERS", "12")))
    parser.add_argument("--state-file",
                        default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_mqtt_state.json")))
    parser.add_argument("--stations", default=os.getenv("BOM_STATIONS", ""))
    parser.add_argument("--state-filter", default=os.getenv("BOM_STATE_FILTER", ""))
    parser.add_argument("--warning-feeds", default=os.getenv("BOM_WARNING_FEEDS", ""))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_run_live(args))


if __name__ == "__main__":
    main()
