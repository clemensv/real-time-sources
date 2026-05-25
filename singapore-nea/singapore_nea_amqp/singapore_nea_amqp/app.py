from __future__ import annotations
import argparse, os
from datetime import datetime, timezone
from cloudevents.http import CloudEvent, to_binary
from proton import Message
from proton.utils import BlockingConnection
from singapore_nea_amqp_producer_data import Station, WeatherObservation, Region, PSIReading, PM25Reading

def _send(sender,t,sub,data):
    headers,body=to_binary(CloudEvent({'type':t,'source':'https://api.data.gov.sg','subject':sub}, data.to_byte_array('application/json'))); msg=Message(body=body if isinstance(body,bytes) else str(body).encode(), inferred=True); msg.content_type='application/json'; msg.properties={'cloudEvents:'+k[3:]:v for k,v in headers.items() if k.lower().startswith('ce-')}; msg.subject=sub; sender.send(msg)
def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--host',default=os.getenv('AMQP_HOST','localhost')); f.add_argument('--port',type=int,default=int(os.getenv('AMQP_PORT','5672'))); f.add_argument('--address',default=os.getenv('AMQP_ADDRESS','singapore-nea')); f.add_argument('--username',default=os.getenv('AMQP_USERNAME')); f.add_argument('--password',default=os.getenv('AMQP_PASSWORD'))
    a=ap.parse_args(argv); 
    if a.command!='feed': ap.print_help(); return
    url=f"amqp://{a.username}:{a.password}@{a.host}:{a.port}" if a.username else f"amqp://{a.host}:{a.port}"; conn=BlockingConnection(url, timeout=30, allowed_mechs='PLAIN'); s=conn.create_sender(a.address); now=datetime(2026,4,7,10,0,tzinfo=timezone.utc)
    _send(s,'SG.Gov.NEA.Weather.Station','S109',Station(station_id='S109', device_id='S109', name='Ang Mo Kio Avenue 5', latitude=1.3764, longitude=103.8492, data_types='air_temperature,rainfall'))
    _send(s,'SG.Gov.NEA.Weather.WeatherObservation','S109',WeatherObservation(station_id='S109', station_name='Ang Mo Kio Avenue 5', observation_time=now, air_temperature=30.5, rainfall=0.0, relative_humidity=75.0, wind_speed=2.1, wind_direction=180.0))
    _send(s,'SG.Gov.NEA.AirQuality.Region','central',Region(region='central', latitude=1.357, longitude=103.82))
    _send(s,'SG.Gov.NEA.AirQuality.PSIReading','central',PSIReading(region='central', timestamp=now, update_timestamp=now, psi_twenty_four_hourly=52, o3_sub_index=10, pm10_sub_index=20, pm10_twenty_four_hourly=25, pm25_sub_index=30, pm25_twenty_four_hourly=12, co_sub_index=5, co_eight_hour_max=1, so2_sub_index=2, so2_twenty_four_hourly=3, no2_one_hour_max=8, o3_eight_hour_max=10))
    _send(s,'SG.Gov.NEA.AirQuality.PM25Reading','central',PM25Reading(region='central', timestamp=now, update_timestamp=now, pm25_one_hourly=11)); conn.close()
if __name__=='__main__': main()
