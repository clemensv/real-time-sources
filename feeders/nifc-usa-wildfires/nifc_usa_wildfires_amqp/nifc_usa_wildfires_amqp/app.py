
"""AMQP feeder for NIFC USA wildfire incident events."""
from __future__ import annotations
import argparse, dataclasses, logging, os
from urllib.parse import urlparse
from nifc_usa_wildfires.nifc_usa_wildfires import NIFCWildfirePoller, SOURCE_URI
from nifc_usa_wildfires_amqp_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident
from nifc_usa_wildfires_amqp_producer_amqp_producer.producer import GovNIFCWildfiresAmqpProducer
logger=logging.getLogger(__name__); DEFAULT_ENTRA_AUDIENCE_SERVICEBUS='https://servicebus.azure.net/.default'
def _parse(url):
 p=urlparse(url if '://' in url else f'amqp://{url}'); tls=(p.scheme or 'amqp').lower() in ('amqps','ssl','tls'); return p.hostname or 'localhost', p.port or (5671 if tls else 5672), tls, p.username, p.password, (p.path or '').lstrip('/') or None
def _sample():
 return [WildfireIncident(irwin_id='sample-irwin-001', state='ca', status='active', incident_name='Sample Fire', unique_fire_identifier='2026-CANIF-000001', incident_type_category='WF', incident_type_kind='FI', fire_discovery_datetime='2026-01-01T00:00:00+00:00', daily_acres=100.0, calculated_acres=None, discovery_acres=10.0, percent_contained=0.0, poo_state='US-CA', poo_county='Sample', latitude=38.5, longitude=-121.5, fire_cause='Undetermined', fire_cause_general=None, gacc='ONCC', total_incident_personnel=None, incident_management_organization=None, fire_mgmt_complexity=None, residences_destroyed=None, other_structures_destroyed=None, injuries=None, fatalities=None, containment_datetime=None, control_datetime=None, fire_out_datetime=None, final_acres=None, modified_on_datetime='2026-01-01T01:00:00+00:00')]
def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            import logging; logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def producer(args):
 address=args.address
 if args.broker_url:
  host,port,tls,user,pwd,path=_parse(args.broker_url); username=args.username or user; password=args.password or pwd; address=path or address
 else:
  host=args.host or 'localhost'; tls=args.tls or args.auth_mode in ('entra','sas'); port=args.port or (5671 if tls else 5672); username=args.username; password=args.password
 if args.auth_mode=='entra':
  from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
  cred=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(); return GovNIFCWildfiresAmqpProducer(host=host,address=address,port=port,credential=cred,entra_audience=args.entra_audience,use_tls=tls,content_mode=args.content_mode)
 if args.auth_mode=='sas': return GovNIFCWildfiresAmqpProducer(host=host,address=address,port=port,sas_key_name=args.sas_key_name,sas_key=args.sas_key,use_tls=tls,content_mode=args.content_mode)
 return GovNIFCWildfiresAmqpProducer(host=host,address=address,port=port,username=username,password=password,use_tls=tls,content_mode=args.content_mode)
def feed(args):
 prod=_retry_producer_init(lambda: producer(args))
 try:
  if os.getenv('NIFC_USA_WILDFIRES_SAMPLE_MODE','').lower() in ('1','true','yes'): incidents=_sample()
  else:
   import asyncio; poller=NIFCWildfirePoller(); incidents=[]
   for f in asyncio.run(poller.fetch_incidents()):
    i=poller.parse_incident(f)
    if i: incidents.append(WildfireIncident(**dataclasses.asdict(i)))
  for i in incidents: prod.send_wildfire_incident(data=i,_source_uri=SOURCE_URI,_irwin_id=i.irwin_id,_time=i.modified_on_datetime,_state=i.state,_status=i.status)
  logger.info('Published %d NIFC wildfire incidents to AMQP',len(incidents))
 finally: prod.close()
def main():
 logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s'); ap=argparse.ArgumentParser(); ap.add_argument('command',nargs='?',default='feed'); ap.add_argument('--broker-url',default=os.getenv('AMQP_BROKER_URL')); ap.add_argument('--host',default=os.getenv('AMQP_HOST')); ap.add_argument('--port',type=int,default=int(os.getenv('AMQP_PORT','0')) or None); ap.add_argument('--address',default=os.getenv('AMQP_ADDRESS','nifc-usa-wildfires')); ap.add_argument('--username',default=os.getenv('AMQP_USERNAME')); ap.add_argument('--password',default=os.getenv('AMQP_PASSWORD')); ap.add_argument('--tls',action='store_true',default=os.getenv('AMQP_TLS','').lower() in ('1','true','yes')); ap.add_argument('--content-mode',choices=('binary','structured'),default=os.getenv('AMQP_CONTENT_MODE','binary')); ap.add_argument('--auth-mode',choices=('password','entra','sas'),default=os.getenv('AMQP_AUTH_MODE','password')); ap.add_argument('--entra-audience',default=os.getenv('AMQP_ENTRA_AUDIENCE',DEFAULT_ENTRA_AUDIENCE_SERVICEBUS)); ap.add_argument('--entra-client-id',default=os.getenv('AMQP_ENTRA_CLIENT_ID')); ap.add_argument('--sas-key-name',default=os.getenv('AMQP_SAS_KEY_NAME')); ap.add_argument('--sas-key',default=os.getenv('AMQP_SAS_KEY'))
 a=ap.parse_args();
 if a.command!='feed': ap.error("only the 'feed' command is supported")
 feed(a)
if __name__=='__main__': main()
