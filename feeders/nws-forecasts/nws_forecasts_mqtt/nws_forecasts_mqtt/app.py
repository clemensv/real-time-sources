from __future__ import annotations
import argparse, asyncio, os, time
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from nws_forecasts_mqtt_producer_data import ForecastZone, LandForecastPeriod, LandZoneForecast, MarineForecastPeriod, MarineZoneForecast, ZoneTypeenum
from nws_forecasts_mqtt_producer_mqtt_client.client import MicrosoftOpenDataUSNOAANWSForecastsMqttMqttClient

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
async def _mock(client):
    zone=ForecastZone(zone_id='WAZ315', zone_type=ZoneTypeenum.public, name='City of Seattle', state='wa', forecast_office_url='https://api.weather.gov/offices/SEW', grid_identifier='SEW', awips_location_identifier='WAZ315', cwa_ids=['SEW'], forecast_office_urls=['https://api.weather.gov/offices/SEW'], time_zones=['America/Los_Angeles'], observation_station_ids=['KSEA'], radar_station='ATX', effective_date='2026-04-07T00:00:00+00:00', expiration_date='2030-01-01T00:00:00+00:00')
    land=LandZoneForecast(zone_id='WAZ315', updated='2026-04-07T10:00:00+00:00', periods=[LandForecastPeriod(period_number=1, period_name='Today', detailed_forecast='Synthetic land forecast.')])
    marine=MarineZoneForecast(zone_id='PZZ135', zone_name='Puget Sound and Hood Canal', product_title='Coastal Waters Forecast', office_name='NWS Seattle WA', issued_at_text='300 AM PDT Tue Apr 7 2026', expires_text='Tue Apr 7 2026', wmo_header='FZUS56 KSEW', bulletin_awips_id='CWFSEW', synopsis='Synthetic synopsis.', periods=[MarineForecastPeriod(period_name='TODAY', forecast_text='Synthetic marine forecast.')], bulletin_text='Synthetic marine bulletin.')
    await client.publish_microsoft_open_data_us_noaa_nws_forecasts_forecast_zone_mqtt(zone_id='WAZ315', state='wa', zone_type='public', event='info', data=zone)
    await client.publish_microsoft_open_data_us_noaa_nws_forecasts_land_zone_forecast_mqtt(zone_id='WAZ315', state='wa', zone_type='public', event='land-forecast', data=land)
    await client.publish_microsoft_open_data_us_noaa_nws_forecasts_marine_zone_forecast_mqtt(zone_id='PZZ135', state='pz', zone_type='marine', event='marine-forecast', data=marine)

def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--mqtt-broker-url', default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); f.add_argument('--once', action='store_true', default=True)
    args=ap.parse_args(argv)
    if args.command!='feed': ap.print_help(); return
    async def run():
        resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
            auth_mode=os.getenv("MQTT_AUTH_MODE"),
        )
        host,port=_parse(args.mqtt_broker_url); p=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
        if _entra_props is None and (resolved_username or resolved_password): p.username_pw_set(resolved_username, resolved_password)
        if _entra_props is not None or args.mqtt_broker_url.startswith(('mqtts://', 'ssl://')): p.tls_set()
        c=MicrosoftOpenDataUSNOAANWSForecastsMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop())
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
            await c.connect(host,port)
        await _mock(c); await asyncio.sleep(1); await c.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()

