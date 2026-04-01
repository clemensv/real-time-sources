"""German Waters bridge — aggregates water level data from German state open data portals."""

from datetime import datetime, timedelta, timezone
import os
import logging
import sys
import time
import argparse
import json
from typing import Dict, List, Optional

from confluent_kafka import Producer
from german_waters_producer_data.de.waters.hydrology.station import Station
from german_waters_producer_data.de.waters.hydrology.waterlevelobservation import WaterLevelObservation
from german_waters_producer_kafka_producer.producer import DEWatersHydrologyEventProducer

from german_waters.providers import BaseProvider, StationData, ObservationData
from german_waters.providers.bayern_gkd import BayernGKDProvider
from german_waters.providers.nrw_hygon import NRWHygonProvider
from german_waters.providers.sh_lkn import SchleswigHolsteinProvider
from german_waters.providers.nds_nlwkn import NiedersachsenProvider
from german_waters.providers.sa_lhw import SachsenAnhaltProvider
from german_waters.providers.he_hlnug import HessenHLNUGProvider
from german_waters.providers.sn_lfulg import SachsenLfULGProvider
from german_waters.providers.bw_hvz import BadenWuerttembergProvider
from german_waters.providers.bb_lfu import BrandenburgProvider
from german_waters.providers.th_tlubn import ThueringenProvider
from german_waters.providers.mv_lung import MecklenburgVorpommernProvider
from german_waters.providers.be_senumvk import BerlinProvider

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Registry of available providers
PROVIDER_CLASSES: Dict[str, type] = {
    "bayern_gkd": BayernGKDProvider,
    "nrw_hygon": NRWHygonProvider,
    "sh_lkn": SchleswigHolsteinProvider,
    "nds_nlwkn": NiedersachsenProvider,
    "sa_lhw": SachsenAnhaltProvider,
    "he_hlnug": HessenHLNUGProvider,
    "sn_lfulg": SachsenLfULGProvider,
    "bw_hvz": BadenWuerttembergProvider,
    "bb_lfu": BrandenburgProvider,
    "th_tlubn": ThueringenProvider,
    "mv_lung": MecklenburgVorpommernProvider,
    "be_senumvk": BerlinProvider,
}

PROVIDER_STATE_MAP: Dict[str, str] = {
    "bayern_gkd": "Bayern",
    "nrw_hygon": "Nordrhein-Westfalen",
    "sh_lkn": "Schleswig-Holstein",
    "nds_nlwkn": "Niedersachsen",
    "sa_lhw": "Sachsen-Anhalt",
    "he_hlnug": "Hessen",
    "sn_lfulg": "Sachsen",
    "bw_hvz": "Baden-Württemberg",
    "bb_lfu": "Brandenburg",
    "th_tlubn": "Thüringen",
    "mv_lung": "Mecklenburg-Vorpommern",
    "be_senumvk": "Berlin",
}

ALL_PROVIDERS = sorted(PROVIDER_CLASSES.keys())


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file."""
    if not state_file:
        return
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logger.warning("Could not save state to %s: %s", state_file, e)


def _resolve_providers(include_csv: Optional[str], exclude_csv: Optional[str]) -> List[BaseProvider]:
    """Instantiate providers based on --providers / --exclude-providers filters."""
    include = set(p.strip() for p in include_csv.split(",") if p.strip()) if include_csv else None
    exclude = set(p.strip() for p in exclude_csv.split(",") if p.strip()) if exclude_csv else set()
    providers: List[BaseProvider] = []
    for key, cls in PROVIDER_CLASSES.items():
        if include is not None and key not in include:
            continue
        if key in exclude:
            continue
        providers.append(cls())
    return providers


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').strip().replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"').strip()
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def _station_to_event(s: StationData) -> Station:
    return Station(
        station_id=s.station_id,
        station_name=s.station_name,
        water_body=s.water_body,
        state=s.state,
        region=s.region,
        provider=s.provider,
        latitude=s.latitude,
        longitude=s.longitude,
        river_km=s.river_km,
        altitude=s.altitude,
        station_type=s.station_type,
        warn_level_cm=s.warn_level_cm,
        alarm_level_cm=s.alarm_level_cm,
        warn_level_m3s=s.warn_level_m3s,
        alarm_level_m3s=s.alarm_level_m3s,
    )


def _obs_to_event(o: ObservationData) -> WaterLevelObservation:
    return WaterLevelObservation(
        station_id=o.station_id,
        provider=o.provider,
        water_level=o.water_level,
        water_level_unit=o.water_level_unit,
        water_level_timestamp=o.water_level_timestamp,
        discharge=o.discharge,
        discharge_unit=o.discharge_unit,
        discharge_timestamp=o.discharge_timestamp,
        trend=o.trend,
        situation=o.situation,
    )


def send_stations(producer_client: DEWatersHydrologyEventProducer,
                  stations: List[StationData]) -> int:
    """Emit Station events. Returns count sent."""
    count = 0
    for s in stations:
        producer_client.send_de_waters_hydrology_station(
            data=_station_to_event(s), flush_producer=False)
        count += 1
    return count


def feed_observations(producer_client: DEWatersHydrologyEventProducer,
                      providers: List[BaseProvider],
                      previous_readings: Dict[str, str],
                      kafka_producer: Producer) -> int:
    """Emit WaterLevelObservation events, deduplicating by timestamp. Returns count sent."""
    count = 0
    for provider in providers:
        try:
            observations = provider.get_observations()
        except Exception as e:
            logger.error("Error fetching observations from %s: %s", provider.name, e, exc_info=True)
            continue
        for o in observations:
            ts_key = o.water_level_timestamp or o.discharge_timestamp
            if not ts_key:
                continue
            prev_ts = previous_readings.get(o.station_id)
            if prev_ts == ts_key:
                continue
            producer_client.send_de_waters_hydrology_water_level_observation(
                data=_obs_to_event(o), flush_producer=False)
            previous_readings[o.station_id] = ts_key
            count += 1
    kafka_producer.flush()
    return count


def run_feed(kafka_config: dict, kafka_topic: str, polling_interval: int,
             state_file: str, providers: List[BaseProvider]) -> None:
    """Main feed loop: emit stations once, then poll observations."""
    previous_readings: Dict[str, str] = _load_state(state_file)
    kafka_producer = Producer(kafka_config)
    event_producer = DEWatersHydrologyEventProducer(kafka_producer, kafka_topic)

    provider_names = ", ".join(p.name for p in providers)
    logger.info("Starting German Waters feed → topic=%s, bootstrap=%s, providers=[%s]",
                kafka_topic, kafka_config.get('bootstrap.servers'), provider_names)

    # Send station metadata once at startup
    total_stations = 0
    for provider in providers:
        try:
            stations = provider.get_stations()
            n = send_stations(event_producer, stations)
            total_stations += n
            logger.info("Sent %d station records from %s", n, provider.name)
        except Exception as e:
            logger.error("Error fetching stations from %s: %s", provider.name, e, exc_info=True)
    kafka_producer.flush()
    logger.info("Sent %d total station records", total_stations)

    while True:
        try:
            start = datetime.now(timezone.utc)
            # Invalidate caches for providers that support it
            for provider in providers:
                if hasattr(provider, 'invalidate'):
                    provider.invalidate()
            n = feed_observations(event_producer, providers, previous_readings, kafka_producer)
            elapsed = (datetime.now(timezone.utc) - start).total_seconds()
            wait = max(0, polling_interval - elapsed)
            logger.info("Sent %d observations in %.1fs. Next poll at %s.",
                        n, elapsed,
                        (datetime.now(timezone.utc) + timedelta(seconds=wait)).isoformat())
            _save_state(state_file, previous_readings)
            if wait > 0:
                time.sleep(wait)
        except KeyboardInterrupt:
            logger.info("Interrupted — exiting.")
            break
        except Exception as e:
            logger.error("Error: %s", e, exc_info=True)
            logger.info("Retrying in %ds …", polling_interval)
            time.sleep(polling_interval)
    kafka_producer.flush()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="German Waters bridge — aggregates water level data from German state flood services")
    subparsers = parser.add_subparsers(dest="command")

    # --- list-providers ---
    subparsers.add_parser("list-providers", help="Show available provider keys")

    # --- list ---
    list_p = subparsers.add_parser("list", help="List stations (prints to stdout)")
    list_p.add_argument("--providers", type=str, default=os.getenv("PROVIDERS"),
                        help="Comma-separated provider keys to include")
    list_p.add_argument("--exclude-providers", type=str, default=os.getenv("EXCLUDE_PROVIDERS"),
                        help="Comma-separated provider keys to exclude")

    # --- feed ---
    feed_p = subparsers.add_parser("feed", help="Feed stations & observations to Kafka")
    feed_p.add_argument("--kafka-bootstrap-servers", type=str,
                        default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_p.add_argument("--kafka-topic", type=str, default=os.getenv("KAFKA_TOPIC"))
    feed_p.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_p.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_p.add_argument("-c", "--connection-string", type=str,
                        default=os.getenv("CONNECTION_STRING"))
    polling_default = int(os.getenv("POLLING_INTERVAL", "900"))
    feed_p.add_argument("-i", "--polling-interval", type=int, default=polling_default,
                        help="Polling interval in seconds (default: 900)")
    feed_p.add_argument("--state-file", type=str,
                        default=os.getenv("STATE_FILE",
                                          os.path.expanduser("~/.german_waters_state.json")))
    feed_p.add_argument("--providers", type=str, default=os.getenv("PROVIDERS"),
                        help="Comma-separated provider keys to include")
    feed_p.add_argument("--exclude-providers", type=str, default=os.getenv("EXCLUDE_PROVIDERS"),
                        help="Comma-separated provider keys to exclude")

    args = parser.parse_args()

    if args.command == "list-providers":
        for key in ALL_PROVIDERS:
            state = PROVIDER_STATE_MAP.get(key, "")
            cls = PROVIDER_CLASSES[key]
            inst = cls()
            print(f"  {key:20s}  {state:25s}  {inst.description}")
        return

    if args.command == "list":
        providers = _resolve_providers(args.providers, args.exclude_providers)
        for provider in providers:
            stations = provider.get_stations()
            for s in stations:
                print(f"{s.station_id:30s}  {s.water_body:20s}  {s.station_name:25s}  {s.provider}")
            print(f"  [{provider.name}] {len(stations)} stations")
        return

    if args.command == "feed":
        if args.connection_string:
            cfg = parse_connection_string(args.connection_string)
            bootstrap = cfg.get("bootstrap.servers")
            topic = cfg.get("kafka_topic")
            sasl_user = cfg.get("sasl.username")
            sasl_pw = cfg.get("sasl.password")
        else:
            bootstrap = args.kafka_bootstrap_servers
            topic = args.kafka_topic
            sasl_user = args.sasl_username
            sasl_pw = args.sasl_password

        if not bootstrap:
            print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers or -c).")
            sys.exit(1)
        if not topic:
            print("Error: Kafka topic required (--kafka-topic or -c).")
            sys.exit(1)

        tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
        kafka_config: Dict[str, str] = {"bootstrap.servers": bootstrap}
        if sasl_user and sasl_pw:
            kafka_config.update({
                "sasl.mechanisms": "PLAIN",
                "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
                "sasl.username": sasl_user,
                "sasl.password": sasl_pw,
            })
        elif tls_enabled:
            kafka_config["security.protocol"] = "SSL"

        inc, exc = args.providers, args.exclude_providers
        providers = _resolve_providers(inc, exc)
        run_feed(kafka_config, topic, args.polling_interval, args.state_file, providers)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
