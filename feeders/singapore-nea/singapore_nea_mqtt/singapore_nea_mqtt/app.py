from __future__ import annotations
import argparse, asyncio, os
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from singapore_nea_mqtt_producer_data import Station, WeatherObservation, Region, PSIReading, PM25Reading
from singapore_nea_mqtt_producer_mqtt_client.client import SGGovNEAWeatherMqttMqttClient, SGGovNEAAirQualityMqttMqttClient

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

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883'))
    a=ap.parse_args(argv)
    if a.command!='feed': ap.print_help(); return
    async def run():
        resolved_client_id, resolved_username, resolved_password = _resolve_mqtt_connection_settings(
            auth_mode=os.getenv("MQTT_AUTH_MODE"),
        )
        host,port=_parse(a.mqtt_broker_url); p=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if resolved_username or resolved_password: p.username_pw_set(resolved_username, resolved_password)
        w=SGGovNEAWeatherMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); aq=SGGovNEAAirQualityMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); await w.connect(host,port); await _mock(w,aq); await asyncio.sleep(1); await w.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()
