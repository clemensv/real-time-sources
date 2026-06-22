from __future__ import annotations
import argparse, asyncio, logging, os, sys, time
from urllib.parse import quote, urlparse
import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5
from cap_alerts_core import CapClient, build_kafka_config, load_sources, load_state, mock_client_and_sources, parse_bool, parse_kafka_connection_string, save_state
from cap_alerts_mqtt_producer_data import CapAlert, CapArea, CapInfo, CapResource, CapZone, ValuePair
from cap_alerts_mqtt_producer_mqtt_client.client import OrgOasisCapAlertsAlertsMqttMqttClient, OrgOasisCapAlertsZonesMqttMqttClient
logger=logging.getLogger(__name__)
DEFAULT_STATE_FILE=os.path.expanduser("~/.cap_alerts_mqtt_state.json")

def _pairs(rows):
    return [ValuePair(value_name=str(r.get("value_name") or ""), value=str(r.get("value") or "")) for r in (rows or [])]

def _area(row):
    return CapArea(area_desc=row.get("area_desc"), polygon=row.get("polygon") or [], circle=row.get("circle") or [], geocode=_pairs(row.get("geocode")), altitude=row.get("altitude"), ceiling=row.get("ceiling"))

def _resource(row):
    return CapResource(resource_desc=row.get("resource_desc"), mime_type=row.get("mime_type"), size=row.get("size"), uri=row.get("uri"), deref_uri=row.get("deref_uri"), digest=row.get("digest"))

def _info(row):
    return CapInfo(language=row.get("language"), category=row.get("category") or [], event=row.get("event"), response_type=row.get("response_type") or [], urgency=row.get("urgency") or "Unknown", severity=row.get("severity") or "Unknown", certainty=row.get("certainty") or "Unknown", audience=row.get("audience"), event_code=_pairs(row.get("event_code")), effective=row.get("effective"), onset=row.get("onset"), expires=row.get("expires"), ends=row.get("ends"), sender_name=row.get("sender_name"), headline=row.get("headline"), description=row.get("description"), instruction=row.get("instruction"), web=row.get("web"), contact=row.get("contact"), parameter=_pairs(row.get("parameter")), resource=[_resource(x) for x in (row.get("resource") or [])], area=[_area(x) for x in (row.get("area") or [])])

def build_alert(row):
    return CapAlert(cap_source_id=row["cap_source_id"], identifier=row["identifier"], sender=row["sender"], sent=row["sent"], status=row.get("status") or "Actual", msg_type=row.get("msg_type") or "Alert", source=row.get("source"), scope=row.get("scope") or "Public", restriction=row.get("restriction"), addresses=row.get("addresses") or [], code=_pairs(row.get("code")), note=row.get("note"), references=row.get("references") or [], incidents=row.get("incidents") or [], affected_zones=row.get("affected_zones") or [], raw_source_json=row.get("raw_source_json"), info=[_info(x) for x in row.get("info", [])], provider_url=row["provider_url"], raw_cap_xml=row.get("raw_cap_xml"), area_desc=row.get("area_desc"), same_codes=row.get("same_codes") or [], ugc_codes=row.get("ugc_codes") or [], vtec=row.get("vtec") or [], awareness_level=row.get("awareness_level"), awareness_type=row.get("awareness_type"), event_type=row.get("event_type"), state=row.get("state"))

def build_zone(row):
    return CapZone(cap_source_id=row["cap_source_id"], zone_id=row["zone_id"], name=row.get("name"), zone_type=row.get("zone_type"), state=row.get("state"), forecast_office=row.get("forecast_office"), time_zones=row.get("time_zones") or [], geometry=row.get("geometry"), provider_url=row["provider_url"])

async def feed(args):
    broker_url = args.mqtt_broker_url or "localhost:1883"
    parsed = urlparse(broker_url if "://" in broker_url else "mqtt://" + broker_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 8883 if parsed.scheme == "mqtts" else parsed.port or 1883
    paho_alerts=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=(args.mqtt_client_id or "") + "-alerts", protocol=MQTTv5)
    paho_zones=mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id=(args.mqtt_client_id or "") + "-zones", protocol=MQTTv5)
    if args.mqtt_auth_mode=="userpass" and args.mqtt_username:
      paho_alerts.username_pw_set(args.mqtt_username,args.mqtt_password or "")
      paho_zones.username_pw_set(args.mqtt_username,args.mqtt_password or "")
    if parse_bool(args.mqtt_enable_tls, False):
      paho_alerts.tls_set(ca_certs=args.mqtt_ca_file or None)
      paho_zones.tls_set(ca_certs=args.mqtt_ca_file or None)
    loop=asyncio.get_running_loop(); alerts_client=OrgOasisCapAlertsAlertsMqttMqttClient(paho_alerts, content_mode="binary", loop=loop); zones_client=OrgOasisCapAlertsZonesMqttMqttClient(paho_zones, content_mode="binary", loop=loop)
    await alerts_client.connect(host, port)
    await zones_client.connect(host, port)
    mock=getattr(args,"mock",False); client=CapClient(); sources=load_sources(args.cap_sources, sources_file=args.cap_sources_file, selector=args.cap_select) if not mock else []
    if mock: client,sources=mock_client_and_sources(); args.once=True
    state=load_state(args.state_file); last_ref=0.0
    try:
      while True:
        started=time.time(); pending={}
        if last_ref==0 or started-last_ref>=args.reference_refresh_interval:
          for source in sources:
            for z in client.fetch_zones(source): await zones_client.publish_org_oasis_cap_alerts_mqtt_cap_zone(provider_url=z["provider_url"], cap_source_id=z["cap_source_id"], zone_id=z["zone_id"], zone_id_segment=quote(str(z["zone_id"]), safe=""), data=build_zone(z))
          last_ref=started
        for source in sources:
          for a in client.fetch_alerts(source):
            key=f"{a['cap_source_id']}/{a['identifier']}"; sent=a["sent"].isoformat()
            if state.get(key)==sent: continue
            await alerts_client.publish_org_oasis_cap_alerts_mqtt_cap_alert(provider_url=a["provider_url"], cap_source_id=a["cap_source_id"], identifier=a["identifier"], identifier_segment=quote(str(a["identifier"]), safe=""), data=build_alert(a)); pending[key]=sent
        state.update(pending); save_state(args.state_file,state)
        if args.once: return
        await asyncio.sleep(max(1,args.poll_interval-int(time.time()-started)))
    finally:
      await alerts_client.disconnect()
      await zones_client.disconnect()
def build_parser():
 p=argparse.ArgumentParser(); sp=p.add_subparsers(dest="command"); f=sp.add_parser("feed"); f.add_argument("--cap-sources", default=os.getenv("CAP_SOURCES")); f.add_argument("--cap-sources-file", default=os.getenv("CAP_SOURCES_FILE", "")); f.add_argument("--cap-select", default=os.getenv("CAP_SELECT", "")); f.add_argument("--mqtt-broker-url", default=os.getenv("MQTT_BROKER_URL")); f.add_argument("--mqtt-auth-mode", default=os.getenv("MQTT_AUTH_MODE","anonymous")); f.add_argument("--mqtt-username", default=os.getenv("MQTT_USERNAME")); f.add_argument("--mqtt-password", default=os.getenv("MQTT_PASSWORD")); f.add_argument("--mqtt-enable-tls", default=os.getenv("MQTT_ENABLE_TLS","false")); f.add_argument("--mqtt-ca-file", default=os.getenv("MQTT_CA_FILE")); f.add_argument("--mqtt-client-id", default=os.getenv("MQTT_CLIENT_ID")); f.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL","300"))); f.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL","21600"))); f.add_argument("--state-file", default=os.getenv("STATE_FILE",DEFAULT_STATE_FILE)); f.add_argument("--once", action="store_true", default=parse_bool(os.getenv("ONCE_MODE"),False)); f.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("CAP_ALERTS_MOCK"),False)); return p
def main(argv=None): logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO")); args=build_parser().parse_args(argv); asyncio.run(feed(args))
if __name__=="__main__": main(sys.argv[1:])
