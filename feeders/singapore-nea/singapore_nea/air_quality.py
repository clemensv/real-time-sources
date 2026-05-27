"""Air quality helpers for the Singapore NEA bridge."""

from datetime import datetime, timezone
import logging

import requests

from singapore_nea_producer_data import PM25Reading, PSIReading, Region
from singapore_nea_producer_kafka_producer.producer import SGGovNEAAirQualityEventProducer

logger = logging.getLogger(__name__)

NEA_AIR_QUALITY_BASE_URL = "https://api.data.gov.sg/v1/environment"


class NEAAirQualityAPI:
    """Client for Singapore NEA PSI and PM2.5 regional endpoints."""

    def __init__(self, base_url: str = NEA_AIR_QUALITY_BASE_URL, polling_interval: int = 3600):
        self.base_url = base_url
        self.polling_interval = polling_interval
        self.session = requests.Session()

    def _get_endpoint(self, endpoint: str) -> dict:
        response = self.session.get(f"{self.base_url}/{endpoint}", timeout=30)
        response.raise_for_status()
        return response.json()

    def get_psi(self) -> dict:
        """Fetch the PSI endpoint."""
        return self._get_endpoint("psi")

    def get_pm25(self) -> dict:
        """Fetch the PM2.5 endpoint."""
        return self._get_endpoint("pm25")

    def get_regions(self) -> dict[str, Region]:
        """Fetch air quality region metadata."""
        data = self.get_psi()
        return self.extract_regions(data)

    @staticmethod
    def extract_regions(data: dict) -> dict[str, Region]:
        """Extract region metadata from a PSI or PM2.5 response."""
        regions: dict[str, Region] = {}
        for entry in data.get("region_metadata", []):
            label_location = entry.get("label_location", {})
            region_name = entry.get("name")
            if not region_name:
                continue
            regions[region_name] = Region(
                region=region_name,
                latitude=float(label_location.get("latitude", 0.0)),
                longitude=float(label_location.get("longitude", 0.0)),
            )
        return regions


def _parse_iso_datetime(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def _reading_value(region_readings: dict, region: str):
    value = region_readings.get(region)
    return int(value) if value is not None else None


def fetch_and_send_regions(api: NEAAirQualityAPI, producer: SGGovNEAAirQualityEventProducer) -> int:
    """Fetch and emit region reference data."""
    regions = api.get_regions()
    for region_name, region in regions.items():
        producer.send_sg_gov_nea_air_quality_region(region_name, region, flush_producer=False)
    producer.producer.flush()
    logger.info("Sent %d air quality region reference events", len(regions))
    return len(regions)


def fetch_and_send_psi(
    api: NEAAirQualityAPI,
    producer: SGGovNEAAirQualityEventProducer,
    previous_psi: dict,
) -> int:
    """Fetch and emit PSI readings, deduplicated by region and timestamp."""
    data = api.get_psi()
    items = data.get("items", [])
    if not items:
        return 0

    item = items[0]
    timestamp = _parse_iso_datetime(item.get("timestamp"))
    update_timestamp = _parse_iso_datetime(item.get("update_timestamp"))
    readings = item.get("readings", {})
    regions = NEAAirQualityAPI.extract_regions(data)
    sent = 0

    for region_name in sorted(regions.keys()):
        reading_key = f"{region_name}:{timestamp.isoformat()}"
        if reading_key in previous_psi:
            continue
        psi_reading = PSIReading(
            region=region_name,
            timestamp=timestamp,
            update_timestamp=update_timestamp,
            psi_twenty_four_hourly=_reading_value(readings.get("psi_twenty_four_hourly", {}), region_name),
            o3_sub_index=_reading_value(readings.get("o3_sub_index", {}), region_name),
            pm10_sub_index=_reading_value(readings.get("pm10_sub_index", {}), region_name),
            pm10_twenty_four_hourly=_reading_value(
                readings.get("pm10_twenty_four_hourly", {}),
                region_name,
            ),
            pm25_sub_index=_reading_value(readings.get("pm25_sub_index", {}), region_name),
            pm25_twenty_four_hourly=_reading_value(
                readings.get("pm25_twenty_four_hourly", {}),
                region_name,
            ),
            co_sub_index=_reading_value(readings.get("co_sub_index", {}), region_name),
            co_eight_hour_max=_reading_value(readings.get("co_eight_hour_max", {}), region_name),
            so2_sub_index=_reading_value(readings.get("so2_sub_index", {}), region_name),
            so2_twenty_four_hourly=_reading_value(
                readings.get("so2_twenty_four_hourly", {}),
                region_name,
            ),
            no2_one_hour_max=_reading_value(readings.get("no2_one_hour_max", {}), region_name),
            o3_eight_hour_max=_reading_value(readings.get("o3_eight_hour_max", {}), region_name),
        )
        producer.send_sg_gov_nea_air_quality_psireading(
            region_name,
            psi_reading,
            flush_producer=False,
        )
        previous_psi[reading_key] = timestamp.isoformat()
        sent += 1

    producer.producer.flush()
    return sent


def fetch_and_send_pm25(
    api: NEAAirQualityAPI,
    producer: SGGovNEAAirQualityEventProducer,
    previous_pm25: dict,
) -> int:
    """Fetch and emit PM2.5 readings, deduplicated by region and timestamp."""
    data = api.get_pm25()
    items = data.get("items", [])
    if not items:
        return 0

    item = items[0]
    timestamp = _parse_iso_datetime(item.get("timestamp"))
    update_timestamp = _parse_iso_datetime(item.get("update_timestamp"))
    readings = item.get("readings", {}).get("pm25_one_hourly", {})
    regions = NEAAirQualityAPI.extract_regions(data)
    sent = 0

    for region_name in sorted(regions.keys()):
        reading_key = f"{region_name}:{timestamp.isoformat()}"
        if reading_key in previous_pm25:
            continue
        reading = PM25Reading(
            region=region_name,
            timestamp=timestamp,
            update_timestamp=update_timestamp,
            pm25_one_hourly=_reading_value(readings, region_name),
        )
        producer.send_sg_gov_nea_air_quality_pm25_reading(
            region_name,
            reading,
            flush_producer=False,
        )
        previous_pm25[reading_key] = timestamp.isoformat()
        sent += 1

    producer.producer.flush()
    return sent
