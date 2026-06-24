from __future__ import annotations

import argparse
import dataclasses
import logging
import os
from typing import Any, Dict, Optional, Type, TypeVar
from urllib.parse import urlparse

from digitraffic_road_core import (
    MQTTSource,
    fetch_maintenance_task_payloads,
    fetch_tms_station_payloads,
    fetch_weather_station_payloads,
    flatten_traffic_message,
    parse_station_filter,
    parse_subscribe,
)
from digitraffic_road_amqp_producer_data import (
    MaintenanceTaskType,
    MaintenanceTracking,
    TmsSensorData,
    TmsStation,
    TrafficMessage,
    WeatherSensorData,
    WeatherStation,
)
from digitraffic_road_amqp_producer_amqp_producer.producer import FiDigitrafficRoadAmqpProducer

logger = logging.getLogger(__name__)
DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
T = TypeVar("T")


def _serializer_dict(data_cls: Type[T], payload: Dict[str, Any]) -> Dict[str, Any]:
    allowed = {field.name for field in dataclasses.fields(data_cls)}  # type: ignore[arg-type]
    return {key: value for key, value in payload.items() if key in allowed}


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_amqp_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    return parsed.hostname or "localhost", port, tls, parsed.username or None, parsed.password or None, (parsed.path or "").lstrip("/") or None


def _build_amqp_producer(producer_cls, *, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]):
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return producer_cls(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)
    return producer_cls(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)


def add_amqp_arguments(parser: argparse.ArgumentParser, default_address: str) -> None:
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", default_address))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))


def create_amqp_producer(args: argparse.Namespace, producer_cls):
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
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
    if not address:
        raise RuntimeError("AMQP address is required")
    logging.info("Connecting AMQP producer to %s:%s/%s auth=%s tls=%s", host, port, address, args.auth_mode, tls)
    return _build_amqp_producer(producer_cls, host=host, port=port, address=address, use_tls=tls, content_mode=args.content_mode, auth_mode=args.auth_mode, username=username, password=password, entra_audience=args.entra_audience, entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key)


class DigitrafficRoadAmqpBridge:
    def __init__(self, upstream_source: MQTTSource, producer: FiDigitrafficRoadAmqpProducer) -> None:
        self._upstream_source = upstream_source
        self._producer = producer

    def run(self) -> None:
        self._emit_reference_data()
        self._upstream_source.stream(self._on_message)

    def _emit_reference_data(self) -> None:
        for flat in fetch_tms_station_payloads():
            self._producer.send_tms_station(data=TmsStation.from_serializer_dict(_serializer_dict(TmsStation, flat)), _station_id=str(flat["station_id"]))
        for flat in fetch_weather_station_payloads():
            self._producer.send_weather_station(data=WeatherStation.from_serializer_dict(_serializer_dict(WeatherStation, flat)), _station_id=str(flat["station_id"]))
        for flat in fetch_maintenance_task_payloads():
            self._producer.send_maintenance_task_type(data=MaintenanceTaskType.from_serializer_dict(flat), _task_id=flat["task_id"])

    def _on_message(self, data_type: str, metadata: Dict[str, Any], payload: Dict[str, Any]) -> None:
        if data_type == "tms":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            enriched.setdefault("start", None)
            enriched.setdefault("end", None)
            data = TmsSensorData.from_serializer_dict(_serializer_dict(TmsSensorData, enriched))
            self._producer.send_tms_sensor_data(data=data, _station_id=str(station_id), _sensor_id=str(sensor_id))
        elif data_type == "weather":
            station_id = int(metadata["station_id"])
            sensor_id = int(metadata["sensor_id"])
            enriched = dict(payload)
            enriched["station_id"] = station_id
            enriched["sensor_id"] = sensor_id
            data = WeatherSensorData.from_serializer_dict(_serializer_dict(WeatherSensorData, enriched))
            self._producer.send_weather_sensor_data(data=data, _station_id=str(station_id), _sensor_id=str(sensor_id))
        elif data_type in {"traffic-announcement", "road-work", "weight-restriction", "exempted-transport"}:
            flat = flatten_traffic_message(str(metadata["situation_type"]), payload)
            data = TrafficMessage.from_serializer_dict(flat)
            if data_type == "traffic-announcement":
                self._producer.send_traffic_announcement(data=data, _situation_id=flat["situation_id"])
            elif data_type == "road-work":
                self._producer.send_road_work(data=data, _situation_id=flat["situation_id"])
            elif data_type == "weight-restriction":
                self._producer.send_weight_restriction(data=data, _situation_id=flat["situation_id"])
            else:
                self._producer.send_exempted_transport(data=data, _situation_id=flat["situation_id"])
        elif data_type == "maintenance":
            domain = str(metadata["domain"])
            enriched = dict(payload)
            enriched["domain"] = domain
            enriched.setdefault("direction", None)
            enriched.setdefault("source", None)
            data = MaintenanceTracking.from_serializer_dict(_serializer_dict(MaintenanceTracking, enriched))
            self._producer.send_maintenance_tracking(data=data, _domain=domain)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG if os.getenv("PYTHONDEBUG") else logging.INFO)
    parser = argparse.ArgumentParser(description="Digitraffic Road -> AMQP 1.0 bridge")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Bridge Digitraffic Road events to AMQP 1.0")
    add_amqp_arguments(feed_parser, "digitraffic-road")
    feed_parser.add_argument("--subscribe", default=os.getenv("DIGITRAFFIC_ROAD_SUBSCRIBE", "tms,weather,traffic-messages,maintenance"))
    feed_parser.add_argument("--station-filter", default=os.getenv("DIGITRAFFIC_ROAD_STATION_FILTER"))
    args = parser.parse_args()
    if args.command != "feed":
        parser.print_help()
        return
    subscribe_flags = parse_subscribe(args.subscribe)
    station_filter = parse_station_filter(args.station_filter)
    producer = create_amqp_producer(args, FiDigitrafficRoadAmqpProducer)
    source = MQTTSource(station_filter=station_filter, **subscribe_flags)  # type: ignore[arg-type]
    bridge = DigitrafficRoadAmqpBridge(source, producer)
    try:
        bridge.run()
    finally:
        producer.close()


if __name__ == "__main__":
    main()
