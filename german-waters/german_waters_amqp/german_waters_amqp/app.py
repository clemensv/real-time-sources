"""AMQP feeder application for German Waters Hydrology → Unified Namespace.

Reuses the upstream HTTP providers and station catalog logic from the existing
``german_waters`` Kafka bridge and pushes CloudEvents into AMQP 1.0 using the
xrcg-generated :class:`DEWatersHydrologyAmqpProducer`.

Topic tree: ``hydro/de/wsv/german-waters/{water_body}/{station_id}/{info|water-level}``.
``{water_body}`` is sourced from the per-provider station catalog
(field ``water_body``) and normalized to lowercase kebab-case by
:func:`_uns_slug` so umlauts, spaces and slashes never reach the broker.
"""

from __future__ import annotations

import argparse
import time
import logging
import os
import sys
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from german_waters.german_waters import (
    PROVIDER_CLASSES,
    _load_state,
    _resolve_providers,
    _save_state,
    _station_to_event,
)
from german_waters.providers import BaseProvider, ObservationData, StationData
from german_waters_amqp_producer_data import Station, WaterLevelObservation
from german_waters_amqp_producer_amqp_producer.producer import DEWatersHydrologyAmqpProducer

logger = logging.getLogger(__name__)

_UNS_REPLACEMENTS = str.maketrans({
    "ä": "a", "ö": "o", "ü": "u", "Ä": "a", "Ö": "o", "Ü": "u", "ß": "ss",
    "à": "a", "á": "a", "â": "a", "è": "e", "é": "e", "ê": "e",
    "ì": "i", "í": "i", "î": "i", "ò": "o", "ó": "o", "ô": "o",
    "ù": "u", "ú": "u", "û": "u", "ç": "c", "ñ": "n",
})


def _uns_slug(value: str) -> str:
    """Normalize an arbitrary upstream label to a UNS-safe lowercase kebab segment."""
    if not value:
        return "unknown"
    raw = value.translate(_UNS_REPLACEMENTS).lower().strip()
    out = []
    for ch in raw:
        if ch.isalnum():
            out.append(ch)
        elif ch in ("-", "_"):
            out.append(ch)
        else:
            out.append("-")
    slug = "".join(out).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "unknown"


def _station_to_amqp_event(s: StationData) -> Station:
    """Convert internal StationData to the AMQP producer dataclass."""
    return Station(
        station_id=s.station_id,
        station_name=s.station_name,
        water_body=s.water_body,
        state=s.state or None,
        region=s.region or None,
        provider=s.provider,
        latitude=s.latitude or None,
        longitude=s.longitude or None,
        river_km=s.river_km or None,
        altitude=s.altitude or None,
        station_type=s.station_type or None,
        warn_level_cm=s.warn_level_cm or None,
        alarm_level_cm=s.alarm_level_cm or None,
        warn_level_m3s=s.warn_level_m3s or None,
        alarm_level_m3s=s.alarm_level_m3s or None,
    )


def _obs_to_amqp_event(o: ObservationData, water_body: str) -> WaterLevelObservation:
    """Convert internal ObservationData to the AMQP producer dataclass."""
    wl_ts = None
    if o.water_level_timestamp:
        try:
            wl_ts = datetime.fromisoformat(o.water_level_timestamp)
        except (ValueError, TypeError):
            pass
    dis_ts = None
    if o.discharge_timestamp:
        try:
            dis_ts = datetime.fromisoformat(o.discharge_timestamp)
        except (ValueError, TypeError):
            pass
    return WaterLevelObservation(
        station_id=o.station_id,
        provider=o.provider,
        water_body=water_body,
        water_level=o.water_level or None,
        water_level_unit=o.water_level_unit or None,
        water_level_timestamp=wl_ts,
        discharge=o.discharge or None,
        discharge_unit=o.discharge_unit or None,
        discharge_timestamp=dis_ts,
        trend=o.trend or None,
        situation=o.situation or None,
    )


def _publish_stations(
    producer: DEWatersHydrologyAmqpProducer,
    providers: List[BaseProvider],
) -> Dict[str, str]:
    """Publish station info events. Returns station_id → water_body map."""
    station_water_map: Dict[str, str] = {}
    for provider in providers:
        try:
            stations = provider.get_stations()
        except Exception as exc:
            logger.error("Error fetching stations from %s: %s", provider.name, exc)
            continue
        for s in stations:
            water_slug = _uns_slug(s.water_body or "unknown")
            station_water_map[s.station_id] = s.water_body or "unknown"
            producer.send_station(
                _station_id=s.station_id,
                _water_body=water_slug,
                data=_station_to_amqp_event(s),
            )
    return station_water_map


def _publish_observations(
    producer: DEWatersHydrologyAmqpProducer,
    providers: List[BaseProvider],
    station_water_map: Dict[str, str],
    previous_readings: Dict[str, str],
) -> int:
    """Publish observation events. Returns count of published messages."""
    sent = 0
    for provider in providers:
        try:
            if hasattr(provider, 'invalidate'):
                provider.invalidate()
            observations = provider.get_observations()
        except Exception as exc:
            logger.error("Error fetching observations from %s: %s", provider.name, exc, exc_info=True)
            continue
        for o in observations:
            ts_key = o.water_level_timestamp or o.discharge_timestamp
            if not ts_key:
                continue
            prev_ts = previous_readings.get(o.station_id)
            if prev_ts == ts_key:
                continue
            water_body_raw = station_water_map.get(o.station_id, "unknown")
            water_slug = _uns_slug(water_body_raw)
            try:
                producer.send_water_level_observation(
                    _station_id=o.station_id,
                    _water_body=water_slug,
                    data=_obs_to_amqp_event(o, water_body_raw),
                )
                sent += 1
                previous_readings[o.station_id] = ts_key
            except Exception as exc:
                logger.error("Error publishing observation for %s: %s", o.station_id, exc)
    return sent


def _publish_mock(producer: DEWatersHydrologyAmqpProducer) -> None:
    station = Station(station_id="mock-station", station_name="Mock Station", water_body="Mock River", state="BY", region="Mock", provider="mock", latitude=50.0, longitude=8.0, river_km=1.0, altitude=100.0, station_type="gauge", warn_level_cm=200.0, alarm_level_cm=300.0, warn_level_m3s=20.0, alarm_level_m3s=30.0)
    observation = WaterLevelObservation(station_id="mock-station", provider="mock", water_body="Mock River", water_level=123.0, water_level_unit="cm", water_level_timestamp=datetime.now(timezone.utc), discharge=12.3, discharge_unit="m3/s", discharge_timestamp=datetime.now(timezone.utc), trend=None, situation=None)
    producer.send_station(data=station, _station_id="mock-station", _water_body="mock-river")
    producer.send_water_level_observation(data=observation, _station_id="mock-station", _water_body="mock-river")


def feed(
    providers: List[BaseProvider],
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
    address: str = "german-waters",
    auth_mode: str = "password",
    entra_audience: str = "https://servicebus.azure.net/.default",
    entra_client_id: Optional[str] = None,
    sas_key_name: Optional[str] = None,
    sas_key: Optional[str] = None,
) -> None:
    previous_readings = _load_state(state_file)
    producer = _build_producer(host=broker_host, port=broker_port, address=address, use_tls=tls, content_mode=content_mode, auth_mode=auth_mode, username=username, password=password, entra_audience=entra_audience, entra_client_id=entra_client_id, sas_key_name=sas_key_name, sas_key=sas_key)
    if os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"):
        _publish_mock(producer)
        producer.close()
        return


    provider_names = ", ".join(p.name for p in providers)
    logger.info("Publishing station info events for providers: [%s]", provider_names)
    station_water_map = _publish_stations(producer, providers)
    logger.info("Published %d station info events", len(station_water_map))

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = _publish_observations(
                    producer, providers, station_water_map, previous_readings
                )
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %s observations in %.1fs. Sleeping until %s.",
                    count,
                    (end_time - start_time).total_seconds(),
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                _save_state(state_file, previous_readings)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:
                logger.error("Error during polling cycle: %s", exc, exc_info=True)
                time.sleep(polling_interval)
    finally:
        producer.close()



DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _build_producer(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]) -> DEWatersHydrologyAmqpProducer:
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return DEWatersHydrologyAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)  # type: ignore[arg-type]
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return DEWatersHydrologyAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)  # type: ignore[arg-type]
    return DEWatersHydrologyAmqpProducer(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)  # type: ignore[arg-type]

def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="German Waters Hydrology → AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed stations and observations as CloudEvents to AMQP")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("AMQP_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "german-waters"))
    feed_parser.add_argument("--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra", "sas"])
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "900")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.german_waters_amqp_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--providers", type=str, default=os.getenv("PROVIDERS"),
                             help="Comma-separated provider keys to include")
    feed_parser.add_argument("--exclude-providers", type=str, default=os.getenv("EXCLUDE_PROVIDERS"),
                             help="Comma-separated provider keys to exclude")
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        address = path or args.address
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (5671 if tls else 5672)
        username = args.username
        password = args.password
        address = args.address
    providers = _resolve_providers(args.providers, args.exclude_providers)
    feed(
            providers, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
            address=address, auth_mode=args.auth_mode, entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key,
        )


if __name__ == "__main__":
    main()
