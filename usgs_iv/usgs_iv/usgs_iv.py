"""
USGS Data Poller
Polls USGS Instantaneous Values Service data and sends it to a Kafka topic using SASL PLAIN authentication.
"""

import os
import json
import sys
import asyncio
import aiohttp
import re
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, AsyncIterator, Any
from zoneinfo import ZoneInfo
import argparse
from requests import session, RequestException
from confluent_kafka import Producer

# Import data classes generated from the schema
# pylint: disable=import-error
from usgs_iv_producer_data.usgs.instantaneousvalues.streamflow import Streamflow
from usgs_iv_producer_data.usgs.instantaneousvalues.gageheight import GageHeight
from usgs_iv_producer_data.usgs.instantaneousvalues.watertemperature import WaterTemperature
from usgs_iv_producer_data.usgs.instantaneousvalues.dissolvedoxygen import DissolvedOxygen
from usgs_iv_producer_data.usgs.instantaneousvalues.ph import PH
from usgs_iv_producer_data.usgs.instantaneousvalues.specificconductance import SpecificConductance
from usgs_iv_producer_data.usgs.instantaneousvalues.turbidity import Turbidity
from usgs_iv_producer_data.usgs.sites import Site
# pylint: enable=import-error

from usgs_iv_producer_kafka_producer.producer import USGSSitesEventProducer, USGSInstantaneousValuesEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

state_codes = [
    'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM',
    'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
    'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
    'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW',
    'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA',
    'WA', 'WV', 'WI', 'WY'
]

# Mapping USGS timezone abbreviations to IANA timezones
usgs_tz_map = {
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "MST": "America/Denver",    # or America/Phoenix depending on region
    "MDT": "America/Denver",
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "AKST": "America/Anchorage",
    "AKDT": "America/Anchorage",
    "HST": "Pacific/Honolulu",
    "ChST": "Pacific/Guam",
    "SST": "Pacific/Pago_Pago",
    "AST": "America/Puerto_Rico"
}


class USGSDataPoller:
    """
    Class to poll USGS Instantaneous Values Service data and send it to a Kafka topic.
    """
    BASE_URL = "https://waterservices.usgs.gov/nwis/iv/"

    PARAMETERS = {
        "00045": "Precipitation",
        "00060": "Streamflow",
        "00065": "GageHeight",
        "00010": "WaterTemperature",
        "00300": "DissolvedOxygen",
        "00400": "pH",
        "00095": "SpecificConductance",
        "00076": "Turbidity"
    }

    TS_PARAM_REGEX = re.compile(r'^(\d+)_(\d{5})$')

    def __init__(self, kafka_config: Dict[str, str] = None, kafka_topic: str = None, last_polled_file: str = None, site: str = None):
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
        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.site_producer = USGSSitesEventProducer(producer, kafka_topic)
            self.values_producer = USGSInstantaneousValuesEventProducer(producer, kafka_topic)

        self.site = site

    async def get_data_by_state(self, state_code: str) -> AsyncIterator[List[Dict[str, Any]]]:
        """
        Asynchronously fetches data for a given state code from the USGS service and yields arrays of records.
        Each record is a dictionary with key/value pairs as found in the RDB response.

        Args:
            state_code (str): The USPS state code (e.g., 'NY' for New York).

        Yields:
            AsyncIterator[List[Dict[str, Any]]]: An async iterator of lists of records (dictionaries).
        """

        url = f'https://waterservices.usgs.gov/nwis/iv/?stateCd={state_code}&format=rdb&modifiedSince=PT2H'

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            try:
                async with asyncio.timeout(30):  # Set timeout to 30 seconds
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.text()
            except asyncio.TimeoutError:
                print(f"Request timed out for state {state_code}")
                return
            except aiohttp.ClientError as e:
                print(f"HTTP error occurred: {e}")
                return

        # Process the RDB data
        lines = data.splitlines()
        site_sections = []
        current_site_lines = []
        in_data_section = False

        for line in lines:
            if line.startswith('# Data provided for site'):
                # Start of a new site section
                if current_site_lines:
                    site_sections.append(current_site_lines)
                    current_site_lines = []
                current_site_lines.append(line)
                in_data_section = False
            elif line.startswith('#'):
                # Comment line, add to current site lines
                current_site_lines.append(line)
            elif line.strip() == '':
                # Empty line, ignore
                continue
            else:
                # Data or header line
                current_site_lines.append(line)
                in_data_section = True

        # Add the last site section
        if current_site_lines:
            site_sections.append(current_site_lines)

        # Now process each site section
        for site_lines in site_sections:
            records = []
            headers = []
            types = []
            data_started = False
            site_no = None

            for line in site_lines:
                if line.startswith('# Data provided for site'):
                    # Extract site number
                    parts = line.split()
                    if len(parts) >= 5:
                        site_no = parts[5]
                elif not line.startswith('#') and not data_started:
                    # Header line
                    headers = line.strip().split('\t')
                    data_started = True
                elif data_started and not types:
                    # Data types line
                    types = line.strip().split('\t')
                elif data_started and types:
                    # Data line
                    fields = line.strip().split('\t')
                    record = dict(zip(headers, fields))
                    records.append(record)

            if records:
                yield records

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

    async def poll_and_send(self):
        """
        Poll USGS data and send it to Kafka.
        """

        stations_sent = False
        last_polled_times = self.load_last_polled_times()
        while True:
            for state_code in state_codes:
                if not stations_sent:
                    async for site in self.get_sites_in_state(state_code):
                        await self.site_producer.send_usgs_sites_site(_source_uri=self.BASE_URL, data=site, flush_producer=False)
                    self.site_producer.producer.flush()

                total_records = 0
                total_precipitation = 0
                total_streamflow = 0
                total_gage_height = 0
                total_water_temperature = 0
                total_dissolved_oxygen = 0
                total_ph = 0
                total_specific_conductance = 0
                total_turbidity = 0

                async for records in self.get_data_by_state(state_code):
                    for record in records:
                        total_records += 1
                        ts = datetime.fromisoformat(record.get('datetime', None))
                        tz = record.get('tz_cd', None)
                        site_no = record.get('site_no', None)
                        agency_cd = record.get('agency_cd', None)
                        # map US timezone codes to offsets
                        timestamp = ts.replace(tzinfo=ZoneInfo(usgs_tz_map.get(tz, 'UTC')))

                        for k, value in record.items():
                            # if the key matches TS_PARAM_REGEX, extract the parameter name and site number
                            match = self.TS_PARAM_REGEX.match(k)
                            if match:
                                parameter_name = self.PARAMETERS.get(match.group(2), None)
                                last_polled_time = last_polled_times.get(parameter_name, {}).get(
                                    site_no, datetime.now(timezone.utc) - timedelta(hours=2))
                                if timestamp <= last_polled_time:
                                    continue
                                max_timestamp = timestamp
                                qualifiers = record.get(k+'_cd', None)
                                # Map data to corresponding data classes
                                if parameter_name == "Precipitation" and value:
                                    total_precipitation += 1
                                    precipitation = Streamflow(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_precipitation(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=precipitation, flush_producer=False)
                                elif parameter_name == "Streamflow" and value:
                                    total_streamflow += 1
                                    streamflow = Streamflow(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_streamflow(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=streamflow, flush_producer=False)
                                elif parameter_name == "GageHeight" and value:
                                    total_gage_height += 1
                                    gage_height = GageHeight(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_gage_height(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=gage_height, flush_producer=False)
                                elif parameter_name == "WaterTemperature" and value and value != 'Dis':
                                    total_water_temperature += 1
                                    water_temperature = WaterTemperature(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_water_temperature(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=water_temperature, flush_producer=False)
                                elif parameter_name == "DissolvedOxygen" and value:
                                    total_dissolved_oxygen += 1
                                    dissolved_oxygen = DissolvedOxygen(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_dissolved_oxygen(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=dissolved_oxygen, flush_producer=False)
                                elif parameter_name == "pH" and value:
                                    total_ph += 1
                                    ph_value = PH(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_p_h(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=ph_value, flush_producer=False)
                                elif parameter_name == "SpecificConductance" and value:
                                    total_specific_conductance += 1
                                    specific_conductance = SpecificConductance(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_specific_conductance(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=specific_conductance, flush_producer=False)
                                elif parameter_name == "Turbidity" and value:
                                    total_turbidity += 1
                                    turbidity = Turbidity(
                                        site_no=site_no,
                                        datetime=timestamp.isoformat(),
                                        value=value,
                                        qualifiers=qualifiers,
                                        parameter_cd=match.group(2),
                                        timeseries_cd=match.group(1)
                                    )
                                    await self.values_producer.send_usgs_instantaneous_values_turbidity(
                                        _source_uri=self.BASE_URL, _agency_cd=agency_cd, _site_no=site_no, _datetime=timestamp.isoformat(), _parameter_cd=match.group(2), _timeseries_cd=match.group(1),
                                        data=turbidity, flush_producer=False)
                                else:
                                    continue
                                if max_timestamp > last_polled_time:
                                    if parameter_name not in last_polled_times:
                                        last_polled_times[parameter_name] = {}
                                    last_polled_times[parameter_name][site_no] = max_timestamp
                    self.values_producer.producer.flush()
                    self.save_last_polled_times(last_polled_times)
                logger.info("Processed %d records for state %s", total_records, state_code)
                logger.info("Streamflow: %d, GageHeight: %d, WaterTemperature: %d, DissolvedOxygen: %d, pH: %d, SpecificConductance: %d, Turbidity: %d",
                            total_streamflow, total_gage_height, total_water_temperature, total_dissolved_oxygen, total_ph, total_specific_conductance, total_turbidity)
            stations_sent = True

    async def get_sites_in_state(self, state_code: str) -> AsyncIterator[Site]:
        """Get all sites in a state."""
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            url = f'https://waterservices.usgs.gov/nwis/site/?format=rdb&stateCd={state_code}'
            async with session.get(url) as response:
                data = await response.text()

            lines = data.splitlines()
            data_lines = [line for line in lines if not line.startswith('#') and line.strip() != '']

            if not data_lines:
                return

            logger.debug("Processing data for state %s, %d lines", state_code, len(data_lines))

            header_line = data_lines[0]
            headers = header_line.split('\t')
            data_lines = data_lines[2:]  # Skip header and types lines

            def parse_float(s):
                try:
                    return float(s)
                except (ValueError, TypeError):
                    return None

            for line in data_lines:
                fields = line.split('\t')
                site_data = dict(zip(headers, fields))
                site = Site(
                    agency_cd=site_data.get('agency_cd', ''),
                    site_no=site_data.get('site_no', ''),
                    station_nm=site_data.get('station_nm', ''),
                    site_tp_cd=site_data.get('site_tp_cd', ''),
                    dec_lat_va=parse_float(site_data.get('dec_lat_va', '')),
                    dec_long_va=parse_float(site_data.get('dec_long_va', '')),
                    coord_acy_cd=site_data.get('coord_acy_cd', ''),
                    dec_coord_datum_cd=site_data.get('dec_coord_datum_cd', ''),
                    alt_va=parse_float(site_data.get('alt_va', '')),
                    alt_acy_va=parse_float(site_data.get('alt_acy_va', '')),
                    alt_datum_cd=site_data.get('alt_datum_cd', ''),
                )
                yield site


    async def get_all_sites(self) -> AsyncIterator[Site]:
        """Get all sites in the US."""
        poller = USGSDataPoller()

        for state_code in state_codes:
            async for site in poller.get_sites_in_state(state_code):
                yield site


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




async def print_site(site: Site):
    """Print a site."""
    print(f"Site {site.site_no}: {site.station_nm}")


async def run_get_sites_in_state(state_code: str):
    """ Get the sites in a state. """
    client = USGSDataPoller()
    async for site in client.get_sites_in_state(state_code):
        await print_site(site)


async def run_get_all_sites():
    """ Get all sites in the US. """
    client = USGSDataPoller()
    async for site in client.get_all_sites():
        await print_site(site)


def main():
    """
    Main function to parse arguments and start the USGS data poller.
    """
    parser = argparse.ArgumentParser(description="USGS Data Poller")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")
    feed_parser = subparsers.add_parser('feed', help="Poll USGS data and feed it to Kafka")
    feed_parser.add_argument('--last-polled-file', type=str,
                             help="File to store the last polled times for each site and parameter")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str,
                             help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument('--kafka-topic', type=str,
                             help="Kafka topic to send messages to")
    feed_parser.add_argument('--sasl-username', type=str,
                             help="Username for SASL PLAIN authentication")
    feed_parser.add_argument('--sasl-password', type=str,
                             help="Password for SASL PLAIN authentication")
    feed_parser.add_argument('--connection-string', type=str,
                             help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    feed_parser.add_argument('--site', type=str,
                             help='USGS site number to poll data for.')

    sites_parser = subparsers.add_parser('sites', help="List USGS sites")
    sites_parser.add_argument('--state', type=str, help='USGS state code to poll sites for.', required=False)

    params_parser = subparsers.add_parser('params', help="List USGS parameters")
    params_parser.add_argument('--site', type=str, help='USGS site number to poll data for.')

    args = parser.parse_args()

    if args.subcommand == 'sites':
        if args.state:
            asyncio.run(run_get_sites_in_state(args.state))
        else:
            asyncio.run(run_get_all_sites())
    elif args.subcommand == 'params':
        params = USGSDataPoller.PARAMETERS
        print(params)
    elif args.subcommand == 'feed':
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

        asyncio.run(poller.poll_and_send())


if __name__ == "__main__":
    main()
