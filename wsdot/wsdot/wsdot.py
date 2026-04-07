"""WSDOT Traveler Information and Ferries bridge to Kafka."""

import os
import re
import sys
import time
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
from wsdot_producer_kafka_producer.producer import UsWaWsdotTrafficEventProducer

if sys.gettrace() is not None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

TRAVELER_BASE = "https://www.wsdot.wa.gov/Traffic/api"
FERRIES_BASE = "https://www.wsdot.wa.gov/ferries/api/vessels/rest"
FEED_URL = "https://www.wsdot.wa.gov/Traffic/api"

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
            "User-Agent": "real-time-sources/1.0 (github.com/clemensv/real-time-sources)",
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
        return self._traveler_get("WeatherInformation", "WeatherInformation")

    def fetch_weather_stations(self) -> List[Dict[str, Any]]:
        return self._traveler_get("WeatherStations", "WeatherStations")

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
            flow_reading=flow_reading,
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
        return WeatherStation(
            station_id=str(raw.get("StationCode", "")),
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

    producer = Producer(kafka_config)
    ep = UsWaWsdotTrafficEventProducer(producer, kafka_topic)
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
                c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_traffic_traffic_flow_station(
                    _feedurl=FEED_URL, _flow_data_id=str(raw.get("FlowDataID", "")),
                    data=WSDOTApi.parse_station(raw), flush_producer=False), all_flows, "traffic station")
                total += c
                logging.info("Sent %d traffic flow stations", c)

            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_traffic_traffic_flow_reading(
                _feedurl=FEED_URL, _flow_data_id=str(raw.get("FlowDataID", "")),
                data=WSDOTApi.parse_reading(raw), flush_producer=False), all_flows, "traffic reading")
            total += c
            logging.info("Sent %d traffic flow readings", c)
        except Exception as e:
            logging.error("Error fetching traffic flows: %s", e)

        # --- Travel Times ---
        try:
            travel_times = api.fetch_travel_times()
            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_traveltimes_travel_time_route(
                _feedurl=FEED_URL, _travel_time_id=str(raw.get("TravelTimeID", "")),
                data=WSDOTApi.parse_travel_time(raw), flush_producer=False), travel_times, "travel time")
            total += c
            logging.info("Sent %d travel times", c)
        except Exception as e:
            logging.error("Error fetching travel times: %s", e)

        # --- Mountain Pass Conditions ---
        try:
            passes = api.fetch_mountain_pass_conditions()
            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_mountainpass_mountain_pass_condition(
                _feedurl=FEED_URL, _mountain_pass_id=str(raw.get("MountainPassId", "")),
                data=WSDOTApi.parse_mountain_pass(raw), flush_producer=False), passes, "mountain pass")
            total += c
            logging.info("Sent %d mountain pass conditions", c)
        except Exception as e:
            logging.error("Error fetching mountain passes: %s", e)

        # --- Weather ---
        try:
            if emit_reference:
                stations = api.fetch_weather_stations()
                c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_weather_weather_station(
                    _feedurl=FEED_URL, _station_id=str(raw.get("StationCode", "")),
                    data=WSDOTApi.parse_weather_station(raw), flush_producer=False), stations, "weather station")
                total += c
                logging.info("Sent %d weather stations", c)

            weather = api.fetch_weather_information()
            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_weather_weather_reading(
                _feedurl=FEED_URL, _station_id=str(raw.get("StationID", "")),
                data=WSDOTApi.parse_weather_reading(raw), flush_producer=False), weather, "weather reading")
            total += c
            logging.info("Sent %d weather readings", c)
        except Exception as e:
            logging.error("Error fetching weather: %s", e)

        # --- Toll Rates ---
        try:
            tolls = api.fetch_toll_rates()
            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_tolls_toll_rate(
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
                c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_cvrestrictions_commercial_vehicle_restriction(
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
            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_border_border_crossing(
                _feedurl=FEED_URL, _crossing_name=raw.get("CrossingName", ""),
                data=WSDOTApi.parse_border_crossing(raw), flush_producer=False), crossings, "border crossing")
            total += c
            logging.info("Sent %d border crossings", c)
        except Exception as e:
            logging.error("Error fetching border crossings: %s", e)

        # --- Ferry Vessel Locations ---
        try:
            vessels = api.fetch_vessel_locations()
            c = _emit_batch(producer, lambda raw: ep.send_us_wa_wsdot_ferries_vessel_location(
                _feedurl=FEED_URL, _vessel_id=str(raw.get("VesselID", "")),
                data=WSDOTApi.parse_vessel_location(raw), flush_producer=False), vessels, "vessel location")
            total += c
            logging.info("Sent %d vessel locations", c)
        except Exception as e:
            logging.error("Error fetching vessel locations: %s", e)

        return total

    # Initial: emit reference data + first round of telemetry
    total = _poll_and_emit(is_initial=True, emit_reference=True)
    logging.info("Initial batch: %d total events", total)

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

    args = parser.parse_args()
    if args.command == "feed":
        feed(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
