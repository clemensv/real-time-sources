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

DEFAULT_DOCUMENT_TYPES = ["A75", "A44", "A65"]

# Document type to CloudEvent type mapping
DOC_TYPE_NAMES = {
    "A75": "ActualGenerationPerType",
    "A44": "DayAheadPrices",
    "A65": "ActualTotalLoad",
}


class EntsoePoller:
    """Polls the ENTSO-E API and sends CloudEvents to Kafka."""

    def __init__(self, security_token: str, producer: EuEntsoeTransparencyEventProducer,
                 state_file: str, domains: List[str], document_types: List[str],
                 lookback_hours: int = 24, polling_interval: int = 900):
        self.security_token = security_token
        self.producer = producer
        self.state_file = state_file
        self.domains = domains
        self.document_types = document_types
        self.lookback_hours = lookback_hours
        self.polling_interval = polling_interval
        self.state = load_state(state_file)

    def _query_api(self, document_type: str, domain: str,
                   period_start: datetime, period_end: datetime) -> Optional[str]:
        """Query the ENTSO-E API and return XML response text."""
        url = build_api_url(BASE_URL, self.security_token, document_type,
                            domain, period_start, period_end)
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
        if point.document_type == "A75":
            data = ActualGenerationPerType(
                inDomain=point.in_domain,
                psrType=point.psr_type,
                quantity=point.quantity or 0.0,
                resolution=point.resolution,
                businessType=point.business_type,
                documentType=point.document_type,
                unitName=point.unit_name or "MAW",
            )
            self.producer.send_eu_entsoe_transparency_actual_generation_per_type(
                data, flush_producer=False)

        elif point.document_type == "A44":
            data = DayAheadPrices(
                inDomain=point.in_domain,
                price=point.price or 0.0,
                currency=point.currency or "EUR",
                unitName=point.unit_name or "MWH",
                resolution=point.resolution,
                documentType=point.document_type,
            )
            self.producer.send_eu_entsoe_transparency_day_ahead_prices(
                data, flush_producer=False)

        elif point.document_type == "A65":
            data = ActualTotalLoad(
                inDomain=point.in_domain,
                quantity=point.quantity or 0.0,
                resolution=point.resolution,
                outDomain=point.out_domain,
                documentType=point.document_type,
            )
            self.producer.send_eu_entsoe_transparency_actual_total_load(
                data, flush_producer=False)

    def poll_once(self) -> int:
        """
        Execute one polling cycle across all configured document types and domains.

        Returns:
            Total number of events emitted.
        """
        now = datetime.now(timezone.utc)
        total_emitted = 0

        for doc_type in self.document_types:
            for domain in self.domains:
                last_polled = get_last_polled(self.state, doc_type, domain)
                if last_polled is None:
                    last_polled = now - timedelta(hours=self.lookback_hours)

                period_start = last_polled
                period_end = now

                logger.info("Polling %s for %s since %s",
                            DOC_TYPE_NAMES.get(doc_type, doc_type), domain,
                            period_start.isoformat())

                xml_text = self._query_api(doc_type, domain, period_start, period_end)
                if not xml_text:
                    continue

                points = parse_entsoe_xml(xml_text, doc_type)

                # Filter to delta-only: points strictly after the last checkpoint
                new_points = [p for p in points if p.timestamp > last_polled]

                if not new_points:
                    logger.info("  No new points for %s/%s", doc_type, domain)
                    continue

                max_timestamp = last_polled
                for point in new_points:
                    self._emit_point(point)
                    if point.timestamp > max_timestamp:
                        max_timestamp = point.timestamp
                    total_emitted += 1

                self.producer.producer.flush()

                # Advance checkpoint
                set_last_polled(self.state, doc_type, domain, max_timestamp)
                save_state(self.state_file, self.state)

                logger.info("  Emitted %d events for %s/%s (up to %s)",
                            len(new_points), doc_type, domain,
                            max_timestamp.isoformat())

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
