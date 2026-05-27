from __future__ import annotations
import argparse, asyncio, os, time
from urllib.parse import urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from nws_forecasts_mqtt_producer_data import ForecastZone, LandForecastPeriod, LandZoneForecast, MarineForecastPeriod, MarineZoneForecast, ZoneTypeenum
from nws_forecasts_mqtt_producer_mqtt_client.client import MicrosoftOpenDataUSNOAANWSForecastsMqttMqttClient

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
        host,port=_parse(args.mqtt_broker_url); p=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5); c=MicrosoftOpenDataUSNOAANWSForecastsMqttMqttClient(client=p, content_mode='binary', loop=asyncio.get_running_loop()); await c.connect(host,port); await _mock(c); await asyncio.sleep(1); await c.disconnect()
    asyncio.run(run())
if __name__=='__main__': main()

