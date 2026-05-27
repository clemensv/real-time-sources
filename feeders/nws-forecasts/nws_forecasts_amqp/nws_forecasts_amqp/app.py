from __future__ import annotations
import argparse, json, os
from cloudevents.http import CloudEvent, to_binary
from proton import Message
from proton.utils import BlockingConnection
from nws_forecasts_amqp_producer_data import ForecastZone, LandForecastPeriod, LandZoneForecast, MarineForecastPeriod, MarineZoneForecast, ZoneTypeenum

def _send(sender, type_, subject, data):
    attrs={'type':type_,'source':'https://api.weather.gov','subject':subject}; headers,body=to_binary(CloudEvent(attrs, data.to_byte_array('application/json'))); msg=Message(body=body if isinstance(body,bytes) else str(body).encode(), inferred=True); msg.content_type='application/json'; msg.properties={'cloudEvents:'+k[3:]:v for k,v in headers.items() if k.lower().startswith('ce-')}; msg.subject=subject; sender.send(msg)
def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--host',default=os.getenv('AMQP_HOST','localhost')); f.add_argument('--port',type=int,default=int(os.getenv('AMQP_PORT','5672'))); f.add_argument('--address',default=os.getenv('AMQP_ADDRESS','nws-forecasts')); f.add_argument('--username',default=os.getenv('AMQP_USERNAME')); f.add_argument('--password',default=os.getenv('AMQP_PASSWORD'))
    a=ap.parse_args(argv); 
    if a.command!='feed': ap.print_help(); return
    url=f"amqp://{a.username}:{a.password}@{a.host}:{a.port}" if a.username else f"amqp://{a.host}:{a.port}"; conn=BlockingConnection(url, timeout=30, allowed_mechs='PLAIN'); s=conn.create_sender(a.address)
    z=ForecastZone(zone_id='WAZ315', zone_type=ZoneTypeenum.public, name='City of Seattle', state='wa', forecast_office_url='https://api.weather.gov/offices/SEW', grid_identifier='SEW', awips_location_identifier='WAZ315', cwa_ids=['SEW'], forecast_office_urls=['https://api.weather.gov/offices/SEW'], time_zones=['America/Los_Angeles'], observation_station_ids=['KSEA'], radar_station='ATX', effective_date='2026-04-07T00:00:00+00:00', expiration_date='2030-01-01T00:00:00+00:00')
    l=LandZoneForecast(zone_id='WAZ315', updated='2026-04-07T10:00:00+00:00', periods=[LandForecastPeriod(period_number=1, period_name='Today', detailed_forecast='Synthetic land forecast.')])
    m=MarineZoneForecast(zone_id='PZZ135', zone_name='Puget Sound and Hood Canal', product_title='Coastal Waters Forecast', office_name='NWS Seattle WA', issued_at_text='300 AM PDT Tue Apr 7 2026', expires_text='Tue Apr 7 2026', wmo_header='FZUS56 KSEW', bulletin_awips_id='CWFSEW', synopsis='Synthetic synopsis.', periods=[MarineForecastPeriod(period_name='TODAY', forecast_text='Synthetic marine forecast.')], bulletin_text='Synthetic marine bulletin.')
    _send(s,'Microsoft.OpenData.US.NOAA.NWS.ForecastZone','WAZ315',z); _send(s,'Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast','WAZ315',l); _send(s,'Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast','PZZ135',m); conn.close()
if __name__=='__main__': main()

