"""
USGS Data Poller
Polls USGS Instantaneous Values Service data and sends it to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, List
import argparse
import requests

# Import data classes generated from the schema
from usgs_iv_producer_data.usgs.instantaneousvalues.streamflow import Streamflow
from usgs_iv_producer_data.usgs.instantaneousvalues.gageheight import GageHeight
from usgs_iv_producer_data.usgs.instantaneousvalues.watertemperature import WaterTemperature
from usgs_iv_producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen
from usgs_iv_producer_data.usgs.instantaneousvalues.ph import pH
from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance
from usgs_iv_producer_data.usgs.instantaneousvalues.turbidity import Turbidity
from usgs_iv_producer_data.usgs.instantaneousvalues.producer_client import USGSInstantaneousValuesEventProducer


class USGSDataPoller:
    """
    Class to poll USGS Instantaneous Values Service data and send it to a Kafka topic.
    """
    BASE_URL = "https://waterservices.usgs.gov/nwis/iv/"

    PARAMETERS = {
        "Streamflow": "00060",
        "GageHeight": "00065",
        "WaterTemperature": "00010",
        "DissolvedOxygen": "00300",
        "pH": "00400",
        "SpecificConductance": "00095",
        "Turbidity": "00076"
    }

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str, site: str = None):
        """
        Initialize the USGSDataPoller class.

        Args:
            kafka_config (Dict[str, str]): Kafka configuration settings.
            kafka_topic (str): Kafka topic to send messages to.
            last_polled_file (str): File to store the last polled times for each site and parameter.
            site (str): Specific USGS site number to poll. If None, poll all sites.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.producer = USGSInstantaneousValuesEventProducer(kafka_config, kafka_topic)
        self.site = site

    def fetch_sites(self) -> List[str]:
        """
        Fetch a list of USGS site numbers.

        Returns:
            List[str]: List of site numbers.
        """
        if self.site:
            return [self.site]
        else:
            print("No site specified. Please provide a site number using the '--site' argument.")
            sys.exit(1)

    def poll_usgs_api(self, parameter_code: str, site_no: str, last_polled_time: datetime) -> dict:
        """
        Poll the USGS Instantaneous Values Service for new data.

        Args:
            parameter_code (str): The parameter code to poll.
            site_no (str): The USGS site number.
            last_polled_time (datetime): The last time data was polled.

        Returns:
            dict: The JSON response data.
        """
        params = {
            'format': 'json',
            'sites': site_no,
            'parameterCd': parameter_code,
            'startDT': last_polled_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'endDT': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
            'siteStatus': 'all'
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as err:
            print(f"Error fetching data for site {site_no}: {err}")
            return {}

    def load_last_polled_times(self) -> Dict:
        """
        Load the last polled times from a file.

        Returns:
            Dict: The last polled times for each site and parameter.
        """
        if os.path.exists(self.last_polled_file):
            with open(self.last_polled_file, 'r', encoding='utf-8') as file:
                saved_times = json.load(file)
                last_polled_times = {}
                for parameter, sites in saved_times.items():
                    for site_no, timestamp in sites.items():
                        if parameter not in last_polled_times:
                            last_polled_times[parameter] = {}
                        last_polled_times[parameter][site_no] = datetime.fromisoformat(timestamp)
                return last_polled_times
        return {}

    def save_last_polled_times(self, last_polled_times: Dict):
        """
        Save the last polled times to a file.

        Args:
            last_polled_times (Dict): The last polled times for each site and parameter.
        """
        # Convert all datetime objects to string for serialization
        saved_times = {}
        for parameter, sites in last_polled_times.items():
            for site_no, timestamp in sites.items():
                if parameter not in saved_times:
                    saved_times[parameter] = {}
                saved_times[parameter][site_no] = timestamp.isoformat()
        with open(self.last_polled_file, 'w', encoding='utf-8') as file:
            json.dump(saved_times, file)

    def poll_and_send(self):
        """
        Poll USGS data and send it to Kafka.
        """
        last_polled_times = self.load_last_polled_times()
        sites = self.fetch_sites()

        while True:
            for site_no in sites:
                for parameter_name, parameter_code in self.PARAMETERS.items():
                    print(f"Polling {parameter_name} data for site {site_no}:", end=' ')
                    last_polled_time = last_polled_times.get(parameter_name, {}).get(
                        site_no, datetime.now(timezone.utc) - timedelta(hours=1))
                    data = self.poll_usgs_api(parameter_code, site_no, last_polled_time)
                    time_series = data.get('value', {}).get('timeSeries', [])
                    total_values = sum(len(ts.get('values', [])[0].get('value', [])) for ts in time_series)
                    print(f"{total_values} new records found.")

                    max_timestamp = last_polled_time
                    for ts in time_series:
                        values = ts.get('values', [])
                        for value_entry in values:
                            value_list = value_entry.get('value', [])
                            for value_dict in value_list:
                                timestamp = datetime.strptime(value_dict['dateTime'], '%Y-%m-%dT%H:%M:%S.%f%z')
                                if timestamp > max_timestamp:
                                    max_timestamp = timestamp
                                qualifiers = value_dict.get('qualifiers', [])
                                value = float(value_dict.get('value', 'NaN'))

                                # Map data to corresponding data classes
                                if parameter_name == "Streamflow":
                                    streamflow = Streamflow(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_streamflow(
                                        streamflow, site_no, flush_producer=False)
                                elif parameter_name == "GageHeight":
                                    gage_height = GageHeight(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_gageheight(
                                        gage_height, site_no, flush_producer=False)
                                elif parameter_name == "WaterTemperature":
                                    water_temperature = WaterTemperature(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_watertemperature(
                                        water_temperature, site_no, flush_producer=False)
                                elif parameter_name == "DissolvedOxygen":
                                    dissolved_oxygen = DissolvedOxygen(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_dissolvedoxygen(
                                        dissolved_oxygen, site_no, flush_producer=False)
                                elif parameter_name == "pH":
                                    ph_value = pH(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_ph(
                                        ph_value, site_no, flush_producer=False)
                                elif parameter_name == "SpecificConductance":
                                    specific_conductance = SpecificConductance(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_specificconductance(
                                        specific_conductance, site_no, flush_producer=False)
                                elif parameter_name == "Turbidity":
                                    turbidity = Turbidity(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers
                                    )
                                    self.producer.send_usgs_instantaneousvalues_turbidity(
                                        turbidity, site_no, flush_producer=False)
                    self.producer.producer.flush()
                    if max_timestamp > last_polled_time:
                        if parameter_name not in last_polled_times:
                            last_polled_times[parameter_name] = {}
                        last_polled_times[parameter_name][site_no] = max_timestamp
                        self.save_last_polled_times(last_polled_times)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string (str): The connection string.

    Returns:
        Dict[str, str]: Extracted connection parameters.
    """
    config_dict = {
        'sasl.username': '$ConnectionString',
        'sasl.password': connection_string.strip(),
    }
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    return config_dict


def main():
    """
    Main function to parse arguments and start the USGS data poller.
    """
    parser = argparse.ArgumentParser(description="USGS Data Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store the last polled times for each site and parameter")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    parser.add_argument('--site', type=str,
                        help='USGS site number to poll data for.')

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('USGS_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.usgs_last_polled.json')

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    # Check if required parameters are provided
    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)
    if not sasl_username or not sasl_password:
        print("Error: SASL username and password must be provided either through the command line or connection string.")
        sys.exit(1)

    kafka_config = {
        'bootstrap.servers': kafka_bootstrap_servers,
        'sasl.mechanisms': 'PLAIN',
        'security.protocol': 'SASL_SSL',
        'sasl.username': sasl_username,
        'sasl.password': sasl_password
    }

    poller = USGSDataPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
        site=args.site
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
