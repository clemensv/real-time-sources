
"""MQTT feeder for NIFC USA wildfire incident events."""
from __future__ import annotations
import argparse, asyncio, dataclasses, logging, os
from typing import Optional
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from nifc_usa_wildfires.nifc_usa_wildfires import NIFCWildfirePoller, SOURCE_URI
from nifc_usa_wildfires_mqtt_producer_data.gov.nifc.wildfires.wildfireincident import WildfireIncident
from nifc_usa_wildfires_mqtt_producer_mqtt_client.client import GovNIFCWildfiresMqttMqttClient
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

logger=logging.getLogger(__name__)
def _parse(url):
 p=urlparse(url if '://' in url else f'mqtt://{url}'); tls=(p.scheme or 'mqtt').lower() in ('mqtts','ssl','tls'); return p.hostname or 'localhost', p.port or (8883 if tls else 1883), tls
def _sample():
 return [WildfireIncident(irwin_id='sample-irwin-001', state='ca', status='active', incident_name='Sample Fire', unique_fire_identifier='2026-CANIF-000001', incident_type_category='WF', incident_type_kind='FI', fire_discovery_datetime='2026-01-01T00:00:00+00:00', daily_acres=100.0, calculated_acres=None, discovery_acres=10.0, percent_contained=0.0, poo_state='US-CA', poo_county='Sample', latitude=38.5, longitude=-121.5, fire_cause='Undetermined', fire_cause_general=None, gacc='ONCC', total_incident_personnel=None, incident_management_organization=None, fire_mgmt_complexity=None, residences_destroyed=None, other_structures_destroyed=None, injuries=None, fatalities=None, containment_datetime=None, control_datetime=None, fire_out_datetime=None, final_acres=None, modified_on_datetime='2026-01-01T01:00:00+00:00')]
def _to_mqtt(i): return WildfireIncident(**dataclasses.asdict(i))
async def feed(host,port,*,username:Optional[str]=None,password:Optional[str]=None,tls=False,client_id:Optional[str]=None,once=False,content_mode='binary',polling_interval=300):
 resolved_client_id, resolved_username, resolved_password, _entra_props = _resolve_mqtt_connection_settings(
     username=username,
     password=password or '',
     client_id=client_id or '',
     auth_mode=os.getenv("MQTT_AUTH_MODE"),
 )

 paho=mqtt.Client(client_id=resolved_client_id or "", callback_api_version=CallbackAPIVersion.VERSION2, protocol=MQTTv5)
 if _entra_props is None and (resolved_username or resolved_password):
     paho.username_pw_set(resolved_username, resolved_password)
 if tls: paho.tls_set()
 client=GovNIFCWildfiresMqttMqttClient(client=paho, content_mode=content_mode, loop=asyncio.get_running_loop())
 # WORKAROUND(xregistry/codegen#432): EG MQTT requires OAUTH2-JWT extended auth, not username/password
 if _entra_props is not None:
     paho.connect(host, port, keepalive=60, clean_start=True, properties=_entra_props)
     paho.loop_start()
 else:
     await client.connect(host, port)
 try:
  while True:
   if os.getenv('NIFC_USA_WILDFIRES_SAMPLE_MODE','').lower() in ('1','true','yes'): incidents=_sample()
   else:
    poller=NIFCWildfirePoller(); incidents=[_to_mqtt(poller.parse_incident(f)) for f in await poller.fetch_incidents() if poller.parse_incident(f)]
   for i in incidents:
    await client.publish_gov_nifc_wildfires_mqtt_wildfire_incident(source_uri=SOURCE_URI, irwin_id=i.irwin_id, _time=i.modified_on_datetime, state=i.state, status=i.status, data=i)
   logger.info('Published %d NIFC wildfire incidents to MQTT',len(incidents))
   if once: break
   await asyncio.sleep(max(1,polling_interval))
 finally: await client.disconnect()
def main():
 logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s'); ap=argparse.ArgumentParser(); ap.add_argument('command',nargs='?',default='feed'); ap.add_argument('--broker-url',default=os.getenv('MQTT_BROKER_URL','mqtt://localhost:1883')); ap.add_argument('--username',default=os.getenv('MQTT_USERNAME','')); ap.add_argument('--password',default=os.getenv('MQTT_PASSWORD','')); ap.add_argument('--client-id',default=os.getenv('MQTT_CLIENT_ID','')); ap.add_argument('--content-mode',choices=('binary','structured'),default=os.getenv('MQTT_CONTENT_MODE','binary')); ap.add_argument('--polling-interval',type=int,default=int(os.getenv('POLLING_INTERVAL','300'))); ap.add_argument('--once',action='store_true',default=os.getenv('ONCE_MODE','').lower() in ('1','true','yes'))
 a=ap.parse_args();
 if a.command!='feed': ap.error("only the 'feed' command is supported")
 host,port,tls=_parse(a.broker_url); asyncio.run(feed(host,port,username=a.username or None,password=a.password or None,tls=tls,client_id=a.client_id or None,content_mode=a.content_mode,polling_interval=a.polling_interval,once=a.once))
if __name__=='__main__': main()
