# pylint: disable=unused-import, line-too-long, missing-module-docstring, missing-function-docstring, missing-class-docstring, consider-using-f-string, trailing-whitespace, trailing-newlines

import asyncio
import csv
import glob
import hashlib
import io
import os
import shutil
import subprocess
import time
import json
import argparse
import logging
import dataclasses
import dataclasses_json
from typing import Any, Dict, List
from datetime import UTC, datetime, timedelta
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from math import radians, cos, sin, asin, sqrt
from enum import Enum
from gtfs_rt_producer_data.generaltransitfeed.alert.alert import Alert
from gtfs_rt_producer_data.generaltransitfeed.alert.alert_types.cause import Cause
from gtfs_rt_producer_data.generaltransitfeed.alert.alert_types.effect import Effect
from gtfs_rt_producer_data.generaltransitfeed.alert.entityselector import EntitySelector
from gtfs_rt_producer_data.generaltransitfeed.alert.timerange import TimeRange
from gtfs_rt_producer_data.generaltransitfeed.alert.translatedstring import TranslatedString
from gtfs_rt_producer_data.generaltransitfeed.alert.translatedstring_types.translation import Translation
from gtfs_rt_producer_data.generaltransitfeed.alert.tripdescriptor import TripDescriptor as AlertTripDescriptor
from gtfs_rt_producer_data.generaltransitfeed.alert.tripdescriptor_types import ScheduleRelationship as AlertScheduleRelationship
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.position import Position
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicledescriptor import VehicleDescriptor as PositionVehicleDescriptor
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition import VehiclePosition
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition_types.congestionlevel import CongestionLevel
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition_types.occupancystatus import OccupancyStatus
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.vehicleposition_types.vehiclestopstatus import VehicleStopStatus
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.tripdescriptor import TripDescriptor as PositionTripDescriptor
from gtfs_rt_producer_data.generaltransitfeed.vehicleposition.tripdescriptor_types.schedulerelationship import ScheduleRelationship as PositionScheduleRelationship
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate import TripUpdate
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate_types.stoptimeevent import StopTimeEvent
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate_types.stoptimeupdate import StopTimeUpdate
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripdescriptor import TripDescriptor as TripTripDescriptor
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripdescriptor_types.schedulerelationship import ScheduleRelationship as TripScheduleRelationship
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.tripupdate_types.stoptimeupdate_types.schedulerelationship import ScheduleRelationship as StopTimeUpdateScheduleRelationship
from gtfs_rt_producer_data.generaltransitfeed.tripupdate.vehicledescriptor import VehicleDescriptor as TripVehicleDescriptor
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
from cloudevents.http import CloudEvent
from cloudevents.conversion import to_json
from confluent_kafka import Producer
from gtfs_rt_producer_kafka_producer.producer import GeneralTransitFeedRealTimeEventProducer, GeneralTransitFeedStaticEventProducer
import sys
import gtfs_rt_producer_data.generaltransitfeedstatic



poll_interval: float = 20
vehicle_last_report_times = {}
vehicle_last_positions = {}

if sys.gettrace():
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_speed(last_position, current_position, last_report_time, current_report_time) -> float:
    """Calculate the speed between two positions"""
    logger.info("Calculating speed...")
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [last_position.longitude, last_position.latitude,
                                 current_position.longitude, current_position.latitude])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c

    # Calculate speed in km/hr
    time_diff = current_report_time - last_report_time
    speed = km / (time_diff / 3600)
    return speed


def fetch_schedule_file(gtfs_url: str, mdb_source_id: str, headers: dict) -> str:
    """
    Fetches the latest schedule file from the schedule URL if the file does not exist in the cache.
    """

    if not gtfs_url:
        schedule_url = get_gtfs_schedule_url(mdb_source_id)
    else:
        schedule_url = gtfs_url

    url_hash = hashlib.sha256(schedule_url.encode()).hexdigest()
    cache_dir = os.path.join(os.path.expanduser("~"), ".gtfs_cli", "cache")
    os.makedirs(cache_dir, exist_ok=True)
    schedule_file_path = os.path.join(cache_dir, f"{url_hash}.json")
    if os.path.exists(schedule_file_path):
        # Check if the file is older than 24 hours
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(schedule_file_path))
        if datetime.now() - file_modified_time < timedelta(hours=24):
            return schedule_file_path

    # Fetch the latest schedule file
    if not headers:
        headers = {}

    response = requests.get(schedule_url, headers={**headers,  "User-Agent": "gtfs-rt-cli/0.1"}, timeout=10)
    response.raise_for_status()
    # write the binary file to the cache directory

    with open(schedule_file_path, "wb") as f:
        f.write(response.content)
    return schedule_file_path


def calculate_file_hashes(schedule_file_path: str):
    """Calculates the hash for each *.txt file in the given schedule file"""
    hashes = {}
    with ZipFile(schedule_file_path) as schedule_zip:
        for file_name in schedule_zip.namelist():
            if file_name.endswith('.txt'):
                with schedule_zip.open(file_name) as f:
                    file_content = f.read()
                    file_hash = hashlib.sha256(file_content).hexdigest()
                    hashes[file_name] = file_hash
    return hashes


def read_file_hashes(schedule_file_path: str):
    """Reads the file hashes from the given file path"""
    cache_dir = cache_dir = os.path.join(os.path.expanduser("~"), ".gtfs_cli", "cache")
    hashes_file_path = os.path.join(cache_dir, f"{os.path.basename(schedule_file_path)}.hashes.json")
    if not os.path.exists(hashes_file_path):
        return {}
    with open(hashes_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_file_hashes(schedule_file_path: str, hashes: dict):
    """Writes the file hashes to the given file path"""
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


hashes_vehicles: Dict[str, int] = {}
hashes_trip: Dict[str, int] = {}
hashes_alert: Dict[str, int] = {}

async def poll_and_submit_realtime_feed(producer_client: GeneralTransitFeedRealTimeEventProducer, feed_url: str, headers: dict, agency_tag: str, route: str | None):
    """Polls vehicle locations and submits them to an Event Hub"""

    global hashes_alert
    global hashes_trip
    global hashes_vehicles

    if not headers:
        headers = {}

    # Make a request to the GTFS Realtime API to get the vehicle locations for the specified route
    response = requests.get(feed_url, headers={**headers, "User-Agent": "gtfs-rt-cli/0.1"}, timeout=10)
    response.raise_for_status()

    # Parse the Protocol Buffer message and submit each vehicle location to the Event Hub
    try:
        # pylint: disable=no-member
        incoming_feed_message = gtfs_realtime_pb2.FeedMessage()
        # pylint: enable=no-member
        incoming_feed_message.ParseFromString(response.content)
    # pylint: disable=broad-except
    except Exception as entity:
        raise ValueError("Failed to parse the GTFS Realtime message") from entity

    for entity in incoming_feed_message.entity:
        if entity.vehicle and entity.vehicle.vehicle and entity.vehicle.vehicle.id:
            vehicle=map_vehicle_position(entity)
            vph = map_vehicle_position(entity)
            vph.timestamp = 0
            vph_str = vph.to_json()
            hash_vph=hashlib.sha256(vph_str.encode()).hexdigest()
            if vehicle.vehicle.id in hashes_vehicles:
                if hashes_vehicles[vehicle.vehicle.id] == hash_vph:
                    logging.debug("Skipping vehicle position: %s, %s", vehicle.vehicle.id, entity.id)
                    continue
            logging.debug("Sending vehicle position: %s, %s", vehicle.vehicle.id, entity.id)
            await producer_client.send_general_transit_feed_real_time_vehicle_position(feed_url, agency_tag, vehicle, "application/json", flush_producer=False)
            hashes_vehicles[vehicle.vehicle.id] = hash_vph
        elif entity.trip_update and entity.trip_update.trip and entity.trip_update.trip.trip_id:
            trip_update=map_trip_update(entity)
            tuh = map_trip_update(entity)
            tuh.timestamp = 0
            tuh_str = tuh.to_json()
            hash_tuh=hashlib.sha256(tuh_str.encode()).hexdigest()
            if trip_update.trip.trip_id in hashes_trip:
                if hashes_trip[trip_update.trip.trip_id] == hash_tuh:
                    logging.debug("Skipping trip update: %s, %s", trip_update.trip.trip_id, entity.id)
                    continue
            logging.debug("Sending trip update: %s, %s", trip_update.trip.trip_id, entity.id)
            await producer_client.send_general_transit_feed_real_time_trip_update(feed_url, agency_tag, trip_update, "application/json", flush_producer=False)
            hashes_trip[trip_update.trip.trip_id] = hash_tuh
        elif entity.alert and len(entity.alert.header_text.translation) > 0:
            alert=map_alert(entity)
            sah = map_alert(entity)
            sah.timestamp = 0
            sah_str = sah.to_json()
            hash_sah=hashlib.sha256(sah_str.encode()).hexdigest()
            if hash_sah in hashes_alert:
                if hashes_alert[hash_sah] == hash_sah:
                    logging.debug("Skipping alert: %s, %s", alert.header_text, entity.id)
                    continue
            logging.debug("Sending alert: %s, %s", alert.header_text, entity.id)
            await producer_client.send_general_transit_feed_real_time_alert(feed_url, agency_tag, alert, "application/json", flush_producer=False)
            hashes_alert[hash_sah] = hash_sah
    producer_client.producer.flush()


def map_agency(rows: List[Dict[str, Any]]) -> List[Agency]:
    """Maps the rows from the agency.txt file to a list of Agency objects"""
    return [Agency(
        agencyId=row.get("agency_id"),
        agencyName=row.get("agency_name"),
        agencyUrl=row.get("agency_url"),
        agencyTimezone=row.get("agency_timezone"),
        agencyLang=row.get("agency_lang"),
        agencyPhone=row.get("agency_phone"),
        agencyFareUrl=row.get("agency_fare_url"),
        agencyEmail=row.get("agency_email")
    ) for row in rows]


def map_areas(rows: List[Dict[str, Any]]) -> List[Areas]:
    """Maps the rows from the areas.txt file to a list of Areas objects"""
    return [Areas(
        areaId=row.get("area_id"),
        areaName=row.get("area_name"),
        areaDesc=row.get("area_desc"),
        areaUrl=row.get("area_url"),
    ) for row in rows]


def map_attributions(rows: List[Dict[str, Any]]) -> List[Attributions]:
    """Maps the rows from the attributions.txt file to a list of Attributions objects"""
    return [Attributions(
        attributionId=row.get("attribution_id"),
        agencyId=row.get("agency_id"),
        routeId=row.get("route_id"),
        tripId=row.get("trip_id"),
        organizationName=row.get("organization_name"),
        isProducer=int(row.get("is_producer")) if row.get("is_producer") else 0,
        isOperator=int(row.get("is_operator")) if row.get("is_operator") else 0,
        isAuthority=int(row.get("is_authority")) if row.get("is_authority") else 0,
        attributionUrl=row.get("attribution_url"),
        attributionEmail=row.get("attribution_email"),
        attributionPhone=row.get("attribution_phone")
    ) for row in rows]


def map_booking_rules(rows: List[Dict[str, Any]]) -> List[BookingRules]:
    """Maps the rows from the booking_rules.txt file to a list of BookingRules objects"""
    return [BookingRules(
        bookingRuleId=row.get("booking_rule_id"),
        bookingRuleName=row.get("booking_rule_name"),
        bookingRuleDesc=row.get("booking_rule_desc"),
        bookingRuleUrl=row.get("booking_rule_url")
    ) for row in rows]


def map_fare_attributes(rows: List[Dict[str, Any]]) -> List[FareAttributes]:
    """Maps the rows from the fare_attributes.txt file to a list of FareAttributes objects"""
    return [FareAttributes(
        fareId=row.get("fare_id"),
        price=float(row.get("price")) if row.get("price") else 0,
        currencyType=row.get("currency_type"),
        paymentMethod=int(row.get("payment_method")) if row.get("payment_method") else 0,
        transfers=int(row.get("transfers")) if row.get("transfers") else 0,
        agencyId=row.get("agency_id"),
        transferDuration=int(row.get("transfer_duration")) if row.get("transfer_duration") else 0
    ) for row in rows]


def map_fare_leg_rules(rows: List[Dict[str, Any]]) -> List[FareLegRules]:
    """Maps the rows from the fare_leg_rules.txt file to a list of FareLegRules objects"""
    return [FareLegRules(
        fareLegRuleId=row.get("fare_leg_rule_id"),
        fareProductId=row.get("fare_product_id"),
        legGroupId=row.get("leg_group_id"),
        networkId=row.get("network_id"),
        fromAreaId=row.get("from_area_id"),
        toAreaId=row.get("to_area_id")
    ) for row in rows]


def map_fare_media(rows: List[Dict[str, Any]]) -> List[FareMedia]:
    """Maps the rows from the fare_media.txt file to a list of FareMedia objects"""
    return [FareMedia(
        fareMediaId=row.get("fare_media_id"),
        fareMediaName=row.get("fare_media_name"),
        fareMediaDesc=row.get("fare_media_desc"),
        fareMediaUrl=row.get("fare_media_url")
    ) for row in rows]


def map_fare_products(rows: List[Dict[str, Any]]) -> List[FareProducts]:
    """Maps the rows from the fare_products.txt file to a list of FareProducts objects"""
    return [FareProducts(
        fareProductId=row.get("fare_product_id"),
        fareProductName=row.get("fare_product_name"),
        fareProductDesc=row.get("fare_product_desc"),
        fareProductUrl=row.get("fare_product_url")
    ) for row in rows]


def map_fare_rules(rows: List[Dict[str, Any]]) -> List[FareRules]:
    """Maps the rows from the fare_rules.txt file to a list of FareRules objects"""
    return [FareRules(
        fareId=row.get("fare_id"),
        routeId=row.get("route_id"),
        originId=row.get("origin_id"),
        destinationId=row.get("destination_id"),
        containsId=row.get("contains_id")
    ) for row in rows]


def map_fare_transfer_rules(rows: List[Dict[str, Any]]) -> List[FareTransferRules]:
    """Maps the rows from the fare_transfer_rules.txt file to a list of FareTransferRules objects"""
    return [FareTransferRules(
        fareTransferRuleId=row.get("fare_transfer_rule_id"),
        fareProductId=row.get("fare_product_id"),
        transferCount=int(row.get("transfer_count")) if row.get("transfer_count") else 0,
        fromLegGroupId=row.get("from_leg_group_id"),
        toLegGroupId=row.get("to_leg_group_id"),
        duration=int(row.get("duration")) if row.get("duration") else 0,
        durationType=row.get("duration_type")
    ) for row in rows]


def map_feed_info(rows: List[Dict[str, Any]]) -> List[FeedInfo]:
    """Maps the rows from the feed_info.txt file to a list of FeedInfo objects"""
    return [FeedInfo(
        feedPublisherName=row.get("feed_publisher_name"),
        feedPublisherUrl=row.get("feed_publisher_url"),
        feedLang=row.get("feed_lang"),
        defaultLang=row.get("default_lang"),
        feedStartDate=row.get("feed_start_date"),
        feedEndDate=row.get("feed_end_date"),
        feedVersion=row.get("feed_version"),
        feedContactEmail=row.get("feed_contact_email"),
        feedContactUrl=row.get("feed_contact_url")
    ) for row in rows]


def map_frequencies(rows: List[Dict[str, Any]]) -> List[Frequencies]:
    """Maps the rows from the frequencies.txt file to a list of Frequencies objects"""
    return [Frequencies(
        tripId=row.get("trip_id"),
        startTime=row.get("start_time"),
        endTime=row.get("end_time"),
        headwaySecs=int(row.get("headway_secs")) if row.get("headway_secs") else 0,
        exactTimes=int(row.get("exact_times")) if row.get("exact_times") else 0
    ) for row in rows]


def map_levels(rows: List[Dict[str, Any]]) -> List[Levels]:
    """Maps the rows from the levels.txt file to a list of Levels objects"""
    return [Levels(
        levelId=row.get("level_id"),
        levelIndex=float(row.get("level_index")) if row.get("level_index") else 0,
        levelName=row.get("level_name")
    ) for row in rows]


def map_location_groups(rows: List[Dict[str, Any]]) -> List[LocationGroups]:
    """Maps the rows from the location_groups.txt file to a list of LocationGroups objects"""
    return [LocationGroups(
        locationGroupId=row.get("location_group_id"),
        locationGroupName=row.get("location_group_name"),
        locationGroupDesc=row.get("location_group_desc"),
        locationGroupUrl=row.get("location_group_url")
    ) for row in rows]


def map_location_group_stores(rows: List[Dict[str, Any]]) -> List[LocationGroupStores]:
    """Maps the rows from the location_group_stores.txt file to a list of LocationGroupStores objects"""
    return [LocationGroupStores(
        locationGroupStoreId=row.get("location_group_store_id"),
        locationGroupId=row.get("location_group_id"),
        storeId=row.get("store_id")
    ) for row in rows]


def map_networks(rows: List[Dict[str, Any]]) -> List[Networks]:
    """Maps the rows from the networks.txt file to a list of Networks objects"""
    return [Networks(
        networkId=row.get("network_id"),
        networkName=row.get("network_name"),
        networkDesc=row.get("network_desc"),
        networkUrl=row.get("network_url")
    ) for row in rows]


def map_pathways(rows: List[Dict[str, Any]]) -> List[Pathways]:
    """Maps the rows from the pathways.txt file to a list of Pathways objects"""
    return [Pathways(
        pathwayId=row.get("pathway_id"),
        fromStopId=row.get("from_stop_id"),
        toStopId=row.get("to_stop_id"),
        pathwayMode=int(row.get("pathway_mode")) if row.get("pathway_mode") else 0,
        isBidirectional=int(row.get("is_bidirectional")) if row.get("is_bidirectional") else 0,
        length=float(row.get("length")) if row.get("length") else 0,
        traversalTime=int(row.get("traversal_time")) if row.get("traversal_time") else 0,
        stairCount=int(row.get("stair_count")) if row.get("stair_count") else 0,
        maxSlope=float(row.get("max_slope")) if row.get("max_slope") else 0,
        minWidth=float(row.get("min_width")) if row.get("min_width") else 0,
        signpostedAs=row.get("signposted_as"),
        reversedSignpostedAs=row.get("reversed_signposted_as")
    ) for row in rows]


def map_route_networks(rows: List[Dict[str, Any]]) -> List[RouteNetworks]:
    """Maps the rows from the route_networks.txt file to a list of RouteNetworks objects"""
    return [RouteNetworks(
        routeNetworkId=row.get("route_network_id"),
        routeId=row.get("route_id"),
        networkId=row.get("network_id")
    ) for row in rows]


def map_routes(rows: List[Dict[str, Any]]) -> List[Routes]:
    """Maps the rows from the routes.txt file to a list of Routes objects"""
    return [Routes(
        routeId=row.get("route_id"),
        agencyId=row.get("agency_id"),
        routeShortName=row.get("route_short_name"),
        routeLongName=row.get("route_long_name"),
        routeDesc=row.get("route_desc"),
        routeType=RouteType.from_ordinal(row.get("route_type")) if row.get(
            "route_type") and (int(row.get("route_type")) < 12) else RouteType.OTHER,
        routeUrl=row.get("route_url"),
        routeColor=row.get("route_color"),
        routeTextColor=row.get("route_text_color"),
        routeSortOrder=int(row.get("route_sort_order")) if row.get("route_sort_order") else 0,
        continuousPickup=ContinuousPickup.from_ordinal(row.get("continuous_pickup")) if row.get(
            "continuous_pickup") else ContinuousPickup.NO_CONTINUOUS_STOPPING,
        continuousDropOff=ContinuousDropOff.from_ordinal(row.get("continuous_drop_off")) if row.get(
            "continuous_drop_off") else ContinuousDropOff.NO_CONTINUOUS_STOPPING,
        networkId=row.get("network_id")
    ) for row in rows]


def map_shapes(rows: List[Dict[str, Any]]) -> List[Shapes]:
    """Maps the rows from the shapes.txt file to a list of Shapes objects"""
    return [Shapes(
        shapeId=row.get("shape_id"),
        shapePtLat=float(row.get("shape_pt_lat")) if row.get("shape_pt_lat") else 0,
        shapePtLon=float(row.get("shape_pt_lon")) if row.get("shape_pt_lon") else 0,
        shapePtSequence=int(row.get("shape_pt_sequence")) if row.get("shape_pt_sequence") else 0,
        shapeDistTraveled=float(row.get("shape_dist_traveled")) if row.get("shape_dist_traveled") else 0
    ) for row in rows]


def map_stop_areas(rows: List[Dict[str, Any]]) -> List[StopAreas]:
    """Maps the rows from the stop_areas.txt file to a list of StopAreas objects"""
    return [StopAreas(
        stopAreaId=row.get("stop_area_id"),
        areaId=row.get("area_id"),
        stopId=row.get("stop_id"),
    ) for row in rows]


def map_stops(rows: List[Dict[str, Any]]) -> List[Stops]:
    """Maps the rows from the stops.txt file to a list of Stops objects"""
    return [Stops(
        stopId=row.get("stop_id"),
        stopCode=row.get("stop_code"),
        stopName=row.get("stop_name"),
        stopDesc=row.get("stop_desc"),
        stopLat=float(row.get("stop_lat")) if row.get("stop_lat") else 0,
        stopLon=float(row.get("stop_lon")) if row.get("stop_lon") else 0,
        zoneId=row.get("zone_id"),
        stopUrl=row.get("stop_url"),
        locationType=LocationType.from_ordinal(row.get("location_type")) if row.get("location_type") else LocationType.STOP,
        parentStation=row.get("parent_station"),
        stopTimezone=row.get("stop_timezone"),
        wheelchairBoarding=WheelchairBoarding.from_ordinal(row.get("wheelchair_boarding")) if row.get("wheelchair_boarding") else WheelchairBoarding.NO_INFO,
        levelId=row.get("level_id"),
        platformCode=row.get("platform_code"),
        ttsStopName=row.get("tts_stop_name"),
    ) for row in rows]


def map_stop_times(rows: List[Dict[str, Any]]) -> List[StopTimes]:
    """Maps the rows from the stop_times.txt file to a list of StopTimes objects"""
    return [StopTimes(
        tripId=row.get("trip_id"),
        arrivalTime=row.get("arrival_time"),
        departureTime=row.get("departure_time"),
        stopId=row.get("stop_id"),
        stopSequence=int(row.get("stop_sequence")) if row.get("stop_sequence") else 0,
        stopHeadsign=row.get("stop_headsign"),
        pickupType=PickupType.from_ordinal(row.get("pickup_type")) if row.get("pickup_type") else PickupType.REGULAR,
        dropOffType=DropOffType.from_ordinal(row.get("drop_off_type")) if row.get("drop_off_type") else DropOffType.REGULAR,
        continuousPickup=ContinuousPickup.from_ordinal(row.get("continuous_pickup")) if row.get("continuous_pickup") else ContinuousPickup.NO_CONTINUOUS_STOPPING,
        continuousDropOff=ContinuousDropOff.from_ordinal(row.get("continuous_drop_off")) if row.get("continuous_drop_off") else ContinuousDropOff.NO_CONTINUOUS_STOPPING,
        shapeDistTraveled=row.get("shape_dist_traveled"),
        timepoint=Timepoint.from_ordinal(row.get("timepoint")) if row.get("timepoint") else Timepoint.EXACT
    ) for row in rows]


def map_timeframes(rows: List[Dict[str, Any]], calendar_rows: List[Dict[str, Any]], calendar_dates_rows: List[Dict[str, Any]]) -> List[Timeframes]:
    """Maps the rows from the timeframes.txt file to a list of Timeframes objects"""
    return [Timeframes(
        timeframeGroupId=row.get("timeframe_group_id"),
        startTime=row.get("start_time"),
        endTime=row.get("end_time"),
        serviceDates=next(iter([Calendar(
            serviceId=calendarRow.get("service_id"),
            startDate=calendarRow.get("start_date"),
            endDate=calendarRow.get("end_date"),
            monday=ServiceAvailability.from_ordinal(calendarRow.get("monday")) if calendarRow.get(
                "monday") else ServiceAvailability.NO_SERVICE,
            tuesday=ServiceAvailability.from_ordinal(calendarRow.get("tuesday")) if calendarRow.get(
                "tuesday") else ServiceAvailability.NO_SERVICE,
            wednesday=ServiceAvailability.from_ordinal(calendarRow.get("wednesday")) if calendarRow.get(
                "wednesday") else ServiceAvailability.NO_SERVICE,
            thursday=ServiceAvailability.from_ordinal(calendarRow.get("thursday")) if calendarRow.get(
                "thursday") else ServiceAvailability.NO_SERVICE,
            friday=ServiceAvailability.from_ordinal(calendarRow.get("friday")) if calendarRow.get(
                "friday") else ServiceAvailability.NO_SERVICE,
            saturday=ServiceAvailability.from_ordinal(calendarRow.get("saturday")) if calendarRow.get(
                "saturday") else ServiceAvailability.NO_SERVICE,
            sunday=ServiceAvailability.from_ordinal(calendarRow.get("sunday")) if calendarRow.get("sunday") else ServiceAvailability.NO_SERVICE)
            for calendarRow in calendar_rows if calendarRow.get("service_id") == row.get("service_id")]
            + [CalendarDates(
                serviceId=calendarDatesRow.get("service_id"),
                date=calendarDatesRow.get("date"),
                exceptionType=ExceptionType.from_ordinal(calendarDatesRow.get("exception_type")) if calendarDatesRow.get("exception_type") else ExceptionType.SERVICE_REMOVED)
               for calendarDatesRow in calendar_dates_rows if calendarDatesRow.get("service_id") == row.get("service_id")]))

    ) for row in rows]


def map_transfers(rows: List[Dict[str, Any]]) -> List[Transfers]:
    """Maps the rows from the transfers.txt"""
    return [Transfers(
        fromStopId=row.get("from_stop_id"),
        toStopId=row.get("to_stop_id"),
        transferType=int(row.get("transfer_type")) if row.get("transfer_type") else 0,
        minTransferTime=int(row.get("min_transfer_time")) if row.get("min_transfer_time") else 0
    ) for row in rows]


def map_translations(rows: List[Dict[str, Any]]) -> List[Translations]:
    """Maps the rows from the translations.txt file to a list of Translations objects"""
    return [Translations(
        tableName=row.get("table_name"),
        fieldName=row.get("field_name"),
        language=row.get("language"),
        translation=row.get("translation")
    ) for row in rows]


def map_trips(rows: List[Dict[str, Any]], calendar_rows: List[Dict[str, Any]], calendar_dates_rows: List[Dict[str, Any]]) -> List[Trips]:
    """Maps the rows from the trips.txt file to a list of Trips objects"""
    trips = []
    for row in rows:
        calendar_dates = []
        calendars = []
        for calendar_row in calendar_rows:
            if calendar_row.get("service_id") == row.get("service_id"):
                calendars.append(
                    Calendar(
                        serviceId=calendar_row.get("service_id"),
                        monday=ServiceAvailability.from_ordinal(calendar_row.get("monday")) if calendar_row.get("monday") else ServiceAvailability.NO_SERVICE,
                        tuesday=ServiceAvailability.from_ordinal(calendar_row.get("tuesday")) if calendar_row.get("tuesday") else ServiceAvailability.NO_SERVICE,
                        wednesday=ServiceAvailability.from_ordinal(calendar_row.get("wednesday")) if calendar_row.get("wednesday") else ServiceAvailability.NO_SERVICE,
                        thursday=ServiceAvailability.from_ordinal(calendar_row.get("thursday")) if calendar_row.get("thursday") else ServiceAvailability.NO_SERVICE,
                        friday=ServiceAvailability.from_ordinal(calendar_row.get("friday")) if calendar_row.get("friday") else ServiceAvailability.NO_SERVICE,
                        saturday=ServiceAvailability.from_ordinal(calendar_row.get("saturday")) if calendar_row.get("saturday") else ServiceAvailability.NO_SERVICE,
                        sunday=ServiceAvailability.from_ordinal(calendar_row.get("sunday")) if calendar_row.get("sunday") else ServiceAvailability.NO_SERVICE,
                        startDate=calendar_row.get("start_date"),
                        endDate=calendar_row.get("end_date")
                    )
                )

        for calendar_dates_row in calendar_dates_rows:
            if calendar_dates_row.get("service_id") == row.get("service_id"):
                calendar_dates.append(
                    CalendarDates(
                        serviceId=calendar_dates_row.get("service_id"),
                        date=calendar_dates_row.get("date"),
                        exceptionType=ExceptionType.from_ordinal(calendar_dates_row.get("exception_type")) if calendar_dates_row.get("exception_type") and int(calendar_dates_row.get("exception_type")) < 2 else ExceptionType.SERVICE_REMOVED
                    )
                )

        trips.append(
            Trips(
                routeId=row.get("route_id"),
                serviceDates= calendars[0] if len(calendars) > 0 else None,
                serviceExceptions= calendar_dates,
                tripId=row.get("trip_id"),
                tripHeadsign=row.get("trip_headsign"),
                tripShortName=row.get("trip_short_name"),
                directionId=DirectionId.from_ordinal(row.get("direction_id")) if row.get("direction_id") else DirectionId.OUTBOUND,
                blockId=row.get("block_id"),
                shapeId=row.get("shape_id"),
                wheelchairAccessible=WheelchairAccessible.from_ordinal(row.get("wheelchair_accessible")) if row.get("wheelchair_accessible") else WheelchairAccessible.NO_INFO,
                bikesAllowed=BikesAllowed.from_ordinal(row.get("bikes_allowed")) if row.get("bikes_allowed") else BikesAllowed.NO_INFO
            )
        )
    return trips


async def send_agency_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[Agency]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_agency(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_areas_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[Areas]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_areas(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_attributions_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[Attributions]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_attributions(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_booking_rules_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[BookingRules]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_booking_rules(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_fare_attributes_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[FareAttributes]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_fare_attributes(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_fare_leg_rules_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[FareLegRules]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_fare_leg_rules(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_fare_media_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[FareMedia]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_fare_media(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_fare_products_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[FareProducts]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_fare_products(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_fare_rules_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[FareRules]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_fare_rules(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def send_fare_transfer_rules_events(reference_producer_client: GeneralTransitFeedStaticEventProducer, feed_url: str, agency_id: str, entities: List[FareTransferRules]):
    tasks = []
    for entity in entities:
        tasks.append(await reference_producer_client.send_general_transit_feed_static_fare_transfer_rules(feed_url, agency_id, entity, "application/json"))
    await asyncio.gather(*tasks)


async def fetch_and_process_schedule(reference_producer_client: GeneralTransitFeedStaticEventProducer, schedule_url: str, mdb_id: str, headers: dict, force_refresh: bool = False):
    """Fetches the schedule file, calculates file hashes, and processes new/changed files"""
    # Fetch the schedule file
    schedule_file_path = fetch_schedule_file(schedule_url, None, headers)
    # Calculate the file hashes
    new_hashes = calculate_file_hashes(schedule_file_path)
    # Read the existing file hashes
    old_hashes = read_file_hashes(schedule_file_path)

    last_report_time = time.time()
    last_report_time_iso = datetime.fromtimestamp(last_report_time, UTC).isoformat()

    # Find new/changed files
    changed_files = []
    for file_name, new_hash in new_hashes.items():
        if force_refresh or (file_name not in old_hashes or old_hashes[file_name] != new_hash):
            changed_files.append(file_name)

    agency_rows = read_schedule_file_contents(schedule_file_path, "agency.txt")
    calendar_rows = read_schedule_file_contents(schedule_file_path, "calendar.txt")
    calendar_dates_rows = read_schedule_file_contents(schedule_file_path, "calendar_dates.txt")

    # Read the contents of new/changed files
    send_count = 0
    for file_name in changed_files:
        # create eventdata batch
        file_contents = read_schedule_file_contents(schedule_file_path, file_name)
        file_base_name = os.path.basename(file_name).split(".")[0]

        if file_base_name == "agency":
            entities = map_agency(file_contents)
            logger.info("Processing %s agency entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_agency(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "areas":
            entities = map_areas(file_contents)
            logger.info("Processing %s areas entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_areas(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "attributions":
            entities = map_attributions(file_contents)
            logger.info("Processing %s attributions entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_attributions(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "booking_rules":
            entities = map_booking_rules(file_contents)
            logger.info("Processing %s booking_rules entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_booking_rules(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "fare_attributes":
            entities = map_fare_attributes(file_contents)
            logger.info("Processing %s fare_attributes entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_fare_attributes(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "fare_leg_rules":
            entities = map_fare_leg_rules(file_contents)
            logger.info("Processing %s fare_leg_rules entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_fare_leg_rules(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "fare_media":
            entities = map_fare_media(file_contents)
            logger.info("Processing %s fare_media entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_fare_media(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "fare_products":
            entities = map_fare_products(file_contents)
            logger.info("Processing %s fare_products entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_fare_products(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "fare_rules":
            entities = map_fare_rules(file_contents)
            logger.info("Processing %s fare_rules entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_fare_rules(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "fare_transfer_rules":
            entities = map_fare_transfer_rules(file_contents)
            logger.info("Processing %s fare_transfer_rules entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_fare_transfer_rules(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "feed_info":
            entities = map_feed_info(file_contents)
            logger.info("Processing %s feed_info entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_feed_info(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "frequencies":
            entities = map_frequencies(file_contents)
            logger.info("Processing %s frequencies entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_frequencies(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "levels":
            entities = map_levels(file_contents)
            logger.info("Processing %s levels entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_levels(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "location_groups":
            entities = map_location_groups(file_contents)
            logger.info("Processing %s location_groups entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_location_groups(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "location_group_stores":
            entities = map_location_group_stores(file_contents)
            logger.info("Processing %s location_group_stores entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_location_group_stores(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "networks":
            entities = map_networks(file_contents)
            logger.info("Processing %s networks entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_networks(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "pathways":
            entities = map_pathways(file_contents)
            logger.info("Processing %s pathways entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_pathways(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "route_networks":
            entities = map_route_networks(file_contents)
            logger.info("Processing %s route_networks entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_route_networks(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "routes":
            entities = map_routes(file_contents)
            logger.info("Processing %s routes entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_routes(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "shapes":
            entities = map_shapes(file_contents)
            logger.info("Processing %s shapes entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_shapes(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "stop_areas":
            entities = map_stop_areas(file_contents)
            logger.info("Processing %s stop_areas entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_stop_areas(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "stops":
            entities = map_stops(file_contents)
            logger.info("Processing %s stops entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_stops(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "stop_times":
            entities = map_stop_times(file_contents)
            logger.info("Processing %s stop_times entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_stop_times(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "timeframes":
            entities = map_timeframes(file_contents, calendar_rows, calendar_dates_rows)
            logger.info("Processing %s timeframes entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_timeframes(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "transfers":
            entities = map_transfers(file_contents)
            logger.info("Processing %s transfers entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_transfers(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "translations":
            entities = map_translations(file_contents)
            logger.info("Processing %s translations entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_translations(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        elif file_base_name == "trips":
            entities = map_trips(file_contents, calendar_rows, calendar_dates_rows)
            logger.info("Processing %s trips entities", len(entities))
            for entity in entities:
                await reference_producer_client.send_general_transit_feed_static_trips(schedule_url, mdb_id, entity, flush_producer=False)
                send_count += 1
                if send_count % 100 == 0:
                    reference_producer_client.producer.flush()
        reference_producer_client.producer.flush()
    # Write the new file hashes
    write_file_hashes(schedule_file_path, new_hashes)


async def feed_realtime_messages(kafka_bootstrap_servers: str, kafka_topic:str, sasl_username:str|None, sasl_password:str|None, gtfs_feed_urls: List[str], schedule_url: str, mdb_source_id: str, headers: dict, route: str | None, poll_interval: int = 30, cloudevents_mode: str = "structured"):
    """Poll vehicle locations and submit to an Event Hub"""
    if not gtfs_feed_urls and mdb_source_id:
        gtfs_feed_urls = [get_gtfs_rt_url(mdb_source_id)]
    if not gtfs_feed_urls:
        logger.info("No vehicle positions feed URL(s) specified")
    if not schedule_url:
        schedule_url = get_gtfs_schedule_url(mdb_source_id)
    if not schedule_url:
        logger.info("No schedule URL specified")

    if not kafka_bootstrap_servers:
        raise ValueError("No Kafka bootstrap servers specified")
    if not kafka_topic:
        raise ValueError("No Kafka topic specified")
    if not sasl_username:
        raise ValueError("No SASL username specified")
    if not sasl_password:
        raise ValueError("No SASL password specified")

    kafka_config = {
        "bootstrap.servers": kafka_bootstrap_servers,
        "sasl.mechanisms": "PLAIN",
        "security.protocol": "SASL_SSL",
        "sasl.username": sasl_username,
        "sasl.password": sasl_password,
        "acks": "all",
        "linger.ms": 100,
        "retries": 5,
        "retry.backoff.ms": 1000,
        "batch.size": 512*1024
    }
    producer: Producer = Producer(kafka_config)
    gtfs_rt_producer = GeneralTransitFeedRealTimeEventProducer(producer, kafka_topic,cloudevents_mode)
    gtfs_static_producer = GeneralTransitFeedStaticEventProducer(producer, kafka_topic, cloudevents_mode)

    last_schedule_run = None
    try:
        while True:
            if schedule_url:
                if last_schedule_run is None or datetime.now() - last_schedule_run > timedelta(hours=1):
                    last_schedule_run = datetime.now()
                    logger.info("Fetching schedule from %s", schedule_url)
                    await fetch_and_process_schedule(gtfs_static_producer, schedule_url, mdb_source_id, headers=headers, force_refresh=True)
            if gtfs_feed_urls:
                logger.info("Polling feed updates from %s", gtfs_feed_urls)
                for gtfs_feed_url in gtfs_feed_urls:
                    await poll_and_submit_realtime_feed(gtfs_rt_producer, gtfs_feed_url, headers, mdb_source_id, route)
            logger.info("Sleeping for %s seconds. Press Ctrl+C to stop.", poll_interval)
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        logger.info("Loop interrupted by user")

    producer.flush()
    producer.close()


async def print_feed_items(feed_url: str, mdb_source_id: str, headers: dict, agency, route):
    if not feed_url and mdb_source_id:
        feed_url = get_gtfs_rt_url(mdb_source_id)

    if not feed_url:
        raise ValueError("No GTFS Realtime URL specified")

    if not headers:
        headers = {}

    # Make a request to the GTFS Realtime API to get the vehicle locations for the specified route
    response = requests.get(feed_url, headers={**headers, "User-Agent": "gtfs-rt-cli/0.1"}, timeout=10)
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
    # pylint: enable=no-member

def create_gtfs_sources_dir():
    # Get the user's profile directory
    gtfs_sources_dir = get_gtfs_sources_dir()

    # Check if Git is installed
    try:
        subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        logger.info("Git is not installed.")
        return

    # Clone the mobility-database-catalogs repository if it does not exist
    mobility_database_catalogs_dir = get_mobility_database_dir()
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


def get_mobility_database_dir():
    mobility_database_catalogs_dir = os.path.join(get_gtfs_sources_dir(), "mobility-database-catalogs")
    return mobility_database_catalogs_dir


def get_gtfs_sources_dir():
    profile_dir = os.path.expanduser("~")
    gtfs_sources_dir = os.path.join(profile_dir, ".gtfs-sources")

    # Create the directory if it does not exist
    if not os.path.exists(gtfs_sources_dir):
        os.mkdir(gtfs_sources_dir)
    return gtfs_sources_dir


def get_gtfs_rt_url(mdb_source_id):
    """
    Helper function to look up the GTFS-RT URL from the JSON files in the clone repository's catalogs/sources/gtfs/realtime directory.
    the mdb_source_id is appended to the filename of each JSON file, so filter the files by mdb_source_id.
    """
    create_gtfs_sources_dir()
    gtfs_rt_dir = os.path.join(get_mobility_database_dir(), "catalogs", "sources", "gtfs", "realtime")
    for filename in glob.glob(f"*-{mdb_source_id}.json", root_dir=gtfs_rt_dir):
        with open(os.path.join(gtfs_rt_dir, filename), "r", encoding='utf-8') as f:
            data = json.load(f)
            return data["urls"]["latest"] if data["urls"].get("latest") else data["urls"]["direct_download"]

    return None


def get_gtfs_schedule_url(mdb_source_id):
    """
    Helper function to look up the GTFS schedule URL from the JSON files in the clone repository's catalogs/sources/gtfs/schedule directory.
    """
    create_gtfs_sources_dir()
    gtfs_schedule_dir = os.path.join(get_mobility_database_dir(), "catalogs", "sources", "gtfs", "schedule")
    for filename in glob.glob(f"*-{mdb_source_id}.json", root_dir=gtfs_schedule_dir):
        # find the file that ends with -<mdb_source_id>.json
        with open(os.path.join(gtfs_schedule_dir, filename), "r", encoding='utf-8') as f:
            data = json.load(f)
            if str(data.get("mdb_source_id")) == mdb_source_id:
                return data["urls"]["latest"] if data["urls"].get("latest") else data["urls"]["direct_download"]
    return None


async def run_print_agencies(_):
    """
    Helper function to print the list of transit agencies in the Mobility Database.
    """
    agencies = await read_agencies()

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

async def read_agencies():
    global read_agencies_cache
    if read_agencies_cache:
        return read_agencies_cache

    create_gtfs_sources_dir()
    gtfs_schedule_dir = os.path.join(get_mobility_database_dir(), "catalogs", "sources", "gtfs", "schedule")
    gtfs_realtime_dir = os.path.join(get_mobility_database_dir(), "catalogs", "sources", "gtfs", "realtime")
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


async def print_routes(gtfs_url: str, mdb_source_id: str, headers: dict):
    """
    Helper function to print the list of routes in the Mobility Database.
    """
    schedule_file_path = fetch_schedule_file(gtfs_url, mdb_source_id, headers)

    # the schedule file is a GTFS feed based on the Google Transit Feed Specification
    # we need to unzip the file into a temp directory and then parse the routes.txt file

    routes_content = read_schedule_file_contents(schedule_file_path, "routes.txt")
    if not routes_content:
        logger.info("No routes found in the schedule file")
        return
    routes = map_routes(routes_content)
    for route in routes:
        logger.info("- %s: %s - %s", route.routeId, route.routeShortName, route.routeLongName)


async def print_stops(gtfs_url: str, mdb_source_id: str, headers: dict, route_id: str = None):
    """
    Helper function to print the list of stops in the Mobility Database.
    """
    schedule_file_path = fetch_schedule_file(gtfs_url, mdb_source_id, headers)
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
            logger.info(f"- {key}: {stop.stopId}: {stop.stopName}, ({stop.stopLat},{stop.stopLon}), https://geohack.toolforge.org/geohack.php?language=en&params={stop.stopLat};{stop.stopLon}")
    else:
        logger.info(f"Stops for {mdb_source_id}:")
        for stop in stop_data:
            logger.info(f"- {stop.stopId}: {stop.stopName}, ({stop.stopLat},{stop.stopLon}), https://geohack.toolforge.org/geohack.php?language=en&params={stop.stopLat};{stop.stopLon}")


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
    await print_stops(args.gtfs_url, args.mdb_source_id, headers, args.route)


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
    await print_routes(args.gtfs_url, args.mdb_source_id, headers)


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    """
    Parse the connection string and extract bootstrap server, topic name, username, and password.

    Args:
        connection_string (str): The connection string.

    Returns:
        Dict[str, str]: Extracted connection parameters.
    """
    config_dict = {
        'sasl.username': '$ConnectionString',
        'sasl.password': connection_string.strip(),
    }
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '')+':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    return config_dict


async def run_feed(args):
    """
    Helper function to launch the feed function with the specified arguments.

    Args:
        args: The command-line arguments.
    """

    if not args.gtfs_urls and not args.mdb_source_id:
        raise ValueError("No GTFS URL or Mobility Database source ID specified")
    poll_interval = args.poll_interval
    headers = None
    if args.header:
        headers = {k: v for k, v in args.header}

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

    await feed_realtime_messages(kafka_bootstrap_servers, kafka_topic, sasl_username, sasl_password,
                           args.gtfs_urls, args.schedule_url, args.mdb_source_id, headers, args.route, args.poll_interval, args.cloudevents_mode)


async def main():
    """
    Main function to parse the command-line arguments and execute the selected command.
    """
    # Define the command-line arguments and subcommands
    parser = argparse.ArgumentParser(description="Real-time transit data bridge for the Mobility Database and GTFS")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Define the "feed" command
    feed_parser = subparsers.add_parser("feed", help="poll vehicle locations and submit to a Kafka endpoint, Event Hub, or Fabric Event Stream custom endpoint")
    feed_parser.add_argument('--kafka-bootstrap-servers', type=str, help="Comma separated list of Kafka bootstrap servers")
    feed_parser.add_argument('--kafka-topic', type=str, help="Kafka topic to send messages to")
    feed_parser.add_argument('--sasl-username', type=str, help="Username for SASL PLAIN authentication")
    feed_parser.add_argument('--sasl-password', type=str, help="Password for SASL PLAIN authentication")
    feed_parser.add_argument('-c', '--connection-string', dest="connection_string", type=str, help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    feed_parser.add_argument("-r", "--route", help="the route to poll vehicle locations for, omit or '*' to poll all routes", required=False, default="*")
    feed_parser.add_argument("--gtfs-urls", help="the URL(s) of the GTFS Realtime feed(s)", required=False, default=None, nargs="+")
    feed_parser.add_argument("--schedule-url", help="the URL of the GTFS Schedule feed", required=False, default=None)
    feed_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Realtime feed", required=False, default=None)
    feed_parser.add_argument('--header', action='append', nargs=2, help='HTTP header expressed as a pair of strings to send with the request to the GTFS Realtime feed, e.g. "API-Key abc')
    feed_parser.add_argument("--poll-interval", help="the number of seconds to wait between polling vehicle locations", required=False, type=float, default=20)
    feed_parser.add_argument("--cloudevents-mode", help="the CloudEvents mode to use for the Kafka producer", required=False, choices=["structured", "binary"], default="structured")
    feed_parser.set_defaults(func=run_feed)

    # Define the "printfeed" command
    vehicle_locations_parser = subparsers.add_parser("printfeed", help="Print the feed data for a route for a single request")
    vehicle_locations_parser.add_argument("--agency", help="the tag of the agency to get vehicle locations for", required=False)
    vehicle_locations_parser.add_argument("-r", "--route", help="the route to get vehicle locations for", required=False)
    vehicle_locations_parser.add_argument("--gtfs-url", help="the URL of the GTFS Realtime feed", required=False)
    vehicle_locations_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Realtime feed", required=False, default=None)
    vehicle_locations_parser.add_argument('--header', action='append', nargs=2,
                                          help='HTTP header to send with the request to the GTFS Realtime feed')
    async def cmd_print_feed_items(args):
        if not args.gtfs_url and not args.mdb_source_id:
            raise ValueError("No GTFS URL or Mobility Database source ID specified")
        headers = {}
        if args.header:
            headers = {k: v for k, v in args.header}
        await print_feed_items(args.gtfs_url, args.mdb_source_id, headers, args.agency, args.route)

    vehicle_locations_parser.set_defaults(func=cmd_print_feed_items)

    # Define the "agencies" command that lists the agencies in the Mobility Database, using the schedule data
    agencies_parser = subparsers.add_parser("agencies", help="get the list of transit agencies")
    agencies_parser.set_defaults(func=run_print_agencies)

    route_parser = subparsers.add_parser("routes", help="get the list of routes for an agency")
    route_parser.add_argument("gtfs_url", help="the URL of the GTFS Schedule feed")
    route_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Schedule feed", required=False, default=None)
    route_parser.add_argument('--header', action='append', nargs=2,
                              help='HTTP header to send with the request to the GTFS Realtime feed')
    route_parser.set_defaults(func=run_print_routes)

    # Define the "stops" command that lists the stops for a route
    stops_parser = subparsers.add_parser("stops", help="get the list of stops for a route")
    stops_parser.add_argument("-r", "--route", help="the route to get stops for", required=False)
    stops_parser.add_argument("gtfs_url", help="the URL of the GTFS Schedule feed")
    stops_parser.add_argument("-m", "--mdb-source-id", help="the Mobility Database source ID of the GTFS Schedule feed", required=False, default=None)
    stops_parser.add_argument('--header', action='append', nargs=2,
                              help='HTTP header to send with the request to the GTFS Realtime feed')
    stops_parser.set_defaults(func=run_print_stops)

    # Parse the command-line arguments and execute the selected command
    args = parser.parse_args()
    # Check if the 'func' attribute is present in the 'Namespace' object
    if hasattr(args, 'func') and callable(args.func):
        await args.func(args)
    else:
        parser.print_help()

def cli():
    asyncio.run(main())

if __name__ == "__main__":
    cli()