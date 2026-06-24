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

from .config import DEFAULT_BODS_URL, DEFAULT_ENTUR_CLIENT_NAME, DEFAULT_ENTUR_URL, DEFAULT_TRAFIKLAB_URL

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-siri/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RequestSpec:
    request_url: str
    source_url: str
    headers: dict[str, str]
    params: dict[str, str]
    is_zip: bool = False


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
    feedurl: str

    @property
    def identity(self) -> str:
        return f"{self.operator_ref}/{self.vehicle_ref}"


@dataclass(frozen=True)
class FeedSnapshot:
    operators: tuple[str, ...]
    vehicle_positions: tuple[VehiclePositionRecord, ...]
    operator_feed_urls: dict[str, str]


class SiriClient:
    def __init__(
        self,
        *,
        provider: str = "bods",
        siri_url: str = "",
        api_key: str = "",
        operators: Optional[tuple[str, ...]] = None,
        data_types: tuple[str, ...] = ("vm",),
        request_headers: Optional[dict[str, str]] = None,
        session: Optional[requests.Session] = None,
        request_timeout: float = 30.0,
        sample_mode: Optional[bool] = None,
        sample_path: Optional[str] = None,
    ) -> None:
        self._provider = provider
        self._siri_url = siri_url.strip() if siri_url else _default_url_for_provider(provider)
        self._api_key = api_key
        self._operators = tuple(value.strip() for value in operators or tuple() if value and value.strip()) or None
        self._operator_filter = set(self._operators or tuple()) or None
        self._data_types = tuple(data_types or ("vm",))
        self._request_headers = dict(request_headers or {})
        if self._provider == "entur" and not _has_header(self._request_headers, "ET-Client-Name"):
            self._request_headers["ET-Client-Name"] = DEFAULT_ENTUR_CLIENT_NAME
        self._session = session or _build_retrying_session()
        self._session.headers.setdefault("User-Agent", USER_AGENT)
        self._request_timeout = request_timeout
        self._sample_mode = (
            sample_mode if sample_mode is not None
            else (os.getenv("SIRI_SAMPLE_MODE") or os.getenv("BODS_SAMPLE_MODE", "")).lower() in ("1", "true", "yes")
        )
        self._sample_path = sample_path or os.getenv("SIRI_SAMPLE_FILE") or os.getenv("BODS_SAMPLE_FILE") or str(_default_sample_path())

    @property
    def provider(self) -> str:
        return self._provider

    def load_snapshot(self) -> FeedSnapshot:
        positions_by_identity: dict[str, VehiclePositionRecord] = {}
        operator_feed_urls: dict[str, str] = {}

        if self._sample_mode:
            sample_source = self._siri_url or DEFAULT_BODS_URL
            for position in iter_vehicle_positions(Path(self._sample_path).read_bytes(), operators=self._operator_filter, feedurl=sample_source):
                _merge_position(positions_by_identity, position)
                operator_feed_urls.setdefault(position.operator_ref, sample_source)
        else:
            for spec in self._build_request_specs():
                xml_bytes = self._fetch_xml(spec)
                for position in iter_vehicle_positions(xml_bytes, operators=self._operator_filter, feedurl=spec.source_url):
                    _merge_position(positions_by_identity, position)
                    operator_feed_urls.setdefault(position.operator_ref, spec.source_url)

        positions = tuple(sorted(positions_by_identity.values(), key=lambda item: (item.operator_ref, item.vehicle_ref)))
        operators = tuple(sorted(operator_feed_urls))
        return FeedSnapshot(operators=operators, vehicle_positions=positions, operator_feed_urls=operator_feed_urls)

    def _build_request_specs(self) -> list[RequestSpec]:
        if self._provider == "bods":
            bods_url = self._siri_url or DEFAULT_BODS_URL
            # The public BODS bulk archive (the default endpoint) is downloadable
            # without credentials; only the filtered datafeed API requires a key.
            is_bulk_archive = bods_url.rstrip("/").endswith("/bulk_archive")
            if not is_bulk_archive and not self._api_key:
                raise RuntimeError(
                    "SIRI_API_KEY is required for the BODS datafeed API unless "
                    "SIRI_SAMPLE_MODE=true or the public bulk_archive endpoint is used."
                )
            return [
                RequestSpec(
                    request_url=bods_url,
                    source_url=bods_url,
                    headers=dict(self._request_headers),
                    params={"api_key": self._api_key} if self._api_key else {},
                    is_zip=True,
                )
            ]

        if self._provider == "trafiklab":
            base_url = self._siri_url or DEFAULT_TRAFIKLAB_URL
            headers = {"X-Api-Key": self._api_key} if self._api_key else {}
            headers.update(self._request_headers)
            params: dict[str, str] = {}
            return self._expand_specs(base_url, headers=headers, params=params)

        if self._provider == "entur":
            base_url = self._siri_url or DEFAULT_ENTUR_URL
            return self._expand_specs(base_url, headers=dict(self._request_headers), params={})

        if not self._siri_url:
            raise RuntimeError("SIRI_URL is required for provider=custom unless SIRI_SAMPLE_MODE=true.")
        headers = dict(self._request_headers)
        params = {}
        if self._api_key:
            headers.update({"X-Api-Key": self._api_key, "Authorization": f"Bearer {self._api_key}"})
            params.update({"api_key": self._api_key, "key": self._api_key})
        return self._expand_specs(self._siri_url, headers=headers, params=params)

    def _expand_specs(self, base_url: str, *, headers: dict[str, str], params: dict[str, str]) -> list[RequestSpec]:
        operator_values = self._operators or (None,)
        data_type_values = self._data_types or ("vm",)
        needs_operator = "{operator}" in base_url
        needs_data_type = "{data_type}" in base_url

        if needs_operator and not self._operators:
            raise RuntimeError("SIRI_OPERATORS is required when SIRI_URL contains the {operator} placeholder.")

        specs: list[RequestSpec] = []
        for operator in operator_values:
            for data_type in data_type_values:
                if needs_operator and operator is None:
                    continue
                request_url = base_url
                if needs_operator:
                    assert operator is not None
                    request_url = request_url.replace("{operator}", operator)
                if needs_data_type:
                    request_url = request_url.replace("{data_type}", data_type)
                specs.append(
                    RequestSpec(
                        request_url=request_url,
                        source_url=request_url,
                        headers=dict(headers),
                        params=dict(params),
                        is_zip=False,
                    )
                )
                if not needs_operator and not needs_data_type:
                    return specs
                if not needs_data_type:
                    break
            if not needs_operator:
                break
        return specs

    def _fetch_xml(self, spec: RequestSpec) -> bytes:
        response = self._session.get(
            spec.request_url,
            headers=spec.headers,
            params=spec.params,
            timeout=self._request_timeout,
        )
        response.raise_for_status()
        if spec.is_zip:
            with zipfile.ZipFile(BytesIO(response.content)) as archive:
                candidate = next((name for name in archive.namelist() if name.lower().endswith("siri.xml")), None)
                if not candidate:
                    raise RuntimeError("Bulk archive did not contain siri.xml")
                with archive.open(candidate) as handle:
                    return handle.read()
        return response.content


class SiriClientGroup:
    def __init__(self, clients: tuple[SiriClient, ...]) -> None:
        if not clients:
            raise ValueError("At least one SIRI source config is required")
        self._clients = clients

    def load_snapshot(self) -> FeedSnapshot:
        operators: set[str] = set()
        positions_by_identity: dict[str, VehiclePositionRecord] = {}
        operator_feed_urls: dict[str, str] = {}
        for client in self._clients:
            snapshot = client.load_snapshot()
            operators.update(snapshot.operators)
            operator_feed_urls.update(snapshot.operator_feed_urls)
            for position in snapshot.vehicle_positions:
                _merge_position(positions_by_identity, position)
        return FeedSnapshot(
            operators=tuple(sorted(operators)),
            vehicle_positions=tuple(sorted(positions_by_identity.values(), key=lambda item: (item.operator_ref, item.vehicle_ref))),
            operator_feed_urls=operator_feed_urls,
        )


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


def _default_url_for_provider(provider: str) -> str:
    if provider == "bods":
        return DEFAULT_BODS_URL
    if provider == "trafiklab":
        return DEFAULT_TRAFIKLAB_URL
    if provider == "entur":
        return DEFAULT_ENTUR_URL
    return ""


def _has_header(headers: dict[str, str], name: str) -> bool:
    return any(header_name.lower() == name.lower() for header_name in headers)


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


def _merge_position(existing: dict[str, VehiclePositionRecord], position: VehiclePositionRecord) -> None:
    previous = existing.get(position.identity)
    if previous is None or position.recorded_at_time >= previous.recorded_at_time:
        existing[position.identity] = position


def iter_vehicle_positions(
    xml_bytes: bytes,
    *,
    operators: Optional[set[str]] = None,
    feedurl: str,
) -> Iterator[VehiclePositionRecord]:
    context = ET.iterparse(BytesIO(xml_bytes), events=("end",))
    for _event, elem in context:
        if _local_name(elem.tag) != "VehicleActivity":
            continue
        position = _parse_vehicle_activity(elem, feedurl=feedurl)
        elem.clear()
        if position is None:
            continue
        if operators and position.operator_ref not in operators:
            continue
        yield position


def _parse_vehicle_activity(vehicle_activity: ET.Element, *, feedurl: str) -> Optional[VehiclePositionRecord]:
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
        feedurl=feedurl,
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
    if value is None or value == "":
        return None
    return float(value)


def _to_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    return int(float(value))
