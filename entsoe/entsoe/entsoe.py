"""
ENTSO-E Transparency Platform bridge to Kafka endpoints.

Polls the ENTSO-E REST API for electricity market data (generation, load,
prices) and emits delta-only CloudEvents to Kafka / Event Hubs / Fabric
Event Streams.
"""

# pylint: disable=line-too-long

import os
import sys
import time
import logging
import argparse
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests

from entsoe.entsoe_producer.eu.entsoe.transparency.actualgenerationpertype import ActualGenerationPerType
from entsoe.entsoe_producer.eu.entsoe.transparency.dayaheadprices import DayAheadPrices
from entsoe.entsoe_producer.eu.entsoe.transparency.actualtotalload import ActualTotalLoad
from entsoe.entsoe_producer.eu.entsoe.transparency.windsolarforecast import WindSolarForecast
from entsoe.entsoe_producer.eu.entsoe.transparency.loadforecastmargin import LoadForecastMargin
from entsoe.entsoe_producer.eu.entsoe.transparency.generationforecast import GenerationForecast
from entsoe.entsoe_producer.eu.entsoe.transparency.reservoirfillinginformation import ReservoirFillingInformation
from entsoe.entsoe_producer.eu.entsoe.transparency.actualgeneration import ActualGeneration
from entsoe.entsoe_producer.eu.entsoe.transparency.windsolargeneration import WindSolarGeneration
from entsoe.entsoe_producer.eu.entsoe.transparency.installedgenerationcapacitypertype import InstalledGenerationCapacityPerType
from entsoe.entsoe_producer.eu.entsoe.transparency.crossborderphysicalflows import CrossBorderPhysicalFlows
from entsoe.entsoe_producer.producer_client import EuEntsoeTransparencyEventProducer
from entsoe.xml_parser import parse_entsoe_xml, build_api_url, TimeSeriesPoint
from entsoe.delta_state import load_state, save_state, get_last_polled, set_last_polled

logger = logging.getLogger("entsoe")

BASE_URL = "https://web-api.tp.entsoe.eu/api"

DEFAULT_DOMAINS = [
    "10YDE-AT-LU---Q",   # DE-AT-LU
    "10YFR-RTE------C",  # France
    "10YNL----------L",  # Netherlands
    "10YES-REE------0",  # Spain
    "10Y1001A1001A83F",  # Germany
]

DEFAULT_DOCUMENT_TYPES = [
    "A75", "A44", "A65",
    "A69", "A70", "A71", "A72", "A73", "A74", "A68",
    "A11",
]

# Cross-border domain pairs (in_domain, out_domain) for A11 physical flows
DEFAULT_CROSS_BORDER_PAIRS = [
    ("10YFR-RTE------C",  "10YES-REE------0"),   # France → Spain
    ("10YES-REE------0",  "10YFR-RTE------C"),   # Spain → France
    ("10YFR-RTE------C",  "10Y1001A1001A83F"),   # France → Germany
    ("10Y1001A1001A83F",  "10YFR-RTE------C"),   # Germany → France
    ("10Y1001A1001A83F",  "10YNL----------L"),   # Germany → Netherlands
    ("10YNL----------L",  "10Y1001A1001A83F"),   # Netherlands → Germany
    ("10YFR-RTE------C",  "10YGB----------A"),   # France → Great Britain
    ("10YGB----------A",  "10YFR-RTE------C"),   # Great Britain → France
    ("10YNL----------L",  "10YGB----------A"),   # Netherlands → Great Britain
    ("10YGB----------A",  "10YNL----------L"),   # Great Britain → Netherlands
    ("10Y1001A1001A83F",  "10YDK-1--------W"),   # Germany → Denmark DK1
    ("10YDK-1--------W",  "10Y1001A1001A83F"),   # Denmark DK1 → Germany
    ("10Y1001A1001A83F",  "10YPL-AREA-----S"),   # Germany → Poland
    ("10YPL-AREA-----S",  "10Y1001A1001A83F"),   # Poland → Germany
    ("10Y1001A1001A83F",  "10YCH-SWISSGRIDZ"),   # Germany → Switzerland
    ("10YCH-SWISSGRIDZ",  "10Y1001A1001A83F"),   # Switzerland → Germany
    ("10Y1001A1001A83F",  "10YAT-APG------L"),   # Germany → Austria
    ("10YAT-APG------L",  "10Y1001A1001A83F"),   # Austria → Germany
    ("10Y1001A1001A83F",  "10YCZ-CEPS-----N"),   # Germany → Czech Republic
    ("10YCZ-CEPS-----N",  "10Y1001A1001A83F"),   # Czech Republic → Germany
]

# Document type to CloudEvent type mapping
DOC_TYPE_NAMES = {
    "A75": "ActualGenerationPerType",
    "A44": "DayAheadPrices",
    "A65": "ActualTotalLoad",
    "A69": "WindSolarForecast",
    "A70": "LoadForecastMargin",
    "A71": "GenerationForecast",
    "A72": "ReservoirFillingInformation",
    "A73": "ActualGeneration",
    "A74": "WindSolarGeneration",
    "A68": "InstalledGenerationCapacityPerType",
    "A11": "CrossBorderPhysicalFlows",
}

# Document types that use the same schema shape as A75 (with psrType)
DOC_TYPES_WITH_PSR = {"A75", "A69", "A74", "A68"}

# Document types that are simple quantity-per-domain (no psrType, no price)
DOC_TYPES_SIMPLE_QUANTITY = {"A65", "A70", "A71", "A72", "A73"}

# Cross-border document type
DOC_TYPE_CROSS_BORDER = "A11"


class EntsoePoller:
    """Polls the ENTSO-E API and sends CloudEvents to Kafka."""

    def __init__(self, security_token: str, producer: EuEntsoeTransparencyEventProducer,
                 state_file: str, domains: List[str], document_types: List[str],
                 cross_border_pairs: Optional[List[tuple]] = None,
                 lookback_hours: int = 24, polling_interval: int = 900):
        self.security_token = security_token
        self.producer = producer
        self.state_file = state_file
        self.domains = domains
        self.document_types = document_types
        self.cross_border_pairs = cross_border_pairs or DEFAULT_CROSS_BORDER_PAIRS
        self.lookback_hours = lookback_hours
        self.polling_interval = polling_interval
        self.state = load_state(state_file)

    def _query_api(self, document_type: str, domain: str,
                   period_start: datetime, period_end: datetime,
                   out_domain: Optional[str] = None) -> Optional[str]:
        """Query the ENTSO-E API and return XML response text."""
        url = build_api_url(BASE_URL, self.security_token, document_type,
                            domain, period_start, period_end,
                            out_domain=out_domain)
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 400:
                # ENTSO-E returns 400 for "no data" scenarios
                logger.debug("No data for %s/%s (%s - %s)",
                             document_type, domain,
                             period_start.isoformat(), period_end.isoformat())
                return None
            response.raise_for_status()
            return response.text
        except requests.RequestException as err:
            logger.error("API request failed for %s/%s: %s",
                         document_type, domain, err)
            return None

    def _emit_point(self, point: TimeSeriesPoint) -> None:
        """Emit a single data point as a CloudEvent."""
        dt = point.document_type

        if dt in DOC_TYPES_WITH_PSR:
            # A75, A69, A74, A68 — generation-like with psrType
            if dt == "A75":
                data = ActualGenerationPerType(
                    inDomain=point.in_domain, psrType=point.psr_type,
                    quantity=point.quantity or 0.0, resolution=point.resolution,
                    businessType=point.business_type, documentType=dt,
                    unitName=point.unit_name or "MAW")
                self.producer.send_eu_entsoe_transparency_actual_generation_per_type(
                    data, flush_producer=False)
            elif dt == "A69":
                data = WindSolarForecast(
                    inDomain=point.in_domain, psrType=point.psr_type,
                    quantity=point.quantity or 0.0, resolution=point.resolution,
                    businessType=point.business_type, documentType=dt,
                    unitName=point.unit_name or "MAW")
                self.producer.send_eu_entsoe_transparency_wind_solar_forecast(
                    data, flush_producer=False)
            elif dt == "A74":
                data = WindSolarGeneration(
                    inDomain=point.in_domain, psrType=point.psr_type,
                    quantity=point.quantity or 0.0, resolution=point.resolution,
                    businessType=point.business_type, documentType=dt,
                    unitName=point.unit_name or "MAW")
                self.producer.send_eu_entsoe_transparency_wind_solar_generation(
                    data, flush_producer=False)
            elif dt == "A68":
                data = InstalledGenerationCapacityPerType(
                    inDomain=point.in_domain, psrType=point.psr_type,
                    quantity=point.quantity or 0.0, resolution=point.resolution,
                    businessType=point.business_type, documentType=dt,
                    unitName=point.unit_name or "MAW")
                self.producer.send_eu_entsoe_transparency_installed_generation_capacity_per_type(
                    data, flush_producer=False)

        elif dt == "A44":
            data = DayAheadPrices(
                inDomain=point.in_domain, price=point.price or 0.0,
                currency=point.currency or "EUR",
                unitName=point.unit_name or "MWH",
                resolution=point.resolution, documentType=dt)
            self.producer.send_eu_entsoe_transparency_day_ahead_prices(
                data, flush_producer=False)

        elif dt == DOC_TYPE_CROSS_BORDER:
            data = CrossBorderPhysicalFlows(
                inDomain=point.in_domain,
                outDomain=point.out_domain or "",
                quantity=point.quantity or 0.0,
                resolution=point.resolution, documentType=dt,
                unitName=point.unit_name or "MAW")
            self.producer.send_eu_entsoe_transparency_cross_border_physical_flows(
                data, flush_producer=False)

        elif dt == "A65":
            data = ActualTotalLoad(
                inDomain=point.in_domain, quantity=point.quantity or 0.0,
                resolution=point.resolution, outDomain=point.out_domain,
                documentType=dt)
            self.producer.send_eu_entsoe_transparency_actual_total_load(
                data, flush_producer=False)

        elif dt == "A70":
            data = LoadForecastMargin(
                inDomain=point.in_domain, quantity=point.quantity or 0.0,
                resolution=point.resolution, documentType=dt,
                unitName=point.unit_name or "MAW")
            self.producer.send_eu_entsoe_transparency_load_forecast_margin(
                data, flush_producer=False)

        elif dt == "A71":
            data = GenerationForecast(
                inDomain=point.in_domain, quantity=point.quantity or 0.0,
                resolution=point.resolution, documentType=dt,
                unitName=point.unit_name or "MAW")
            self.producer.send_eu_entsoe_transparency_generation_forecast(
                data, flush_producer=False)

        elif dt == "A72":
            data = ReservoirFillingInformation(
                inDomain=point.in_domain, quantity=point.quantity or 0.0,
                resolution=point.resolution, documentType=dt,
                unitName=point.unit_name or "MAW")
            self.producer.send_eu_entsoe_transparency_reservoir_filling_information(
                data, flush_producer=False)

        elif dt == "A73":
            data = ActualGeneration(
                inDomain=point.in_domain, quantity=point.quantity or 0.0,
                resolution=point.resolution, documentType=dt,
                unitName=point.unit_name or "MAW")
            self.producer.send_eu_entsoe_transparency_actual_generation(
                data, flush_producer=False)

    def _poll_domain(self, doc_type: str, domain: str, now: datetime,
                     out_domain: Optional[str] = None) -> int:
        """Poll a single (doc_type, domain[, out_domain]) combination."""
        state_key = f"{domain}>{out_domain}" if out_domain else domain

        last_polled = get_last_polled(self.state, doc_type, state_key)
        if last_polled is None:
            last_polled = now - timedelta(hours=self.lookback_hours)

        period_start = last_polled
        period_end = now

        label = f"{DOC_TYPE_NAMES.get(doc_type, doc_type)} {domain}" + (f"→{out_domain}" if out_domain else "")
        logger.info("Polling %s since %s", label, period_start.isoformat())

        xml_text = self._query_api(doc_type, domain, period_start, period_end,
                                   out_domain=out_domain)
        if not xml_text:
            return 0

        points = parse_entsoe_xml(xml_text, doc_type)
        new_points = [p for p in points if p.timestamp > last_polled]

        if not new_points:
            logger.info("  No new points for %s/%s", doc_type, state_key)
            return 0

        max_timestamp = last_polled
        for point in new_points:
            self._emit_point(point)
            if point.timestamp > max_timestamp:
                max_timestamp = point.timestamp

        self.producer.producer.flush()

        set_last_polled(self.state, doc_type, state_key, max_timestamp)
        save_state(self.state_file, self.state)

        logger.info("  Emitted %d events for %s/%s (up to %s)",
                    len(new_points), doc_type, state_key,
                    max_timestamp.isoformat())
        return len(new_points)

    def poll_once(self) -> int:
        """
        Execute one polling cycle across all configured document types and domains.

        Returns:
            Total number of events emitted.
        """
        now = datetime.now(timezone.utc)
        total_emitted = 0

        for doc_type in self.document_types:
            if doc_type == DOC_TYPE_CROSS_BORDER:
                # Cross-border flows use domain pairs
                for in_dom, out_dom in self.cross_border_pairs:
                    total_emitted += self._poll_domain(doc_type, in_dom, now,
                                                       out_domain=out_dom)
            else:
                for domain in self.domains:
                    total_emitted += self._poll_domain(doc_type, domain, now)

        return total_emitted

    def run(self) -> None:
        """Run the polling loop indefinitely."""
        logger.info("Starting ENTSO-E bridge — polling %d document types across %d domains every %ds",
                    len(self.document_types), len(self.domains), self.polling_interval)
        while True:
            try:
                total = self.poll_once()
                logger.info("Poll cycle complete: %d events emitted", total)
            except Exception:
                logger.exception("Error during poll cycle")
            time.sleep(self.polling_interval)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """Parse an Event Hubs / Fabric Event Stream connection string."""
    config_dict = {}
    for part in connection_string.split(";"):
        if "Endpoint" in part:
            config_dict["bootstrap.servers"] = (
                part.split("=", 1)[1].strip('"')
                .replace("sb://", "").replace("/", "") + ":9093"
            )
        elif "EntityPath" in part:
            config_dict["kafka_topic"] = part.split("=", 1)[1].strip('"')
        elif "SharedAccessKeyName" in part:
            config_dict["sasl.username"] = "$ConnectionString"
        elif "SharedAccessKey" in part:
            config_dict["sasl.password"] = connection_string.strip()
        elif "BootstrapServer" in part:
            config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict


def main():
    """Main entry point for the ENTSO-E bridge."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(description="ENTSO-E Transparency Platform bridge")
    parser.add_argument("--security-token", type=str, help="ENTSO-E API security token")
    parser.add_argument("--domains", type=str, help="Comma-separated EIC codes")
    parser.add_argument("--document-types", type=str, help="Comma-separated document type codes")
    parser.add_argument("--polling-interval", type=int, help="Seconds between poll cycles")
    parser.add_argument("--lookback-hours", type=int, help="Initial lookback window in hours")
    parser.add_argument("--state-file", type=str, help="Path to the delta state file")
    parser.add_argument("--kafka-bootstrap-servers", type=str, help="Kafka bootstrap servers")
    parser.add_argument("--kafka-topic", type=str, help="Kafka topic")
    parser.add_argument("--sasl-username", type=str, help="SASL username")
    parser.add_argument("--sasl-password", type=str, help="SASL password")
    parser.add_argument("--connection-string", type=str, help="Event Hubs / Fabric Event Stream connection string")

    args = parser.parse_args()

    # Resolve config from args or env vars
    security_token = args.security_token or os.getenv("ENTSOE_SECURITY_TOKEN")
    if not security_token:
        print("Error: ENTSO-E security token required (--security-token or ENTSOE_SECURITY_TOKEN)")
        sys.exit(1)

    domains_str = args.domains or os.getenv("ENTSOE_DOMAINS")
    domains = domains_str.split(",") if domains_str else DEFAULT_DOMAINS

    doc_types_str = args.document_types or os.getenv("ENTSOE_DOCUMENT_TYPES")
    document_types = doc_types_str.split(",") if doc_types_str else DEFAULT_DOCUMENT_TYPES

    polling_interval = args.polling_interval or int(os.getenv("POLLING_INTERVAL", "900"))
    lookback_hours = args.lookback_hours or int(os.getenv("ENTSOE_LOOKBACK_HOURS", "24"))

    state_file = args.state_file or os.getenv("STATE_FILE")
    if not state_file:
        state_file = os.path.expanduser("~/.entsoe_state.json")

    connection_string = args.connection_string or os.getenv("CONNECTION_STRING")

    if connection_string:
        config_params = parse_connection_string(connection_string)
        kafka_bootstrap_servers = config_params.get("bootstrap.servers")
        kafka_topic = config_params.get("kafka_topic")
        sasl_username = config_params.get("sasl.username")
        sasl_password = config_params.get("sasl.password")
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers or os.getenv("KAFKA_BOOTSTRAP_SERVERS")
        kafka_topic = args.kafka_topic or os.getenv("KAFKA_TOPIC")
        sasl_username = args.sasl_username or os.getenv("SASL_USERNAME")
        sasl_password = args.sasl_password or os.getenv("SASL_PASSWORD")

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers required (--kafka-bootstrap-servers, CONNECTION_STRING, or KAFKA_BOOTSTRAP_SERVERS)")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic required (--kafka-topic, CONNECTION_STRING, or KAFKA_TOPIC)")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = {"bootstrap.servers": kafka_bootstrap_servers}
    if sasl_username and sasl_password:
        kafka_config.update({
            "sasl.mechanisms": "PLAIN",
            "security.protocol": "SASL_SSL" if tls_enabled else "SASL_PLAINTEXT",
            "sasl.username": sasl_username,
            "sasl.password": sasl_password,
        })
    elif tls_enabled:
        kafka_config["security.protocol"] = "SSL"

    from confluent_kafka import Producer
    kafka_producer = Producer(kafka_config)
    producer = EuEntsoeTransparencyEventProducer(kafka_producer, kafka_topic)

    poller = EntsoePoller(
        security_token=security_token,
        producer=producer,
        state_file=state_file,
        domains=domains,
        document_types=document_types,
        lookback_hours=lookback_hours,
        polling_interval=polling_interval,
    )
    poller.run()


if __name__ == "__main__":
    main()
