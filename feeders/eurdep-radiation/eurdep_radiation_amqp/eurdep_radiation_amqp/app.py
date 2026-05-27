
"""AMQP feeder for EURDEP radiation dose-rate events."""
from __future__ import annotations
import argparse, logging, os
from urllib.parse import urlparse
from eurdep_radiation.eurdep_radiation import EurdepAPI, FEED_URL
from eurdep_radiation_amqp_producer_data.eu.jrc.eurdep.station import Station
from eurdep_radiation_amqp_producer_data.eu.jrc.eurdep.doseratereading import DoseRateReading
from eurdep_radiation_amqp_producer_amqp_producer.producer import EuJrcEurdepAmqpProducer
logger=logging.getLogger(__name__); DEFAULT_ENTRA_AUDIENCE_SERVICEBUS='https://servicebus.azure.net/.default'
def _parse(url):
 p=urlparse(url if '://' in url else f'amqp://{url}'); tls=(p.scheme or 'amqp').lower() in ('amqps','ssl','tls'); return p.hostname or 'localhost', p.port or (5671 if tls else 5672), tls, p.username, p.password, (p.path or '').lstrip('/') or None
def _sample():
 return [Station(station_id='DE0123', country='de', name='Sample EURDEP Station', latitude=52.5, longitude=13.4, height_above_sea=35.0, site_status=1, site_status_text='in operation')],[DoseRateReading(station_id='DE0123', country='de', name='Sample EURDEP Station', value=0.09, unit='µSv/h', start_measure='2026-01-01T00:00:00Z', end_measure='2026-01-01T01:00:00Z', nuclide='Gamma-ODL-Brutto', duration='1h', validated=1)]
def producer(args):
 address=args.address
 if args.broker_url:
  host,port,tls,user,pwd,path=_parse(args.broker_url); username=args.username or user; password=args.password or pwd; address=path or address
 else:
  host=args.host or 'localhost'; tls=args.tls or args.auth_mode in ('entra','sas'); port=args.port or (5671 if tls else 5672); username=args.username; password=args.password
 if args.auth_mode=='entra':
  from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
  cred=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(); return EuJrcEurdepAmqpProducer(host=host,address=address,port=port,credential=cred,entra_audience=args.entra_audience,use_tls=tls,content_mode=args.content_mode)
 if args.auth_mode=='sas': return EuJrcEurdepAmqpProducer(host=host,address=address,port=port,sas_key_name=args.sas_key_name,sas_key=args.sas_key,use_tls=tls,content_mode=args.content_mode)
 return EuJrcEurdepAmqpProducer(host=host,address=address,port=port,username=username,password=password,use_tls=tls,content_mode=args.content_mode)
def feed(args):
 prod=producer(args)
 try:
  if os.getenv('EURDEP_RADIATION_SAMPLE_MODE','').lower() in ('1','true','yes'): stations,readings=_sample()
  else:
   api=EurdepAPI(); features=api.fetch_all_features(); stations=list(api.extract_stations(features).values()); readings=api.extract_readings(features)
  for s in stations: prod.send_station(data=s,_feedurl=FEED_URL,_station_id=s.station_id,_country=s.country)
  for r in readings: prod.send_dose_rate_reading(data=r,_feedurl=FEED_URL,_station_id=r.station_id,_country=r.country)
  logger.info('Published %d EURDEP stations and %d readings to AMQP',len(stations),len(readings))
 finally: prod.close()
def main():
 logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s'); ap=argparse.ArgumentParser(); ap.add_argument('command',nargs='?',default='feed'); ap.add_argument('--broker-url',default=os.getenv('AMQP_BROKER_URL')); ap.add_argument('--host',default=os.getenv('AMQP_HOST')); ap.add_argument('--port',type=int,default=int(os.getenv('AMQP_PORT','0')) or None); ap.add_argument('--address',default=os.getenv('AMQP_ADDRESS','eurdep-radiation')); ap.add_argument('--username',default=os.getenv('AMQP_USERNAME')); ap.add_argument('--password',default=os.getenv('AMQP_PASSWORD')); ap.add_argument('--tls',action='store_true',default=os.getenv('AMQP_TLS','').lower() in ('1','true','yes')); ap.add_argument('--content-mode',choices=('binary','structured'),default=os.getenv('AMQP_CONTENT_MODE','binary')); ap.add_argument('--auth-mode',choices=('password','entra','sas'),default=os.getenv('AMQP_AUTH_MODE','password')); ap.add_argument('--entra-audience',default=os.getenv('AMQP_ENTRA_AUDIENCE',DEFAULT_ENTRA_AUDIENCE_SERVICEBUS)); ap.add_argument('--entra-client-id',default=os.getenv('AMQP_ENTRA_CLIENT_ID')); ap.add_argument('--sas-key-name',default=os.getenv('AMQP_SAS_KEY_NAME')); ap.add_argument('--sas-key',default=os.getenv('AMQP_SAS_KEY'))
 a=ap.parse_args();
 if a.command!='feed': ap.error("only the 'feed' command is supported")
 feed(a)
if __name__=='__main__': main()
