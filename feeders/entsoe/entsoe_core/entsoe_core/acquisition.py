"""Shared ENTSO-E Transparency Platform acquisition and delta polling."""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Protocol, Tuple

import requests

from .delta_state import get_last_polled, load_state, save_state, set_last_polled
from .xml_parser import TimeSeriesPoint, build_api_url, parse_entsoe_xml

logger = logging.getLogger("entsoe")

# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-entsoe/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

BASE_URL = "https://web-api.tp.entsoe.eu/api"

DEFAULT_DOMAINS = [
    "10YDE-AT-LU---Q", "10YFR-RTE------C", "10YNL----------L",
    "10YES-REE------0", "10Y1001A1001A83F",
]
DEFAULT_DOCUMENT_TYPES = ["A75", "A44", "A65", "A69", "A70", "A71", "A72", "A73", "A74", "A68", "A11"]
DEFAULT_CROSS_BORDER_PAIRS = [
    ("10YFR-RTE------C", "10YES-REE------0"), ("10YES-REE------0", "10YFR-RTE------C"),
    ("10YFR-RTE------C", "10Y1001A1001A83F"), ("10Y1001A1001A83F", "10YFR-RTE------C"),
    ("10Y1001A1001A83F", "10YNL----------L"), ("10YNL----------L", "10Y1001A1001A83F"),
    ("10YFR-RTE------C", "10YGB----------A"), ("10YGB----------A", "10YFR-RTE------C"),
    ("10YNL----------L", "10YGB----------A"), ("10YGB----------A", "10YNL----------L"),
    ("10Y1001A1001A83F", "10YDK-1--------W"), ("10YDK-1--------W", "10Y1001A1001A83F"),
    ("10Y1001A1001A83F", "10YPL-AREA-----S"), ("10YPL-AREA-----S", "10Y1001A1001A83F"),
    ("10Y1001A1001A83F", "10YCH-SWISSGRIDZ"), ("10YCH-SWISSGRIDZ", "10Y1001A1001A83F"),
    ("10Y1001A1001A83F", "10YAT-APG------L"), ("10YAT-APG------L", "10Y1001A1001A83F"),
    ("10Y1001A1001A83F", "10YCZ-CEPS-----N"), ("10YCZ-CEPS-----N", "10Y1001A1001A83F"),
]
DOC_TYPE_NAMES = {
    "A75": "ActualGenerationPerType", "A44": "DayAheadPrices", "A65": "ActualTotalLoad",
    "A69": "WindSolarForecast", "A70": "LoadForecastMargin", "A71": "GenerationForecast",
    "A72": "ReservoirFillingInformation", "A73": "ActualGeneration", "A74": "WindSolarGeneration",
    "A68": "InstalledGenerationCapacityPerType", "A11": "CrossBorderPhysicalFlows",
}
DOC_TYPES_WITH_PSR = {"A75", "A69", "A74", "A68"}
DOC_TYPES_SIMPLE_QUANTITY = {"A65", "A70", "A71", "A72", "A73"}
DOC_TYPE_CROSS_BORDER = "A11"


def parse_domain_list(value: Optional[str]) -> List[str]:
    return [v.strip() for v in value.split(",") if v.strip()] if value else list(DEFAULT_DOMAINS)


def parse_document_types(value: Optional[str]) -> List[str]:
    return [v.strip() for v in value.split(",") if v.strip()] if value else list(DEFAULT_DOCUMENT_TYPES)


def parse_cross_border_pairs(value: Optional[str]) -> List[Tuple[str, str]]:
    if not value:
        return list(DEFAULT_CROSS_BORDER_PAIRS)
    pairs = []
    for item in value.split(","):
        if ">" in item:
            left, right = item.split(">", 1)
        else:
            left, right = item.split(":", 1)
        pairs.append((left.strip(), right.strip()))
    return pairs


def sample_points() -> List[TimeSeriesPoint]:
    """Small deterministic corpus covering every ENTSO-E event family for tests."""
    ts = datetime(2025, 1, 1, 0, 0, tzinfo=timezone.utc)
    domain = "10Y1001A1001A83F"
    out_domain = "10YFR-RTE------C"
    return [
        TimeSeriesPoint(timestamp=ts, quantity=1234.0, price=None, in_domain=domain, out_domain=None, psr_type="B16", business_type="A01", currency="", unit_name="MAW", resolution="PT60M", document_type="A75"),
        TimeSeriesPoint(timestamp=ts, quantity=None, price=42.5, in_domain=domain, out_domain=None, psr_type="", business_type="", currency="EUR", unit_name="MWH", resolution="PT60M", document_type="A44"),
        TimeSeriesPoint(timestamp=ts, quantity=51234.0, price=None, in_domain=domain, out_domain=None, psr_type="", business_type="", currency="", unit_name="MAW", resolution="PT60M", document_type="A65"),
        TimeSeriesPoint(timestamp=ts, quantity=2345.0, price=None, in_domain=domain, out_domain=None, psr_type="B18", business_type="A01", currency="", unit_name="MAW", resolution="PT60M", document_type="A69"),
        TimeSeriesPoint(timestamp=ts, quantity=3456.0, price=None, in_domain=domain, out_domain=None, psr_type="", business_type="", currency="", unit_name="MAW", resolution="PT60M", document_type="A70"),
        TimeSeriesPoint(timestamp=ts, quantity=45678.0, price=None, in_domain=domain, out_domain=None, psr_type="", business_type="", currency="", unit_name="MAW", resolution="PT60M", document_type="A71"),
        TimeSeriesPoint(timestamp=ts, quantity=7890.0, price=None, in_domain=domain, out_domain=None, psr_type="", business_type="", currency="", unit_name="MWH", resolution="PT60M", document_type="A72"),
        TimeSeriesPoint(timestamp=ts, quantity=43210.0, price=None, in_domain=domain, out_domain=None, psr_type="", business_type="", currency="", unit_name="MAW", resolution="PT60M", document_type="A73"),
        TimeSeriesPoint(timestamp=ts, quantity=6543.0, price=None, in_domain=domain, out_domain=None, psr_type="B19", business_type="A01", currency="", unit_name="MAW", resolution="PT60M", document_type="A74"),
        TimeSeriesPoint(timestamp=ts, quantity=9876.0, price=None, in_domain=domain, out_domain=None, psr_type="B01", business_type="A01", currency="", unit_name="MAW", resolution="P1Y", document_type="A68"),
        TimeSeriesPoint(timestamp=ts, quantity=111.0, price=None, in_domain=domain, out_domain=out_domain, psr_type="", business_type="", currency="", unit_name="MAW", resolution="PT60M", document_type="A11"),
    ]


class PointPublisher(Protocol):
    def emit_point(self, point: TimeSeriesPoint) -> None: ...
    def flush(self) -> None: ...
    def close(self) -> None: ...


class EntsoeAPI:
    def __init__(self, security_token: str, base_url: str = BASE_URL):
        self.security_token = security_token
        self.base_url = base_url

    def query(self, document_type: str, domain: str, period_start: datetime, period_end: datetime,
              out_domain: Optional[str] = None) -> Optional[str]:
        url = build_api_url(self.base_url, self.security_token, document_type, domain, period_start, period_end, out_domain=out_domain)
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
            if response.status_code == 400:
                logger.debug("No data for %s/%s", document_type, domain)
                return None
            response.raise_for_status()
            return response.text
        except requests.RequestException as err:
            logger.error("API request failed for %s/%s: %s", document_type, domain, err)
            return None


class EntsoePoller:
    def __init__(self, api: EntsoeAPI, publisher: PointPublisher, state_file: str, domains: List[str],
                 document_types: List[str], cross_border_pairs: Optional[List[Tuple[str, str]]] = None,
                 lookback_hours: int = 24, polling_interval: int = 900):
        self.api = api
        self.publisher = publisher
        self.state_file = state_file
        self.domains = domains
        self.document_types = document_types
        self.cross_border_pairs = cross_border_pairs or list(DEFAULT_CROSS_BORDER_PAIRS)
        self.lookback_hours = lookback_hours
        self.polling_interval = polling_interval
        self.state = load_state(state_file)

    def _poll_domain(self, doc_type: str, domain: str, now: datetime, out_domain: Optional[str] = None) -> int:
        state_key = f"{domain}>{out_domain}" if out_domain else domain
        last_polled = get_last_polled(self.state, doc_type, state_key) or (now - timedelta(hours=self.lookback_hours))
        label = f"{DOC_TYPE_NAMES.get(doc_type, doc_type)} {domain}" + (f"→{out_domain}" if out_domain else "")
        logger.info("Polling %s since %s", label, last_polled.isoformat())
        xml_text = self.api.query(doc_type, domain, last_polled, now, out_domain=out_domain)
        if not xml_text:
            return 0
        points = [p for p in parse_entsoe_xml(xml_text, doc_type) if p.timestamp > last_polled]
        if not points:
            return 0
        max_timestamp = last_polled
        for point in points:
            self.publisher.emit_point(point)
            if point.timestamp > max_timestamp:
                max_timestamp = point.timestamp
        self.publisher.flush()
        set_last_polled(self.state, doc_type, state_key, max_timestamp)
        save_state(self.state_file, self.state)
        logger.info("Emitted %d events for %s/%s (up to %s)", len(points), doc_type, state_key, max_timestamp.isoformat())
        return len(points)

    def poll_once(self) -> int:
        now = datetime.now(timezone.utc)
        total = 0
        for doc_type in self.document_types:
            if doc_type == DOC_TYPE_CROSS_BORDER:
                for in_dom, out_dom in self.cross_border_pairs:
                    total += self._poll_domain(doc_type, in_dom, now, out_domain=out_dom)
            else:
                for domain in self.domains:
                    total += self._poll_domain(doc_type, domain, now)
        return total

    def run(self, once: bool = False) -> None:
        logger.info("Starting ENTSO-E bridge — polling %d document types across %d domains every %ds", len(self.document_types), len(self.domains), self.polling_interval)
        try:
            while True:
                try:
                    total = self.poll_once()
                    logger.info("Poll cycle complete: %d events emitted", total)
                except Exception:
                    logger.exception("Error during poll cycle")
                if once:
                    break
                time.sleep(self.polling_interval)
        finally:
            self.publisher.close()
