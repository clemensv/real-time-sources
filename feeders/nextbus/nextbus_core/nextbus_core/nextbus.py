"""Transport-agnostic HTTP acquisition and state handling for NextBus."""

from __future__ import annotations

import json
import os
import time
import xml.etree.ElementTree as ET
from typing import Iterator, Optional

import requests

NEXTBUS_BASE_URL = "https://retro.umoiq.com/service/publicXMLFeed"
USER_AGENT = os.environ.get("USER_AGENT") or (
    "real-time-sources-nextbus/0.1.0 "
    "(+https://github.com/clemensv/real-time-sources; "
    + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")"
)

# Module-level state for change-detection (shared across transport layers)
route_checksums: dict = {}
schedule_checksums: dict = {}
messages_checksums: dict = {}
vehicle_last_report_times: dict = {}


def element_to_dict(element) -> dict:
    """Recursively convert an XML element to a dictionary."""
    data = {}
    for child in element:
        if len(child) > 0 or child.attrib:
            if child.tag in data:
                if not isinstance(data[child.tag], list):
                    data[child.tag] = [data[child.tag]]
                data[child.tag].append(element_to_dict(child))
            else:
                data[child.tag] = element_to_dict(child)
        else:
            data[child.tag] = child.text
    data.update(element.attrib)
    return data


def get_route_config_updates(agency_tag: str, backoff_time: float = 0.0) -> Iterator[dict]:
    """Yield changed route configs as plain dicts (no CloudEvents, no transport)."""
    response = requests.get(
        NEXTBUS_BASE_URL,
        params={"command": "routeList", "a": agency_tag},
        headers={"User-Agent": USER_AGENT},
    )
    if response.status_code == 404:
        return
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        route_tag = route.get("tag")
        if backoff_time > 0:
            time.sleep(backoff_time)
        rc_resp = requests.get(
            NEXTBUS_BASE_URL,
            params={"command": "routeConfig", "a": agency_tag, "r": route_tag},
            headers={"User-Agent": USER_AGENT},
        )
        if rc_resp.status_code == 404:
            # API is flaky, try once more
            rc_resp = requests.get(
                NEXTBUS_BASE_URL,
                params={"command": "routeConfig", "a": agency_tag, "r": route_tag},
                headers={"User-Agent": USER_AGENT},
            )
            if rc_resp.status_code == 404:
                print(f"404 for {agency_tag}/{route_tag}")
                continue
        rc_resp.raise_for_status()
        content = rc_resp.content
        checksum = hash(content)
        if route_tag in route_checksums and route_checksums[route_tag] == checksum:
            continue
        route_checksums[route_tag] = checksum
        config_root = ET.fromstring(content)
        yield {
            "agency": agency_tag,
            "routeTag": route_tag,
            "routeConfig": json.dumps(element_to_dict(config_root)),
        }


def get_schedule_updates(agency_tag: str, backoff_time: float = 0.0) -> Iterator[dict]:
    """Yield changed schedules as plain dicts (no CloudEvents, no transport)."""
    response = requests.get(
        NEXTBUS_BASE_URL,
        params={"command": "routeList", "a": agency_tag},
        headers={"User-Agent": USER_AGENT},
    )
    if response.status_code == 404:
        return
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        route_tag = route.get("tag")
        if backoff_time > 0:
            time.sleep(backoff_time)
        sched_resp = requests.get(
            NEXTBUS_BASE_URL,
            params={"command": "schedule", "a": agency_tag, "r": route_tag},
            headers={"User-Agent": USER_AGENT},
        )
        if sched_resp.status_code == 404:
            print(f"404 for {agency_tag}/{route_tag}")
            continue
        sched_resp.raise_for_status()
        content = sched_resp.content
        checksum = hash(content)
        if route_tag in schedule_checksums and schedule_checksums[route_tag] == checksum:
            continue
        schedule_checksums[route_tag] = checksum
        sched_root = ET.fromstring(content)
        yield {
            "agency": agency_tag,
            "routeTag": route_tag,
            "schedule": json.dumps(element_to_dict(sched_root)),
        }


def get_message_updates(agency_tag: str, backoff_time: float = 0.0) -> Iterator[dict]:
    """Yield changed messages as plain dicts (no CloudEvents, no transport)."""
    response = requests.get(
        NEXTBUS_BASE_URL,
        params={"command": "routeList", "a": agency_tag},
        headers={"User-Agent": USER_AGENT},
    )
    if response.status_code == 404:
        return
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        route_tag = route.get("tag")
        if backoff_time > 0:
            time.sleep(backoff_time)
        msg_resp = requests.get(
            NEXTBUS_BASE_URL,
            params={"command": "messages", "a": agency_tag, "r": route_tag},
            headers={"User-Agent": USER_AGENT},
        )
        if msg_resp.status_code == 404:
            print(f"404 for {agency_tag}/{route_tag}")
            continue
        msg_resp.raise_for_status()
        content = msg_resp.content
        checksum = hash(content)
        if route_tag in messages_checksums and messages_checksums[route_tag] == checksum:
            continue
        messages_checksums[route_tag] = checksum
        msg_root = ET.fromstring(content)
        yield {
            "agency": agency_tag,
            "routeTag": route_tag,
            "messages": json.dumps(element_to_dict(msg_root)),
        }


def get_vehicle_positions(
    agency_tag: str,
    route: Optional[str] = None,
    last_time: Optional[float] = None,
) -> tuple[list[dict], Optional[float]]:
    """Fetch vehicle positions, deduplicating against seen report times.

    Returns (positions, feed_last_time).  On upstream error/404, returns
    ([], last_time) so the caller can preserve its watermark and retry.
    """
    params: dict = {"command": "vehicleLocations", "a": agency_tag}
    if route and route != "*":
        params["r"] = route
    if last_time is not None:
        params["t"] = int(last_time)

    response = requests.get(NEXTBUS_BASE_URL, params=params, headers={"User-Agent": USER_AGENT})
    if response.status_code == 404:
        return [], last_time
    response.raise_for_status()
    root = ET.fromstring(response.content)

    last_time_el = root.find("lastTime")
    if last_time_el is None:
        err_el = root.find("Error")
        detail = (err_el.text or "").strip() if err_el is not None else response.text[:200].strip()
        print(f"NextBus vehicleLocations returned no data for agency '{agency_tag}': {detail}")
        return [], last_time

    feed_last_time = float(last_time_el.get("time") or "0")
    positions = []
    for vehicle in root.findall("vehicle"):
        vehicle_key = f"{agency_tag}/{vehicle.get('id')}"
        last_report_time = feed_last_time / 1000 - float(vehicle.get("secsSinceReport") or "0")
        if vehicle_key in vehicle_last_report_times and last_report_time <= vehicle_last_report_times[vehicle_key]:
            continue
        vehicle_last_report_times[vehicle_key] = last_report_time
        positions.append({
            "agency": agency_tag,
            "routeTag": vehicle.get("routeTag"),
            "dirTag": vehicle.get("dirTag"),
            "id": vehicle.get("id"),
            "lat": vehicle.get("lat"),
            "lon": vehicle.get("lon"),
            "predictable": vehicle.get("predictable"),
            "heading": vehicle.get("heading"),
            "speedKmHr": vehicle.get("speedKmHr"),
            "timestamp": last_report_time,
        })
    return positions, feed_last_time


# ---------------------------------------------------------------------------
# CLI print utilities (no transport dependencies)
# ---------------------------------------------------------------------------

def print_agencies() -> None:
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "agencyList"}, headers={"User-Agent": USER_AGENT})
    if response.status_code == 404:
        return
    root = ET.fromstring(response.content)
    for agency in root.findall("agency"):
        print(f"{agency.get('tag')}: {agency.get('title')}")


def print_routes(agency_tag: str) -> None:
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeList", "a": agency_tag}, headers={"User-Agent": USER_AGENT})
    if response.status_code == 404:
        return
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for route in root.findall("route"):
        print(f"{route.get('tag')}: {route.get('title')}")


def print_route_predictions(agency_tag: str, route_tag: str) -> None:
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "predictions", "a": agency_tag, "r": route_tag}, headers={"User-Agent": USER_AGENT})
    if response.status_code == 404:
        return
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for direction in root.findall("predictions/direction"):
        print(f"Direction: {direction.get('title')}")
        for prediction in direction.findall("prediction"):
            print(f"  {prediction.get('minutes')} minutes")


def print_stops(agency_tag: str, route_tag: str) -> None:
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "routeConfig", "a": agency_tag, "r": route_tag}, headers={"User-Agent": USER_AGENT})
    if response.status_code == 404:
        return
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for stop in root.findall("route/stop"):
        print(
            f"{stop.get('tag')}: {stop.get('title')}, "
            f"({stop.get('lat')},{stop.get('lon')}), "
            f"https://geohack.toolforge.org/geohack.php?language=en&params={stop.get('lat')};{stop.get('lon')}"
        )


def print_vehicle_locations(agency: str, route: str) -> None:
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "vehicleLocations", "a": agency, "r": route}, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    root = ET.fromstring(response.content)
    for vehicle in root.findall("vehicle"):
        print(
            f"{vehicle.get('id')}: ({vehicle.get('lat')},{vehicle.get('lon')}), "
            f"heading {vehicle.get('heading')}°, {vehicle.get('speedKmHr')} km/h, "
            f"https://geohack.toolforge.org/geohack.php?language=en&params={vehicle.get('lat')};{vehicle.get('lon')}"
        )


def print_predictions(agency_tag: str, stop_id: str, route_tag: str) -> None:
    response = requests.get(NEXTBUS_BASE_URL, params={"command": "predictions", "a": agency_tag, "s": stop_id, "r": route_tag}, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    root = ET.fromstring(response.content)
    print(f"Predictions for stop {root.find('predictions').get('stopTitle')}")
    for prediction in root.findall("predictions/direction/prediction"):
        print(f"{prediction.get('minutes')} minutes ({prediction.get('seconds')} seconds), Vehicle {prediction.get('vehicle')}")
