"""
Carbon Intensity UK Bridge
Polls the Carbon Intensity API (National Grid ESO) for GB electricity carbon
intensity, generation mix, and regional breakdowns, and sends them to a Kafka
topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import argparse
from typing import Dict, List, Optional
from datetime import datetime, timezone

import requests

from carbon_intensity_producer_data import Intensity, GenerationMix, RegionalIntensity
from carbon_intensity_producer_kafka_producer.producer import (
    UkOrgCarbonintensityEventProducer,
    UkOrgCarbonintensityRegionalEventProducer,
)

API_BASE = "https://api.carbonintensity.org.uk"
POLL_INTERVAL_SECONDS = 1800  # 30 minutes


FUEL_TYPES = [
    "biomass", "coal", "imports", "gas", "nuclear",
    "other", "hydro", "solar", "wind", "oil",
]


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Azure Event Hubs-style or plain Kafka connection string.

    Returns:
        Dict with bootstrap.servers, kafka_topic, and optional SASL fields.
    """
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = (
                    part.split('=')[1].strip('"')
                    .replace('sb://', '').replace('/', '') + ':9093'
                )
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as exc:
        raise ValueError("Invalid connection string format") from exc
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def flatten_generation_mix(mix_list: List[Dict]) -> Dict[str, Optional[float]]:
    """Convert the upstream generationmix array into flat *_pct fields.

    Args:
        mix_list: List of {"fuel": "<name>", "perc": <number>} dicts.

    Returns:
        Dict mapping e.g. 'biomass_pct' → 7.1.
    """
    lookup = {item["fuel"]: item.get("perc") for item in mix_list}
    return {f"{fuel}_pct": lookup.get(fuel) for fuel in FUEL_TYPES}


def parse_api_datetime(value: str) -> datetime:
    """Parse an ISO 8601 timestamp from the Carbon Intensity API.

    The API returns timestamps like '2026-04-06T09:30Z'.  Python's
    ``fromisoformat`` on older versions may not accept the trailing 'Z',
    so we normalise it first.

    Args:
        value: ISO 8601 timestamp string.

    Returns:
        Timezone-aware datetime in UTC.
    """
    if value.endswith('Z'):
        value = value[:-1] + '+00:00'
    return datetime.fromisoformat(value)


class CarbonIntensityPoller:
    """Polls the Carbon Intensity API and emits CloudEvents to Kafka."""

    def __init__(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        last_polled_file: str,
    ):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.producer = UkOrgCarbonintensityEventProducer(kafka_producer, kafka_topic)
        self.regional_producer = UkOrgCarbonintensityRegionalEventProducer(kafka_producer, kafka_topic)

    # ------------------------------------------------------------------
    # State persistence
    # ------------------------------------------------------------------

    def load_state(self) -> Dict:
        """Load the last-seen period marker from disk."""
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as fh:
                    return json.load(fh)
        except Exception:
            pass
        return {}

    def save_state(self, state: Dict) -> None:
        """Persist the last-seen period marker."""
        try:
            directory = os.path.dirname(self.last_polled_file)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as fh:
                json.dump(state, fh, indent=2)
        except Exception as exc:
            print(f"Error saving state: {exc}")

    # ------------------------------------------------------------------
    # API helpers
    # ------------------------------------------------------------------

    @staticmethod
    def fetch_intensity() -> Optional[Dict]:
        """GET /intensity — current national carbon intensity."""
        try:
            resp = requests.get(f"{API_BASE}/intensity", timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            print(f"Error fetching intensity: {exc}")
            return None

    @staticmethod
    def fetch_generation() -> Optional[Dict]:
        """GET /generation — current national generation mix."""
        try:
            resp = requests.get(f"{API_BASE}/generation", timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            print(f"Error fetching generation: {exc}")
            return None

    @staticmethod
    def fetch_regional() -> Optional[Dict]:
        """GET /regional — all 17 DNO regions."""
        try:
            resp = requests.get(f"{API_BASE}/regional", timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            print(f"Error fetching regional: {exc}")
            return None

    # ------------------------------------------------------------------
    # Parsing helpers
    # ------------------------------------------------------------------

    @staticmethod
    def parse_intensity(data: Dict) -> Optional[Intensity]:
        """Build an Intensity dataclass from the /intensity response."""
        items = data.get("data", [])
        if not items:
            return None
        item = items[0]
        period_from = parse_api_datetime(item["from"])
        period_to = parse_api_datetime(item["to"])
        ival = item.get("intensity", {})
        return Intensity(
            period_from=period_from,
            period_to=period_to,
            forecast=ival.get("forecast"),
            actual=ival.get("actual"),
            index=ival.get("index"),
        )

    @staticmethod
    def parse_generation(data: Dict) -> Optional[GenerationMix]:
        """Build a GenerationMix dataclass from the /generation response."""
        inner = data.get("data")
        if not inner:
            return None
        period_from = parse_api_datetime(inner["from"])
        period_to = parse_api_datetime(inner["to"])
        mix = flatten_generation_mix(inner.get("generationmix", []))
        return GenerationMix(
            period_from=period_from,
            period_to=period_to,
            **mix,
        )

    @staticmethod
    def parse_regional(data: Dict) -> List[RegionalIntensity]:
        """Build RegionalIntensity dataclasses from the /regional response."""
        results: List[RegionalIntensity] = []
        entries = data.get("data", [])
        if not entries:
            return results
        entry = entries[0]
        period_from = parse_api_datetime(entry["from"])
        period_to = parse_api_datetime(entry["to"])
        for region in entry.get("regions", []):
            ival = region.get("intensity", {})
            mix = flatten_generation_mix(region.get("generationmix", []))
            results.append(RegionalIntensity(
                region_id=region["regionid"],
                dnoregion=region.get("dnoregion", ""),
                shortname=region.get("shortname", ""),
                period_from=period_from,
                period_to=period_to,
                forecast=ival.get("forecast"),
                index=ival.get("index"),
                **mix,
            ))
        return results

    # ------------------------------------------------------------------
    # Emit helpers
    # ------------------------------------------------------------------

    def emit_intensity(self, intensity: Intensity) -> None:
        """Send an Intensity event."""
        self.producer.send_uk_org_carbonintensity_intensity(
            _period_from=intensity.period_from.isoformat(),
            data=intensity,
            flush_producer=False,
        )

    def emit_generation_mix(self, gen_mix: GenerationMix) -> None:
        """Send a GenerationMix event."""
        self.producer.send_uk_org_carbonintensity_generation_mix(
            _period_from=gen_mix.period_from.isoformat(),
            data=gen_mix,
            flush_producer=False,
        )

    def emit_regional(self, regional: RegionalIntensity) -> None:
        """Send a RegionalIntensity event."""
        self.regional_producer.send_uk_org_carbonintensity_regional_intensity(
            _region_id=str(regional.region_id),
            data=regional,
            flush_producer=False,
        )

    # ------------------------------------------------------------------
    # Poll loop
    # ------------------------------------------------------------------

    def poll_once(self) -> Optional[str]:
        """Fetch all endpoints and emit events. Returns the period_from key
        of the intensity record if new data was emitted, else None."""
        intensity_data = self.fetch_intensity()
        generation_data = self.fetch_generation()
        regional_data = self.fetch_regional()

        emitted_key = None

        if intensity_data:
            intensity = self.parse_intensity(intensity_data)
            if intensity:
                self.emit_intensity(intensity)
                emitted_key = intensity.period_from.isoformat()
                print(f"Emitted intensity for {emitted_key}")

        if generation_data:
            gen_mix = self.parse_generation(generation_data)
            if gen_mix:
                self.emit_generation_mix(gen_mix)
                print(f"Emitted generation mix for {gen_mix.period_from.isoformat()}")

        if regional_data:
            regionals = self.parse_regional(regional_data)
            for region in regionals:
                self.emit_regional(region)
            if regionals:
                print(f"Emitted {len(regionals)} regional intensity records")

        self.producer.producer.flush()
        return emitted_key

    def poll_and_send(self) -> None:
        """Continuous polling loop with deduplication."""
        state = self.load_state()
        last_period = state.get("last_period_from")
        print(f"Starting Carbon Intensity poller (last_period={last_period})")

        while True:
            try:
                emitted_key = self.poll_once()
                if emitted_key and emitted_key != last_period:
                    last_period = emitted_key
                    state["last_period_from"] = last_period
                    self.save_state(state)
            except Exception as exc:
                print(f"Error during poll cycle: {exc}")

            print(f"Sleeping {POLL_INTERVAL_SECONDS}s until next poll…")
            time.sleep(POLL_INTERVAL_SECONDS)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(description="Carbon Intensity UK Bridge")
    parser.add_argument('--kafka-bootstrap-servers', type=str)
    parser.add_argument('--kafka-topic', type=str)
    parser.add_argument('--sasl-username', type=str)
    parser.add_argument('--sasl-password', type=str)
    parser.add_argument('--connection-string', type=str)
    parser.add_argument('--last-polled-file', type=str)

    args = parser.parse_args()

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv(
            'CARBON_INTENSITY_LAST_POLLED_FILE',
            os.path.expanduser('~/.carbon_intensity_last_polled.json'),
        )

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

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided.")
        sys.exit(1)

    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config: Dict[str, str] = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password,
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = CarbonIntensityPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file,
    )
    poller.poll_and_send()


if __name__ == "__main__":
    main()
