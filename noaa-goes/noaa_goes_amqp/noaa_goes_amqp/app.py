from __future__ import annotations
import argparse, os
from cloudevents.http import CloudEvent, to_binary
from proton import Message
from proton.utils import BlockingConnection
from noaa_goes_amqp_producer_data import GoesXrayFlux, GoesProtonFlux, GoesElectronFlux, GoesMagnetometer, SpaceWeatherAlert, XrayFlare

def _send(sender,t,sub,data):
    headers,body=to_binary(CloudEvent({'type':t,'source':'https://services.swpc.noaa.gov','subject':sub}, data.to_byte_array('application/json'))); msg=Message(body=body if isinstance(body,bytes) else str(body).encode(), inferred=True); msg.content_type='application/json'; msg.properties={'cloudEvents:'+k[3:]:v for k,v in headers.items() if k.lower().startswith('ce-')}; msg.subject=sub; sender.send(msg)
def main(argv=None):
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='command'); f=sub.add_parser('feed'); f.add_argument('--host',default=os.getenv('AMQP_HOST','localhost')); f.add_argument('--port',type=int,default=int(os.getenv('AMQP_PORT','5672'))); f.add_argument('--address',default=os.getenv('AMQP_ADDRESS','noaa-goes')); f.add_argument('--username',default=os.getenv('AMQP_USERNAME')); f.add_argument('--password',default=os.getenv('AMQP_PASSWORD'))
    a=ap.parse_args(argv); 
    if a.command!='feed': ap.print_help(); return
    url=f"amqp://{a.username}:{a.password}@{a.host}:{a.port}" if a.username else f"amqp://{a.host}:{a.port}"; conn=BlockingConnection(url, timeout=30, allowed_mechs='PLAIN'); s=conn.create_sender(a.address); ts='2026-04-07T10:00:00Z'
    _send(s,'Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux','18/0.1-0.8nm/'+ts,GoesXrayFlux(time_tag=ts, satellite=18, flux=1.2e-6, energy='0.1-0.8nm'))
    _send(s,'Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux','18/>=10MeV/'+ts,GoesProtonFlux(time_tag=ts, satellite=18, flux=3.0, energy='>=10MeV'))
    _send(s,'Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux','18/>=2MeV/'+ts,GoesElectronFlux(time_tag=ts, satellite=18, flux=900.0, energy='>=2MeV'))
    _send(s,'Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer','18/'+ts,GoesMagnetometer(time_tag=ts, satellite=18, he=1.0, hp=2.0, hn=3.0, total=3.7, arcjet_flag=False))
    _send(s,'Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert','ALTXMF-20260407',SpaceWeatherAlert(product_id='ALTXMF-20260407', issue_datetime='2026 Apr 07 1000 UTC', message='Synthetic SWPC alert.'))
    _send(s,'Microsoft.OpenData.US.NOAA.SWPC.XrayFlare','18/2026-04-07T09:58:00Z',XrayFlare(time_tag=ts, begin_time='2026-04-07T09:58:00Z', begin_class='C9.0', max_time=ts, max_class='M1.0', max_xrlong=1e-5, max_ratio=0.2, max_ratio_time=ts, current_int_xrlong=1e-3, end_time='2026-04-07T10:10:00Z', end_class='C2.0', satellite=18)); conn.close()
if __name__=='__main__': main()
