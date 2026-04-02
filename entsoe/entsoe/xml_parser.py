"""
XML parser for ENTSO-E Transparency Platform IEC 62325 documents.

Handles GL_MarketDocument and Publication_MarketDocument root types.
Computes point timestamps from period start + (position - 1) * resolution.
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET

# IEC 62325 namespace used in ENTSO-E XML responses
NS = {"e": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0",
      "p": "urn:iec62325.351:tc57wg16:451-3:publicationdocument:7:3"}

# Map ISO 8601 durations to timedelta
RESOLUTION_MAP = {
    "PT15M": timedelta(minutes=15),
    "PT30M": timedelta(minutes=30),
    "PT60M": timedelta(hours=1),
    "P1D": timedelta(days=1),
}


def _parse_duration(iso_duration: str) -> timedelta:
    """Parse an ISO 8601 duration string to timedelta."""
    if iso_duration in RESOLUTION_MAP:
        return RESOLUTION_MAP[iso_duration]
    # Fallback regex for PTnHnMnS
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if m:
        hours = int(m.group(1) or 0)
        minutes = int(m.group(2) or 0)
        seconds = int(m.group(3) or 0)
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    raise ValueError(f"Cannot parse duration: {iso_duration}")


def _find_namespace(root: ET.Element) -> str:
    """Extract the XML namespace from the root element tag."""
    m = re.match(r"\{(.+)\}", root.tag)
    return m.group(1) if m else ""


def _ns(namespace: str, tag: str) -> str:
    """Build a namespaced tag."""
    return f"{{{namespace}}}{tag}"


class TimeSeriesPoint:
    """A single data point extracted from an ENTSO-E time series."""
    __slots__ = ("timestamp", "position", "quantity", "price",
                 "in_domain", "out_domain", "psr_type", "business_type",
                 "currency", "unit_name", "resolution", "document_type")

    def __init__(self, **kwargs):
        for slot in self.__slots__:
            setattr(self, slot, kwargs.get(slot))


def parse_entsoe_xml(xml_text: str, document_type: str) -> List[TimeSeriesPoint]:
    """
    Parse an ENTSO-E XML response and extract time series data points.

    Args:
        xml_text: Raw XML response from the ENTSO-E API.
        document_type: The document type code (A44, A65, A75).

    Returns:
        List of TimeSeriesPoint objects with computed timestamps.
    """
    root = ET.fromstring(xml_text)
    namespace = _find_namespace(root)
    ns = namespace

    points: List[TimeSeriesPoint] = []

    for ts in root.iter(_ns(ns, "TimeSeries")):
        # Extract time series metadata
        in_domain_el = ts.find(_ns(ns, "inBiddingZone_Domain.mRID"))
        if in_domain_el is None:
            in_domain_el = ts.find(_ns(ns, "in_Domain.mRID"))
        in_domain = in_domain_el.text if in_domain_el is not None else ""

        out_domain_el = ts.find(_ns(ns, "outBiddingZone_Domain.mRID"))
        if out_domain_el is None:
            out_domain_el = ts.find(_ns(ns, "out_Domain.mRID"))
        out_domain = out_domain_el.text if out_domain_el is not None else None

        # PSR type (generation per type only)
        psr_type = ""
        mkt_psr = ts.find(_ns(ns, "MktPSRType"))
        if mkt_psr is not None:
            psr_type_el = mkt_psr.find(_ns(ns, "psrType"))
            if psr_type_el is not None:
                psr_type = psr_type_el.text or ""

        # Business type
        bt_el = ts.find(_ns(ns, "businessType"))
        business_type = bt_el.text if bt_el is not None else ""

        # Currency
        currency_el = ts.find(_ns(ns, "currency_Unit.name"))
        currency = currency_el.text if currency_el is not None else ""

        # Quantity unit
        unit_el = ts.find(_ns(ns, "quantity_Measure_Unit.name"))
        if unit_el is None:
            unit_el = ts.find(_ns(ns, "price_Measure_Unit.name"))
        unit_name = unit_el.text if unit_el is not None else ""

        # Iterate periods
        for period in ts.iter(_ns(ns, "Period")):
            # Period start
            time_interval = period.find(_ns(ns, "timeInterval"))
            if time_interval is not None:
                start_el = time_interval.find(_ns(ns, "start"))
                period_start_str = start_el.text if start_el is not None else ""
            else:
                period_start_str = ""

            if not period_start_str:
                continue

            period_start = datetime.fromisoformat(period_start_str.replace("Z", "+00:00"))

            # Resolution
            res_el = period.find(_ns(ns, "resolution"))
            resolution_str = res_el.text if res_el is not None else "PT60M"
            resolution_delta = _parse_duration(resolution_str)

            # Extract points
            for point in period.iter(_ns(ns, "Point")):
                pos_el = point.find(_ns(ns, "position"))
                if pos_el is None:
                    continue
                position = int(pos_el.text)

                # Compute timestamp: period_start + (position - 1) * resolution
                point_timestamp = period_start + (position - 1) * resolution_delta

                # Quantity or price
                qty_el = point.find(_ns(ns, "quantity"))
                price_el = point.find(_ns(ns, "price.amount"))

                quantity = float(qty_el.text) if qty_el is not None else None
                price = float(price_el.text) if price_el is not None else None

                points.append(TimeSeriesPoint(
                    timestamp=point_timestamp,
                    position=position,
                    quantity=quantity,
                    price=price,
                    in_domain=in_domain,
                    out_domain=out_domain,
                    psr_type=psr_type,
                    business_type=business_type,
                    currency=currency,
                    unit_name=unit_name,
                    resolution=resolution_str,
                    document_type=document_type,
                ))

    return points


def build_api_url(base_url: str, security_token: str, document_type: str,
                  in_domain: str, period_start: datetime,
                  period_end: datetime, psr_type: Optional[str] = None) -> str:
    """
    Build an ENTSO-E REST API query URL.

    Args:
        base_url: ENTSO-E API base URL.
        security_token: API security token.
        document_type: ENTSO-E document type code (A44, A65, A75).
        in_domain: EIC code of the bidding zone.
        period_start: Start of the query window.
        period_end: End of the query window.
        psr_type: Optional PSR type filter.

    Returns:
        Fully constructed API URL.
    """
    start_str = period_start.strftime("%Y%m%d%H%M")
    end_str = period_end.strftime("%Y%m%d%H%M")

    url = (f"{base_url}?securityToken={security_token}"
           f"&documentType={document_type}"
           f"&processType=A16"
           f"&in_Domain={in_domain}"
           f"&periodStart={start_str}"
           f"&periodEnd={end_str}")

    if psr_type:
        url += f"&psrType={psr_type}"

    return url
