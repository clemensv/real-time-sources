from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Optional
from urllib.parse import urlparse

from openaq_amqp_producer_amqp_producer.producer import OrgOpenaqLocationsAmqpProducer, OrgOpenaqSensorsAmqpProducer
from openaq_amqp_producer_data import Location, Measurement, Sensor
from openaq_amqp_producer_data.org.openaq.parameternameenum import ParameterNameenum
from openaq_core import OpenAQClient, build_mock_client, load_query_slices, load_state, parse_bool, save_state, should_publish_measurement
from openaq_core.acquisition import LocationRecord, MeasurementRecord, SensorRecord

logger = logging.getLogger(__name__)
DEFAULT_STATE_FILE = os.path.expanduser("~/.openaq_amqp_state.json")
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"

def _enum(name: str) -> ParameterNameenum: return ParameterNameenum(name)
def build_location(r: LocationRecord) -> Location: return Location(**r.__dict__)
def build_sensor(r: SensorRecord) -> Sensor:
    d=dict(r.__dict__); d["parameter_name"]=_enum(r.parameter_name); return Sensor(**d)
def build_measurement(r: MeasurementRecord) -> Measurement:
    d=dict(r.__dict__); d["parameter_name"]=_enum(r.parameter_name); return Measurement(**d)
def _parse_broker_url(url: Optional[str]) -> tuple[str, int, bool, Optional[str], Optional[str]]:
    if not url: return "", 5672, False, None, None
    parsed = urlparse(url if "://" in url else f"amqp://{url}"); tls = (parsed.scheme or "amqp").lower() in {"amqps","ssl","tls"}
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password

def _build_producers(args: argparse.Namespace) -> tuple[OrgOpenaqLocationsAmqpProducer, OrgOpenaqSensorsAmqpProducer]:
    host, port, tls_from_url, user_from_url, password_from_url = _parse_broker_url(args.amqp_broker_url)
    host=args.amqp_host or host; port=args.amqp_port if args.amqp_port is not None else port; use_tls=parse_bool(args.amqp_tls, tls_from_url); address=args.amqp_address or "openaq"
    common={"host":host,"port":port,"address":address,"content_mode":args.amqp_content_mode,"use_tls":use_tls}
    auth=(args.amqp_auth_mode or "password").lower(); username=args.amqp_username or user_from_url; password=args.amqp_password or password_from_url
    if auth == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        cred=ManagedIdentityCredential(client_id=args.amqp_entra_client_id) if args.amqp_entra_client_id else DefaultAzureCredential()
        return OrgOpenaqLocationsAmqpProducer(credential=cred, entra_audience=args.amqp_entra_audience, **common), OrgOpenaqSensorsAmqpProducer(credential=cred, entra_audience=args.amqp_entra_audience, **common)
    if auth == "sas":
        return OrgOpenaqLocationsAmqpProducer(sas_key_name=args.amqp_sas_key_name, sas_key=args.amqp_sas_key, **common), OrgOpenaqSensorsAmqpProducer(sas_key_name=args.amqp_sas_key_name, sas_key=args.amqp_sas_key, **common)
    return OrgOpenaqLocationsAmqpProducer(username=username, password=password, **common), OrgOpenaqSensorsAmqpProducer(username=username, password=password, **common)

def feed(args: argparse.Namespace) -> None:
    loc_producer, sensor_producer = _build_producers(args)
    state=load_state(args.state_file); client=build_mock_client() if args.mock else OpenAQClient(args.openaq_api_key)
    if args.mock: args.once=True
    query_slices = load_query_slices(args.openaq_countries, args.openaq_locations, args.openaq_bbox, args.page_limit, args.max_pages, mock=args.mock, sources_file=args.openaq_sources_file, selector=args.openaq_sources)
    last_reference_refresh=0.0; reference_refresh=max(300,args.reference_refresh_interval); locations_cache=[]; sensors_cache={}
    try:
        while True:
            cycle_started=time.time()
            if last_reference_refresh == 0.0 or cycle_started-last_reference_refresh >= reference_refresh:
                locs=[]; sens={}
                for query_slice in query_slices:
                    for location in client.iter_locations(query_slice.countries, query_slice.locations, query_slice.bbox, query_slice.page_limit, query_slice.max_pages):
                        locs.append(location); loc_producer.send_location(data=build_location(location), _location_id=str(location.location_id), _country_iso=location.country_iso)
                        m={}
                        for sensor in client.sensors_for_location(location):
                            m[sensor.sensor_id]=sensor; sensor_producer.send_sensor(data=build_sensor(sensor), _location_id=str(sensor.location_id), _sensor_id=str(sensor.sensor_id), _country_iso=sensor.country_iso, _parameter_name=sensor.parameter_name)
                        sens[location.location_id]=m
                locations_cache=locs; sensors_cache=sens; last_reference_refresh=cycle_started
            for location in locations_cache:
                for measurement in client.latest_for_location(location, sensors_cache.get(location.location_id, {})):
                    if should_publish_measurement(measurement, state):
                        sensor_producer.send_measurement(data=build_measurement(measurement), _location_id=str(measurement.location_id), _sensor_id=str(measurement.sensor_id), _country_iso=measurement.country_iso, _parameter_name=measurement.parameter_name)
            save_state(args.state_file,state)
            if args.once: return
            time.sleep(max(1,args.poll_interval-int(time.time()-cycle_started)))
    finally:
        for p in (loc_producer, sensor_producer):
            try: p.close()
            except Exception: pass

def build_parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="OpenAQ global air quality -> AMQP bridge"); sub=parser.add_subparsers(dest="command"); f=sub.add_parser("feed")
    for name, env, default in [("openaq-api-key","OPENAQ_API_KEY",None),("openaq-countries","OPENAQ_COUNTRIES",None),("openaq-locations","OPENAQ_LOCATIONS",None),("openaq-bbox","OPENAQ_BBOX",None)]: f.add_argument("--"+name, default=os.getenv(env, default) if default is not None else os.getenv(env))
    f.add_argument("--openaq-sources-file", default=os.getenv("OPENAQ_SOURCES_FILE", "")); f.add_argument("--openaq-sources", default=os.getenv("OPENAQ_SOURCES", ""))
    f.add_argument("--page-limit", type=int, default=int(os.getenv("OPENAQ_PAGE_LIMIT","25"))); f.add_argument("--max-pages", type=int, default=int(os.getenv("OPENAQ_MAX_PAGES","1")))
    f.add_argument("--poll-interval", type=int, default=int(os.getenv("POLL_INTERVAL","900"))); f.add_argument("--reference-refresh-interval", type=int, default=int(os.getenv("REFERENCE_REFRESH_INTERVAL","21600"))); f.add_argument("--state-file", default=os.getenv("STATE_FILE",DEFAULT_STATE_FILE)); f.add_argument("--once", action="store_true", default=parse_bool(os.getenv("ONCE_MODE"),False)); f.add_argument("--mock", action="store_true", default=parse_bool(os.getenv("OPENAQ_MOCK"),False))
    f.add_argument("--amqp-broker-url", default=os.getenv("AMQP_BROKER_URL")); f.add_argument("--amqp-host", default=os.getenv("AMQP_HOST")); f.add_argument("--amqp-port", type=int, default=int(os.getenv("AMQP_PORT")) if os.getenv("AMQP_PORT") else None); f.add_argument("--amqp-address", default=os.getenv("AMQP_ADDRESS","openaq")); f.add_argument("--amqp-username", default=os.getenv("AMQP_USERNAME")); f.add_argument("--amqp-password", default=os.getenv("AMQP_PASSWORD")); f.add_argument("--amqp-auth-mode", default=os.getenv("AMQP_AUTH_MODE","password")); f.add_argument("--amqp-tls", default=os.getenv("AMQP_TLS","false")); f.add_argument("--amqp-content-mode", default=os.getenv("AMQP_CONTENT_MODE","binary")); f.add_argument("--amqp-entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID")); f.add_argument("--amqp-entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE",DEFAULT_ENTRA_AUDIENCE_SERVICEBUS)); f.add_argument("--amqp-sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME")); f.add_argument("--amqp-sas-key", default=os.getenv("AMQP_SAS_KEY"))
    return parser

def main(argv: Optional[list[str]]=None) -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL","INFO").upper()); parser=build_parser(); args=parser.parse_args(argv)
    if args.command != "feed": parser.print_help(); return
    try: feed(args)
    except Exception as exc: logger.error("OpenAQ AMQP bridge failed: %s", exc); sys.exit(1)
if __name__ == "__main__": main()
