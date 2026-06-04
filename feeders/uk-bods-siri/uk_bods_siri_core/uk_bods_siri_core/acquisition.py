from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
import logging
import os
from pathlib import Path
from typing import Iterator, Optional
import xml.etree.ElementTree as ET
import zipfile

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BODS_BULK_URL = "https://data.bus-data.dft.gov.uk/avl/download/bulk_archive"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-uk-bods-siri/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

logger = logging.getLogger(__name__)


def _default_sample_path() -> Path:
    candidates = [
        Path.cwd() / "sample_data" / "siri.xml",
        Path(__file__).resolve().parents[2] / "sample_data" / "siri.xml",
        Path(__file__).resolve().parents[1] / "sample_data" / "siri.xml",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


@dataclass(frozen=True)
class VehiclePositionRecord:
    operator_ref: str
    vehicle_ref: str
    line_ref: Optional[str]
    direction_ref: Optional[str]
    published_line_name: Optional[str]
    origin_ref: Optional[str]
    origin_name: Optional[str]
    destination_ref: Optional[str]
    destination_name: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    bearing: Optional[int]
    recorded_at_time: str
    valid_until_time: Optional[str]
    block_ref: Optional[str]
    vehicle_journey_ref: Optional[str]
    origin_aimed_departure_time: Optional[str]
    data_frame_ref: Optional[str]
    dated_vehicle_journey_ref: Optional[str]
    item_identifier: str

    @property
    def identity(self) -> str:
        return f"{self.operator_ref}/{self.vehicle_ref}"


@dataclass(frozen=True)
class FeedSnapshot:
    operators: tuple[str, ...]
    vehicle_positions: tuple[VehiclePositionRecord, ...]


class BodsSiriClient:
    def __init__(
        self,
        *,
        api_key: str,
        operators: Optional[set[str]] = None,
        session: Optional[requests.Session] = None,
        request_timeout: float = 30.0,
        sample_mode: Optional[bool] = None,
        sample_path: Optional[str] = None,
    ) -> None:
        self._api_key = api_key
        self._operators = {value.strip() for value in operators or set() if value.strip()} or None
        self._session = session or _build_retrying_session()
        self._session.headers.setdefault("User-Agent", USER_AGENT)
        self._request_timeout = request_timeout
        self._sample_mode = (
            sample_mode if sample_mode is not None
            else os.getenv("BODS_SAMPLE_MODE", "").lower() in ("1", "true", "yes")
        )
        self._sample_path = sample_path or os.getenv("BODS_SAMPLE_FILE") or str(_default_sample_path())

    def load_snapshot(self) -> FeedSnapshot:
        xml_bytes = self._load_xml_bytes()
        positions = tuple(iter_vehicle_positions(xml_bytes, operators=self._operators))
        operators = tuple(sorted({position.operator_ref for position in positions}))
        return FeedSnapshot(operators=operators, vehicle_positions=positions)

    def source_url(self) -> str:
        return BODS_BULK_URL

    def _load_xml_bytes(self) -> bytes:
        if self._sample_mode:
            logger.info("Using bundled sample SIRI XML from %s", self._sample_path)
            return Path(self._sample_path).read_bytes()
        if not self._api_key:
            raise RuntimeError("BODS_API_KEY is required unless BODS_SAMPLE_MODE=true.")
        response = self._session.get(
            BODS_BULK_URL,
            params={"api_key": self._api_key},
            timeout=self._request_timeout,
        )
        response.raise_for_status()
        with zipfile.ZipFile(BytesIO(response.content)) as archive:
            candidate = next((name for name in archive.namelist() if name.lower().endswith("siri.xml")), None)
            if not candidate:
                raise RuntimeError("Bulk archive did not contain siri.xml")
            with archive.open(candidate) as handle:
                return handle.read()


def _build_retrying_session() -> requests.Session:
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        backoff_factor=1.0,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def iter_vehicle_positions(xml_bytes: bytes, *, operators: Optional[set[str]] = None) -> Iterator[VehiclePositionRecord]:
    context = ET.iterparse(BytesIO(xml_bytes), events=("end",))
    for _event, elem in context:
        if _local_name(elem.tag) != "VehicleActivity":
            continue
        position = _parse_vehicle_activity(elem)
        elem.clear()
        if position is None:
            continue
        if operators and position.operator_ref not in operators:
            continue
        yield position


def _parse_vehicle_activity(vehicle_activity: ET.Element) -> Optional[VehiclePositionRecord]:
    recorded_at_time = _child_text(vehicle_activity, "RecordedAtTime")
    item_identifier = _child_text(vehicle_activity, "ItemIdentifier")
    journey = _child(vehicle_activity, "MonitoredVehicleJourney")
    if not recorded_at_time or not item_identifier or journey is None:
        return None

    operator_ref = _child_text(journey, "OperatorRef")
    vehicle_ref = _child_text(journey, "VehicleRef")
    if not operator_ref or not vehicle_ref:
        return None

    framed = _child(journey, "FramedVehicleJourneyRef")
    location = _child(journey, "VehicleLocation")

    return VehiclePositionRecord(
        operator_ref=operator_ref,
        vehicle_ref=vehicle_ref,
        line_ref=_child_text(journey, "LineRef"),
        direction_ref=_child_text(journey, "DirectionRef"),
        published_line_name=_child_text(journey, "PublishedLineName"),
        origin_ref=_child_text(journey, "OriginRef"),
        origin_name=_child_text(journey, "OriginName"),
        destination_ref=_child_text(journey, "DestinationRef"),
        destination_name=_child_text(journey, "DestinationName"),
        longitude=_to_float(_child_text(location, "Longitude") if location is not None else None),
        latitude=_to_float(_child_text(location, "Latitude") if location is not None else None),
        bearing=_to_int(_child_text(journey, "Bearing")),
        recorded_at_time=recorded_at_time,
        valid_until_time=_child_text(vehicle_activity, "ValidUntilTime"),
        block_ref=_child_text(journey, "BlockRef"),
        vehicle_journey_ref=_child_text(journey, "VehicleJourneyRef"),
        origin_aimed_departure_time=_child_text(journey, "OriginAimedDepartureTime"),
        data_frame_ref=_child_text(framed, "DataFrameRef") if framed is not None else None,
        dated_vehicle_journey_ref=_child_text(framed, "DatedVehicleJourneyRef") if framed is not None else None,
        item_identifier=item_identifier,
    )


def _child(parent: Optional[ET.Element], local_name: str) -> Optional[ET.Element]:
    if parent is None:
        return None
    for child in list(parent):
        if _local_name(child.tag) == local_name:
            return child
    return None


def _child_text(parent: Optional[ET.Element], local_name: str) -> Optional[str]:
    child = _child(parent, local_name)
    if child is None or child.text is None:
        return None
    text = child.text.strip()
    return text or None


def _local_name(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _to_float(value: Optional[str]) -> Optional[float]:
    if value in (None, ""):
        return None
    return float(value)


def _to_int(value: Optional[str]) -> Optional[int]:
    if value in (None, ""):
        return None
    return int(float(value))
