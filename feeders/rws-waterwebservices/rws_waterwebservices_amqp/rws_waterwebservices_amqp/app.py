"""AMQP feeder application for RWS Waterwebservices → Unified Namespace.

Reuses the upstream HTTP client and station catalog logic from the existing
``rws_waterwebservices`` Kafka bridge (imported as the transport-agnostic "core"
package) and pushes CloudEvents into AMQP 1.0 using the xrcg-generated
:class:`NLRWSWaterwebservicesAmqpProducer`.

Topic tree: ``hydro/nl/rws/rws-waterwebservices/{station_code}/{info|water-level}``.
RWS Waterwebservices does not expose a stable shared water-body axis in the
station catalog, so the AMQP tree uses station code as the stable subscriber axis.
"""

from __future__ import annotations

import argparse
import time
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from rws_waterwebservices.rws_waterwebservices import RWSWaterwebservicesAPI, _load_state, _save_state
from rws_waterwebservices_amqp_producer_data import Station, WaterLevelObservation
from rws_waterwebservices_amqp_producer_amqp_producer.producer import NLRWSWaterwebservicesAmqpProducer

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


def _build_station_map(locations: List[Dict[str, Any]]) -> Dict[str, str]:
    """Build station_code → location display name map from catalog locations."""
    mapping: Dict[str, str] = {}
    for loc in locations:
        code = loc.get("Code", "")
        naam = loc.get("Naam", "")
        if code:
            mapping[code] = naam
    return mapping


def _publish_stations(
    producer: NLRWSWaterwebservicesAmqpProducer,
    locations: List[Dict[str, Any]],
    station_map: Dict[str, str],
) -> None:
    for loc in locations:
        code = loc.get("Code", "")
        if not code:
            continue
        naam = station_map.get(code, "")
        station = Station(
            station_code=code,
            name=naam,
            latitude=float(loc.get("Lat", 0) or 0),
            longitude=float(loc.get("Lon", 0) or 0),
            coordinate_system=loc.get("Coordinatenstelsel") or None,
        )
        producer.send_station(
            _station_code=code,
            data=station,
        )


def _publish_observations(
    api: RWSWaterwebservicesAPI,
    producer: NLRWSWaterwebservicesAmqpProducer,
    station_codes: List[str],
    station_map: Dict[str, str],
    previous_readings: Dict[str, str],
) -> int:
    observations = api.get_latest_observations(station_codes)
    sent = 0
    for entry in observations:
        locatie = entry.get("Locatie", {})
        aquo = entry.get("AquoMetadata", {})
        unit = aquo.get("Eenheid", {}).get("Code", "cm")
        metingen_lijst = entry.get("MetingenLijst", [])

        for meting in metingen_lijst:
            tijdstip = meting.get("Tijdstip")
            meetwaarde = meting.get("Meetwaarde", {})
            waarde = meetwaarde.get("Waarde_Numeriek")

            if waarde is None or tijdstip is None:
                continue

            location_code = locatie.get("Code", "")
            reading_key = f"{location_code}:{tijdstip}"
            if reading_key in previous_readings:
                continue

            naam = station_map.get(location_code, locatie.get("Naam", ""))
            metadata = meting.get("WaarnemingMetadata", {})

            observation = WaterLevelObservation(
                station_code=location_code,
                location_name=naam or None,
                timestamp=tijdstip,
                value=float(waarde),
                unit=unit,
                quality_code=metadata.get("Kwaliteitswaardecode") or None,
                status=metadata.get("Statuswaarde") or None,
                compartment=api.COMPARTIMENT_CODE,
                parameter=api.GROOTHEID_CODE,
            )

            try:
                producer.send_water_level_observation(
                    _station_code=location_code,
                    data=observation,
                )
                sent += 1
                previous_readings[reading_key] = tijdstip
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error publishing observation for %s: %s", location_code, exc)

    return sent


def _publish_mock(producer: NLRWSWaterwebservicesAmqpProducer) -> None:
    station = Station(station_code="MOCK", name="Mock Station", latitude=52.0, longitude=5.0, coordinate_system="EPSG:4326")
    observation = WaterLevelObservation(station_code="MOCK", location_name="Mock Station", timestamp=datetime.now(timezone.utc), value=1.23, unit="m", quality_code="00", status="ok", compartment="OW", parameter="water_level")
    producer.send_station(data=station, _station_code="MOCK")
    producer.send_water_level_observation(data=observation, _station_code="MOCK")


def feed(
    api: RWSWaterwebservicesAPI,
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
    address: str = "rws-waterwebservices",
    auth_mode: str = "password",
    entra_audience: str = "https://servicebus.azure.net/.default",
    entra_client_id: Optional[str] = None,
    sas_key_name: Optional[str] = None,
    sas_key: Optional[str] = None,
) -> None:
    previous_readings = _load_state(state_file)
    producer = _retry_producer_init(lambda: _build_producer(host=broker_host, port=broker_port, address=address, use_tls=tls, content_mode=content_mode, auth_mode=auth_mode, username=username, password=password, entra_audience=entra_audience, entra_client_id=entra_client_id, sas_key_name=sas_key_name, sas_key=sas_key))
    if os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"):
        _publish_mock(producer)
        producer.close()
        return


    # Fetch station catalog and build station display-name map
    locations = api.get_water_level_stations()
    station_map = _build_station_map(locations)
    station_codes = [loc.get("Code", "") for loc in locations if loc.get("Code")]

    logger.info("Publishing %d station info events under hydro/nl/rws/rws-waterwebservices/...", len(locations))
    _publish_stations(producer, locations, station_map)
    logger.info("Finished publishing station catalog")

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count = _publish_observations(api, producer, station_codes, station_map, previous_readings)
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
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                time.sleep(polling_interval)
    finally:
        producer.close()



DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def _build_producer(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]) -> NLRWSWaterwebservicesAmqpProducer:
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return NLRWSWaterwebservicesAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)  # type: ignore[arg-type]
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return NLRWSWaterwebservicesAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)  # type: ignore[arg-type]
    return NLRWSWaterwebservicesAmqpProducer(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)  # type: ignore[arg-type]

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
    parser = argparse.ArgumentParser(description="RWS Waterwebservices → AMQP 1.0 bridge.")
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
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "rws-waterwebservices"))
    feed_parser.add_argument("--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra", "sas"])
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.rws_waterwebservices_amqp_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
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

    api = RWSWaterwebservicesAPI()
    feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
            address=address, auth_mode=args.auth_mode, entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key,
        )


if __name__ == "__main__":
    main()
