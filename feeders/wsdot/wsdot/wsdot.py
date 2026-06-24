"""WSDOT Traveler Information and Ferries bridge to Kafka."""

import os
import re
import sys
import time
import json
import logging
import argparse
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
from confluent_kafka import Producer
from wsdot_producer_data.us.wa.wsdot.traffic.trafficflowstation import TrafficFlowStation
from wsdot_producer_data.us.wa.wsdot.traffic.trafficflowreading import TrafficFlowReading
from wsdot_producer_data.us.wa.wsdot.traveltimes.traveltimeroute import TravelTimeRoute
from wsdot_producer_data.us.wa.wsdot.mountainpass.mountainpasscondition import MountainPassCondition
from wsdot_producer_data.us.wa.wsdot.weather.weatherstation import WeatherStation
from wsdot_producer_data.us.wa.wsdot.weather.weatherreading import WeatherReading
from wsdot_producer_data.us.wa.wsdot.tolls.tollrate import TollRate
from wsdot_producer_data.us.wa.wsdot.cvrestrictions.commercialvehiclerestriction import CommercialVehicleRestriction
from wsdot_producer_data.us.wa.wsdot.border.bordercrossing import BorderCrossing
from wsdot_producer_data.us.wa.wsdot.ferries.vessellocation import VesselLocation
from wsdot_producer_data.us.wa.wsdot.roadweather.roadweatherstation import RoadWeatherStation
from wsdot_producer_data.us.wa.wsdot.roadweather.roadweatherreading import RoadWeatherReading
from wsdot_producer_data.us.wa.wsdot.roadweather.surfacemeasurement import SurfaceMeasurement
from wsdot_producer_data.us.wa.wsdot.roadweather.subsurfacemeasurement import SubSurfaceMeasurement
from wsdot_producer_data.us.wa.wsdot.alerts.highwayalert import HighwayAlert
from wsdot_producer_data.us.wa.wsdot.cameras.highwaycamera import HighwayCamera
from wsdot_producer_data.us.wa.wsdot.bridgeclearances.bridgeclearance import BridgeClearance
from wsdot_producer_data.us.wa.wsdot.ferryterminals.terminalsailingspace import TerminalSailingSpace
from wsdot_producer_data.us.wa.wsdot.ferryterminals.departingspace import DepartingSpace
from wsdot_producer_data.us.wa.wsdot.ferryterminals.spaceforarrivalterminal import SpaceForArrivalTerminal
from cloudevents.http import CloudEvent
from cloudevents.kafka import to_binary, to_structured
from wsdot_producer_kafka_producer.producer import UsWaWsdotTrafficEventProducer
from wsdot_producer_data.us.wa.wsdot.traffic.flowreadingenum import FlowReadingenum


class _WsdotEventProducer:
    def __init__(self, producer: Producer, topic: str, content_mode: str = "structured"):
        self.producer = producer
        self.topic = topic
        self.content_mode = content_mode

    @staticmethod
    def _map_key(event: CloudEvent, data: Any, key_mapper, default_key: str):
        if key_mapper:
            return key_mapper(event, data)
        return default_key or f"{event['type']}:{event['source']}-{event.get('subject', '')}"

    def _send(self, event_type: str, source: str, subject: str, key: str, data: Any, content_type: str, flush_producer: bool, key_mapper) -> None:
        event = CloudEvent.create({"type": event_type, "source": source, "subject": subject, "datacontenttype": content_type}, data)
        if self.content_mode == "structured":
            message = to_structured(event, data_marshaller=lambda x: json.loads(x.to_json()), key_mapper=lambda x: self._map_key(x, data, key_mapper, key))
            message.headers["content-type"] = b"application/cloudevents+json"
        else:
            message = to_binary(event, data_marshaller=lambda x: x.to_byte_array("application/json"), key_mapper=lambda x: self._map_key(x, data, key_mapper, key))
        self.producer.produce(self.topic, key=message.key, value=message.value, headers=message.headers)  # type: ignore[arg-type]
        if flush_producer:
            self.producer.flush()


class UsWaWsdotTraveltimesEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_traveltimes_travel_time_route(self, _feedurl: str, _travel_time_id: str, data: TravelTimeRoute, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.traveltimes.TravelTimeRoute", _feedurl, _travel_time_id, _travel_time_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotMountainpassEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_mountainpass_mountain_pass_condition(self, _feedurl: str, _mountain_pass_id: str, data: MountainPassCondition, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.mountainpass.MountainPassCondition", _feedurl, _mountain_pass_id, _mountain_pass_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotWeatherEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_weather_weather_station(self, _feedurl: str, _station_id: str, data: WeatherStation, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.weather.WeatherStation", _feedurl, _station_id, _station_id, data, content_type, flush_producer, key_mapper)

    def send_us_wa_wsdot_weather_weather_reading(self, _feedurl: str, _station_id: str, data: WeatherReading, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.weather.WeatherReading", _feedurl, _station_id, _station_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotTollsEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_tolls_toll_rate(self, _feedurl: str, _trip_name: str, data: TollRate, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.tolls.TollRate", _feedurl, _trip_name, _trip_name, data, content_type, flush_producer, key_mapper)


class UsWaWsdotCvrestrictionsEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction(self, _feedurl: str, _state_route_id: str, _bridge_number: str, data: CommercialVehicleRestriction, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        subject = f"{_state_route_id}/{_bridge_number}"
        self._send("us.wa.wsdot.cvrestrictions.CommercialVehicleRestriction", _feedurl, subject, subject, data, content_type, flush_producer, key_mapper)


class UsWaWsdotBorderEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_border_border_crossing(self, _feedurl: str, _crossing_name: str, data: BorderCrossing, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.border.BorderCrossing", _feedurl, _crossing_name, _crossing_name, data, content_type, flush_producer, key_mapper)


class UsWaWsdotFerriesEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_ferries_vessel_location(self, _feedurl: str, _vessel_id: str, data: VesselLocation, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.ferries.VesselLocation", _feedurl, _vessel_id, _vessel_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotRoadweatherEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_roadweather_road_weather_station(self, _feedurl: str, _station_id: str, data: RoadWeatherStation, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.roadweather.RoadWeatherStation", _feedurl, _station_id, _station_id, data, content_type, flush_producer, key_mapper)

    def send_us_wa_wsdot_roadweather_road_weather_reading(self, _feedurl: str, _station_id: str, data: RoadWeatherReading, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.roadweather.RoadWeatherReading", _feedurl, _station_id, _station_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotAlertsEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_alerts_highway_alert(self, _feedurl: str, _alert_id: str, data: HighwayAlert, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.alerts.HighwayAlert", _feedurl, _alert_id, _alert_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotCamerasEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_cameras_highway_camera(self, _feedurl: str, _camera_id: str, data: HighwayCamera, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.cameras.HighwayCamera", _feedurl, _camera_id, _camera_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotBridgeclearancesEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_bridgeclearances_bridge_clearance(self, _feedurl: str, _crossing_location_id: str, data: BridgeClearance, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.bridgeclearances.BridgeClearance", _feedurl, _crossing_location_id, _crossing_location_id, data, content_type, flush_producer, key_mapper)


class UsWaWsdotFerryterminalsEventProducer(_WsdotEventProducer):
    def send_us_wa_wsdot_ferryterminals_terminal_sailing_space(self, _feedurl: str, _terminal_id: str, data: TerminalSailingSpace, content_type: str = "application/json", flush_producer=True, key_mapper=None) -> None:
        self._send("us.wa.wsdot.ferryterminals.TerminalSailingSpace", _feedurl, _terminal_id, _terminal_id, data, content_type, flush_producer, key_mapper)


if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

TRAVELER_BASE = "https://www.wsdot.wa.gov/Traffic/api"
FERRIES_BASE = "https://www.wsdot.wa.gov/ferries/api/vessels/rest"
FERRIES_TERMINALS_BASE = "https://www.wsdot.wa.gov/ferries/api/terminals/rest"
# WSDOT Scanweb (RWIS) road weather endpoint. Distinct host/path from the
# Traveler Information REST services; takes an AccessCode query parameter.
SCANWEB_URL = "https://wsdot.wa.gov/traffic/api/api/Scanweb"
# Bridge vertical clearances are served by the Bridges service under a
# differently-named .svc (ClearanceREST, not BridgesREST), so it does not fit
# the generic _traveler_get pattern and has its own fetch method.
BRIDGE_CLEARANCES_URL = "https://www.wsdot.wa.gov/Traffic/api/Bridges/ClearanceREST.svc/GetClearancesAsJson"
FEED_URL = "https://www.wsdot.wa.gov/Traffic/api"
# Outbound HTTP identity. Operators can override the entire string with the
# USER_AGENT env var, or just the contact token with USER_AGENT_CONTACT.
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-wsdot/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

_WCF_DATE_RE = re.compile(r"/Date\((-?\d+)([+-]\d{4})?\)/")

_FLOW_READING_MAP = {
    0: "Unknown",
    1: "WideOpen",
    2: "Moderate",
    3: "Heavy",
    4: "StopAndGo",
    5: "NoData",
}


def _parse_wcf_date(wcf_date: str) -> str:
    """Parse a WCF JSON date string to ISO 8601 UTC."""
    m = _WCF_DATE_RE.search(wcf_date)
    if not m:
        return wcf_date
    millis = int(m.group(1))
    dt = datetime.fromtimestamp(millis / 1000.0, tz=timezone.utc)
    return dt.isoformat()


def _normalize_dt(value: Any) -> Optional[str]:
    """Normalize an upstream timestamp to ISO 8601 UTC.

    Handles both the legacy WCF ``/Date(...)/`` form and ISO 8601 strings that
    already carry a timezone offset (the HighwayAlerts/Bridges/terminals
    services return ``DateTimeOffset`` values serialized as ISO 8601). Returns
    ``None`` for empty input and falls back to the original string if it cannot
    be parsed.
    """
    if not value:
        return None
    if not isinstance(value, str):
        return None
    if _WCF_DATE_RE.search(value):
        return _parse_wcf_date(value)
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        return value
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def _safe_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def _safe_int(v: Any) -> Optional[int]:
    if v is None:
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


class WSDOTApi:
    """Client for the WSDOT Traveler Information and Ferries REST APIs."""

    def __init__(self, access_code: str):
        self.access_code = access_code
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        })

    def _traveler_get(self, service: str, method: str) -> Any:
        resp = self.session.get(
            f"{TRAVELER_BASE}/{service}/{service}REST.svc/Get{method}AsJson",
            params={"AccessCode": self.access_code},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_traffic_flows(self) -> List[Dict[str, Any]]:
        return self._traveler_get("TrafficFlow", "TrafficFlows")

    def fetch_travel_times(self) -> List[Dict[str, Any]]:
        return self._traveler_get("TravelTimes", "TravelTimes")

    def fetch_mountain_pass_conditions(self) -> List[Dict[str, Any]]:
        return self._traveler_get("MountainPassConditions", "MountainPassConditions")

    def fetch_weather_information(self) -> List[Dict[str, Any]]:
        return self._traveler_get("WeatherInformation", "CurrentWeatherInformation")

    def fetch_toll_rates(self) -> List[Dict[str, Any]]:
        return self._traveler_get("TollRates", "TollRates")

    def fetch_cv_restrictions(self) -> List[Dict[str, Any]]:
        return self._traveler_get("CVRestrictions", "CommercialVehicleRestrictions")

    def fetch_border_crossings(self) -> List[Dict[str, Any]]:
        return self._traveler_get("BorderCrossings", "BorderCrossings")

    def fetch_vessel_locations(self) -> List[Dict[str, Any]]:
        resp = self.session.get(
            f"{FERRIES_BASE}/vessellocations",
            params={"apiaccesscode": self.access_code},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_road_weather(self) -> List[Dict[str, Any]]:
        resp = self.session.get(
            SCANWEB_URL,
            params={"AccessCode": self.access_code},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_highway_alerts(self) -> List[Dict[str, Any]]:
        return self._traveler_get("HighwayAlerts", "Alerts")

    def fetch_highway_cameras(self) -> List[Dict[str, Any]]:
        return self._traveler_get("HighwayCameras", "Cameras")

    def fetch_bridge_clearances(self) -> List[Dict[str, Any]]:
        resp = self.session.get(
            BRIDGE_CLEARANCES_URL,
            params={"AccessCode": self.access_code},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_terminal_sailing_space(self) -> List[Dict[str, Any]]:
        resp = self.session.get(
            f"{FERRIES_TERMINALS_BASE}/terminalsailingspace",
            params={"apiaccesscode": self.access_code},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def parse_station(raw: Dict[str, Any]) -> TrafficFlowStation:
        location = raw.get("FlowStationLocation") or {}
        return TrafficFlowStation(
            flow_data_id=str(raw.get("FlowDataID", "")),
            station_name=raw.get("StationName", ""),
            region=raw.get("Region", ""),
            description=location.get("Description") or None,
            road_name=location.get("RoadName", ""),
            direction=location.get("Direction") or None,
            milepost=_safe_float(location.get("MilePost")),
            latitude=float(location.get("Latitude", 0.0)),
            longitude=float(location.get("Longitude", 0.0)),
        )

    @staticmethod
    def parse_reading(raw: Dict[str, Any]) -> TrafficFlowReading:
        flow_value = int(raw.get("FlowReadingValue", 0))
        flow_reading = _FLOW_READING_MAP.get(flow_value, "Unknown")
        time_str = raw.get("Time", "")
        reading_time = _parse_wcf_date(time_str) if time_str else datetime.now(timezone.utc).isoformat()
        return TrafficFlowReading(
            flow_data_id=str(raw.get("FlowDataID", "")),
            station_name=raw.get("StationName", ""),
            region=raw.get("Region", ""),
            flow_reading=FlowReadingenum(flow_reading),
            reading_time=reading_time,
        )

    @staticmethod
    def parse_travel_time(raw: Dict[str, Any]) -> TravelTimeRoute:
        sp = raw.get("StartPoint") or {}
        ep = raw.get("EndPoint") or {}
        time_str = raw.get("TimeUpdated", "")
        return TravelTimeRoute(
            travel_time_id=str(raw.get("TravelTimeID", "")),
            name=raw.get("Name", ""),
            description=raw.get("Description", ""),
            distance=float(raw.get("Distance", 0.0)),
            average_time=int(raw.get("AverageTime", 0)),
            current_time=int(raw.get("CurrentTime", 0)),
            time_updated=_parse_wcf_date(time_str) if time_str else datetime.now(timezone.utc).isoformat(),
            start_description=sp.get("Description") or None,
            start_road_name=sp.get("RoadName") or None,
            start_direction=sp.get("Direction") or None,
            start_milepost=_safe_float(sp.get("MilePost")),
            start_latitude=float(sp.get("Latitude", 0.0)),
            start_longitude=float(sp.get("Longitude", 0.0)),
            end_description=ep.get("Description") or None,
            end_road_name=ep.get("RoadName") or None,
            end_direction=ep.get("Direction") or None,
            end_milepost=_safe_float(ep.get("MilePost")),
            end_latitude=float(ep.get("Latitude", 0.0)),
            end_longitude=float(ep.get("Longitude", 0.0)),
        )

    @staticmethod
    def parse_mountain_pass(raw: Dict[str, Any]) -> MountainPassCondition:
        r1 = raw.get("RestrictionOne") or {}
        r2 = raw.get("RestrictionTwo") or {}
        date_str = raw.get("DateUpdated", "")
        return MountainPassCondition(
            mountain_pass_id=str(raw.get("MountainPassId", "")),
            mountain_pass_name=raw.get("MountainPassName", ""),
            elevation_in_feet=int(raw.get("ElevationInFeet", 0)),
            latitude=float(raw.get("Latitude", 0.0)),
            longitude=float(raw.get("Longitude", 0.0)),
            temperature_in_fahrenheit=_safe_int(raw.get("TemperatureInFahrenheit")),
            weather_condition=raw.get("WeatherCondition", ""),
            road_condition=raw.get("RoadCondition", ""),
            travel_advisory_active=bool(raw.get("TravelAdvisoryActive", False)),
            restriction_one_direction=r1.get("TravelDirection") or None,
            restriction_one_text=r1.get("RestrictionText") or None,
            restriction_two_direction=r2.get("TravelDirection") or None,
            restriction_two_text=r2.get("RestrictionText") or None,
            date_updated=_parse_wcf_date(date_str) if date_str else datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def parse_weather_station(raw: Dict[str, Any]) -> WeatherStation:
        # Station reference is synthesized from the current-readings payload
        # (the legacy WeatherStations endpoint was decommissioned), so the
        # identity field is the numeric StationID that the readings also carry.
        return WeatherStation(
            station_id=str(raw.get("StationID", "")),
            station_name=raw.get("StationName", ""),
            latitude=float(raw.get("Latitude", 0.0)),
            longitude=float(raw.get("Longitude", 0.0)),
        )

    @staticmethod
    def parse_weather_reading(raw: Dict[str, Any]) -> WeatherReading:
        time_str = raw.get("ReadingTime", "")
        return WeatherReading(
            station_id=str(raw.get("StationID", "")),
            station_name=raw.get("StationName", ""),
            reading_time=_parse_wcf_date(time_str) if time_str else datetime.now(timezone.utc).isoformat(),
            temperature_in_fahrenheit=_safe_float(raw.get("TemperatureInFahrenheit")),
            precipitation_in_inches=_safe_float(raw.get("PrecipitationInInches")),
            wind_speed_in_mph=_safe_float(raw.get("WindSpeedInMPH")),
            wind_gust_speed_in_mph=_safe_float(raw.get("WindGustSpeedInMPH")),
            wind_direction=_safe_int(raw.get("WindDirection")),
            wind_direction_cardinal=raw.get("WindDirectionCardinal") or None,
            barometric_pressure=_safe_float(raw.get("BarometricPressure")),
            relative_humidity=_safe_int(raw.get("RelativeHumidity")),
            visibility=_safe_float(raw.get("Visibility")),
            sky_coverage=raw.get("SkyCoverage") or None,
            latitude=float(raw.get("Latitude", 0.0)),
            longitude=float(raw.get("Longitude", 0.0)),
        )

    @staticmethod
    def parse_toll_rate(raw: Dict[str, Any]) -> TollRate:
        time_str = raw.get("TimeUpdated", "")
        return TollRate(
            trip_name=raw.get("TripName", ""),
            state_route=str(raw.get("StateRoute", "")),
            travel_direction=raw.get("TravelDirection", ""),
            current_toll=int(raw.get("CurrentToll", 0)),
            current_message=raw.get("CurrentMessage") or None,
            time_updated=_parse_wcf_date(time_str) if time_str else datetime.now(timezone.utc).isoformat(),
            start_location_name=raw.get("StartLocationName", ""),
            start_latitude=float(raw.get("StartLatitude", 0.0)),
            start_longitude=float(raw.get("StartLongitude", 0.0)),
            start_milepost=float(raw.get("StartMilepost", 0.0)),
            end_location_name=raw.get("EndLocationName", ""),
            end_latitude=float(raw.get("EndLatitude", 0.0)),
            end_longitude=float(raw.get("EndLongitude", 0.0)),
            end_milepost=float(raw.get("EndMilepost", 0.0)),
        )

    @staticmethod
    def parse_cv_restriction(raw: Dict[str, Any]) -> CommercialVehicleRestriction:
        start_loc = raw.get("StartRoadwayLocation") or {}
        date_posted = raw.get("DatePosted", "")
        date_effective = raw.get("DateEffective", "")
        date_expires = raw.get("DateExpires", "")
        return CommercialVehicleRestriction(
            state_route_id=raw.get("StateRouteID", ""),
            bridge_number=raw.get("BridgeNumber", ""),
            bridge_name=raw.get("BridgeName") or None,
            location_name=start_loc.get("Description") or None,
            location_description=raw.get("RestrictionComment") or None,
            latitude=float(start_loc.get("Latitude", 0.0)),
            longitude=float(start_loc.get("Longitude", 0.0)),
            state=start_loc.get("State") or None,
            restriction_type=raw.get("RestrictionType") or None,
            vehicle_type=raw.get("VehicleType") or None,
            restriction_weight_in_pounds=_safe_int(raw.get("RestrictionWeightInPounds")),
            maximum_gross_vehicle_weight_in_pounds=_safe_int(raw.get("MaximumGrossVehicleWeightInPounds")),
            restriction_height_in_inches=_safe_int(raw.get("RestrictionHeightInInches")),
            restriction_width_in_inches=_safe_int(raw.get("RestrictionWidthInInches")),
            restriction_length_in_inches=_safe_int(raw.get("RestrictionLengthInInches")),
            is_permanent_restriction=bool(raw.get("IsPermanentRestriction", False)),
            is_warning=bool(raw.get("IsWarning", False)),
            is_detour_available=bool(raw.get("IsDetourAvailable", False)),
            is_exceptions_allowed=bool(raw.get("IsExceptionsAllowed", False)),
            restriction_comment=raw.get("RestrictionComment") or None,
            date_posted=_parse_wcf_date(date_posted) if date_posted else None,
            date_effective=_parse_wcf_date(date_effective) if date_effective else None,
            date_expires=_parse_wcf_date(date_expires) if date_expires else None,
        )

    @staticmethod
    def parse_border_crossing(raw: Dict[str, Any]) -> BorderCrossing:
        loc = raw.get("BorderCrossingLocation") or {}
        time_str = raw.get("Time", "")
        return BorderCrossing(
            crossing_name=raw.get("CrossingName", ""),
            wait_time=_safe_int(raw.get("WaitTime")),
            time=_parse_wcf_date(time_str) if time_str else datetime.now(timezone.utc).isoformat(),
            description=loc.get("Description") or None,
            road_name=loc.get("RoadName") or None,
            latitude=float(loc.get("Latitude", 0.0)),
            longitude=float(loc.get("Longitude", 0.0)),
        )

    @staticmethod
    def parse_vessel_location(raw: Dict[str, Any]) -> VesselLocation:
        ts = raw.get("TimeStamp", "")
        sched = raw.get("ScheduledDeparture", "")
        left = raw.get("LeftDock", "")
        eta_str = raw.get("Eta", "")
        op_routes = raw.get("OpRouteAbbrev") or []
        route_abbrev = op_routes[0] if op_routes else None
        return VesselLocation(
            vessel_id=str(raw.get("VesselID", "")),
            vessel_name=raw.get("VesselName", ""),
            mmsi=_safe_int(raw.get("Mmsi")),
            in_service=bool(raw.get("InService", False)),
            at_dock=bool(raw.get("AtDock", False)),
            latitude=float(raw.get("Latitude", 0.0)),
            longitude=float(raw.get("Longitude", 0.0)),
            speed=_safe_float(raw.get("Speed")),
            heading=_safe_int(raw.get("Heading")),
            departing_terminal_id=_safe_int(raw.get("DepartingTerminalID")),
            departing_terminal_name=raw.get("DepartingTerminalName") or None,
            departing_terminal_abbrev=raw.get("DepartingTerminalAbbrev") or None,
            arriving_terminal_id=_safe_int(raw.get("ArrivingTerminalID")),
            arriving_terminal_name=raw.get("ArrivingTerminalName") or None,
            arriving_terminal_abbrev=raw.get("ArrivingTerminalAbbrev") or None,
            scheduled_departure=_parse_wcf_date(sched) if sched else None,
            left_dock=_parse_wcf_date(left) if left else None,
            eta=_parse_wcf_date(eta_str) if eta_str else None,
            eta_basis=raw.get("EtaBasis") or None,
            route_abbreviation=route_abbrev,
            timestamp=_parse_wcf_date(ts) if ts else datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def _road_weather_station_id(raw: Dict[str, Any]) -> str:
        # A few Scanweb stations report a blank StationId (whitespace); fall
        # back to the unique StationName so every station has a stable,
        # non-empty key that aligns subject and Kafka key.
        sid = (raw.get("StationId") or "").strip()
        return sid or (raw.get("StationName") or "").strip()

    @staticmethod
    def parse_road_weather_station(raw: Dict[str, Any]) -> RoadWeatherStation:
        return RoadWeatherStation(
            station_id=WSDOTApi._road_weather_station_id(raw),
            station_name=raw.get("StationName", ""),
            latitude=float(raw.get("Latitude", 0.0)),
            longitude=float(raw.get("Longitude", 0.0)),
            elevation=_safe_int(raw.get("Elevation")),
        )

    @staticmethod
    def parse_road_weather_reading(raw: Dict[str, Any]) -> RoadWeatherReading:
        surfaces = [
            SurfaceMeasurement(
                sensor_id=_safe_int(sm.get("SensorId")) or 0,
                surface_temperature=_safe_float(sm.get("SurfaceTemperature")),
                road_freezing_temperature=_safe_float(sm.get("RoadFreezingTemperature")),
                road_surface_condition=_safe_int(sm.get("RoadSurfaceCondition")),
            )
            for sm in (raw.get("SurfaceMeasurements") or [])
        ]
        sub_surfaces = [
            SubSurfaceMeasurement(
                sensor_id=_safe_int(sm.get("SensorId")) or 0,
                sub_surface_temperature=_safe_float(sm.get("SubSurfaceTemperature")),
            )
            for sm in (raw.get("SubSurfaceMeasurements") or [])
        ]
        return RoadWeatherReading(
            station_id=WSDOTApi._road_weather_station_id(raw),
            station_name=raw.get("StationName", ""),
            latitude=float(raw.get("Latitude", 0.0)),
            longitude=float(raw.get("Longitude", 0.0)),
            elevation=_safe_int(raw.get("Elevation")),
            # ReadingTime has no timezone offset; the schema documents it as the
            # station's local reporting clock, so it is preserved verbatim.
            reading_time=raw.get("ReadingTime") or datetime.now(timezone.utc).isoformat(),
            air_temperature=_safe_float(raw.get("AirTemperature")),
            relative_humidity=_safe_int(raw.get("RelativeHumidty")),
            average_wind_speed=_safe_float(raw.get("AverageWindSpeed")),
            average_wind_direction=_safe_int(raw.get("AverageWindDirection")),
            wind_gust=_safe_float(raw.get("WindGust")),
            visibility=_safe_int(raw.get("Visibility")),
            precipitation_intensity=_safe_int(raw.get("PrecipitationIntensity")),
            precipitation_type=_safe_int(raw.get("PrecipitationType")),
            precipitation_past_1_hour=_safe_float(raw.get("PrecipitationPast1Hour")),
            precipitation_past_3_hours=_safe_float(raw.get("PrecipitationPast3Hours")),
            precipitation_past_6_hours=_safe_float(raw.get("PrecipitationPast6Hours")),
            precipitation_past_12_hours=_safe_float(raw.get("PrecipitationPast12Hours")),
            precipitation_past_24_hours=_safe_float(raw.get("PrecipitationPast24Hours")),
            precipitation_accumulation=_safe_float(raw.get("PrecipitationAccumulation")),
            barometric_pressure=_safe_float(raw.get("BarometricPressure")),
            snow_depth=_safe_float(raw.get("SnowDepth")),
            surface_measurements=surfaces,
            sub_surface_measurements=sub_surfaces,
        )

    @staticmethod
    def parse_highway_alert(raw: Dict[str, Any]) -> HighwayAlert:
        start_loc = raw.get("StartRoadwayLocation") or {}
        end_loc = raw.get("EndRoadwayLocation") or {}
        return HighwayAlert(
            alert_id=str(raw.get("AlertID", "")),
            county=raw.get("County") or None,
            region=raw.get("Region") or None,
            priority=raw.get("Priority") or None,  # type: ignore[arg-type]
            event_category=raw.get("EventCategory") or None,
            event_status=raw.get("EventStatus") or None,  # type: ignore[arg-type]
            headline_description=raw.get("HeadlineDescription") or None,
            extended_description=raw.get("ExtendedDescription") or None,
            start_time=_normalize_dt(raw.get("StartTime")),
            end_time=_normalize_dt(raw.get("EndTime")),
            last_updated_time=_normalize_dt(raw.get("LastUpdatedTime")),
            start_description=start_loc.get("Description") or None,
            start_direction=start_loc.get("Direction") or None,
            start_road_name=start_loc.get("RoadName") or None,
            start_milepost=_safe_float(start_loc.get("MilePost")),
            start_latitude=_safe_float(start_loc.get("Latitude")),
            start_longitude=_safe_float(start_loc.get("Longitude")),
            end_description=end_loc.get("Description") or None,
            end_direction=end_loc.get("Direction") or None,
            end_road_name=end_loc.get("RoadName") or None,
            end_milepost=_safe_float(end_loc.get("MilePost")),
            end_latitude=_safe_float(end_loc.get("Latitude")),
            end_longitude=_safe_float(end_loc.get("Longitude")),
        )

    @staticmethod
    def parse_highway_camera(raw: Dict[str, Any]) -> HighwayCamera:
        loc = raw.get("CameraLocation") or {}
        return HighwayCamera(
            camera_id=str(raw.get("CameraID", "")),
            title=raw.get("Title") or None,
            description=raw.get("Description") or None,
            camera_owner=raw.get("CameraOwner") or None,
            owner_url=raw.get("OwnerURL") or None,
            image_url=raw.get("ImageURL", ""),
            image_width=_safe_int(raw.get("ImageWidth")),
            image_height=_safe_int(raw.get("ImageHeight")),
            is_active=bool(raw.get("IsActive", False)),
            region=raw.get("Region") or None,
            sort_order=_safe_int(raw.get("SortOrder")),
            display_latitude=_safe_float(raw.get("DisplayLatitude")),
            display_longitude=_safe_float(raw.get("DisplayLongitude")),
            location_description=loc.get("Description") or None,
            location_direction=loc.get("Direction") or None,
            location_road_name=loc.get("RoadName") or None,
            location_milepost=_safe_float(loc.get("MilePost")),
            location_latitude=_safe_float(loc.get("Latitude")),
            location_longitude=_safe_float(loc.get("Longitude")),
        )

    @staticmethod
    def parse_bridge_clearance(raw: Dict[str, Any]) -> BridgeClearance:
        return BridgeClearance(
            crossing_location_id=str(raw.get("CrossingLocationId", "")),
            bridge_number=raw.get("BridgeNumber") or None,
            state_route_id=(str(raw["StateRouteID"]) if raw.get("StateRouteID") is not None else None),
            state_structure_id=raw.get("StateStructureId") or None,
            crossing_description=raw.get("CrossingDescription") or None,
            inventory_direction=raw.get("InventoryDirection") or None,
            srmp=_safe_float(raw.get("SRMP")),
            srmp_ahead_back_indicator=raw.get("SRMPAheadBackIndicator") or None,
            latitude=_safe_float(raw.get("Latitude")),
            longitude=_safe_float(raw.get("Longitude")),
            vertical_clearance_maximum_inches=_safe_int(raw.get("VerticalClearanceMaximumInches")),
            vertical_clearance_maximum_feet_inch=raw.get("VerticalClearanceMaximumFeetInch") or None,
            vertical_clearance_minimum_inches=_safe_int(raw.get("VerticalClearanceMinimumInches")),
            vertical_clearance_minimum_feet_inch=raw.get("VerticalClearanceMinimumFeetInch") or None,
            control_entity_guid=raw.get("ControlEntityGuid") or None,
            crossing_record_guid=raw.get("CrossingRecordGuid") or None,
            location_guid=raw.get("LocationGuid") or None,
            route_date=_normalize_dt(raw.get("RouteDate")),
            api_last_update=_normalize_dt(raw.get("APILastUpdate")),
        )

    @staticmethod
    def parse_terminal_sailing_space(raw: Dict[str, Any]) -> TerminalSailingSpace:
        departing = []
        for ds in (raw.get("DepartingSpaces") or []):
            arrivals = [
                SpaceForArrivalTerminal(
                    terminal_id=_safe_int(sa.get("TerminalID")),
                    terminal_name=sa.get("TerminalName") or None,
                    vessel_id=_safe_int(sa.get("VesselID")),
                    vessel_name=sa.get("VesselName") or None,
                    display_reservable_space=bool(sa.get("DisplayReservableSpace", False)),
                    reservable_space_count=_safe_int(sa.get("ReservableSpaceCount")),
                    reservable_space_hex_color=sa.get("ReservableSpaceHexColor") or None,
                    display_drive_up_space=bool(sa.get("DisplayDriveUpSpace", False)),
                    drive_up_space_count=_safe_int(sa.get("DriveUpSpaceCount")),
                    drive_up_space_hex_color=sa.get("DriveUpSpaceHexColor") or None,
                    max_space_count=_safe_int(sa.get("MaxSpaceCount")),
                    arrival_terminal_ids=[int(t) for t in (sa.get("ArrivalTerminalIDs") or []) if t is not None],
                )
                for sa in (ds.get("SpaceForArrivalTerminals") or [])
            ]
            departing.append(DepartingSpace(
                departure=_normalize_dt(ds.get("Departure")),
                is_cancelled=bool(ds.get("IsCancelled", False)),
                vessel_id=_safe_int(ds.get("VesselID")),
                vessel_name=ds.get("VesselName") or None,
                max_space_count=_safe_int(ds.get("MaxSpaceCount")),
                space_for_arrival_terminals=arrivals,
            ))
        return TerminalSailingSpace(
            terminal_id=str(raw.get("TerminalID", "")),
            terminal_subject_id=_safe_int(raw.get("TerminalSubjectID")),
            region_id=_safe_int(raw.get("RegionID")),
            terminal_name=raw.get("TerminalName") or None,
            terminal_abbrev=raw.get("TerminalAbbrev") or None,
            sort_seq=_safe_int(raw.get("SortSeq")),
            departing_spaces=departing,
            is_no_fare_collected=(bool(raw["IsNoFareCollected"]) if raw.get("IsNoFareCollected") is not None else None),
            no_fare_collected_msg=raw.get("NoFareCollectedMsg") or None,
        )


def _parse_connection_string(connection_string: str):
    """Parse the connection string and extract Kafka config and topic."""
    config_dict: Dict[str, str] = {}
    kafka_topic = None
    try:
        for part in connection_string.split(";"):
            if "Endpoint" in part:
                config_dict["bootstrap.servers"] = (
                    part.split("=")[1].strip('"').replace("sb://", "").replace("/", "") + ":9093"
                )
            elif "EntityPath" in part:
                kafka_topic = part.split("=")[1].strip('"')
            elif "SharedAccessKeyName" in part:
                config_dict["sasl.username"] = "$ConnectionString"
            elif "SharedAccessKey" in part:
                config_dict["sasl.password"] = connection_string.strip()
            elif "BootstrapServer" in part:
                config_dict["bootstrap.servers"] = part.split("=", 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if "sasl.username" in config_dict:
        config_dict["security.protocol"] = "SASL_SSL"
        config_dict["sasl.mechanism"] = "PLAIN"
    return config_dict, kafka_topic


def _emit_batch(producer, send_fn, items, label):
    """Emit a batch of items using the given send function, return count."""
    count = 0
    for item in items:
        try:
            send_fn(item)
            count += 1
        except Exception as e:
            logging.error("Error sending %s: %s", label, e)
    producer.flush()
    return count


def feed(args):
    """Main feed loop: emit reference data then poll all channels."""
    connection_string = args.connection_string or os.environ.get("CONNECTION_STRING", "")
    if not connection_string:
        logging.error("CONNECTION_STRING is required")
        sys.exit(1)

    access_code = args.access_code or os.environ.get("WSDOT_ACCESS_CODE", "")
    if not access_code:
        logging.error(
            "WSDOT_ACCESS_CODE is required. Register for a free access code at "
            "https://www.wsdot.wa.gov/traffic/api/"
        )
        sys.exit(1)

    kafka_config, kafka_topic = _parse_connection_string(connection_string)

    tls_enabled = os.environ.get("KAFKA_ENABLE_TLS", "true").lower()
    if tls_enabled == "false" and "security.protocol" not in kafka_config:
        kafka_config["security.protocol"] = "PLAINTEXT"

    polling_interval = int(args.polling_interval or os.environ.get("POLLING_INTERVAL", "120"))
    region_filter = args.region_filter or os.environ.get("REGION_FILTER", "")
    once = bool(getattr(args, "once", False)) or os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes")

    producer = Producer(kafka_config)
    traffic_ep = UsWaWsdotTrafficEventProducer(producer, kafka_topic)
    traveltimes_ep = UsWaWsdotTraveltimesEventProducer(producer, kafka_topic)
    mountainpass_ep = UsWaWsdotMountainpassEventProducer(producer, kafka_topic)
    weather_ep = UsWaWsdotWeatherEventProducer(producer, kafka_topic)
    tolls_ep = UsWaWsdotTollsEventProducer(producer, kafka_topic)
    cvrestrictions_ep = UsWaWsdotCvrestrictionsEventProducer(producer, kafka_topic)
    border_ep = UsWaWsdotBorderEventProducer(producer, kafka_topic)
    ferries_ep = UsWaWsdotFerriesEventProducer(producer, kafka_topic)
    roadweather_ep = UsWaWsdotRoadweatherEventProducer(producer, kafka_topic)
    alerts_ep = UsWaWsdotAlertsEventProducer(producer, kafka_topic)
    cameras_ep = UsWaWsdotCamerasEventProducer(producer, kafka_topic)
    bridgeclearances_ep = UsWaWsdotBridgeclearancesEventProducer(producer, kafka_topic)
    ferryterminals_ep = UsWaWsdotFerryterminalsEventProducer(producer, kafka_topic)
    api = WSDOTApi(access_code)

    logging.info("Starting WSDOT feed to Kafka topic %s", kafka_topic)

    def _poll_and_emit(is_initial=False, emit_reference=False):
        total = 0

        # --- Traffic Flow ---
        try:
            all_flows = api.fetch_traffic_flows()
            if region_filter:
                fs = set(r.strip() for r in region_filter.split(",") if r.strip())
                all_flows = [f for f in all_flows if f.get("Region", "") in fs]

            if emit_reference:
                c = _emit_batch(producer, lambda raw: traffic_ep.send_us_wa_wsdot_traffic_traffic_flow_station(
                    _feedurl=FEED_URL, _flow_data_id=str(raw.get("FlowDataID", "")),
                    data=WSDOTApi.parse_station(raw), flush_producer=False), all_flows, "traffic station")
                total += c
                logging.info("Sent %d traffic flow stations", c)

            c = _emit_batch(producer, lambda raw: traffic_ep.send_us_wa_wsdot_traffic_traffic_flow_reading(
                _feedurl=FEED_URL, _flow_data_id=str(raw.get("FlowDataID", "")),
                data=WSDOTApi.parse_reading(raw), flush_producer=False), all_flows, "traffic reading")
            total += c
            logging.info("Sent %d traffic flow readings", c)
        except Exception as e:
            logging.error("Error fetching traffic flows: %s", e)

        # --- Travel Times ---
        try:
            travel_times = api.fetch_travel_times()
            c = _emit_batch(producer, lambda raw: traveltimes_ep.send_us_wa_wsdot_traveltimes_travel_time_route(
                _feedurl=FEED_URL, _travel_time_id=str(raw.get("TravelTimeID", "")),
                data=WSDOTApi.parse_travel_time(raw), flush_producer=False), travel_times, "travel time")
            total += c
            logging.info("Sent %d travel times", c)
        except Exception as e:
            logging.error("Error fetching travel times: %s", e)

        # --- Mountain Pass Conditions ---
        try:
            passes = api.fetch_mountain_pass_conditions()
            c = _emit_batch(producer, lambda raw: mountainpass_ep.send_us_wa_wsdot_mountainpass_mountain_pass_condition(
                _feedurl=FEED_URL, _mountain_pass_id=str(raw.get("MountainPassId", "")),
                data=WSDOTApi.parse_mountain_pass(raw), flush_producer=False), passes, "mountain pass")
            total += c
            logging.info("Sent %d mountain pass conditions", c)
        except Exception as e:
            logging.error("Error fetching mountain passes: %s", e)

        # --- Weather (current readings + synthesized station reference) ---
        try:
            weather = api.fetch_weather_information()
        except Exception as e:
            logging.error("Error fetching weather information: %s", e)
            weather = None

        if weather is not None:
            if emit_reference:
                # The legacy WeatherStations endpoint was decommissioned, so the
                # WeatherStation reference events are synthesized from the
                # current-readings payload, deduplicated by StationID. This keeps
                # the {station_id} key aligned with the WeatherReading events.
                seen_stations: Dict[str, Dict[str, Any]] = {}
                for raw in weather:
                    sid = str(raw.get("StationID", ""))
                    if sid and sid not in seen_stations:
                        seen_stations[sid] = raw
                c = _emit_batch(producer, lambda raw: weather_ep.send_us_wa_wsdot_weather_weather_station(
                    _feedurl=FEED_URL, _station_id=str(raw.get("StationID", "")),
                    data=WSDOTApi.parse_weather_station(raw), flush_producer=False),
                    list(seen_stations.values()), "weather station")
                total += c
                logging.info("Sent %d weather stations", c)

            c = _emit_batch(producer, lambda raw: weather_ep.send_us_wa_wsdot_weather_weather_reading(
                _feedurl=FEED_URL, _station_id=str(raw.get("StationID", "")),
                data=WSDOTApi.parse_weather_reading(raw), flush_producer=False), weather, "weather reading")
            total += c
            logging.info("Sent %d weather readings", c)

        # --- Toll Rates ---
        try:
            tolls = api.fetch_toll_rates()
            c = _emit_batch(producer, lambda raw: tolls_ep.send_us_wa_wsdot_tolls_toll_rate(
                _feedurl=FEED_URL, _trip_name=raw.get("TripName", ""),
                data=WSDOTApi.parse_toll_rate(raw), flush_producer=False), tolls, "toll rate")
            total += c
            logging.info("Sent %d toll rates", c)
        except Exception as e:
            logging.error("Error fetching toll rates: %s", e)

        # --- CV Restrictions (reference-like, infrequent updates) ---
        try:
            if emit_reference or is_initial:
                restrictions = api.fetch_cv_restrictions()
                c = _emit_batch(producer, lambda raw: cvrestrictions_ep.send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction(
                    _feedurl=FEED_URL, _state_route_id=raw.get("StateRouteID", ""),
                    _bridge_number=raw.get("BridgeNumber", ""),
                    data=WSDOTApi.parse_cv_restriction(raw), flush_producer=False), restrictions, "cv restriction")
                total += c
                logging.info("Sent %d CV restrictions", c)
        except Exception as e:
            logging.error("Error fetching CV restrictions: %s", e)

        # --- Border Crossings ---
        try:
            crossings = api.fetch_border_crossings()
            c = _emit_batch(producer, lambda raw: border_ep.send_us_wa_wsdot_border_border_crossing(
                _feedurl=FEED_URL, _crossing_name=raw.get("CrossingName", ""),
                data=WSDOTApi.parse_border_crossing(raw), flush_producer=False), crossings, "border crossing")
            total += c
            logging.info("Sent %d border crossings", c)
        except Exception as e:
            logging.error("Error fetching border crossings: %s", e)

        # --- Ferry Vessel Locations ---
        try:
            vessels = api.fetch_vessel_locations()
            c = _emit_batch(producer, lambda raw: ferries_ep.send_us_wa_wsdot_ferries_vessel_location(
                _feedurl=FEED_URL, _vessel_id=str(raw.get("VesselID", "")),
                data=WSDOTApi.parse_vessel_location(raw), flush_producer=False), vessels, "vessel location")
            total += c
            logging.info("Sent %d vessel locations", c)
        except Exception as e:
            logging.error("Error fetching vessel locations: %s", e)

        # --- Road Weather (Scanweb RWIS): station reference + telemetry reading ---
        try:
            road_weather = api.fetch_road_weather()
        except Exception as e:
            logging.error("Error fetching road weather: %s", e)
            road_weather = None

        if road_weather is not None:
            if emit_reference:
                # Deduplicate station reference by the resolved station id so
                # the {station_id} key aligns with the reading events.
                seen_rw: Dict[str, Dict[str, Any]] = {}
                for raw in road_weather:
                    sid = WSDOTApi._road_weather_station_id(raw)
                    if sid and sid not in seen_rw:
                        seen_rw[sid] = raw
                c = _emit_batch(producer, lambda raw: roadweather_ep.send_us_wa_wsdot_roadweather_road_weather_station(
                    _feedurl=FEED_URL, _station_id=WSDOTApi._road_weather_station_id(raw),
                    data=WSDOTApi.parse_road_weather_station(raw), flush_producer=False),
                    list(seen_rw.values()), "road weather station")
                total += c
                logging.info("Sent %d road weather stations", c)

            c = _emit_batch(producer, lambda raw: roadweather_ep.send_us_wa_wsdot_roadweather_road_weather_reading(
                _feedurl=FEED_URL, _station_id=WSDOTApi._road_weather_station_id(raw),
                data=WSDOTApi.parse_road_weather_reading(raw), flush_producer=False), road_weather, "road weather reading")
            total += c
            logging.info("Sent %d road weather readings", c)

        # --- Highway Alerts (telemetry) ---
        try:
            alerts = api.fetch_highway_alerts()
            c = _emit_batch(producer, lambda raw: alerts_ep.send_us_wa_wsdot_alerts_highway_alert(
                _feedurl=FEED_URL, _alert_id=str(raw.get("AlertID", "")),
                data=WSDOTApi.parse_highway_alert(raw), flush_producer=False), alerts, "highway alert")
            total += c
            logging.info("Sent %d highway alerts", c)
        except Exception as e:
            logging.error("Error fetching highway alerts: %s", e)

        # --- Highway Cameras (reference / claim-check; refreshed periodically) ---
        try:
            if emit_reference or is_initial:
                cameras = api.fetch_highway_cameras()
                c = _emit_batch(producer, lambda raw: cameras_ep.send_us_wa_wsdot_cameras_highway_camera(
                    _feedurl=FEED_URL, _camera_id=str(raw.get("CameraID", "")),
                    data=WSDOTApi.parse_highway_camera(raw), flush_producer=False), cameras, "highway camera")
                total += c
                logging.info("Sent %d highway cameras", c)
        except Exception as e:
            logging.error("Error fetching highway cameras: %s", e)

        # --- Bridge Clearances (reference; refreshed periodically) ---
        try:
            if emit_reference or is_initial:
                clearances = api.fetch_bridge_clearances()
                c = _emit_batch(producer, lambda raw: bridgeclearances_ep.send_us_wa_wsdot_bridgeclearances_bridge_clearance(
                    _feedurl=FEED_URL, _crossing_location_id=str(raw.get("CrossingLocationId", "")),
                    data=WSDOTApi.parse_bridge_clearance(raw), flush_producer=False), clearances, "bridge clearance")
                total += c
                logging.info("Sent %d bridge clearances", c)
        except Exception as e:
            logging.error("Error fetching bridge clearances: %s", e)

        # --- Ferry Terminal Sailing Space (telemetry) ---
        try:
            terminals = api.fetch_terminal_sailing_space()
            c = _emit_batch(producer, lambda raw: ferryterminals_ep.send_us_wa_wsdot_ferryterminals_terminal_sailing_space(
                _feedurl=FEED_URL, _terminal_id=str(raw.get("TerminalID", "")),
                data=WSDOTApi.parse_terminal_sailing_space(raw), flush_producer=False), terminals, "terminal sailing space")
            total += c
            logging.info("Sent %d terminal sailing spaces", c)
        except Exception as e:
            logging.error("Error fetching terminal sailing space: %s", e)

        return total

    # Initial: emit reference data + first round of telemetry
    total = _poll_and_emit(is_initial=True, emit_reference=True)
    logging.info("Initial batch: %d total events", total)
    producer.flush()

    if once:
        logging.info("--once mode: exiting after first polling cycle")
        return

    # Polling loop
    last_reference_time = datetime.now(timezone.utc)
    reference_refresh_hours = 6

    while True:
        try:
            time.sleep(polling_interval)
            start_time = datetime.now(timezone.utc)
            emit_ref = (start_time - last_reference_time).total_seconds() >= reference_refresh_hours * 3600

            total = _poll_and_emit(emit_reference=emit_ref)

            if emit_ref:
                last_reference_time = start_time

            elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
            logging.info("Sent %d events in %.1f s. Next poll in %d s.", total, elapsed, polling_interval)
        except KeyboardInterrupt:
            logging.info("Exiting...")
            break
        except Exception as e:
            logging.error("Error occurred: %s", e)
            logging.info("Retrying in %d seconds...", polling_interval)
            time.sleep(polling_interval)


def main():
    parser = argparse.ArgumentParser(description="WSDOT Traveler Information bridge to Kafka")
    subparsers = parser.add_subparsers(dest="command")

    feed_parser = subparsers.add_parser("feed", help="Start the feed loop")
    feed_parser.add_argument("--connection-string", help="Kafka connection string")
    feed_parser.add_argument("--access-code", help="WSDOT API access code")
    feed_parser.add_argument("--polling-interval", type=int, default=120, help="Polling interval in seconds")
    feed_parser.add_argument("--region-filter", help="Comma-separated WSDOT regions for traffic flow")
    feed_parser.add_argument(
        "--once",
        action="store_true",
        default=os.environ.get("ONCE_MODE", "").lower() in ("1", "true", "yes"),
        help="Exit after one polling cycle (also via ONCE_MODE env var). "
             "Useful for scheduled execution in Fabric notebooks.",
    )

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
