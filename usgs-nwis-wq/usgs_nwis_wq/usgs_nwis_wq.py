"""
USGS NWIS Water Quality Bridge

Polls the USGS Instantaneous Values Service for continuous water quality sensor
data (dissolved oxygen, pH, temperature, turbidity, specific conductance, nitrate)
and sends readings to a Kafka topic as CloudEvents.

API: https://waterservices.usgs.gov/nwis/iv/?format=json
Protocol: REST JSON (WaterML 2.0)
Auth: None (US Government public domain)
"""

import os
import json
import sys
import asyncio
import aiohttp
import html
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any, Set
from confluent_kafka import Producer

# pylint: disable=import-error, line-too-long
from usgs_nwis_wq_producer_data.usgs_nwis_wq_producer_data.monitoringsite import MonitoringSite
from usgs_nwis_wq_producer_data.usgs_nwis_wq_producer_data.waterqualityreading import WaterQualityReading
from usgs_nwis_wq_producer_kafka_producer.producer import (
    USGSWaterQualitySitesEventProducer,
    USGSWaterQualityReadingsEventProducer,
)
# pylint: enable=import-error, line-too-long

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Water quality parameter codes
WQ_PARAMETER_CODES = {
    "00010": "Water Temperature",
    "00300": "Dissolved Oxygen",
    "00400": "pH",
    "00095": "Specific Conductance",
    "63680": "Turbidity (FNU)",
    "00076": "Turbidity (NTU)",
    "99133": "Nitrate+Nitrite",
    "00480": "Salinity",
    "32295": "Fluorescent DOM (fDOM)",
    "32322": "Fluorescent DOM (fDOM)",
    "00094": "Specific Conductance (field)",
    "00299": "Dissolved Oxygen (percent)",
}

ALL_WQ_PARAM_CODES = ",".join(WQ_PARAMETER_CODES.keys())

STATE_CODES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC',
    'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA',
    'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV',
    'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW',
    'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA',
    'WA', 'WV', 'WI', 'WY'
]


class USGSWaterQualityPoller:
    """Polls USGS NWIS IV service for water quality data and sends to Kafka."""

    BASE_URL = "https://waterservices.usgs.gov/nwis/iv/"
    NO_DATA_VALUE = -999999.0

    def __init__(
        self,
        kafka_config: Optional[Dict[str, str]] = None,
        kafka_topic: Optional[str] = None,
        last_polled_file: Optional[str] = None,
        states: Optional[List[str]] = None,
        sites: Optional[List[str]] = None,
        parameter_codes: Optional[str] = None,
    ):
        """
        Initialize the water quality poller.

        Args:
            kafka_config: Kafka producer configuration dict.
            kafka_topic: Kafka topic name.
            last_polled_file: Path to persist last-polled timestamps.
            states: List of state codes to poll. Defaults to all states.
            sites: Specific site numbers to poll. Overrides states.
            parameter_codes: Comma-separated WQ parameter codes.
        """
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        self.states = states or STATE_CODES
        self.sites = sites
        self.parameter_codes = parameter_codes or ALL_WQ_PARAM_CODES

        if kafka_config is not None:
            producer = Producer(kafka_config)
            self.site_producer = USGSWaterQualitySitesEventProducer(producer, kafka_topic)
            self.readings_producer = USGSWaterQualityReadingsEventProducer(producer, kafka_topic)
        else:
            self.site_producer = None
            self.readings_producer = None

    @staticmethod
    def build_api_url(
        state_cd: Optional[str] = None,
        sites: Optional[List[str]] = None,
        parameter_codes: str = ALL_WQ_PARAM_CODES,
        period: str = "PT2H",
    ) -> str:
        """Build the USGS IV API URL for water quality parameters."""
        base = "https://waterservices.usgs.gov/nwis/iv/?format=json"
        if sites:
            base += f"&sites={','.join(sites)}"
        elif state_cd:
            base += f"&stateCd={state_cd}"
        base += f"&parameterCd={parameter_codes}"
        base += f"&period={period}"
        return base

    @staticmethod
    def parse_waterml_response(data: dict) -> Tuple[List[MonitoringSite], List[WaterQualityReading]]:
        """
        Parse a WaterML 2.0 JSON response into site metadata and readings.

        Args:
            data: The parsed JSON response from the USGS IV API.

        Returns:
            Tuple of (list of MonitoringSite, list of WaterQualityReading).
        """
        sites_list: List[MonitoringSite] = []
        readings_list: List[WaterQualityReading] = []
        seen_sites: Set[str] = set()

        ts_response = data.get("value", {})
        time_series_list = ts_response.get("timeSeries", [])

        for ts in time_series_list:
            source_info = ts.get("sourceInfo", {})
            variable = ts.get("variable", {})
            values_sets = ts.get("values", [])

            # Extract site info
            site_codes = source_info.get("siteCode", [])
            site_number = site_codes[0].get("value", "") if site_codes else ""
            agency_code = site_codes[0].get("agencyCode", "USGS") if site_codes else "USGS"
            site_name = source_info.get("siteName", "")

            geo = source_info.get("geoLocation", {}).get("geogLocation", {})
            latitude = geo.get("latitude")
            longitude = geo.get("longitude")

            # Extract site properties
            site_type = None
            state_code = None
            county_code = None
            huc_code = None
            for prop in source_info.get("siteProperty", []):
                prop_name = prop.get("name", "")
                prop_value = prop.get("value", "")
                if prop_name == "siteTypeCd":
                    site_type = prop_value
                elif prop_name == "stateCd":
                    state_code = prop_value
                elif prop_name == "countyCd":
                    county_code = prop_value
                elif prop_name == "hucCd":
                    huc_code = prop_value

            # Build MonitoringSite if not seen
            if site_number and site_number not in seen_sites:
                seen_sites.add(site_number)
                site = MonitoringSite(
                    site_number=site_number,
                    site_name=site_name,
                    agency_code=agency_code,
                    latitude=latitude,
                    longitude=longitude,
                    site_type=site_type,
                    state_code=state_code,
                    county_code=county_code,
                    huc_code=huc_code,
                )
                sites_list.append(site)

            # Extract variable info
            var_codes = variable.get("variableCode", [])
            parameter_code = var_codes[0].get("value", "") if var_codes else ""
            parameter_name = html.unescape(variable.get("variableDescription", variable.get("variableName", "")))
            unit_code = variable.get("unit", {}).get("unitCode", "")
            no_data_value = variable.get("noDataValue", USGSWaterQualityPoller.NO_DATA_VALUE)

            # Extract timezone info
            tz_info = source_info.get("timeZoneInfo", {})
            default_tz_offset = tz_info.get("defaultTimeZone", {}).get("zoneOffset", "+00:00")
            dst_tz_offset = tz_info.get("daylightSavingsTimeZone", {}).get("zoneOffset")
            uses_dst = tz_info.get("siteUsesDaylightSavingsTime", False)

            for values_set in values_sets:
                for val_entry in values_set.get("value", []):
                    raw_value = val_entry.get("value")
                    dt_str = val_entry.get("dateTime", "")
                    qualifiers = val_entry.get("qualifiers", [])

                    if not dt_str:
                        continue

                    # Parse the datetime - it includes timezone offset
                    try:
                        dt = datetime.fromisoformat(dt_str)
                    except ValueError:
                        logger.warning("Could not parse datetime: %s", dt_str)
                        continue

                    # Convert to UTC
                    if dt.tzinfo is not None:
                        dt_utc = dt.astimezone(timezone.utc)
                    else:
                        dt_utc = dt.replace(tzinfo=timezone.utc)

                    # Parse value, handle noDataValue and non-numeric
                    value: Optional[float] = None
                    if raw_value is not None:
                        try:
                            v = float(raw_value)
                            if v != no_data_value:
                                value = v
                        except (ValueError, TypeError):
                            pass

                    qualifier = qualifiers[0] if qualifiers else None

                    reading = WaterQualityReading(
                        site_number=site_number,
                        site_name=site_name,
                        parameter_code=parameter_code,
                        parameter_name=parameter_name,
                        value=value,
                        unit=unit_code,
                        qualifier=qualifier,
                        date_time=dt_utc.isoformat(),
                    )
                    readings_list.append(reading)

        return sites_list, readings_list

    async def fetch_json(self, url: str) -> Optional[dict]:
        """Fetch JSON from the USGS API."""
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            try:
                async with asyncio.timeout(60):
                    async with session.get(url) as response:
                        response.raise_for_status()
                        return await response.json(content_type=None)
            except asyncio.TimeoutError:
                logger.error("Request timed out for URL: %s", url)
                return None
            except aiohttp.ClientError as e:
                logger.error("HTTP error: %s for URL: %s", e, url)
                return None

    def load_last_polled_times(self) -> Dict:
        """Load persisted last-polled timestamps."""
        if self.last_polled_file and os.path.exists(self.last_polled_file):
            with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    logger.error("Error decoding last polled times file")
                    return {}
        return {}

    def save_last_polled_times(self, last_polled: Dict) -> None:
        """Save last-polled timestamps to file."""
        if self.last_polled_file:
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(last_polled, f)

    def is_duplicate(self, last_polled: Dict, site_number: str, parameter_code: str, date_time: str) -> bool:
        """Check if a reading is a duplicate based on stored timestamps."""
        key = f"{site_number}/{parameter_code}"
        return last_polled.get(key, "") >= date_time

    def update_last_polled(self, last_polled: Dict, site_number: str, parameter_code: str, date_time: str) -> None:
        """Update the last polled timestamp for a site/parameter pair."""
        key = f"{site_number}/{parameter_code}"
        if last_polled.get(key, "") < date_time:
            last_polled[key] = date_time

    async def poll_and_send(self) -> None:
        """Main polling loop: fetches water quality data and sends to Kafka."""
        last_polled = self.load_last_polled_times()

        while True:
            start_time = datetime.now(timezone.utc)
            total_sites = 0
            total_readings = 0

            if self.sites:
                # Poll specific sites
                url = self.build_api_url(sites=self.sites, parameter_codes=self.parameter_codes)
                data = await self.fetch_json(url)
                if data:
                    sites, readings = self.parse_waterml_response(data)
                    total_sites += len(sites)

                    for site in sites:
                        if self.site_producer:
                            self.site_producer.send_usgs_water_quality_sites_monitoring_site(
                                _source_uri=self.BASE_URL,
                                _site_number=site.site_number,
                                data=site,
                                flush_producer=False,
                            )

                    for reading in readings:
                        if not self.is_duplicate(last_polled, reading.site_number, reading.parameter_code, reading.date_time):
                            if self.readings_producer:
                                self.readings_producer.send_usgs_water_quality_readings_water_quality_reading(
                                    _source_uri=self.BASE_URL,
                                    _site_number=reading.site_number,
                                    _parameter_code=reading.parameter_code,
                                    data=reading,
                                    flush_producer=False,
                                )
                            self.update_last_polled(last_polled, reading.site_number, reading.parameter_code, reading.date_time)
                            total_readings += 1

                    if self.site_producer:
                        self.site_producer.producer.flush()
                    if self.readings_producer:
                        self.readings_producer.producer.flush()
            else:
                # Poll by state
                for state_code in self.states:
                    url = self.build_api_url(state_cd=state_code, parameter_codes=self.parameter_codes)
                    data = await self.fetch_json(url)
                    if not data:
                        continue

                    sites, readings = self.parse_waterml_response(data)
                    total_sites += len(sites)

                    for site in sites:
                        if self.site_producer:
                            self.site_producer.send_usgs_water_quality_sites_monitoring_site(
                                _source_uri=self.BASE_URL,
                                _site_number=site.site_number,
                                data=site,
                                flush_producer=False,
                            )

                    for reading in readings:
                        if not self.is_duplicate(last_polled, reading.site_number, reading.parameter_code, reading.date_time):
                            if self.readings_producer:
                                self.readings_producer.send_usgs_water_quality_readings_water_quality_reading(
                                    _source_uri=self.BASE_URL,
                                    _site_number=reading.site_number,
                                    _parameter_code=reading.parameter_code,
                                    data=reading,
                                    flush_producer=False,
                                )
                            self.update_last_polled(last_polled, reading.site_number, reading.parameter_code, reading.date_time)
                            total_readings += 1

                    if self.site_producer:
                        self.site_producer.producer.flush()
                    if self.readings_producer:
                        self.readings_producer.producer.flush()

                    logger.info("State %s: %d sites, %d new readings", state_code, len(sites), sum(
                        1 for r in readings if not self.is_duplicate({}, r.site_number, r.parameter_code, r.date_time)
                    ))

            self.save_last_polled_times(last_polled)
            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            logger.info("Poll complete: %d sites, %d new readings in %.1fs", total_sites, total_readings, elapsed)

            # Wait before next poll (5 minutes)
            await asyncio.sleep(300)


def parse_connection_string(connection_string: str) -> Tuple[Dict[str, str], str]:
    """Parse Event Hubs / Fabric connection string into Kafka config + topic."""
    config_dict: Dict[str, str] = {}
    kafka_topic = None

    # Check for simple BootstrapServer format
    parts = {}
    for part in connection_string.split(';'):
        part = part.strip()
        if '=' in part:
            key, _, value = part.partition('=')
            parts[key.strip()] = value.strip().strip('"')

    if 'BootstrapServer' in parts:
        config_dict['bootstrap.servers'] = parts['BootstrapServer']
        kafka_topic = parts.get('EntityPath', '')
        enable_tls = os.environ.get('KAFKA_ENABLE_TLS', 'true').lower()
        if enable_tls == 'false':
            config_dict['security.protocol'] = 'PLAINTEXT'
    elif 'Endpoint' in parts:
        endpoint = parts['Endpoint'].replace('sb://', '').rstrip('/')
        config_dict['bootstrap.servers'] = f"{endpoint}:9093"
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanisms'] = 'PLAIN'
        config_dict['sasl.username'] = '$ConnectionString'
        config_dict['sasl.password'] = connection_string.strip()
        kafka_topic = parts.get('EntityPath', '')

    return config_dict, kafka_topic


def main():
    """Entry point for the USGS NWIS Water Quality bridge."""
    parser = argparse.ArgumentParser(description="USGS NWIS Water Quality bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    # feed command
    feed_parser = subparsers.add_parser("feed", help="Poll and send water quality data to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str, help="Kafka bootstrap servers")
    feed_parser.add_argument("--kafka-topic", type=str, help="Kafka topic")
    feed_parser.add_argument("--sasl-username", type=str, help="SASL username")
    feed_parser.add_argument("--sasl-password", type=str, help="SASL password")
    feed_parser.add_argument("--connection-string", type=str, help="Event Hubs connection string")
    feed_parser.add_argument("--states", type=str, help="Comma-separated state codes (default: all)")
    feed_parser.add_argument("--sites", type=str, help="Comma-separated USGS site numbers")
    feed_parser.add_argument("--parameter-codes", type=str, help="Comma-separated parameter codes")

    args = parser.parse_args()

    if not args.command:
        args.command = "feed"

    connection_string = args.connection_string if hasattr(args, 'connection_string') else None
    connection_string = connection_string or os.environ.get("CONNECTION_STRING", "")

    kafka_bootstrap_servers = getattr(args, 'kafka_bootstrap_servers', None) or os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "")
    kafka_topic = getattr(args, 'kafka_topic', None) or os.environ.get("KAFKA_TOPIC", "")
    sasl_username = getattr(args, 'sasl_username', None) or os.environ.get("SASL_USERNAME", "")
    sasl_password = getattr(args, 'sasl_password', None) or os.environ.get("SASL_PASSWORD", "")

    last_polled_file = os.environ.get("USGS_WQ_LAST_POLLED_FILE", "/mnt/state/usgs_wq_last_polled.json")
    states_arg = getattr(args, 'states', None) or os.environ.get("USGS_WQ_STATES", "")
    sites_arg = getattr(args, 'sites', None) or os.environ.get("USGS_WQ_SITES", "")
    param_codes = getattr(args, 'parameter_codes', None) or os.environ.get("USGS_WQ_PARAMETER_CODES", "")

    kafka_config = None
    if connection_string:
        kafka_config, topic_from_cs = parse_connection_string(connection_string)
        if not kafka_topic:
            kafka_topic = topic_from_cs
    elif kafka_bootstrap_servers:
        kafka_config = {
            'bootstrap.servers': kafka_bootstrap_servers,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
        }

    if not kafka_config:
        logger.error("No Kafka configuration provided. Set CONNECTION_STRING or KAFKA_BOOTSTRAP_SERVERS.")
        sys.exit(1)

    states = [s.strip() for s in states_arg.split(",") if s.strip()] if states_arg else None
    sites = [s.strip() for s in sites_arg.split(",") if s.strip()] if sites_arg else None

    poller = USGSWaterQualityPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=last_polled_file,
        states=states,
        sites=sites,
        parameter_codes=param_codes or None,
    )

    asyncio.run(poller.poll_and_send())


if __name__ == "__main__":
    main()
