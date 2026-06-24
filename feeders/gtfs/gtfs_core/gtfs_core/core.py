"""Transport-neutral GTFS acquisition core."""
from __future__ import annotations

import asyncio

import csv

import glob

import hashlib

import inspect

import io

import os

import re

import shutil

import subprocess

import time

import json

import argparse

import logging

import threading

from typing import Any, Dict, Generator, Iterable, List, Tuple

from datetime import datetime, timedelta, timezone

from tempfile import TemporaryDirectory

import uuid

from zipfile import ZipFile

from enum import Enum

import dataclasses

import dataclasses_json

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert import Alert

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.cause import Cause

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.effect import Effect

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.entityselector import EntitySelector

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.timerange import TimeRange

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.translatedstring import TranslatedString

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.translatedstring_types.translation import Translation

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.tripdescriptor import TripDescriptor as AlertTripDescriptor

from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.tripdescriptor_types import ScheduleRelationship as AlertScheduleRelationship

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.position import Position

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicledescriptor import VehicleDescriptor as PositionVehicleDescriptor

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition import VehiclePosition

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.congestionlevel import CongestionLevel

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.occupancystatus import OccupancyStatus

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.vehicleposition_types.vehiclestopstatus import VehicleStopStatus

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.tripdescriptor import TripDescriptor as PositionTripDescriptor

from gtfs_rt_producer_data.generaltransitfeedrealtime.vehicle.tripdescriptor_types.schedulerelationship import ScheduleRelationship as PositionScheduleRelationship

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate import TripUpdate

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeevent import StopTimeEvent

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate import StopTimeUpdate

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripdescriptor import TripDescriptor as TripTripDescriptor

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripdescriptor_types.schedulerelationship import ScheduleRelationship as TripScheduleRelationship

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.tripupdate_types.stoptimeupdate_types.schedulerelationship import ScheduleRelationship as StopTimeUpdateScheduleRelationship

from gtfs_rt_producer_data.generaltransitfeedrealtime.trip.vehicledescriptor import VehicleDescriptor as TripVehicleDescriptor

from gtfs_rt_producer_data.generaltransitfeedstatic.bookingrules import BookingRules

from gtfs_rt_producer_data.generaltransitfeedstatic.fareattributes import FareAttributes

from gtfs_rt_producer_data.generaltransitfeedstatic.farelegrules import FareLegRules

from gtfs_rt_producer_data.generaltransitfeedstatic.faremedia import FareMedia

from gtfs_rt_producer_data.generaltransitfeedstatic.fareproducts import FareProducts

from gtfs_rt_producer_data.generaltransitfeedstatic.farerules import FareRules

from gtfs_rt_producer_data.generaltransitfeedstatic.faretransferrules import FareTransferRules

from gtfs_rt_producer_data.generaltransitfeedstatic.feedinfo import FeedInfo

from gtfs_rt_producer_data.generaltransitfeedstatic.frequencies import Frequencies

from gtfs_rt_producer_data.generaltransitfeedstatic.levels import Levels

from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroups import LocationGroups

from gtfs_rt_producer_data.generaltransitfeedstatic.locationgroupstores import LocationGroupStores

from gtfs_rt_producer_data.generaltransitfeedstatic.networks import Networks

from gtfs_rt_producer_data.generaltransitfeedstatic.pathways import Pathways

from gtfs_rt_producer_data.generaltransitfeedstatic.routenetworks import RouteNetworks

from gtfs_rt_producer_data.generaltransitfeedstatic.routes import Routes

from gtfs_rt_producer_data.generaltransitfeedstatic.shapes import Shapes

from gtfs_rt_producer_data.generaltransitfeedstatic.stopareas import StopAreas

from gtfs_rt_producer_data.generaltransitfeedstatic.stops import Stops

from gtfs_rt_producer_data.generaltransitfeedstatic.timeframes import Timeframes

from gtfs_rt_producer_data.generaltransitfeedstatic.transfers import Transfers

from gtfs_rt_producer_data.generaltransitfeedstatic.translations import Translations

from gtfs_rt_producer_data.generaltransitfeedstatic.trips import Trips

from gtfs_rt_producer_data.generaltransitfeedstatic.agency import Agency

from gtfs_rt_producer_data.generaltransitfeedstatic.areas import Areas

from gtfs_rt_producer_data.generaltransitfeedstatic.attributions import Attributions

from gtfs_rt_producer_data.generaltransitfeedstatic.routetype import RouteType

from gtfs_rt_producer_data.generaltransitfeedstatic.continuousdropoff import ContinuousDropOff

from gtfs_rt_producer_data.generaltransitfeedstatic.continuouspickup import ContinuousPickup

from gtfs_rt_producer_data.generaltransitfeedstatic.locationtype import LocationType

from gtfs_rt_producer_data.generaltransitfeedstatic.wheelchairboarding import WheelchairBoarding

from gtfs_rt_producer_data.generaltransitfeedstatic.stoptimes import StopTimes

from gtfs_rt_producer_data.generaltransitfeedstatic.pickuptype import PickupType

from gtfs_rt_producer_data.generaltransitfeedstatic.timepoint import Timepoint

from gtfs_rt_producer_data.generaltransitfeedstatic.serviceavailability import ServiceAvailability

from gtfs_rt_producer_data.generaltransitfeedstatic.dropofftype import DropOffType

from gtfs_rt_producer_data.generaltransitfeedstatic.exceptiontype import ExceptionType

from gtfs_rt_producer_data.generaltransitfeedstatic.calendardates import CalendarDates

from gtfs_rt_producer_data.generaltransitfeedstatic.calendar import Calendar

from gtfs_rt_producer_data.generaltransitfeedstatic.directionid import DirectionId

from gtfs_rt_producer_data.generaltransitfeedstatic.wheelchairaccessible import WheelchairAccessible

from gtfs_rt_producer_data.generaltransitfeedstatic.bikesallowed import BikesAllowed

import requests

from google.transit import gtfs_realtime_pb2

import sys

import gtfs_rt_producer_data.generaltransitfeedstatic

vehicle_last_report_times = {}

vehicle_last_positions = {}

if sys.gettrace():
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-gtfs/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

# Packaged source catalog shipped inside the wheel/Docker image. Override at
# runtime with GTFS_SOURCES_FILE (a path to a copy of this JSON document).
DEFAULT_SOURCES_FILE = os.path.join(os.path.dirname(__file__), "sources", "gtfs-sources.json")

# ${ENV_VAR} placeholders in catalog string fields are expanded from the
# process environment at load time so secrets never live in the file.
_ENV_REF = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")
_CATALOG_METADATA_KEYS = {"name", "enabled", "description"}


def _interpolate_env(value: Any) -> Any:
    """Expand ${ENV_VAR} placeholders in strings (recursing into lists/dicts)."""
    if isinstance(value, str):
        return _ENV_REF.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    if isinstance(value, dict):
        return {key: _interpolate_env(item) for key, item in value.items()}
    return value


def _read_config_text(raw: str) -> str:
    """Resolve an inline-config string: JSON literal, @path, or bare path."""
    raw = raw.strip()
    if raw.startswith("@"):
        with open(raw[1:].strip(), "r", encoding="utf-8") as handle:
            return handle.read()
    if raw.startswith("[") or raw.startswith("{"):
        return raw
    if os.path.exists(raw):
        with open(raw, "r", encoding="utf-8") as handle:
            return handle.read()
    return raw


def _coerce_entries(data: Any) -> List[Dict[str, Any]]:
    """Accept either a {"sources": [...]} catalog or a bare list of entries."""
    if isinstance(data, dict):
        data = data.get("sources", [])
    if not isinstance(data, list):
        return []
    return [dict(item) for item in data if isinstance(item, dict)]


def select_entries(entries: List[Dict[str, Any]], selector: str = "") -> List[Dict[str, Any]]:
    """Filter catalog entries by the GTFS_SOURCES selector.

    Empty selector -> every entry whose ``enabled`` flag is true (default true).
    ``*`` -> every entry, including disabled templates.
    Otherwise a comma-separated allow-list of entry ``name`` values, returned in
    the order requested. An unknown name raises ``ValueError``.
    """
    selector = (selector or "").strip()
    if selector == "*":
        return list(entries)
    if not selector:
        return [entry for entry in entries if entry.get("enabled", True)]
    by_name = {entry["name"]: entry for entry in entries if entry.get("name")}
    chosen: List[Dict[str, Any]] = []
    unknown: List[str] = []
    for token in (part.strip() for part in selector.split(",")):
        if not token:
            continue
        if token in by_name:
            chosen.append(by_name[token])
        else:
            unknown.append(token)
    if unknown:
        known = ", ".join(sorted(by_name)) or "(none)"
        raise ValueError(f"Unknown GTFS_SOURCES entries: {', '.join(unknown)}. Known names: {known}")
    return chosen


def _normalize_headers(value: Any) -> List[List[str]] | None:
    """Normalize env/CLI/catalog header forms to [[name, value], ...]."""
    if not value:
        return None
    if isinstance(value, dict):
        return [[str(key), str(item)] for key, item in value.items()]
    if isinstance(value, str):
        return [value.split("=", 1)] if "=" in value else None
    if not isinstance(value, list):
        return None
    headers: List[List[str]] = []
    for item in value:
        if isinstance(item, dict):
            headers.extend([[str(key), str(val)] for key, val in item.items()])
        elif isinstance(item, str):
            if "=" in item:
                headers.append(item.split("=", 1))
        elif isinstance(item, (list, tuple)):
            if len(item) == 2 and all(not isinstance(part, (list, tuple, dict)) for part in item):
                headers.append([str(item[0]), str(item[1])])
            else:
                nested = _normalize_headers(list(item))
                if nested:
                    headers.extend(nested)
    return headers or None


def _clean_source_config(entry: Dict[str, Any]) -> Dict[str, Any]:
    item = _interpolate_env(entry)
    config = {key: value for key, value in item.items() if key not in _CATALOG_METADATA_KEYS}
    if "route" not in config or config.get("route") in (None, ""):
        config["route"] = "*"
    config["gtfs_rt_headers"] = _normalize_headers(config.get("gtfs_rt_headers"))
    config["gtfs_headers"] = _normalize_headers(config.get("gtfs_headers"))
    return config


def load_source_configs(
    *,
    gtfs_rt_urls: List[str] | None = None,
    gtfs_urls: List[str] | None = None,
    mdb_source_id: str | None = None,
    agency: str | None = None,
    route: str | None = None,
    gtfs_rt_headers: Any = None,
    gtfs_headers: Any = None,
    sources_file: str = "",
    selector: str = "",
) -> List[Dict[str, Any]]:
    """Resolve GTFS feeds to run.

    Legacy one-feed configuration (GTFS_RT_URLS, GTFS_URLS, or MDB_SOURCE_ID)
    takes precedence over the file catalog. Otherwise the selected catalog
    entries are returned with metadata keys stripped.
    """
    if gtfs_rt_urls or gtfs_urls or mdb_source_id:
        return [
            _clean_source_config(
                {
                    "gtfs_rt_urls": gtfs_rt_urls,
                    "gtfs_urls": gtfs_urls,
                    "mdb_source_id": mdb_source_id,
                    "agency": agency,
                    "route": route or "*",
                    "gtfs_rt_headers": gtfs_rt_headers,
                    "gtfs_headers": gtfs_headers,
                }
            )
        ]

    path = sources_file.strip() if sources_file and sources_file.strip() else DEFAULT_SOURCES_FILE
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as handle:
            entries = _coerce_entries(json.load(handle))
    elif sources_file and sources_file.strip():
        raise FileNotFoundError(path)
    else:
        entries = []
    return [_clean_source_config(entry) for entry in select_entries(entries, selector)]

def fetch_schedule_file(gtfs_url: str, mdb_source_id: str | None, gtfs_headers: list | dict | None, etag: str | None, cache_dir: str | None) -> Tuple[str, str]:
    """
    Fetches the latest schedule file from the schedule URL if the file does not exist in the cache.
    """

    if not gtfs_url:
        gtfs_url = get_gtfs_url(mdb_source_id, cache_dir)

    url_hash = hashlib.sha256(gtfs_url.encode()).hexdigest()
    if not cache_dir:
        cache_dir = os.path.join(os.path.expanduser("~"), ".gtfs_cli", "cache")
    os.makedirs(cache_dir, exist_ok=True)
    schedule_file_path = os.path.join(cache_dir, f"{url_hash}.json")
    if os.path.exists(schedule_file_path):
        # Check if the file is older than 24 hours
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(schedule_file_path))
        if datetime.now() - file_modified_time < timedelta(hours=24):
            return None, schedule_file_path

    # Fetch the latest schedule file
    request_headers: Dict[str, str] = {}
    if gtfs_headers:
        for header in gtfs_headers:
            request_headers[header[0]] = header[1]

    if etag and os.path.exists(schedule_file_path):
        request_headers["If-None-Match"] = etag
    response = requests.get(gtfs_url, headers={**request_headers, "User-Agent": USER_AGENT}, timeout=300, stream=True)
    if response.status_code == 304:
        return etag, schedule_file_path
    etag = response.headers.get("ETag")
    response.raise_for_status()
    # stream the binary file to the cache directory in chunks to avoid
    # holding the entire response (potentially hundreds of MB) in memory
    with open(schedule_file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            f.write(chunk)
    return etag, schedule_file_path

def calculate_file_hashes(schedule_file_path: str):
    """Calculates the hash for each *.txt file in the given schedule file"""
    hashes = {}
    with ZipFile(schedule_file_path) as schedule_zip:
        for file_name in schedule_zip.namelist():
            if file_name.endswith('.txt'):
                h = hashlib.sha256()
                with schedule_zip.open(file_name) as f:
                    while True:
                        chunk = f.read(65536)
                        if not chunk:
                            break
                        h.update(chunk)
                hashes[file_name] = h.hexdigest()
    return hashes

def read_file_hashes(schedule_file_path: str, cache_dir: str | None) -> dict:
    """Reads the file hashes from the given file path"""
    if not cache_dir:
        cache_dir = cache_dir = os.path.join(os.path.expanduser("~"), ".gtfs_cli", "cache")
    hashes_file_path = os.path.join(cache_dir, f"{os.path.basename(schedule_file_path)}.hashes.json")
    if not os.path.exists(hashes_file_path):
        return {}
    with open(hashes_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_file_hashes(schedule_file_path: str, hashes: dict, cache_dir: str | None):
    """Writes the file hashes to the given file path"""
    if not cache_dir:
        cache_dir = cache_dir = os.path.join(os.path.expanduser("~"), ".gtfs_cli", "cache")
    hashes_file_path = os.path.join(cache_dir, f"{os.path.basename(schedule_file_path)}.hashes.json")
    with open(hashes_file_path, 'w', encoding="utf-8") as f:
        json.dump(hashes, f)

def read_schedule_file_contents(schedule_file_path: str, file_name: str) -> List[Dict[str, Any]]:
    """Reads the contents of the given file name from the given schedule file"""
    with ZipFile(schedule_file_path) as schedule_zip:
        if file_name not in schedule_zip.namelist():
            return []
        with schedule_zip.open(file_name, "r") as f:
            # f is a byte stream, so decode it to utf-8
            reader = csv.DictReader(io.TextIOWrapper(f, 'utf-8'))
            return [row for row in reader]

def iter_schedule_file_contents(schedule_file_path: str, file_name: str) -> Generator[Dict[str, Any], None, None]:
    """Yields rows one at a time from a CSV inside the schedule ZIP, avoiding
    full materialization of very large files like stop_times.txt."""
    with ZipFile(schedule_file_path) as schedule_zip:
        if file_name not in schedule_zip.namelist():
            return
        with schedule_zip.open(file_name, "r") as f:
            reader = csv.DictReader(io.TextIOWrapper(f, 'utf-8'))
            yield from reader

hashes_vehicles: Dict[str, int] = {}

hashes_trip: Dict[str, int] = {}

hashes_alert: Dict[str, int] = {}

def map_agency(rows: Iterable[Dict[str, Any]]) -> Generator[Agency, None, None]:
    """Maps the rows from the agency.txt file to Agency objects"""
    for row in rows:
        yield Agency(
            agencyId=str(row.get("agency_id")) if row.get("agency_id") is not None else None,  # type: ignore[arg-type]
            agencyName=str(row.get("agency_name")) if row.get("agency_name") is not None else None,  # type: ignore[arg-type]
            agencyUrl=str(row.get("agency_url")) if row.get("agency_url") is not None else None,  # type: ignore[arg-type]
            agencyTimezone=str(row.get("agency_timezone")) if row.get("agency_timezone") is not None else None,  # type: ignore[arg-type]
            agencyLang=row.get("agency_lang"),
            agencyPhone=row.get("agency_phone"),
            agencyFareUrl=row.get("agency_fare_url"),
            agencyEmail=row.get("agency_email")
        )

def map_areas(rows: Iterable[Dict[str, Any]]) -> Generator[Areas, None, None]:
    """Maps the rows from the areas.txt file to Areas objects"""
    for row in rows:
        yield Areas(
            areaId=str(row.get("area_id")) if row.get("area_id") is not None else None,  # type: ignore[arg-type]
            areaName=str(row.get("area_name")) if row.get("area_name") is not None else None,  # type: ignore[arg-type]
            areaDesc=row.get("area_desc"),
            areaUrl=row.get("area_url"),
        )

def map_attributions(rows: Iterable[Dict[str, Any]]) -> Generator[Attributions, None, None]:
    """Maps the rows from the attributions.txt file to Attributions objects"""
    for row in rows:
        yield Attributions(
            attributionId=row.get("attribution_id", row.get("trip_id", uuid.uuid4().hex)),
            agencyId=row.get("agency_id"),
            routeId=row.get("route_id"),
            tripId=row.get("trip_id"),
            organizationName=str(row.get("organization_name")) if row.get("organization_name") is not None else None,  # type: ignore[arg-type]
            isProducer=int(row.get("is_producer") or 0),
            isOperator=int(row.get("is_operator") or 0),
            isAuthority=int(row.get("is_authority") or 0),
            attributionUrl=row.get("attribution_url"),
            attributionEmail=row.get("attribution_email"),
            attributionPhone=row.get("attribution_phone")
        )

def map_booking_rules(rows: Iterable[Dict[str, Any]]) -> Generator[BookingRules, None, None]:
    """Maps the rows from the booking_rules.txt file to BookingRules objects"""
    for row in rows:
        yield BookingRules(
            bookingRuleId=str(row.get("booking_rule_id")) if row.get("booking_rule_id") is not None else None,  # type: ignore[arg-type]
            bookingRuleName=str(row.get("booking_rule_name")) if row.get("booking_rule_name") is not None else None,  # type: ignore[arg-type]
            bookingRuleDesc=row.get("booking_rule_desc"),
            bookingRuleUrl=row.get("booking_rule_url")
        )

def map_fare_attributes(rows: Iterable[Dict[str, Any]]) -> Generator[FareAttributes, None, None]:
    """Maps the rows from the fare_attributes.txt file to FareAttributes objects"""
    for row in rows:
        yield FareAttributes(
            fareId=str(row.get("fare_id")) if row.get("fare_id") is not None else None,  # type: ignore[arg-type]
            price=float(row.get("price") or 0),
            currencyType=str(row.get("currency_type")) if row.get("currency_type") is not None else None,  # type: ignore[arg-type]
            paymentMethod=int(row.get("payment_method") or 0),
            transfers=int(row.get("transfers") or 0),
            agencyId=row.get("agency_id"),
            transferDuration=int(row.get("transfer_duration") or 0)
        )

def map_fare_leg_rules(rows: Iterable[Dict[str, Any]]) -> Generator[FareLegRules, None, None]:
    """Maps the rows from the fare_leg_rules.txt file to FareLegRules objects"""
    for row in rows:
        yield FareLegRules(
            fareLegRuleId=str(row.get("fare_leg_rule_id")) if row.get("fare_leg_rule_id") is not None else None,  # type: ignore[arg-type]
            fareProductId=str(row.get("fare_product_id")) if row.get("fare_product_id") is not None else None,  # type: ignore[arg-type]
            legGroupId=row.get("leg_group_id"),
            networkId=row.get("network_id"),
            fromAreaId=row.get("from_area_id"),
            toAreaId=row.get("to_area_id")
        )

def map_fare_media(rows: Iterable[Dict[str, Any]]) -> Generator[FareMedia, None, None]:
    """Maps the rows from the fare_media.txt file to FareMedia objects"""
    for row in rows:
        yield FareMedia(
            fareMediaId=str(row.get("fare_media_id")) if row.get("fare_media_id") is not None else None,  # type: ignore[arg-type]
            fareMediaName=str(row.get("fare_media_name")) if row.get("fare_media_name") is not None else None,  # type: ignore[arg-type]
            fareMediaDesc=row.get("fare_media_desc"),
            fareMediaUrl=row.get("fare_media_url")
        )

def map_fare_products(rows: Iterable[Dict[str, Any]]) -> Generator[FareProducts, None, None]:
    """Maps the rows from the fare_products.txt file to FareProducts objects"""
    for row in rows:
        yield FareProducts(
            fareProductId=str(row.get("fare_product_id")) if row.get("fare_product_id") is not None else None,  # type: ignore[arg-type]
            fareProductName=str(row.get("fare_product_name")) if row.get("fare_product_name") is not None else None,  # type: ignore[arg-type]
            fareProductDesc=row.get("fare_product_desc"),
            fareProductUrl=row.get("fare_product_url")
        )

def map_fare_rules(rows: Iterable[Dict[str, Any]]) -> Generator[FareRules, None, None]:
    """Maps the rows from the fare_rules.txt file to FareRules objects"""
    for row in rows:
        yield FareRules(
            fareId=str(row.get("fare_id")) if row.get("fare_id") is not None else None,  # type: ignore[arg-type]
            routeId=row.get("route_id"),
            originId=row.get("origin_id"),
            destinationId=row.get("destination_id"),
            containsId=row.get("contains_id")
        )

def map_fare_transfer_rules(rows: Iterable[Dict[str, Any]]) -> Generator[FareTransferRules, None, None]:
    """Maps the rows from the fare_transfer_rules.txt file to FareTransferRules objects"""
    for row in rows:
        yield FareTransferRules(
            fareTransferRuleId=str(row.get("fare_transfer_rule_id")) if row.get("fare_transfer_rule_id") is not None else None,  # type: ignore[arg-type]
            fareProductId=str(row.get("fare_product_id")) if row.get("fare_product_id") is not None else None,  # type: ignore[arg-type]
            transferCount=int(row.get("transfer_count") or 0),
            fromLegGroupId=row.get("from_leg_group_id"),
            toLegGroupId=row.get("to_leg_group_id"),
            duration=int(row.get("duration") or 0),
            durationType=row.get("duration_type")
        )

def map_feed_info(rows: Iterable[Dict[str, Any]]) -> Generator[FeedInfo, None, None]:
    """Maps the rows from the feed_info.txt file to FeedInfo objects"""
    for row in rows:
        yield FeedInfo(
            feedPublisherName=str(row.get("feed_publisher_name")) if row.get("feed_publisher_name") is not None else None,  # type: ignore[arg-type]
            feedPublisherUrl=str(row.get("feed_publisher_url")) if row.get("feed_publisher_url") is not None else None,  # type: ignore[arg-type]
            feedLang=str(row.get("feed_lang")) if row.get("feed_lang") is not None else None,  # type: ignore[arg-type]
            defaultLang=row.get("default_lang"),
            feedStartDate=row.get("feed_start_date"),
            feedEndDate=row.get("feed_end_date"),
            feedVersion=row.get("feed_version"),
            feedContactEmail=row.get("feed_contact_email"),
            feedContactUrl=row.get("feed_contact_url")
        )

def map_frequencies(rows: Iterable[Dict[str, Any]]) -> Generator[Frequencies, None, None]:
    """Maps the rows from the frequencies.txt file to Frequencies objects"""
    for row in rows:
        yield Frequencies(
            tripId=str(row.get("trip_id")) if row.get("trip_id") is not None else None,  # type: ignore[arg-type]
            startTime=str(row.get("start_time")) if row.get("start_time") is not None else None,  # type: ignore[arg-type]
            endTime=str(row.get("end_time")) if row.get("end_time") is not None else None,  # type: ignore[arg-type]
            headwaySecs=int(row.get("headway_secs") or 0),
            exactTimes=int(row.get("exact_times") or 0)
        )

def map_levels(rows: Iterable[Dict[str, Any]]) -> Generator[Levels, None, None]:
    """Maps the rows from the levels.txt file to Levels objects"""
    for row in rows:
        yield Levels(
            levelId=str(row.get("level_id")) if row.get("level_id") is not None else None,  # type: ignore[arg-type]
            levelIndex=float(row.get("level_index") or 0),
            levelName=row.get("level_name")
        )

def map_location_groups(rows: Iterable[Dict[str, Any]]) -> Generator[LocationGroups, None, None]:
    """Maps the rows from the location_groups.txt file to LocationGroups objects"""
    for row in rows:
        yield LocationGroups(
            locationGroupId=str(row.get("location_group_id")) if row.get("location_group_id") is not None else None,  # type: ignore[arg-type]
            locationGroupName=str(row.get("location_group_name")) if row.get("location_group_name") is not None else None,  # type: ignore[arg-type]
            locationGroupDesc=row.get("location_group_desc"),
            locationGroupUrl=row.get("location_group_url")
        )

def map_location_group_stores(rows: Iterable[Dict[str, Any]]) -> Generator[LocationGroupStores, None, None]:
    """Maps the rows from the location_group_stores.txt file to LocationGroupStores objects"""
    for row in rows:
        yield LocationGroupStores(
            locationGroupStoreId=str(row.get("location_group_store_id")) if row.get("location_group_store_id") is not None else None,  # type: ignore[arg-type]
            locationGroupId=str(row.get("location_group_id")) if row.get("location_group_id") is not None else None,  # type: ignore[arg-type]
            storeId=str(row.get("store_id")) if row.get("store_id") is not None else None  # type: ignore[arg-type]
        )

def map_networks(rows: Iterable[Dict[str, Any]]) -> Generator[Networks, None, None]:
    """Maps the rows from the networks.txt file to Networks objects"""
    for row in rows:
        yield Networks(
            networkId=str(row.get("network_id")) if row.get("network_id") is not None else None,  # type: ignore[arg-type]
            networkName=str(row.get("network_name")) if row.get("network_name") is not None else None,  # type: ignore[arg-type]
            networkDesc=row.get("network_desc"),
            networkUrl=row.get("network_url")
        )

def map_pathways(rows: Iterable[Dict[str, Any]]) -> Generator[Pathways, None, None]:
    """Maps the rows from the pathways.txt file to Pathways objects"""
    for row in rows:
        yield Pathways(
            pathwayId=str(row.get("pathway_id")) if row.get("pathway_id") is not None else None,  # type: ignore[arg-type]
            fromStopId=str(row.get("from_stop_id")) if row.get("from_stop_id") is not None else None,  # type: ignore[arg-type]
            toStopId=str(row.get("to_stop_id")) if row.get("to_stop_id") is not None else None,  # type: ignore[arg-type]
            pathwayMode=int(row.get("pathway_mode") or 0),
            isBidirectional=int(row.get("is_bidirectional") or 0),
            length=float(row.get("length") or 0),
            traversalTime=int(row.get("traversal_time") or 0),
            stairCount=int(row.get("stair_count") or 0),
            maxSlope=float(row.get("max_slope") or 0),
            minWidth=float(row.get("min_width") or 0),
            signpostedAs=row.get("signposted_as"),
            reversedSignpostedAs=row.get("reversed_signposted_as")
        )

def map_route_networks(rows: Iterable[Dict[str, Any]]) -> Generator[RouteNetworks, None, None]:
    """Maps the rows from the route_networks.txt file to RouteNetworks objects"""
    for row in rows:
        yield RouteNetworks(
            routeNetworkId=str(row.get("route_network_id")) if row.get("route_network_id") is not None else None,  # type: ignore[arg-type]
            routeId=str(row.get("route_id")) if row.get("route_id") is not None else None,  # type: ignore[arg-type]
            networkId=str(row.get("network_id")) if row.get("network_id") is not None else None  # type: ignore[arg-type]
        )

def map_routes(rows: Iterable[Dict[str, Any]]) -> Generator[Routes, None, None]:
    """Maps the rows from the routes.txt file to Routes objects"""
    for row in rows:
        yield Routes(
            routeId=str(row.get("route_id")) if row.get("route_id") is not None else None,  # type: ignore[arg-type]
            agencyId=row.get("agency_id"),
            routeShortName=row.get("route_short_name"),
            routeLongName=row.get("route_long_name"),
            routeDesc=row.get("route_desc"),
            routeType=RouteType.from_ordinal(row.get("route_type")) if row.get(  # type: ignore[arg-type]
                "route_type") and (int(row.get("route_type") or 0) < 12) else RouteType.OTHER,
            routeUrl=row.get("route_url"),
            routeColor=row.get("route_color"),
            routeTextColor=row.get("route_text_color"),
            routeSortOrder=int(row.get("route_sort_order") or 0),
            continuousPickup=ContinuousPickup.from_ordinal(row.get("continuous_pickup")) if row.get(  # type: ignore[arg-type]
                "continuous_pickup") else ContinuousPickup.NO_CONTINUOUS_STOPPING,
            continuousDropOff=ContinuousDropOff.from_ordinal(row.get("continuous_drop_off")) if row.get(  # type: ignore[arg-type]
                "continuous_drop_off") else ContinuousDropOff.NO_CONTINUOUS_STOPPING,
            networkId=row.get("network_id")
        )

def map_shapes(rows: Iterable[Dict[str, Any]]) -> Generator[Shapes, None, None]:
    """Maps the rows from the shapes.txt file to Shapes objects"""
    for row in rows:
        yield Shapes(
            shapeId=str(row.get("shape_id")) if row.get("shape_id") is not None else None,  # type: ignore[arg-type]
            shapePtLat=float(row.get("shape_pt_lat") or 0),
            shapePtLon=float(row.get("shape_pt_lon") or 0),
            shapePtSequence=int(row.get("shape_pt_sequence") or 0),
            shapeDistTraveled=float(row.get("shape_dist_traveled") or 0)
        )

def map_stop_areas(rows: Iterable[Dict[str, Any]]) -> Generator[StopAreas, None, None]:
    """Maps the rows from the stop_areas.txt file to StopAreas objects"""
    for row in rows:
        yield StopAreas(
            stopAreaId=str(row.get("stop_area_id")) if row.get("stop_area_id") is not None else None,  # type: ignore[arg-type]
            areaId=str(row.get("area_id")) if row.get("area_id") is not None else None,  # type: ignore[arg-type]
            stopId=str(row.get("stop_id")) if row.get("stop_id") is not None else None,  # type: ignore[arg-type]
        )

def map_stops(rows: Iterable[Dict[str, Any]]) -> Generator[Stops, None, None]:
    """Maps the rows from the stops.txt file to Stops objects"""
    for row in rows:
        yield Stops(
            stopId=str(row.get("stop_id")) if row.get("stop_id") is not None else None,  # type: ignore[arg-type]
            stopCode=row.get("stop_code"),
            stopName=row.get("stop_name"),
            stopDesc=row.get("stop_desc"),
            stopLat=float(row.get("stop_lat") or 0),
            stopLon=float(row.get("stop_lon") or 0),
            zoneId=row.get("zone_id"),
            stopUrl=row.get("stop_url"),
            locationType=LocationType.from_ordinal(row.get("location_type")) if row.get("location_type") else LocationType.STOP,  # type: ignore[arg-type]
            parentStation=row.get("parent_station"),
            stopTimezone=row.get("stop_timezone"),
            wheelchairBoarding=WheelchairBoarding.from_ordinal(row.get("wheelchair_boarding")) if row.get("wheelchair_boarding") else WheelchairBoarding.NO_INFO,  # type: ignore[arg-type]
            levelId=row.get("level_id"),
            platformCode=row.get("platform_code"),
            ttsStopName=row.get("tts_stop_name"),
        )

def map_stop_times(rows: Iterable[Dict[str, Any]]) -> Generator[StopTimes, None, None]:
    """Maps the rows from the stop_times.txt file to StopTimes objects"""
    for row in rows:
        yield StopTimes(
            tripId=str(row.get("trip_id")) if row.get("trip_id") is not None else None,  # type: ignore[arg-type]
            arrivalTime=row.get("arrival_time"),
            departureTime=row.get("departure_time"),
            stopId=row.get("stop_id"),
            stopSequence=int(row.get("stop_sequence") or 0),
            stopHeadsign=row.get("stop_headsign"),
            pickupType=PickupType.from_ordinal(row.get("pickup_type")) if row.get("pickup_type") else PickupType.REGULAR,  # type: ignore[arg-type]
            dropOffType=DropOffType.from_ordinal(row.get("drop_off_type")) if row.get("drop_off_type") else DropOffType.REGULAR,  # type: ignore[arg-type]
            continuousPickup=ContinuousPickup.from_ordinal(row.get("continuous_pickup")) if row.get("continuous_pickup") else ContinuousPickup.NO_CONTINUOUS_STOPPING,  # type: ignore[arg-type]
            continuousDropOff=ContinuousDropOff.from_ordinal(row.get("continuous_drop_off")) if row.get("continuous_drop_off") else ContinuousDropOff.NO_CONTINUOUS_STOPPING,  # type: ignore[arg-type]
            shapeDistTraveled=row.get("shape_dist_traveled"),
            timepoint=Timepoint.from_ordinal(row.get("timepoint")) if row.get("timepoint") else Timepoint.EXACT  # type: ignore[arg-type]
        )

def map_timeframes(rows: Iterable[Dict[str, Any]], calendar_rows: List[Dict[str, Any]], calendar_dates_rows: List[Dict[str, Any]]) -> Generator[Timeframes, None, None]:
    """Maps the rows from the timeframes.txt file to Timeframes objects"""
    for row in rows:
        service_dates = [
            Calendar(
                serviceId=str(calendarRow.get("service_id")) if calendarRow.get("service_id") is not None else None,  # type: ignore[arg-type]
                startDate=str(calendarRow.get("start_date")) if calendarRow.get("start_date") is not None else None,  # type: ignore[arg-type]
                endDate=str(calendarRow.get("end_date")) if calendarRow.get("end_date") is not None else None,  # type: ignore[arg-type]
                monday=ServiceAvailability.from_ordinal(calendarRow.get("monday")) if calendarRow.get(  # type: ignore[arg-type]
                    "monday") else ServiceAvailability.NO_SERVICE,
                tuesday=ServiceAvailability.from_ordinal(calendarRow.get("tuesday")) if calendarRow.get(  # type: ignore[arg-type]
                    "tuesday") else ServiceAvailability.NO_SERVICE,
                wednesday=ServiceAvailability.from_ordinal(calendarRow.get("wednesday")) if calendarRow.get(  # type: ignore[arg-type]
                    "wednesday") else ServiceAvailability.NO_SERVICE,
                thursday=ServiceAvailability.from_ordinal(calendarRow.get("thursday")) if calendarRow.get(  # type: ignore[arg-type]
                    "thursday") else ServiceAvailability.NO_SERVICE,
                friday=ServiceAvailability.from_ordinal(calendarRow.get("friday")) if calendarRow.get(  # type: ignore[arg-type]
                    "friday") else ServiceAvailability.NO_SERVICE,
                saturday=ServiceAvailability.from_ordinal(calendarRow.get("saturday")) if calendarRow.get(  # type: ignore[arg-type]
                    "saturday") else ServiceAvailability.NO_SERVICE,
                sunday=ServiceAvailability.from_ordinal(calendarRow.get("sunday")) if calendarRow.get("sunday") else ServiceAvailability.NO_SERVICE)  # type: ignore[arg-type]
            for calendarRow in calendar_rows if calendarRow.get("service_id") == row.get("service_id")
        ] + [
            CalendarDates(
                serviceId=str(calendarDatesRow.get("service_id")) if calendarDatesRow.get("service_id") is not None else None,  # type: ignore[arg-type]
                date=str(calendarDatesRow.get("date")) if calendarDatesRow.get("date") is not None else None,  # type: ignore[arg-type]
                exceptionType=ExceptionType.from_ordinal(calendarDatesRow.get("exception_type")) if calendarDatesRow.get("exception_type") else ExceptionType.SERVICE_REMOVED)  # type: ignore[arg-type]
            for calendarDatesRow in calendar_dates_rows if calendarDatesRow.get("service_id") == row.get("service_id")
        ]

        yield Timeframes(
            timeframeGroupId=str(row.get("timeframe_group_id")) if row.get("timeframe_group_id") is not None else None,  # type: ignore[arg-type]
            startTime=row.get("start_time"),
            endTime=row.get("end_time"),
            serviceDates=next(iter(service_dates))
        )

def map_transfers(rows: Iterable[Dict[str, Any]]) -> Generator[Transfers, None, None]:
    """Maps the rows from the transfers.txt"""
    for row in rows:
        yield Transfers(
            fromStopId=str(row.get("from_stop_id")) if row.get("from_stop_id") is not None else None,  # type: ignore[arg-type]
            toStopId=str(row.get("to_stop_id")) if row.get("to_stop_id") is not None else None,  # type: ignore[arg-type]
            transferType=int(row.get("transfer_type") or 0),
            minTransferTime=int(row.get("min_transfer_time") or 0)
        )

def map_translations(rows: Iterable[Dict[str, Any]]) -> Generator[Translations, None, None]:
    """Maps the rows from the translations.txt file to Translations objects"""
    for row in rows:
        yield Translations(
            tableName=str(row.get("table_name")) if row.get("table_name") is not None else None,  # type: ignore[arg-type]
            fieldName=str(row.get("field_name")) if row.get("field_name") is not None else None,  # type: ignore[arg-type]
            language=str(row.get("language")) if row.get("language") is not None else None,  # type: ignore[arg-type]
            translation=str(row.get("translation")) if row.get("translation") is not None else None  # type: ignore[arg-type]
        )

def map_trips(trip_rows: Iterable[Dict[str, Any]], calendar_rows: List[Dict[str, Any]], calendar_dates_rows: List[Dict[str, Any]]) -> Generator[Trips, None, None]:
    """Maps the rows from the trips.txt file to Trips objects"""

    # we do some indexing here because the combinations of the files can be enormous
    calendar_rows_by_service: Dict[str, List[Dict[str, Any]]] = {}
    for calendar_row in calendar_rows:
        service_id = calendar_row.get("service_id")
        if service_id not in calendar_rows_by_service:
            calendar_rows_by_service[service_id] = []
        calendar_rows_by_service[service_id].append(calendar_row)
    calendar_dates_rows_by_service: Dict[str, List[Dict[str, Any]]] = {}
    for calendar_dates_row in calendar_dates_rows:
        service_id = calendar_dates_row.get("service_id")
        if service_id not in calendar_dates_rows_by_service:
            calendar_dates_rows_by_service[service_id] = []
        calendar_dates_rows_by_service[service_id].append(calendar_dates_row)

    for row in trip_rows:
        calendar_dates = []
        calendars = []
        for calendar_row in calendar_rows_by_service.get(row.get("service_id") or "", []):
            calendars.append(
                Calendar(
                    serviceId=str(calendar_row.get("service_id")) if calendar_row.get("service_id") is not None else None,  # type: ignore[arg-type]
                    monday=ServiceAvailability.from_ordinal(calendar_row.get("monday")) if calendar_row.get("monday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    tuesday=ServiceAvailability.from_ordinal(calendar_row.get("tuesday")) if calendar_row.get("tuesday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    wednesday=ServiceAvailability.from_ordinal(calendar_row.get("wednesday")) if calendar_row.get("wednesday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    thursday=ServiceAvailability.from_ordinal(calendar_row.get("thursday")) if calendar_row.get("thursday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    friday=ServiceAvailability.from_ordinal(calendar_row.get("friday")) if calendar_row.get("friday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    saturday=ServiceAvailability.from_ordinal(calendar_row.get("saturday")) if calendar_row.get("saturday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    sunday=ServiceAvailability.from_ordinal(calendar_row.get("sunday")) if calendar_row.get("sunday") else ServiceAvailability.NO_SERVICE,  # type: ignore[arg-type]
                    startDate=str(calendar_row.get("start_date")) if calendar_row.get("start_date") is not None else None,  # type: ignore[arg-type]
                    endDate=str(calendar_row.get("end_date")) if calendar_row.get("end_date") is not None else None  # type: ignore[arg-type]
                )
            )

        for calendar_dates_row in calendar_dates_rows_by_service.get(row.get("service_id") or "", []):
            calendar_dates.append(
                CalendarDates(
                    serviceId=str(calendar_dates_row.get("service_id")) if calendar_dates_row.get("service_id") is not None else None,  # type: ignore[arg-type]
                    date=str(calendar_dates_row.get("date")) if calendar_dates_row.get("date") is not None else None,  # type: ignore[arg-type]
                    exceptionType=ExceptionType.from_ordinal(calendar_dates_row.get("exception_type")) if calendar_dates_row.get("exception_type") and int(calendar_dates_row.get("exception_type") or 0) < 2 else ExceptionType.SERVICE_REMOVED  # type: ignore[arg-type]
                )
            )

        yield Trips(
            routeId=str(row.get("route_id")) if row.get("route_id") is not None else None,  # type: ignore[arg-type]
            serviceDates=calendars[0] if len(calendars) > 0 else None,  # type: ignore[arg-type]
            serviceExceptions=calendar_dates,
            tripId=str(row.get("trip_id")) if row.get("trip_id") is not None else None,  # type: ignore[arg-type]
            tripHeadsign=row.get("trip_headsign"),
            tripShortName=row.get("trip_short_name"),
            directionId=DirectionId.from_ordinal(row.get("direction_id")) if row.get("direction_id") else DirectionId.OUTBOUND,  # type: ignore[arg-type]
            blockId=row.get("block_id"),
            shapeId=row.get("shape_id"),
            wheelchairAccessible=WheelchairAccessible.from_ordinal(row.get("wheelchair_accessible")) if row.get("wheelchair_accessible") else WheelchairAccessible.NO_INFO,  # type: ignore[arg-type]
            bikesAllowed=BikesAllowed.from_ordinal(row.get("bikes_allowed")) if row.get("bikes_allowed") else BikesAllowed.NO_INFO  # type: ignore[arg-type]
        )

etags = {}

async def print_feed_items(feed_url: str, mdb_source_id: str, gtfs_rt_headers: List[List[str]], cache_dir: str | None):
    """Prints the GTFS Realtime feed items to the console"""
    if not feed_url and mdb_source_id:
        feed_url = get_gtfs_rt_url(mdb_source_id, cache_dir)

    if not feed_url:
        raise ValueError("No GTFS Realtime URL specified")

    headers: Dict[str, str] = {}
    if gtfs_rt_headers:
        for header in gtfs_rt_headers:
            headers[header[0]] = header[1]

    # Make a request to the GTFS Realtime API to get the vehicle locations for the specified route
    response = requests.get(feed_url, headers={**headers, "User-Agent": USER_AGENT}, timeout=10)
    response.raise_for_status()

    # Parse the Protocol Buffer message and submit each vehicle location to the Event Hub
    try:
        # pylint: disable=no-member
        incoming_feed_message = gtfs_realtime_pb2.FeedMessage()
        # pylint: enable=no-member
        incoming_feed_message.ParseFromString(response.content)
    # pylint: disable=broad-except
    except Exception as e:
        raise ValueError("Failed to parse the GTFS Realtime message") from e

    # pylint: disable=no-member
    print("[")
    count = len(incoming_feed_message.entity)
    for i, entity in enumerate(incoming_feed_message.entity):
        if entity.vehicle and entity.vehicle.trip and entity.vehicle.trip.trip_id:
            vehicle = map_vehicle_position(entity)
            print(vehicle.to_json() + ("," if i+1 < count else ""))
        if entity.alert and entity.alert.active_period and entity.alert.informed_entity:
            alert = map_alert(entity)
            print(alert.to_json()+ ("," if i+1 < count else ""))
        if entity.trip_update and entity.trip_update.trip and entity.trip_update.trip.trip_id:
            trip_update = map_trip_update(entity)
            trip_update = remove_nulls(trip_update)
            print(trip_update.to_json() + ("," if i+1 < count else ""))
    print("]")

def map_vehicle_position(e):
    """Maps the GTFS Realtime VehiclePosition entity to a VehiclePosition object"""
    vehicle = VehiclePosition(
                trip=PositionTripDescriptor(
                    trip_id=e.vehicle.trip.trip_id,
                    route_id=e.vehicle.trip.route_id,
                    direction_id=e.vehicle.trip.direction_id,
                    start_time=e.vehicle.trip.start_time,
                    start_date=e.vehicle.trip.start_date,
                    schedule_relationship=PositionScheduleRelationship.from_ordinal(e.vehicle.trip.schedule_relationship)) if e.vehicle.trip else None,
                vehicle=PositionVehicleDescriptor(
                    id=e.vehicle.vehicle.id,
                    label=e.vehicle.vehicle.label,
                    license_plate=e.vehicle.vehicle.license_plate) if e.vehicle.vehicle else None,
                position=Position(
                    latitude=e.vehicle.position.latitude,
                    longitude=e.vehicle.position.longitude,
                    bearing=e.vehicle.position.bearing,
                    odometer=e.vehicle.position.odometer,
                    speed=e.vehicle.position.speed) if e.vehicle.position else None,
                current_stop_sequence=e.vehicle.current_stop_sequence,
                stop_id=e.vehicle.stop_id,
                current_status=VehicleStopStatus.from_ordinal(e.vehicle.current_status),
                timestamp=e.vehicle.timestamp,
                congestion_level=CongestionLevel.from_ordinal(e.vehicle.congestion_level),
                occupancy_status=OccupancyStatus.from_ordinal(e.vehicle.occupancy_status))
    return vehicle

def map_trip_update(entity):
    """Maps the GTFS Realtime TripUpdate entity to a TripUpdate object"""
    trip_update = TripUpdate(
                trip=TripTripDescriptor(
                    trip_id=entity.trip_update.trip.trip_id,
                    route_id=entity.trip_update.trip.route_id,
                    direction_id=entity.trip_update.trip.direction_id,
                    start_time=entity.trip_update.trip.start_time,
                    start_date=entity.trip_update.trip.start_date,
                    schedule_relationship=TripScheduleRelationship.from_ordinal(entity.trip_update.trip.schedule_relationship)
                ),
                vehicle=TripVehicleDescriptor(
                    id=entity.trip_update.vehicle.id,
                    label=entity.trip_update.vehicle.label,
                    license_plate=entity.trip_update.vehicle.license_plate
                ),
                stop_time_update=[StopTimeUpdate(
                    stop_sequence=stop_time_update.stop_sequence,
                    stop_id=stop_time_update.stop_id,
                    arrival=StopTimeEvent(
                        delay=stop_time_update.arrival.delay,
                        time=stop_time_update.arrival.time,
                        uncertainty=stop_time_update.arrival.uncertainty
                    ),
                    departure=StopTimeEvent(
                        delay=stop_time_update.departure.delay,
                        time=stop_time_update.departure.time,
                        uncertainty=stop_time_update.departure.uncertainty
                    ),
                    schedule_relationship=StopTimeUpdateScheduleRelationship.from_ordinal(stop_time_update.schedule_relationship)
                ) for stop_time_update in entity.trip_update.stop_time_update],
                timestamp=entity.trip_update.timestamp,
                delay=entity.trip_update.delay
            )
    return trip_update

def map_alert(entity):
    """Maps the GTFS Realtime Alert entity to an Alert object"""
    alert = Alert(
                active_period=[TimeRange(start=period.start, end=period.end) for period in entity.alert.active_period],
                informed_entity=[EntitySelector(
                    agency_id=selector.agency_id,
                    route_id=selector.route_id,
                    route_type=selector.route_type,
                    stop_id=selector.stop_id,
                    trip=AlertTripDescriptor(
                        trip_id=selector.trip.trip_id,
                        route_id=selector.trip.route_id,
                        direction_id=selector.trip.direction_id,
                        start_time=selector.trip.start_time,
                        start_date=selector.trip.start_date,
                        schedule_relationship=selector.trip.schedule_relationship
                    )
                ) for selector in entity.alert.informed_entity],
                cause=Cause.from_ordinal(entity.alert.cause),
                effect=Effect.from_ordinal(entity.alert.effect),
                url=TranslatedString(translation=[Translation(language=translation.language, text=translation.text) for translation in entity.alert.url.translation]),
                header_text=TranslatedString(translation=[Translation(language=translation.language, text=translation.text) for translation in entity.alert.header_text.translation]),
                description_text=TranslatedString(translation=[Translation(language=translation.language, text=translation.text) for translation in entity.alert.description_text.translation])
            )
    return alert

def create_gtfs_sources_dir(cache_dir: str | None):
    # Check if Git is installed
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        logger.info("Git is not installed.")
        return

    # Clone the mobility-database-catalogs repository if it does not exist
    mobility_database_catalogs_dir = get_mobility_database_dir(cache_dir)
    if not os.path.exists(mobility_database_catalogs_dir):
        try:
            subprocess.run(["git", "clone", "https://github.com/MobilityData/mobility-database-catalogs.git",
                           mobility_database_catalogs_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=2)
        except subprocess.TimeoutExpired:
            logger.info("Cloning the mobility-database-catalogs repository timed out.")
        except subprocess.CalledProcessError as e:
            logger.info("Error cloning the mobility-database-catalogs repository: %s", e.stderr.decode().strip())

    # Refresh the files with a pull
    try:
        subprocess.run(["git", "pull"], cwd=mobility_database_catalogs_dir,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=2)
    except subprocess.TimeoutExpired:
        logger.info("Pulling the mobility-database-catalogs repository timed out.")
    except subprocess.CalledProcessError as e:
        logger.info("Error pulling the mobility-database-catalogs repository: %s", e.stderr.decode().strip())

def get_mobility_database_dir(cache_dir: str | None):
    mobility_database_catalogs_dir = os.path.join(get_gtfs_sources_dir(cache_dir), "mobility-database-catalogs")
    return mobility_database_catalogs_dir

def get_gtfs_sources_dir(cache_dir: str | None):
    if cache_dir:
        profile_dir = cache_dir
    else:
        profile_dir = os.path.expanduser("~")
    gtfs_sources_dir = os.path.join(profile_dir, ".gtfs-sources")

    # Create the directory if it does not exist
    if not os.path.exists(gtfs_sources_dir):
        os.mkdir(gtfs_sources_dir)
    return gtfs_sources_dir

def get_gtfs_rt_url(mdb_source_id, cache_dir: str | None = None):
    """
    Helper function to look up the GTFS-RT URL from the JSON files in the clone repository's catalogs/sources/gtfs/realtime directory.
    the mdb_source_id is appended to the filename of each JSON file, so filter the files by mdb_source_id.
    """
    create_gtfs_sources_dir(cache_dir)
    gtfs_rt_dir = os.path.join(get_mobility_database_dir(cache_dir), "catalogs", "sources", "gtfs", "realtime")
    for filename in glob.glob(f"*-{mdb_source_id}.json", root_dir=gtfs_rt_dir):
        with open(os.path.join(gtfs_rt_dir, filename), "r", encoding='utf-8') as f:
            data = json.load(f)
            return data["urls"]["latest"] if data["urls"].get("latest") else data["urls"]["direct_download"]

    return None

def get_gtfs_url(mdb_source_id, cache_dir: str | None = None):
    """
    Helper function to look up the GTFS schedule URL from the JSON files in the clone repository's catalogs/sources/gtfs/schedule directory.
    """
    create_gtfs_sources_dir(cache_dir)
    gtfs_schedule_dir = os.path.join(get_mobility_database_dir(cache_dir), "catalogs", "sources", "gtfs", "schedule")
    for filename in glob.glob(f"*-{mdb_source_id}.json", root_dir=gtfs_schedule_dir):
        # find the file that ends with -<mdb_source_id>.json
        with open(os.path.join(gtfs_schedule_dir, filename), "r", encoding='utf-8') as f:
            data = json.load(f)
            if str(data.get("mdb_source_id")) == mdb_source_id:
                return data["urls"]["latest"] if data["urls"].get("latest") else data["urls"]["direct_download"]
    return None

async def run_print_agencies(args: Any):
    """
    Helper function to print the list of transit agencies in the Mobility Database.
    """
    agencies = await read_agencies(args.cache_dir)

    print("[")
    agencies_values = list(agencies.values())
    agencies_values = sorted(agencies_values, key=lambda x: x["provider"])
    for agency in agencies_values:
        print(json.dumps(agency) + ("," if agency != agencies_values[-1] else ""))
    print("]")

def remove_nulls(d):
    """Recursively remove null values from dictionaries."""
    if not isinstance(d, dict):
        return d
    return {k: remove_nulls(v) for k, v in d.items() if v is not None}

read_agencies_cache: Dict[str, Any] | None = None

async def read_agencies(cache_dir: str):
    """ Reads the list of transit agencies in the Mobility Database from the JSON files in the clone repository's catalogs/sources/gtfs directory. """

    # pylint: disable=global-variable-not-assigned
    global read_agencies_cache
    # pylint: enable=global-variable-not-assigned

    if read_agencies_cache:
        return read_agencies_cache

    create_gtfs_sources_dir(cache_dir)
    gtfs_schedule_dir = os.path.join(get_mobility_database_dir(cache_dir), "catalogs", "sources", "gtfs", "schedule")
    gtfs_realtime_dir = os.path.join(get_mobility_database_dir(cache_dir), "catalogs", "sources", "gtfs", "realtime")
    agencies:Dict[str, Any] = {}
    for filename in os.listdir(gtfs_schedule_dir):
        with open(os.path.join(gtfs_schedule_dir, filename), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                key = data["provider"] + (("/"+data.get("name")) if data.get("name") else "")

                agencies[key] = {
                    "mdb_source_id": data.get("mdb_source_id"),
                    "name": data.get("name"),
                    "provider": data.get("provider"),
                    "location": data.get("location"),
                    "feed_contact_email": data.get("feed_contact_email"),
                    "schedule": {
                        "status": data.get("status"),
                        "features": data.get("features"),
                        "url": data["urls"]["latest"] if data["urls"].get("latest") else data["urls"]["direct_download"],
                        "license": data["urls"].get("license"),
                        "autentication_type": data["urls"].get("authentication_type"),
                        "autentication_info": data["urls"].get("authentication_info"),
                        "api_key_parameter_name": data["urls"].get("api_key_parameter_name")
                    }
                }
            except json.decoder.JSONDecodeError:
                pass
            except UnicodeDecodeError:
                pass

    for filename in os.listdir(gtfs_realtime_dir):
        with open(os.path.join(gtfs_realtime_dir, filename), "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                key = data["provider"] + (("/"+data.get("name")) if data.get("name") else "")
                agency = agencies.get(key)
                if not agency:
                    agency = {
                        "mdb_source_id": data["mdb_source_id"],
                        "name": data.get("name"),
                        "provider": data.get("provider"),
                        "key": key
                    }
                agency["location"] = data.get("location") if not agency.get("location") else agency["location"]
                if not agency.get("realtime"):
                    agency["realtime"] = []
                agency["realtime"].append({
                    "status": data.get("status"),
                    "entity_type": data.get("entity_type"),
                    "features": data.get("features"),
                    "note": data.get("note"),
                    "url": data["urls"]["latest"] if data["urls"].get("latest") else data["urls"]["direct_download"],
                    "license": data["urls"].get("license"),
                    "autentication_type": data["urls"].get("authentication_type"),
                    "autentication_info": data["urls"].get("authentication_info"),
                    "api_key_parameter_name": data["urls"].get("api_key_parameter_name")
                })
                agencies[key] = agency
            except json.decoder.JSONDecodeError:
                pass
            except UnicodeDecodeError:
                pass

    remove_nulls(agencies)
    read_agencies_cache = agencies
    return agencies

async def print_routes(gtfs_url: str, mdb_source_id: str, headers: dict, cache_dir: str | None):
    """
    Helper function to print the list of routes in the Mobility Database.
    """
    _, schedule_file_path = fetch_schedule_file(gtfs_url, mdb_source_id, headers, None, cache_dir)

    # the schedule file is a GTFS feed based on the Google Transit Feed Specification
    # we need to unzip the file into a temp directory and then parse the routes.txt file

    routes_content = read_schedule_file_contents(schedule_file_path, "routes.txt")
    if not routes_content:
        logger.info("No routes found in the schedule file")
        return
    routes = map_routes(routes_content)
    for route in routes:
        logger.info("- %s: %s - %s", route.routeId, route.routeShortName, route.routeLongName)

async def print_stops(gtfs_url: str, mdb_source_id: str, headers: dict, route_id: str | None, cache_dir: str | None):
    """
    Helper function to print the list of stops in the Mobility Database.
    """
    _, schedule_file_path = fetch_schedule_file(gtfs_url, mdb_source_id, headers, None, cache_dir)
    calendar_content = read_schedule_file_contents(schedule_file_path, "calendar.txt")
    calendar_dates_content = read_schedule_file_contents(schedule_file_path, "calendar_dates.txt")
    stop_data = map_stops(read_schedule_file_contents(schedule_file_path, "stops.txt"))
    trips_data = map_trips(read_schedule_file_contents(schedule_file_path, "trips.txt"),
                           calendar_rows=calendar_content, calendar_dates_rows=calendar_dates_content)
    stop_times_data = map_stop_times(read_schedule_file_contents(schedule_file_path, "stop_times.txt"))

    # the schedule file is a GTFS feed based on the Google Transit Feed Specification
    # we need to unzip the file into a temp directory and then parse the stops.txt file

    if route_id:
        trips = [trip for trip in trips_data if trip.routeId == route_id]
        if not trips:
            logger.info("No trips found for route %s", route_id)
            return
        stop_times = [stop_time for stop_time in stop_times_data if stop_time.tripId in [trip.tripId for trip in trips]]
        if not stop_times:
            logger.info("No stops found for route %s", route_id)
            return
        stops = {stop.stopId: stop for stop in stop_data}
        stops_list: Dict[int, Stops] = {}
        logger.info("Stops for %s route %s:", mdb_source_id, route_id)
        for id, stop in stops.items():
            stop_time = next((stop_time for stop_time in stop_times if stop_time.stopId == id), None)
            if stop_time:
                stops_list[stop_time.stopSequence] = stop
        # sort the stops_list by key
        for key in sorted(stops_list.keys()):
            stop = stops_list[key]
            logger.info("- %s: %s: %s, (%s,%s), https://geohack.toolforge.org/geohack.php?language=en&params=%s;%s", key, stop.stopId, stop.stopName, stop.stopLat, stop.stopLon, stop.stopLat, stop.stopLon)
    else:
        logger.info("Stops for %s:", mdb_source_id)
        for stop in stop_data:
            logger.info("- %s: %s, (%s,%s), https://geohack.toolforge.org/geohack.php?language=en&params=%s;%s", stop.stopId, stop.stopName, stop.stopLat, stop.stopLon, stop.stopLat, stop.stopLon)

async def run_print_stops(args):
    """
    Helper function to launch the print_stops function with the specified arguments.

    Args:
        args: The command-line arguments.
    """
    headers = None
    if args.header:
        headers = {k: v for k, v in args.header}
    if not args.gtfs_url and not args.mdb_source_id:
        raise ValueError("No GTFS URL or Mobility Database source ID specified")
    await print_stops(args.gtfs_url, args.mdb_source_id, headers, args.route, args.cache_dir)

async def run_print_routes(args):
    """
    Helper function to launch the print_routes function with the specified arguments.

    Args:
        args: The command-line arguments.
    """
    headers = None
    if not args.gtfs_url and not args.mdb_source_id:
        raise ValueError("No GTFS URL or Mobility Database source ID specified")
    if args.header:
        headers = {k: v for k, v in args.header}
    await print_routes(args.gtfs_url, args.mdb_source_id, headers, args.cache_dir)

def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string (str): The connection string.

    Returns:
        Dict[str, str]: Extracted connection parameters.
    """
    config_dict = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').strip().replace('sb://', '').replace('/', '')+':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"').strip()
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict

async def run_feed(args):
    """
    Helper function to launch the feed function with the specified arguments.

    Args:
        args: The command-line arguments.
    """

    if args.log_level:
        llevel = getattr(logging, args.log_level)
        logger.setLevel(llevel)
    source_configs = load_source_configs(
        gtfs_rt_urls=args.gtfs_rt_urls,
        gtfs_urls=args.gtfs_urls,
        mdb_source_id=args.mdb_source_id,
        agency=args.agency,
        route=args.route,
        gtfs_rt_headers=args.gtfs_rt_headers,
        gtfs_headers=args.gtfs_headers,
        sources_file=args.gtfs_sources_file,
        selector=args.gtfs_sources,
    )
    if not source_configs:
        if args.agency:
            raise ValueError("No GTFS URL or Mobility Database source ID specified")
        raise ValueError("No agency specified")
    for source_config in source_configs:
        if not source_config.get("agency"):
            raise ValueError("No agency specified")
        if not source_config.get("gtfs_urls") and not source_config.get("gtfs_rt_urls") and not source_config.get("mdb_source_id"):
            raise ValueError("No GTFS URL or Mobility Database source ID specified")

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

    for source_config in source_configs:
        feed_realtime_messages(source_config.get("agency"), kafka_bootstrap_servers, kafka_topic, sasl_username, sasl_password,
                               source_config.get("gtfs_rt_urls"), source_config.get("gtfs_rt_headers"), source_config.get("gtfs_urls"), source_config.get("gtfs_headers"), source_config.get("mdb_source_id"), source_config.get("route", "*"), args.poll_interval, args.schedule_poll_interval, args.cloudevents_mode, args.cache_dir, args.force_schedule_refresh)

async def main():
    """
    Main function to parse the command-line arguments and execute the selected command.
    """
    # Define the command-line arguments and subcommands
    parser = argparse.ArgumentParser(description="Real-time transit data bridge for the Mobility Database and GTFS")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    split_pattern = r'''(?:(?<!\\)"[^"]*"|'[^']*'|[^\s"']+)+'''
    # Define the "feed" command
    feed_parser = subparsers.add_parser("feed", help="poll real-time feeds and submit to a Kafka endpoint, Event Hub, or Fabric Event Stream custom endpoint")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str, help="Comma separated list of Kafka bootstrap servers", default=os.environ.get("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument('--kafka-topic', type=str, help="Kafka topic to send messages to", default=os.environ.get("KAFKA_TOPIC"))
    feed_parser.add_argument('--sasl-username', type=str, help="Username for SASL PLAIN authentication", default=os.environ.get("SASL_USERNAME"))
    feed_parser.add_argument('--sasl-password', type=str, help="Password for SASL PLAIN authentication", default=os.environ.get("SASL_PASSWORD"))
    feed_parser.add_argument('-c', '--connection-string', dest="connection_string", type=str, help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string', default=os.environ.get("CONNECTION_STRING"))
    feed_parser.add_argument("-r", "--route", help="the route to poll vehicle locations for, omit or '*' to poll all routes", required=False, default="*" if not os.environ.get("ROUTE") else os.environ.get("ROUTE"))
    feed_parser.add_argument("--gtfs-rt-urls", help="the URL(s) of the GTFS Realtime feed(s)", required=False, nargs="+", default=os.environ.get("GTFS_RT_URLS").split(",") if os.environ.get("GTFS_RT_URLS") else None)
    feed_parser.add_argument("--gtfs-urls", help="the URL(s) of the GTFS Schedule feed", nargs='+', required=False,default=os.environ.get("GTFS_URLS").split(",") if os.environ.get("GTFS_URLS") else None)
    feed_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Realtime feed", required=False, default=os.environ.get("MDB_SOURCE_ID"))
    feed_parser.add_argument("-a", "--agency", help="the tag of the agency to get vehicle locations for", required=False, default=os.environ.get("AGENCY"))
    feed_parser.add_argument("--gtfs-sources-file", help="path to a GTFS source catalog JSON file", required=False, default=os.environ.get("GTFS_SOURCES_FILE", ""))
    feed_parser.add_argument("--gtfs-sources", help="comma-separated catalog source names to run, or '*' for all", required=False, default=os.environ.get("GTFS_SOURCES", ""))
    feed_parser.add_argument('--gtfs-rt-headers', action='append', nargs='*', help='HTTP header(s) expressed as "key=value", e.g. "API-Key=abc', default=re.findall(split_pattern, os.environ.get("GTFS_RT_HEADERS")) if os.environ.get("GTFS_RT_HEADERS") else None)
    feed_parser.add_argument('--gtfs-headers', action='append', nargs='*', help='HTTP header(s) expressed as "key=value", e.g. "API-Key=abc', default=re.findall(split_pattern, os.environ.get("GTFS_HEADERS")) if os.environ.get("GTFS_HEADERS") else None)
    feed_parser.add_argument("--poll-interval", help="the number of seconds to wait between polling vehicle locations", required=False, type=float, default=float(os.environ.get("POLL_INTERVAL")) if os.environ.get("POLL_INTERVAL") else 90)
    feed_parser.add_argument("--schedule-poll-interval", help="the number of seconds to wait between polling the GTFS schedule", required=False, type=float, default=float(os.environ.get("SCHEDULE_POLL_INTERVAL")) if os.environ.get("SCHEDULE_POLL_INTERVAL") else 24*60*60)
    feed_parser.add_argument("--cloudevents-mode", help="the CloudEvents mode to use for the Kafka producer", required=False, choices=["structured", "binary"], default="structured")
    feed_parser.add_argument('--cache-dir', type=str, help="the directory to store the GTFS schedule files", required=False, default=os.environ.get("CACHE_DIR"))
    feed_parser.add_argument('--log-level', type=str, help="the logging level", required=False, default=os.environ.get("LOG_LEVEL"), choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    feed_parser.add_argument('--force-schedule-refresh', action='store_true', help="force a refresh of the GTFS schedule data", required=False, default=False)
    feed_parser.set_defaults(func=run_feed)

    # Define the "printfeed" command
    printfeed_parser = subparsers.add_parser("printfeed", help="Print the feed data for a route for a single request")
    printfeed_parser.add_argument("--gtfs-rt-url", help="the URL of the GTFS Realtime feed", required=False)
    printfeed_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Realtime feed", required=False, default=None)
    printfeed_parser.add_argument('--header', action='append', nargs=2,
                                          help='HTTP header to send with the request to the GTFS Realtime feed')
    printfeed_parser.add_argument('--cache-dir', type=str, help="the directory to store the GTFS schedule files", required=False, default=os.environ.get("CACHE_DIR"))

    async def cmd_print_feed_items(args):
        if not args.gtfs_rt_url and not args.mdb_source_id:
            raise ValueError("No GTFS URL or Mobility Database source ID specified")
        headers = {}
        if args.header:
            headers = {k: v for k, v in args.header}
        await print_feed_items(args.gtfs_rt_url, args.mdb_source_id, headers, args.cache_dir)

    printfeed_parser.set_defaults(func=cmd_print_feed_items)

    # Define the "agencies" command that lists the agencies in the Mobility Database, using the schedule data
    agencies_parser = subparsers.add_parser("agencies", help="get the list of transit agencies")
    agencies_parser.add_argument('--cache-dir', type=str, help="the directory to store the GTFS schedule files", required=False, default=os.environ.get("CACHE_DIR"))
    agencies_parser.set_defaults(func=run_print_agencies)

    route_parser = subparsers.add_parser("routes", help="get the list of routes for an agency")
    route_parser.add_argument("gtfs_url", help="the URL of the GTFS Schedule feed")
    route_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Schedule feed", required=False, default=None)
    route_parser.add_argument('--header', action='append', nargs=2,
                              help='HTTP header to send with the request to the GTFS Realtime feed')
    route_parser.add_argument('--cache-dir', type=str, help="the directory to store the GTFS schedule files", required=False, default=os.environ.get("CACHE_DIR"))
    route_parser.set_defaults(func=run_print_routes)

    # Define the "stops" command that lists the stops for a route
    stops_parser = subparsers.add_parser("stops", help="get the list of stops for a route")
    stops_parser.add_argument("-r", "--route", help="the route to get stops for", required=False)
    stops_parser.add_argument("gtfs_url", help="the URL of the GTFS Schedule feed")
    stops_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Schedule feed", required=False, default=None)
    stops_parser.add_argument('--header', action='append', nargs=2,
                              help='HTTP header to send with the request to the GTFS Realtime feed')
    stops_parser.add_argument('--cache-dir', type=str, help="the directory to store the GTFS schedule files", required=False, default=os.environ.get("CACHE_DIR"))
    stops_parser.set_defaults(func=run_print_stops)

    # Parse the command-line arguments and execute the selected command
    args = parser.parse_args()
    # Check if the 'func' attribute is present in the 'Namespace' object
    if hasattr(args, 'func') and callable(args.func):
        await args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    import asyncio as _asyncio
    _asyncio.run(main())


DEFAULT_POLL_INTERVAL_SECONDS = 90
DEFAULT_SCHEDULE_POLL_INTERVAL_SECONDS = 24 * 60 * 60

REALTIME_PUBLISH_METHODS: dict[str, str] = {
    "vehicle": "publish_general_transit_feed_real_time_vehicle_vehicle_position_mqtt",
    "trip": "publish_general_transit_feed_real_time_trip_trip_update_mqtt",
    "alert": "publish_general_transit_feed_real_time_alert_alert_mqtt",
}

EVENT_TYPE_BY_PUBLISH_METHOD: dict[str, str] = {
    "publish_general_transit_feed_real_time_vehicle_vehicle_position_mqtt": "GeneralTransitFeedRealTime.Vehicle.VehiclePosition",
    "publish_general_transit_feed_real_time_trip_trip_update_mqtt": "GeneralTransitFeedRealTime.Trip.TripUpdate",
    "publish_general_transit_feed_real_time_alert_alert_mqtt": "GeneralTransitFeedRealTime.Alert.Alert",
    "publish_general_transit_feed_static_agency_mqtt": "GeneralTransitFeedStatic.Agency",
    "publish_general_transit_feed_static_areas_mqtt": "GeneralTransitFeedStatic.Areas",
    "publish_general_transit_feed_static_attributions_mqtt": "GeneralTransitFeedStatic.Attributions",
    "publish_general_transit_feed_booking_rules_mqtt": "GeneralTransitFeed.BookingRules",
    "publish_general_transit_feed_static_fare_attributes_mqtt": "GeneralTransitFeedStatic.FareAttributes",
    "publish_general_transit_feed_static_fare_leg_rules_mqtt": "GeneralTransitFeedStatic.FareLegRules",
    "publish_general_transit_feed_static_fare_media_mqtt": "GeneralTransitFeedStatic.FareMedia",
    "publish_general_transit_feed_static_fare_products_mqtt": "GeneralTransitFeedStatic.FareProducts",
    "publish_general_transit_feed_static_fare_rules_mqtt": "GeneralTransitFeedStatic.FareRules",
    "publish_general_transit_feed_static_fare_transfer_rules_mqtt": "GeneralTransitFeedStatic.FareTransferRules",
    "publish_general_transit_feed_static_feed_info_mqtt": "GeneralTransitFeedStatic.FeedInfo",
    "publish_general_transit_feed_static_frequencies_mqtt": "GeneralTransitFeedStatic.Frequencies",
    "publish_general_transit_feed_static_levels_mqtt": "GeneralTransitFeedStatic.Levels",
    "publish_general_transit_feed_static_location_groups_mqtt": "GeneralTransitFeedStatic.LocationGroups",
    "publish_general_transit_feed_static_location_group_stores_mqtt": "GeneralTransitFeedStatic.LocationGroupStores",
    "publish_general_transit_feed_static_networks_mqtt": "GeneralTransitFeedStatic.Networks",
    "publish_general_transit_feed_static_pathways_mqtt": "GeneralTransitFeedStatic.Pathways",
    "publish_general_transit_feed_static_route_networks_mqtt": "GeneralTransitFeedStatic.RouteNetworks",
    "publish_general_transit_feed_static_routes_mqtt": "GeneralTransitFeedStatic.Routes",
    "publish_general_transit_feed_static_shapes_mqtt": "GeneralTransitFeedStatic.Shapes",
    "publish_general_transit_feed_static_stop_areas_mqtt": "GeneralTransitFeedStatic.StopAreas",
    "publish_general_transit_feed_static_stops_mqtt": "GeneralTransitFeedStatic.Stops",
    "publish_general_transit_feed_static_stop_times_mqtt": "GeneralTransitFeedStatic.StopTimes",
    "publish_general_transit_feed_static_timeframes_mqtt": "GeneralTransitFeedStatic.Timeframes",
    "publish_general_transit_feed_static_transfers_mqtt": "GeneralTransitFeedStatic.Transfers",
    "publish_general_transit_feed_static_translations_mqtt": "GeneralTransitFeedStatic.Translations",
    "publish_general_transit_feed_static_trips_mqtt": "GeneralTransitFeedStatic.Trips",
}


def _key_segment(value: Any, default: str = "unknown") -> str:
    text = str(value if value not in (None, "") else default)
    return text or default


def _join_key(*parts: Any) -> str:
    return "/".join(_key_segment(part) for part in parts)


def _alert_route_id(alert: Alert) -> str:
    for selector in alert.informed_entity or []:
        route_id = getattr(selector, "route_id", None)
        if route_id:
            return str(route_id)
        trip = getattr(selector, "trip", None)
        trip_route_id = getattr(trip, "route_id", None) if trip is not None else None
        if trip_route_id:
            return str(trip_route_id)
    return "unknown"


def _async_result(value: Any):
    if inspect.isawaitable(value):
        return value

    async def _noop() -> Any:
        return value

    return _noop()


async def _call_publish(method: Any, **kwargs: Any) -> None:
    await _async_result(method(**kwargs))


async def _maybe_call(member: Any, *args: Any, **kwargs: Any) -> Any:
    if member is None:
        return None
    result = member(*args, **kwargs)
    if inspect.isawaitable(result):
        return await result
    return result


async def _flush_publisher(publisher: Any) -> None:
    await _maybe_call(getattr(publisher, "flush", None))


async def _poll_publisher(publisher: Any) -> None:
    await _maybe_call(getattr(publisher, "poll", None))


def _static_event_specs() -> dict[str, tuple[Any, str, Any]]:
    return {
        "agency": (map_agency, "publish_general_transit_feed_static_agency_mqtt", lambda e, agency_id: _key_segment(e.agencyId, agency_id)),
        "areas": (map_areas, "publish_general_transit_feed_static_areas_mqtt", lambda e, agency_id: _join_key(agency_id, e.areaId)),
        "attributions": (map_attributions, "publish_general_transit_feed_static_attributions_mqtt", lambda e, agency_id: _join_key(e.agencyId or agency_id, e.attributionId, e.routeId or "any", e.tripId)),
        "booking_rules": (map_booking_rules, "publish_general_transit_feed_booking_rules_mqtt", lambda e, agency_id: _join_key(agency_id, e.bookingRuleId)),
        "fare_attributes": (map_fare_attributes, "publish_general_transit_feed_static_fare_attributes_mqtt", lambda e, agency_id: _join_key(e.agencyId or agency_id, e.fareId)),
        "fare_leg_rules": (map_fare_leg_rules, "publish_general_transit_feed_static_fare_leg_rules_mqtt", lambda e, agency_id: _join_key(agency_id, e.fareLegRuleId)),
        "fare_media": (map_fare_media, "publish_general_transit_feed_static_fare_media_mqtt", lambda e, agency_id: _join_key(agency_id, e.fareMediaId)),
        "fare_products": (map_fare_products, "publish_general_transit_feed_static_fare_products_mqtt", lambda e, agency_id: _join_key(agency_id, e.fareProductId)),
        "fare_rules": (map_fare_rules, "publish_general_transit_feed_static_fare_rules_mqtt", lambda e, agency_id: _join_key(agency_id, e.fareId)),
        "fare_transfer_rules": (map_fare_transfer_rules, "publish_general_transit_feed_static_fare_transfer_rules_mqtt", lambda e, agency_id: _join_key(agency_id, e.fareTransferRuleId)),
        "feed_info": (map_feed_info, "publish_general_transit_feed_static_feed_info_mqtt", lambda e, agency_id: _join_key(agency_id, e.feedVersion)),
        "frequencies": (map_frequencies, "publish_general_transit_feed_static_frequencies_mqtt", lambda e, agency_id: _join_key(agency_id, e.tripId)),
        "levels": (map_levels, "publish_general_transit_feed_static_levels_mqtt", lambda e, agency_id: _join_key(agency_id, e.levelId)),
        "location_groups": (map_location_groups, "publish_general_transit_feed_static_location_groups_mqtt", lambda e, agency_id: _join_key(agency_id, e.locationGroupId)),
        "location_group_stores": (map_location_group_stores, "publish_general_transit_feed_static_location_group_stores_mqtt", lambda e, agency_id: _join_key(agency_id, e.locationGroupId)),
        "networks": (map_networks, "publish_general_transit_feed_static_networks_mqtt", lambda e, agency_id: _join_key(agency_id, e.networkId)),
        "pathways": (map_pathways, "publish_general_transit_feed_static_pathways_mqtt", lambda e, agency_id: _join_key(agency_id, e.pathwayId)),
        "route_networks": (map_route_networks, "publish_general_transit_feed_static_route_networks_mqtt", lambda e, agency_id: _join_key(agency_id, e.routeNetworkId)),
        "routes": (map_routes, "publish_general_transit_feed_static_routes_mqtt", lambda e, agency_id: _join_key(e.agencyId or agency_id, e.routeId)),
        "shapes": (map_shapes, "publish_general_transit_feed_static_shapes_mqtt", lambda e, agency_id: _join_key(agency_id, e.shapeId, e.shapePtSequence)),
        "stop_areas": (map_stop_areas, "publish_general_transit_feed_static_stop_areas_mqtt", lambda e, agency_id: _join_key(agency_id, e.stopAreaId)),
        "stops": (map_stops, "publish_general_transit_feed_static_stops_mqtt", lambda e, agency_id: _join_key(agency_id, e.stopId)),
        "stop_times": (map_stop_times, "publish_general_transit_feed_static_stop_times_mqtt", lambda e, agency_id: _join_key(agency_id, e.stopId, e.tripId)),
        "timeframes": (map_timeframes, "publish_general_transit_feed_static_timeframes_mqtt", lambda e, agency_id: _join_key(agency_id, e.timeframeGroupId)),
        "transfers": (map_transfers, "publish_general_transit_feed_static_transfers_mqtt", lambda e, agency_id: _join_key(agency_id, e.fromStopId, e.toStopId)),
        "translations": (map_translations, "publish_general_transit_feed_static_translations_mqtt", lambda e, agency_id: _join_key(agency_id, e.tableName, e.fieldName)),
        "trips": (map_trips, "publish_general_transit_feed_static_trips_mqtt", lambda e, agency_id: _join_key(agency_id, e.tripId)),
    }


STATIC_EVENT_SPECS = _static_event_specs()


async def poll_and_publish_realtime_feed(agency_id: str, publisher: Any, feed_url: str, gtfs_rt_headers: List[List[str]] | None, route: str | None) -> None:
    global hashes_alert, hashes_trip, hashes_vehicles

    headers: Dict[str, str] = {}
    if gtfs_rt_headers:
        for header in gtfs_rt_headers:
            headers[header[0]] = header[1]

    response = requests.get(feed_url, headers={**headers, "User-Agent": USER_AGENT}, timeout=10)
    response.raise_for_status()

    try:
        incoming_feed_message = gtfs_realtime_pb2.FeedMessage()
        incoming_feed_message.ParseFromString(response.content)
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Failed to parse a GTFS Realtime message from %s with %s", feed_url, exc)
        return

    for entity in incoming_feed_message.entity:
        if entity.vehicle and entity.vehicle.vehicle and entity.vehicle.vehicle.id:
            vehicle = map_vehicle_position(entity)
            if route and route != "*" and vehicle.trip and vehicle.trip.route_id != route:
                continue
            vph = map_vehicle_position(entity)
            vph.timestamp = 0
            hash_vph = hashlib.sha256(vph.to_json().encode()).hexdigest()
            vehicle_id = _key_segment(vehicle.vehicle.id)
            if hashes_vehicles.get(vehicle_id) == hash_vph:
                logger.debug("Skipping vehicle position: %s, %s", vehicle_id, entity.id)
                continue
            await _call_publish(
                getattr(publisher, REALTIME_PUBLISH_METHODS["vehicle"]),
                feedurl=feed_url,
                agencyid=agency_id,
                route_id=_key_segment(vehicle.trip.route_id if vehicle.trip else None),
                vehicle_id=vehicle_id,
                data=vehicle,
                content_type="application/json",
            )
            hashes_vehicles[vehicle_id] = hash_vph
        elif entity.trip_update and entity.trip_update.trip and entity.trip_update.trip.trip_id:
            trip_update = map_trip_update(entity)
            if route and route != "*" and trip_update.trip and trip_update.trip.route_id != route:
                continue
            tuh = map_trip_update(entity)
            tuh.timestamp = 0
            hash_tuh = hashlib.sha256(tuh.to_json().encode()).hexdigest()
            trip_id = _key_segment(trip_update.trip.trip_id if trip_update.trip else None)
            if hashes_trip.get(trip_id) == hash_tuh:
                logger.debug("Skipping trip update: %s, %s", trip_id, entity.id)
                continue
            await _call_publish(
                getattr(publisher, REALTIME_PUBLISH_METHODS["trip"]),
                feedurl=feed_url,
                agencyid=agency_id,
                route_id=_key_segment(trip_update.trip.route_id if trip_update.trip else None),
                trip_id=trip_id,
                data=trip_update,
                content_type="application/json",
            )
            hashes_trip[trip_id] = hash_tuh
        elif entity.alert and len(entity.alert.header_text.translation) > 0:
            alert = map_alert(entity)
            sah = map_alert(entity)
            sah.timestamp = 0
            hash_sah = hashlib.sha256(sah.to_json().encode()).hexdigest()
            if hashes_alert.get(hash_sah) == hash_sah:
                logger.debug("Skipping alert: %s, %s", alert.header_text, entity.id)
                continue
            await _call_publish(
                getattr(publisher, REALTIME_PUBLISH_METHODS["alert"]),
                feedurl=feed_url,
                agencyid=agency_id,
                route_id=_alert_route_id(alert),
                alert_id=_key_segment(getattr(entity, "id", None), hash_sah),
                data=alert,
                content_type="application/json",
            )
            hashes_alert[hash_sah] = hash_sah
    await _flush_publisher(publisher)


async def fetch_and_publish_schedule(agency_id: str, publisher: Any, gtfs_urls: List[str], headers: List[List[str]] | None, force_refresh: bool = False, cache_dir: str | None = None) -> None:
    global etags

    for gtfs_url in gtfs_urls:
        etag, schedule_file_path = fetch_schedule_file(gtfs_url, None, headers, etags.get(gtfs_url, None), cache_dir)
        if not force_refresh and etag == etags.get(gtfs_url, None):
            continue
        etags[gtfs_url] = etag

        old_hashes = read_file_hashes(schedule_file_path, cache_dir)
        new_hashes = calculate_file_hashes(schedule_file_path)

        static_file_priority = [
            "agency", "calendar", "calendar_dates",
            "routes", "stops", "stop_areas",
            "trips", "stop_times", "frequencies",
            "transfers", "feed_info", "levels", "pathways",
            "networks", "route_networks", "areas",
            "attributions", "booking_rules", "fare_attributes",
            "fare_leg_rules", "fare_media", "fare_products",
            "fare_rules", "fare_transfer_rules", "location_groups",
            "location_group_stores", "timeframes", "translations",
            "shapes",
        ]

        def _file_priority(file_name: str) -> int:
            base = os.path.basename(file_name).split(".")[0]
            try:
                return static_file_priority.index(base)
            except ValueError:
                return len(static_file_priority) - 2

        changed_files = [
            file_name
            for file_name, new_hash in new_hashes.items()
            if force_refresh or (file_name not in old_hashes or old_hashes[file_name] != new_hash)
        ]
        changed_files.sort(key=_file_priority)

        agency_url = gtfs_url
        agency_rows = read_schedule_file_contents(schedule_file_path, "agency.txt")
        if agency_rows:
            agency_url = agency_rows[0].get("agency_url") or gtfs_url
        calendar_rows = read_schedule_file_contents(schedule_file_path, "calendar.txt")
        calendar_dates_rows = read_schedule_file_contents(schedule_file_path, "calendar_dates.txt")

        send_count = 0
        for file_name in changed_files:
            file_base_name = os.path.basename(file_name).split(".")[0]
            if file_base_name in {"calendar", "calendar_dates"}:
                continue
            spec = STATIC_EVENT_SPECS.get(file_base_name)
            if spec is None:
                logger.debug("Skipping unsupported GTFS static file %s", file_base_name)
                continue
            mapper, method_name, row_id_builder = spec
            logger.info("Processing %s entities", file_base_name)
            entity_count = 0
            publish_method = getattr(publisher, method_name)
            rows = iter_schedule_file_contents(schedule_file_path, file_name)
            if file_base_name in {"timeframes", "trips"}:
                entities = mapper(rows, calendar_rows, calendar_dates_rows)
            else:
                entities = mapper(rows)
            for entity in entities:
                row_id = row_id_builder(entity, agency_id)
                await _call_publish(
                    publish_method,
                    feedurl=agency_url,
                    agencyid=agency_id,
                    row_id=row_id,
                    data=entity,
                    content_type="application/json",
                )
                send_count += 1
                entity_count += 1
                if send_count % 10000 == 0:
                    await _poll_publisher(publisher)
            logger.info("Processed %s %s entities", entity_count, file_base_name)
            await _flush_publisher(publisher)
            persisted = read_file_hashes(schedule_file_path, cache_dir)
            persisted[file_name] = new_hashes[file_name]
            write_file_hashes(schedule_file_path, persisted, cache_dir)


async def poll_and_publish_gtfs(
    *,
    agency_id: str,
    publisher: Any,
    gtfs_rt_urls: List[str] | None,
    gtfs_rt_headers: List[List[str]] | None,
    gtfs_urls: List[str] | None,
    gtfs_headers: List[List[str]] | None,
    mdb_source_id: str | None,
    route: str | None,
    poll_interval: float,
    schedule_poll_interval: float,
    cache_dir: str | None,
    force_schedule_refresh: bool,
    once: bool = False,
) -> None:
    if not gtfs_rt_urls and mdb_source_id:
        gtfs_rt_url = get_gtfs_rt_url(mdb_source_id, cache_dir)
        gtfs_rt_urls = [gtfs_rt_url] if gtfs_rt_url else None
    if not gtfs_urls and mdb_source_id:
        gtfs_url = get_gtfs_url(mdb_source_id, cache_dir)
        gtfs_urls = [gtfs_url] if gtfs_url else None

    last_schedule_completed: datetime | None = None

    while True:
        cycle_started = datetime.now(timezone.utc)
        if gtfs_urls:
            due = force_schedule_refresh or last_schedule_completed is None or (
                datetime.now() - last_schedule_completed > timedelta(seconds=schedule_poll_interval)
            )
            if due:
                logger.info("Fetching schedule from %s", gtfs_urls)
                await fetch_and_publish_schedule(agency_id, publisher, gtfs_urls, gtfs_headers, force_refresh=force_schedule_refresh, cache_dir=cache_dir)
                last_schedule_completed = datetime.now()
                force_schedule_refresh = False

        if gtfs_rt_urls:
            logger.info("Polling feed updates from %s", gtfs_rt_urls)
            for gtfs_feed_url in gtfs_rt_urls:
                try:
                    await poll_and_publish_realtime_feed(agency_id, publisher, gtfs_feed_url, gtfs_rt_headers, route)
                except Exception as exc:  # pylint: disable=broad-except
                    logger.error("Failed to poll and publish feed updates from %s: %s", gtfs_feed_url, exc)

        if once:
            break

        elapsed = datetime.now(timezone.utc) - cycle_started
        sleep_secs = poll_interval - elapsed.total_seconds()
        if sleep_secs > 0:
            logger.info("Sleeping for %s seconds", sleep_secs)
            await asyncio.sleep(sleep_secs)
