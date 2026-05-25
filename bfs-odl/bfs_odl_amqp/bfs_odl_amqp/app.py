"""AMQP 1.0 feeder application for BfS ODL dose-rate events."""
from __future__ import annotations

import argparse
import logging
import os
from typing import Optional
from urllib.parse import urlparse

from bfs_odl.bfs_odl import BfsOdlAPI, FEED_URL, _load_state, _save_state
from bfs_odl_amqp_producer_data.de.bfs.odl.station import Station
from bfs_odl_amqp_producer_data.de.bfs.odl.doseratemeasurement import DoseRateMeasurement
from bfs_odl_amqp_producer_amqp_producer.producer import DeBfsOdlAmqpProducer

logger = logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"

_AGS_TO_CANTON = {
    "01": "schleswig-holstein", "02": "hamburg", "03": "niedersachsen", "04": "bremen",
    "05": "nordrhein-westfalen", "06": "hessen", "07": "rheinland-pfalz", "08": "baden-wuerttemberg",
    "09": "bayern", "10": "saarland", "11": "berlin", "12": "brandenburg",
    "13": "mecklenburg-vorpommern", "14": "sachsen", "15": "sachsen-anhalt", "16": "thueringen",
}


def _canton_from_station_id(station_id: str) -> str:
    return _AGS_TO_CANTON.get((station_id or "")[:2], "unknown")


def _parse_amqp_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))


def create_amqp_producer(args: argparse.Namespace):
    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_amqp_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode in ("entra", "sas")
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential()
        return DeBfsOdlAmqpProducer(host=host, address=address, port=port, content_mode=args.content_mode, credential=credential, entra_audience=args.entra_audience, use_tls=tls)
    if args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return DeBfsOdlAmqpProducer(host=host, address=address, port=port, content_mode=args.content_mode, sas_key_name=args.sas_key_name, sas_key=args.sas_key, use_tls=tls)
    return DeBfsOdlAmqpProducer(host=host, address=address, port=port, username=username, password=password, content_mode=args.content_mode, use_tls=tls)


def _sample_features():
    station = {"type": "Feature", "properties": {"kenn": "033510091", "id": "DEZ0305", "name": "Sample Station", "plz": "30159", "site_status": 1, "site_status_text": "in Betrieb", "kid": 1, "height_above_sea": 55.0}, "geometry": {"type": "Point", "coordinates": [9.73, 52.37]}}
    measurement = {"type": "Feature", "properties": {"kenn": "033510091", "start_measure": "2026-01-01T00:00:00Z", "end_measure": "2026-01-01T01:00:00Z", "value": 0.08, "value_cosmic": 0.03, "value_terrestrial": 0.05, "validated": 1, "nuclide": "Gamma-ODL-Brutto"}, "geometry": {"type": "Point", "coordinates": [9.73, 52.37]}}
    return [station], [measurement]


def _build_station(feature: dict, canton: str) -> Station:
    props = feature["properties"]
    geom = feature.get("geometry") or {}
    coords = geom.get("coordinates", [None, None])
    return Station(station_id=props["kenn"], canton=canton, station_code=props.get("id", ""), name=props.get("name", ""), postal_code=props.get("plz", ""), site_status=props.get("site_status", 0), site_status_text=props.get("site_status_text", ""), kid=props.get("kid", 0), height_above_sea=props.get("height_above_sea"), longitude=coords[0] if coords[0] is not None else 0.0, latitude=coords[1] if coords[1] is not None else 0.0)


def _build_measurement(feature: dict, canton: str) -> DoseRateMeasurement:
    props = feature["properties"]
    return DoseRateMeasurement(station_id=props["kenn"], canton=canton, start_measure=props.get("start_measure", ""), end_measure=props.get("end_measure", ""), value=props.get("value"), value_cosmic=props.get("value_cosmic"), value_terrestrial=props.get("value_terrestrial"), validated=props.get("validated", 0), nuclide=props.get("nuclide", ""))


def feed(args: argparse.Namespace) -> None:
    producer = create_amqp_producer(args)
    api = BfsOdlAPI()
    previous = _load_state(args.state_file)
    try:
        stations, sample_measurements = _sample_features() if os.getenv("BFS_ODL_SAMPLE_MODE", "").lower() in ("1", "true", "yes") else (api.fetch_stations(), None)
        for feature in stations:
            station_id = feature.get("properties", {}).get("kenn", "")
            canton = _canton_from_station_id(station_id)
            producer.send_station(data=_build_station(feature, canton), _feedurl=FEED_URL, _station_id=station_id, _canton=canton)
        logger.info("Published %d BfS ODL station info events to AMQP", len(stations))
        sent = 0
        for feature in (sample_measurements if sample_measurements is not None else api.fetch_latest_measurements()):
            props = feature.get("properties", {})
            station_id = props.get("kenn", "")
            end_measure = props.get("end_measure", "")
            if previous.get(station_id) == end_measure:
                continue
            canton = _canton_from_station_id(station_id)
            producer.send_dose_rate_measurement(data=_build_measurement(feature, canton), _feedurl=FEED_URL, _station_id=station_id, _canton=canton)
            previous[station_id] = end_measure
            sent += 1
        _save_state(args.state_file, previous)
        logger.info("Published %d BfS ODL dose-rate readings to AMQP", sent)
    finally:
        producer.close()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="BfS ODL AMQP bridge")
    parser.add_argument("command", nargs="?", default="feed")
    add_amqp_arguments(parser, "bfs-odl")
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", ""))
    parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    args = parser.parse_args()
    if args.command != "feed":
        parser.error("only the 'feed' command is supported")
    feed(args)


if __name__ == "__main__":
    main()
