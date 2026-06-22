from __future__ import annotations
import argparse, logging, os, sys, time
from confluent_kafka import Producer
from cap_alerts_core import CapClient, build_kafka_config, load_sources, load_state, mock_client_and_sources, parse_bool, parse_kafka_connection_string, save_state
from cap_alerts_producer_data import CapAlert, CapArea, CapInfo, CapResource, CapZone, ValuePair
from cap_alerts_producer_kafka_producer.producer import OrgOasisCapAlertsAlertsEventProducer, OrgOasisCapAlertsZonesEventProducer
logger=logging.getLogger(__name__)
DEFAULT_STATE_FILE=os.path.expanduser("~/.cap_alerts_state.json")

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

def feed(args):
    mock=getattr(args,"mock",False)
    sources=load_sources(args.cap_sources, sources_file=args.cap_sources_file, selector=args.cap_select) if not mock else []
    client=CapClient()
    if mock:
        client,sources=mock_client_and_sources(); args.once=True
    if args.connection_string:
        cfg=parse_kafka_connection_string(args.connection_string); entity=cfg.pop("kafka_topic", None); topic=entity or args.kafka_topic; bootstrap=cfg.pop("bootstrap.servers", None); kafka_config=cfg; kafka_config["bootstrap.servers"]=bootstrap
    else:
        topic=args.kafka_topic; kafka_config=build_kafka_config(bootstrap_servers=args.kafka_bootstrap_servers, sasl_username=args.sasl_username, sasl_password=args.sasl_password, tls_enabled=parse_bool(args.kafka_enable_tls, True))
    if not kafka_config.get("bootstrap.servers"): raise SystemExit("Kafka bootstrap servers or CONNECTION_STRING required")
    producer=Producer(kafka_config); alert_producer=OrgOasisCapAlertsAlertsEventProducer(producer, topic); zone_producer=OrgOasisCapAlertsZonesEventProducer(producer, topic)
    state=load_state(args.state_file); last_ref=0.0
    while True:
        started=time.time(); pending={}
        if last_ref==0 or started-last_ref>=args.reference_refresh_interval:
            for source in sources:
                for z in client.fetch_zones(source):
                    zone_producer.send_org_oasis_cap_alerts_cap_zone(_provider_url=z["provider_url"], _cap_source_id=z["cap_source_id"], _zone_id=z["zone_id"], data=build_zone(z), flush_producer=False)
            zone_producer.flush(timeout=120); last_ref=started
        for source in sources:
            for a in client.fetch_alerts(source):
                key=f"{a['cap_source_id']}/{a['identifier']}"; sent=a["sent"].isoformat()
                if state.get(key)==sent: continue
                alert_producer.send_org_oasis_cap_alerts_cap_alert(_provider_url=a["provider_url"], _cap_source_id=a["cap_source_id"], _identifier=a["identifier"], data=build_alert(a), flush_producer=False)
                pending[key]=sent
        alert_producer.flush(timeout=120); state.update(pending); save_state(args.state_file,state)
        if args.once: return
        time.sleep(max(1,args.poll_interval-int(time.time()-started)))
def build_parser():
    p=argparse.ArgumentParser(description="CAP alerts -> Kafka bridge"); sp=p.add_subparsers(dest="command"); f=sp.add_parser("feed")
    f.add_argument("--cap-sources", default=os.getenv("CAP_SOURCES")); f.add_argument("--cap-sources-file", default=os.getenv("CAP_SOURCES_FILE", "")); f.add_argument("--cap-select", default=os.getenv("CAP_SELECT", "")); f.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS")); f.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC","cap-alerts")); f.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME")); f.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD")); f.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING")); f.add_argument("--kafka-enable-tls", default=os.getenv("KAFKA_ENABLE_TLS","true")); f.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL","300"))); f.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL","21600"))); f.add_argument("--state-file", default=os.getenv("STATE_FILE",DEFAULT_STATE_FILE)); f.add_argument("--once", action="store_true", default=parse_bool(os.getenv("ONCE_MODE"),False)); f.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("CAP_ALERTS_MOCK"),False)); return p
def main(argv=None):
    logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO")); args=build_parser().parse_args(argv);
    if args.command in (None,"feed"): feed(args)
if __name__=="__main__": main(sys.argv[1:])
