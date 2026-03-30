"""
RWS Waterwebservices Poller
Polls the Dutch Rijkswaterstaat Waterwebservices API and sends water level data
to Kafka as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any
import argparse
import requests
from rws_waterwebservices.rws_waterwebservices_producer.nl.rws.waterwebservices.station import Station
from rws_waterwebservices.rws_waterwebservices_producer.nl.rws.waterwebservices.water_level_observation import WaterLevelObservation
from .rws_waterwebservices_producer.producer_client import NLRWSWaterwebservicesEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


def _load_state(state_file: str) -> dict:
    """Load persisted dedup state from a JSON file."""
    try:
        if state_file and os.path.exists(state_file):
            with open(state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.warning("Could not load state from %s: %s", state_file, e)
    return {}


def _save_state(state_file: str, data: dict) -> None:
    """Save dedup state to a JSON file, keeping at most 100000 entries."""
    if not state_file:
        return
    try:
        if len(data) > 100000:
            keys = list(data.keys())
            data = {k: data[k] for k in keys[-50000:]}
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception as e:
        logging.warning("Could not save state to %s: %s", state_file, e)


class RWSWaterwebservicesAPI:
    """
    Polls the Rijkswaterstaat Waterwebservices API and sends data to Kafka as CloudEvents.
    """
    BASE_URL = "https://ddapi20-waterwebservices.rijkswaterstaat.nl"
    CATALOG_ENDPOINT = "/METADATASERVICES/OphalenCatalogus"
    LATEST_OBSERVATIONS_ENDPOINT = "/ONLINEWAARNEMINGENSERVICES/OphalenLaatsteWaarnemingen"
    POLL_INTERVAL_SECONDS = 600  # 10 minutes

    # Water level filter values
    COMPARTIMENT_CODE = "OW"  # Oppervlaktewater (surface water)
    GROOTHEID_CODE = "WATHTE"  # Waterhoogte (water height)

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    BATCH_SIZE = 100  # Max locations per observations request

    def _post_request(self, endpoint: str, payload: dict) -> Any:
        """Make a POST request to the Waterwebservices API.
        Returns parsed JSON or None for 204 No Content."""
        url = self.BASE_URL + endpoint
        response = self.session.post(url, json=payload, timeout=60)
        response.raise_for_status()
        if response.status_code == 204:
            return None
        return response.json()

    def get_catalog(self) -> Dict[str, Any]:
        """Fetch the catalog with locations and parameter metadata."""
        payload = {
            "CatalogusFilter": {
                "Compartimenten": True,
                "Grootheden": True,
            },
            "LocatieMetadataFilter": {
                "Compartiment": {"Code": self.COMPARTIMENT_CODE},
                "Grootheid": {"Code": self.GROOTHEID_CODE},
            },
        }
        return self._post_request(self.CATALOG_ENDPOINT, payload)

    def get_water_level_stations(self) -> List[Dict[str, Any]]:
        """Fetch all water level monitoring stations from the catalog.

        Uses the catalog endpoint to get all locations, then filters
        to only those linked to WATHTE/OW measurements.
        """
        data = self.get_catalog()
        if not data or not data.get("Succesvol"):
            logging.warning("Catalog returned Succesvol=false: %s",
                            data.get("Foutmelding") if data else "No response")
            return []

        locs = data.get("LocatieLijst", [])
        aquo_meta = data.get("AquoMetadataLijst", [])
        aquo_links = data.get("AquoMetadataLocatieLijst", [])

        # Find the WATHTE/OW message ID
        wathte_id = None
        for m in aquo_meta:
            if (m.get("Grootheid", {}).get("Code") == self.GROOTHEID_CODE
                    and m.get("Compartiment", {}).get("Code") == self.COMPARTIMENT_CODE):
                wathte_id = m.get("AquoMetadata_MessageID")
                break

        if wathte_id is None:
            logging.warning("WATHTE/OW not found in catalog metadata")
            return locs  # Return all locations as fallback

        # Filter to only locations linked to WATHTE/OW
        wathte_loc_ids = {
            link.get("Locatie_MessageID")
            for link in aquo_links
            if link.get("AquoMetaData_MessageID") == wathte_id
        }
        return [loc for loc in locs if loc.get("Locatie_MessageID") in wathte_loc_ids]

    def get_latest_observations(self, station_codes: List[str]) -> List[Dict[str, Any]]:
        """Fetch latest observations for the given station codes.

        Batches requests to stay within API limits.
        Returns combined WaarnemingenLijst from all batches.
        """
        all_observations: List[Dict[str, Any]] = []
        aquo_filter = [
            {"aquoMetadata": {
                "Compartiment": {"Code": self.COMPARTIMENT_CODE},
                "Grootheid": {"Code": self.GROOTHEID_CODE},
            }}
        ]

        for i in range(0, len(station_codes), self.BATCH_SIZE):
            batch = station_codes[i:i + self.BATCH_SIZE]
            payload = {
                "LocatieLijst": [{"Code": code} for code in batch],
                "AquoPlusWaarnemingMetadataLijst": aquo_filter,
            }
            data = self._post_request(self.LATEST_OBSERVATIONS_ENDPOINT, payload)
            if data is None:
                continue  # 204 No Content
            if not data.get("Succesvol"):
                logging.warning("Observations batch failed: %s", data.get("Foutmelding"))
                continue
            all_observations.extend(data.get("WaarnemingenLijst", []))

        return all_observations

    def parse_connection_string(self, connection_string: str) -> Dict[str, str]:
        """Parse an Event Hubs connection string."""
        config_dict = {}
        try:
            for part in connection_string.split(';'):
                if 'Endpoint' in part:
                    config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                        '"').strip().replace('sb://', '').replace('/', '')+':9093'
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

    def feed_stations(self, kafka_config: dict, kafka_topic: str, polling_interval: int, state_file: str = '') -> None:
        """Feed station and water level data as CloudEvents to Kafka."""
        previous_readings: Dict[str, str] = _load_state(state_file)

        from confluent_kafka import Producer
        producer = Producer(kafka_config)
        rws_producer = NLRWSWaterwebservicesEventProducer(producer, kafka_topic)

        logging.info("Starting to feed stations to Kafka topic %s", kafka_topic)

        # Fetch and send station reference data
        water_level_stations = self.get_water_level_stations()
        station_codes: List[str] = []
        station_count = 0

        for loc in water_level_stations:
            code = loc.get("Code", "")
            station = Station(
                code=code,
                name=loc.get("Naam", ""),
                latitude=float(loc.get("Lat", 0) or 0),
                longitude=float(loc.get("Lon", 0) or 0),
                coordinate_system=loc.get("Coordinatenstelsel", ""),
            )
            rws_producer.send_nl_rws_waterwebservices_station(station, flush_producer=False)
            station_codes.append(code)
            station_count += 1
        producer.flush()
        logging.info("Sent %d stations as reference data", station_count)

        # Main polling loop
        while True:
            try:
                count = 0
                start_time = time.time()
                observations = self.get_latest_observations(station_codes)

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

                        metadata = meting.get("WaarnemingMetadata", {})
                        observation = WaterLevelObservation(
                            location_code=location_code,
                            location_name=locatie.get("Naam", ""),
                            timestamp=tijdstip,
                            value=float(waarde),
                            unit=unit,
                            quality_code=metadata.get("Kwaliteitswaardecode", ""),
                            status=metadata.get("Statuswaarde", ""),
                            compartment=self.COMPARTIMENT_CODE,
                            parameter=self.GROOTHEID_CODE,
                        )

                        try:
                            rws_producer.send_nl_rws_waterwebservices_water_level_observation(
                                observation, flush_producer=False)
                            count += 1
                        # pylint: disable=broad-except
                        except Exception as e:
                            logging.error("Error sending observation to kafka: %s", e)
                        # pylint: enable=broad-except

                        previous_readings[reading_key] = tijdstip

                producer.flush()
                end_time = time.time()
                effective_interval = max(0, polling_interval - (end_time - start_time))
                logging.info("Sent %d observations in %.1f seconds. Waiting %.0f seconds.",
                             count, end_time - start_time, effective_interval)
                _save_state(state_file, previous_readings)
                if effective_interval > 0:
                    time.sleep(effective_interval)

            except KeyboardInterrupt:
                logging.info("Exiting...")
                break
            # pylint: disable=broad-except
            except Exception as e:
                logging.error("Error occurred: %s", e)
                logging.info("Retrying in %d seconds...", polling_interval)
                time.sleep(polling_interval)
            # pylint: enable=broad-except
        producer.flush()


def main() -> None:
    """Main entry point for RWS Waterwebservices bridge."""
    parser = argparse.ArgumentParser(description='Rijkswaterstaat Waterwebservices API bridge to Kafka')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('list', help='List water level stations')

    level_parser = subparsers.add_parser('level', help='Get latest water level for a station')
    level_parser.add_argument('station_code', type=str, help='Station code (e.g., HOlv)')

    feed_parser = subparsers.add_parser('feed', help='Feed water levels as CloudEvents to Kafka')
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             default=os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
    feed_parser.add_argument('--kafka-topic', type=str, default=os.getenv('KAFKA_TOPIC'))
    feed_parser.add_argument('--sasl-username', type=str, default=os.getenv('SASL_USERNAME'))
    feed_parser.add_argument('--sasl-password', type=str, default=os.getenv('SASL_PASSWORD'))
    feed_parser.add_argument('-c', '--connection-string', type=str,
                             default=os.getenv('CONNECTION_STRING'))
    polling_interval_default = 600
    if os.getenv('POLLING_INTERVAL'):
        polling_interval_default = int(os.getenv('POLLING_INTERVAL'))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=polling_interval_default)
    feed_parser.add_argument('--state-file', type=str,
                             default=os.getenv('STATE_FILE', os.path.expanduser('~/.rws_waterwebservices_state.json')))

    args = parser.parse_args()
    api = RWSWaterwebservicesAPI()

    if args.command == 'list':
        stations = api.get_water_level_stations()
        for loc in stations:
            print(f"{loc.get('Code', '')}: {loc.get('Naam', '')} ({loc.get('Lat', '')}, {loc.get('Lon', '')})")
    elif args.command == 'level':
        observations = api.get_latest_observations([args.station_code])
        if observations:
            for entry in observations:
                print(json.dumps(entry, indent=4, ensure_ascii=False))
        else:
            print(f"No observations for station {args.station_code}")
    elif args.command == 'feed':
        if args.connection_string:
            config_params = api.parse_connection_string(args.connection_string)
            kafka_bootstrap_servers = config_params.get('bootstrap.servers')
            kafka_topic = config_params.get('kafka_topic')
            sasl_username = config_params.get('sasl.username')
            sasl_password = config_params.get('sasl.password')
        else:
            kafka_bootstrap_servers = args.kafka_bootstrap_servers
            kafka_topic = args.kafka_topic
            sasl_username = args.sasl_username
            sasl_password = args.sasl_password

        if not kafka_bootstrap_servers:
            print("Error: Kafka bootstrap servers must be provided.")
            sys.exit(1)
        if not kafka_topic:
            print("Error: Kafka topic must be provided.")
            sys.exit(1)
        kafka_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
        }
        if sasl_username and sasl_password:
            kafka_config.update({
                'sasl.mechanisms': 'PLAIN',
                'security.protocol': 'SASL_SSL',
                'sasl.username': sasl_username,
                'sasl.password': sasl_password
            })
        api.feed_stations(kafka_config, kafka_topic, args.polling_interval, args.state_file)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
