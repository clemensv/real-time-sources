from __future__ import annotations
import argparse, asyncio, os
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from singapore_nea_mqtt_producer_data import Station, WeatherObservation, Region, PSIReading, PM25Reading
from singapore_nea_mqtt_producer_mqtt_client.client import SGGovNEAWeatherMqttMqttClient, SGGovNEAAirQualityMqttMqttClient

from singapore_nea_core import (
    NEAWeatherAPI,
    NEAAirQualityAPI,
    merge_observations,
    fetch_psi_readings,
    fetch_pm25_readings,
    load_state,
    save_state,
    split_state,
    compose_state,
    AIR_QUALITY_REFERENCE_REFRESH_INTERVAL,
)

import json
import time as _time

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
        return resolved_client_id, str(username or ""), str(password or ""), None

    audience = os.getenv("MQTT_ENTRA_AUDIENCE", "https://eventgrid.azure.net/")
    managed_identity_client_id = os.getenv("MQTT_ENTRA_CLIENT_ID") or None
    resolved_username = resolved_client_id or str(username or "").strip()
    if not resolved_username:
        raise ValueError("MQTT_CLIENT_ID (or --client-id) is required for MQTT_AUTH_MODE=entra")

    resolved_password = _fetch_entra_mqtt_token(audience, managed_identity_client_id)
    # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
    from paho.mqtt.properties import Properties as _MqttConnProps
    from paho.mqtt.packettypes import PacketTypes as _MqttPktTypes
    _connect_props = _MqttConnProps(_MqttPktTypes.CONNECT)
    _connect_props.AuthenticationMethod = "OAUTH2-JWT"
    _connect_props.AuthenticationData = resolved_password.encode("utf-8")
    return resolved_client_id, resolved_username, resolved_password, _connect_props

def _parse(url):
    p=urlparse(url if '://' in url else 'mqtt://'+url); return p.hostname or 'localhost', p.port or 1883

async def _mock(w, aq):
    now=datetime(2026,4,7,10,0,tzinfo=timezone.utc)
    st=Station(station_id='S109', device_id='S109', name='Ang Mo Kio Avenue 5', latitude=1.3764, longitude=103.8492, data_types='air_temperature,rainfall')
    obs=WeatherObservation(station_id='S109', station_name='Ang Mo Kio Avenue 5', observation_time=now, air_temperature=30.5, rainfall=0.0, relative_humidity=75.0, wind_speed=2.1, wind_direction=180.0)
    reg=Region(region='central', latitude=1.357, longitude=103.82)
    psi=PSIReading(region='central', timestamp=now, update_timestamp=now, psi_twenty_four_hourly=52, o3_sub_index=10, pm10_sub_index=20, pm10_twenty_four_hourly=25, pm25_sub_index=30, pm25_twenty_four_hourly=12, co_sub_index=5, co_eight_hour_max=1, so2_sub_index=2, so2_twenty_four_hourly=3, no2_one_hour_max=8, o3_eight_hour_max=10)
    pm=PM25Reading(region='central', timestamp=now, update_timestamp=now, pm25_one_hourly=11)
    await w.publish_sg_gov_nea_weather_station_mqtt(station_id='S109', region='central', event='info', data=st)
    await w.publish_sg_gov_nea_weather_weather_observation_mqtt(station_id='S109', region='central', event='weather', data=obs)
    await aq.publish_sg_gov_nea_air_quality_region_mqtt(region='central', station_id='central', event='info', data=reg)
    await aq.publish_sg_gov_nea_air_quality_psireading_mqtt(region='central', station_id='central', event='psi', data=psi)
    await aq.publish_sg_gov_nea_air_quality_pm25_reading_mqtt(region='central', station_id='central', event='pm25', data=pm)


def _station_region(latitude: float, longitude: float) -> str:
    """Assign a Singapore geographic region based on station coordinates."""
    if latitude > 1.385:
        return "north"
    if latitude < 1.300:
        return "south"
    if longitude > 103.885:
        return "east"
    if longitude < 103.775:
        return "west"
    return "central"


async def _live(w: SGGovNEAWeatherMqttMqttClient, aq: SGGovNEAAirQualityMqttMqttClient, args) -> None:
    """Live acquisition loop using real NEA data published via MQTT."""
    polling_interval = int(os.getenv("POLLING_INTERVAL", "300"))
    aq_polling_interval = int(os.getenv("AIRQUALITY_POLLING_INTERVAL", "3600"))
    state_file = os.getenv("STATE_FILE", os.path.expanduser("~/.singapore_nea_mqtt_state.json"))

    weather_api = NEAWeatherAPI(polling_interval=polling_interval)
    aq_api = NEAAirQualityAPI(polling_interval=aq_polling_interval)

    previous_state = load_state(state_file)
    weather_state, psi_state, pm25_state = split_state(previous_state)

    # Emit station reference data at startup
    stations = weather_api.get_all_stations()
    for sid, sd in stations.items():
        station = Station(
            station_id=sd.station_id,
            device_id=sd.device_id,
            name=sd.name,
            latitude=sd.latitude,
            longitude=sd.longitude,
            data_types=sd.data_types,
        )
        await w.publish_sg_gov_nea_weather_station_mqtt(
            station_id=sid,
            region=_station_region(sd.latitude, sd.longitude),
            event="info",
            data=station,
        )

    # Emit region reference data at startup
    regions = aq_api.get_regions()
    for region_name, rd in regions.items():
        region = Region(region=rd.region, latitude=rd.latitude, longitude=rd.longitude)
        await aq.publish_sg_gov_nea_air_quality_region_mqtt(
            region=region_name, station_id=region_name, event="info", data=region
        )

    now = _time.monotonic()
    next_weather_poll = now
    next_aq_poll = now
    next_aq_region_refresh = now + AIR_QUALITY_REFERENCE_REFRESH_INTERVAL
    did_weather = False
    did_aq = False
    once = os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes")

    while True:
        now = _time.monotonic()
        next_due = min(next_weather_poll, next_aq_poll, next_aq_region_refresh)
        if now < next_due:
            await asyncio.sleep(max(1, min(int(next_due - now), 30)))
            continue

        state_changed = False

        if now >= next_weather_poll:
            did_weather = True
            next_weather_poll = now + polling_interval
            try:
                all_stations, observations = merge_observations(weather_api)
                for obs in observations:
                    key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
                    if key in weather_state:
                        continue
                    observation = WeatherObservation(
                        station_id=obs.station_id,
                        station_name=obs.station_name,
                        observation_time=obs.observation_time,
                        air_temperature=obs.air_temperature,
                        rainfall=obs.rainfall,
                        relative_humidity=obs.relative_humidity,
                        wind_speed=obs.wind_speed,
                        wind_direction=obs.wind_direction,
                    )
                    sd = all_stations.get(obs.station_id)
                    region = _station_region(sd.latitude, sd.longitude) if sd else "central"
                    await w.publish_sg_gov_nea_weather_weather_observation_mqtt(
                        station_id=obs.station_id, region=region, event="weather", data=observation
                    )
                    weather_state[key] = obs.observation_time.isoformat()
                state_changed = True
            except Exception as exc:  # pragma: no cover - runtime safety
                import logging as _log; _log.getLogger(__name__).error("Weather error: %s", exc)

        if now >= next_aq_region_refresh:
            next_aq_region_refresh = now + AIR_QUALITY_REFERENCE_REFRESH_INTERVAL
            try:
                regions = aq_api.get_regions()
                for region_name, rd in regions.items():
                    region = Region(region=rd.region, latitude=rd.latitude, longitude=rd.longitude)
                    await aq.publish_sg_gov_nea_air_quality_region_mqtt(
                        region=region_name, station_id=region_name, event="info", data=region
                    )
            except Exception as exc:  # pragma: no cover - runtime safety
                import logging as _log; _log.getLogger(__name__).error("Region refresh error: %s", exc)

        if now >= next_aq_poll:
            did_aq = True
            next_aq_poll = now + aq_polling_interval
            try:
                psi_readings = fetch_psi_readings(aq_api, psi_state)
                for psi_data in psi_readings:
                    psi = PSIReading(
                        region=psi_data.region,
                        timestamp=psi_data.timestamp,
                        update_timestamp=psi_data.update_timestamp,
                        psi_twenty_four_hourly=psi_data.psi_twenty_four_hourly,
                        o3_sub_index=psi_data.o3_sub_index,
                        pm10_sub_index=psi_data.pm10_sub_index,
                        pm10_twenty_four_hourly=psi_data.pm10_twenty_four_hourly,
                        pm25_sub_index=psi_data.pm25_sub_index,
                        pm25_twenty_four_hourly=psi_data.pm25_twenty_four_hourly,
                        co_sub_index=psi_data.co_sub_index,
                        co_eight_hour_max=psi_data.co_eight_hour_max,
                        so2_sub_index=psi_data.so2_sub_index,
                        so2_twenty_four_hourly=psi_data.so2_twenty_four_hourly,
                        no2_one_hour_max=psi_data.no2_one_hour_max,
                        o3_eight_hour_max=psi_data.o3_eight_hour_max,
                    )
                    await aq.publish_sg_gov_nea_air_quality_psireading_mqtt(
                        region=psi_data.region, station_id=psi_data.region, event="psi", data=psi
                    )
                pm25_readings = fetch_pm25_readings(aq_api, pm25_state)
                for pm25_data in pm25_readings:
                    pm25 = PM25Reading(
                        region=pm25_data.region,
                        timestamp=pm25_data.timestamp,
                        update_timestamp=pm25_data.update_timestamp,
                        pm25_one_hourly=pm25_data.pm25_one_hourly,
                    )
                    await aq.publish_sg_gov_nea_air_quality_pm25_reading_mqtt(
                        region=pm25_data.region, station_id=pm25_data.region, event="pm25", data=pm25
                    )
                state_changed = True
            except Exception as exc:  # pragma: no cover - runtime safety
                import logging as _log; _log.getLogger(__name__).error("Air quality error: %s", exc)

        if state_changed:
            save_state(state_file, compose_state(weather_state, psi_state, pm25_state))

        if once and did_weather and did_aq:
            break

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883'))
    f.add_argument('--mock', action='store_true', default=os.getenv('SINGAPORE_NEA_MOCK','').lower() in ('1','true','yes'), help='Emit one round of sample data and exit')
    a=ap.parse_args(argv)
    if a.command!='feed': ap.print_help(); return
    async def run():
        resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
            auth_mode=os.getenv("MQTT_AUTH_MODE"),
        )
        host,port=_parse(a.mqtt_broker_url); p=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if _entra_props is None and (resolved_username or resolved_password): p.username_pw_set(resolved_username, resolved_password)
        if _entra_props is not None or a.mqtt_broker_url.startswith(('mqtts://', 'ssl://')): p.tls_set()
        w=SGGovNEAWeatherMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); aq=SGGovNEAAirQualityMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop())
        # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
        if _entra_props is not None:
            import threading as _threading
            _connected = _threading.Event()
            def _on_connack(client, userdata, flags, reason_code, props=None):
                if reason_code == 0:
                    _connected.set()
            p.on_connect = _on_connack
            p.connect(host, port, keepalive=60, clean_start=True, properties=_entra_props)
            p.loop_start()
            if not await asyncio.get_running_loop().run_in_executor(None, lambda: _connected.wait(30)):
                raise RuntimeError('MQTT CONNACK timeout after 30s')
        else:
            await w.connect(host,port)
        if a.mock:
            await _mock(w,aq); await asyncio.sleep(1)
        else:
            await _live(w, aq, a)
        await w.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()
