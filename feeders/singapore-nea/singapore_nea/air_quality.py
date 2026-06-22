"""Air quality helpers for the Singapore NEA bridge (Kafka transport)."""

import logging

from singapore_nea_producer_data import PM25Reading, PSIReading, Region
from singapore_nea_producer_kafka_producer.producer import SGGovNEAAirQualityEventProducer

from singapore_nea_core import (
    NEAAirQualityAPI,
    fetch_psi_readings,
    fetch_pm25_readings,
)

logger = logging.getLogger(__name__)


def fetch_and_send_regions(api: NEAAirQualityAPI, producer: SGGovNEAAirQualityEventProducer) -> int:
    """Fetch and emit region reference data."""
    region_data = api.get_regions()
    for region_name, rd in region_data.items():
        region = Region(
            region=rd.region,
            latitude=rd.latitude,
            longitude=rd.longitude,
        )
        producer.send_sg_gov_nea_air_quality_region(region_name, region, flush_producer=False)
    producer.producer.flush()
    logger.info("Sent %d air quality region reference events", len(region_data))
    return len(region_data)


def fetch_and_send_psi(
    api: NEAAirQualityAPI,
    producer: SGGovNEAAirQualityEventProducer,
    previous_psi: dict,
) -> int:
    """Fetch and emit PSI readings, deduplicated by region and timestamp."""
    readings = fetch_psi_readings(api, previous_psi)
    for psi_data in readings:
        psi_reading = PSIReading(
            region=psi_data.region,
            timestamp=psi_data.timestamp,
            update_timestamp=psi_data.update_timestamp,
            psi_twenty_four_hourly=psi_data.psi_twenty_four_hourly,
            o3_sub_index=psi_data.o3_sub_index,
            pm10_sub_index=psi_data.pm10_sub_index,
            pm10_twenty_four_hourly=psi_data.pm10_twenty_four_hourly,
            pm25_sub_index=psi_data.pm25_sub_index,
            pm25_twenty_four_hourly=psi_data.pm25_twenty_four_hourly,
            co_sub_index=psi_data.co_sub_index,
            co_eight_hour_max=psi_data.co_eight_hour_max,
            so2_sub_index=psi_data.so2_sub_index,
            so2_twenty_four_hourly=psi_data.so2_twenty_four_hourly,
            no2_one_hour_max=psi_data.no2_one_hour_max,
            o3_eight_hour_max=psi_data.o3_eight_hour_max,
        )
        producer.send_sg_gov_nea_air_quality_psireading(
            psi_data.region, psi_reading, flush_producer=False
        )
    producer.producer.flush()
    return len(readings)


def fetch_and_send_pm25(
    api: NEAAirQualityAPI,
    producer: SGGovNEAAirQualityEventProducer,
    previous_pm25: dict,
) -> int:
    """Fetch and emit PM2.5 readings, deduplicated by region and timestamp."""
    readings = fetch_pm25_readings(api, previous_pm25)
    for pm25_data in readings:
        reading = PM25Reading(
            region=pm25_data.region,
            timestamp=pm25_data.timestamp,
            update_timestamp=pm25_data.update_timestamp,
            pm25_one_hourly=pm25_data.pm25_one_hourly,
        )
        producer.send_sg_gov_nea_air_quality_pm25_reading(
            pm25_data.region, reading, flush_producer=False
        )
    producer.producer.flush()
    return len(readings)
