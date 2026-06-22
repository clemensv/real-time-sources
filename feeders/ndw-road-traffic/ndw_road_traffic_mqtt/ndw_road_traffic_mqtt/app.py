"""MQTT companion feeder for ndw-road-traffic.

Polls NDW open-data XML feeds and publishes CloudEvents to an MQTT 5 broker
using the generated NLNDWAVGMqttMqttClient / NLNDWDRIPMqttMqttClient /
NLNDWMSIMqttMqttClient / NLNDWSituationsMqttMqttClient producers.

Transport-neutral acquisition lives in ndw_road_traffic_core.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from typing import Optional
from urllib.parse import urlparse
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import paho.mqtt.client as mqtt

from ndw_road_traffic_mqtt_producer_mqtt_client.client import (
    NLNDWAVGMqttMqttClient,
    NLNDWDRIPMqttMqttClient,
    NLNDWMSIMqttMqttClient,
    NLNDWSituationsMqttMqttClient,
)
from ndw_road_traffic_mqtt_producer_data import (
    PointMeasurementSite,
    RouteMeasurementSite,
    TrafficObservation,
    TravelTimeObservation,
    DripSign,
    DripDisplayState,
    MsiSign,
    MsiDisplayState,
    Roadwork,
    BridgeOpening,
    TemporaryClosure,
    TemporarySpeedLimit,
    SafetyRelatedMessage,
)
from ndw_road_traffic_core.ndw_road_traffic import (
    BASE_URL,
    SITUATION_FEEDS,
    DEFAULT_POLL_INTERVAL_SECONDS,
    DEFAULT_REFERENCE_REFRESH_SECONDS,
    DEFAULT_SITUATION_INTERVAL_SECONDS,
    DEFAULT_STATE_FILE,
    DEFAULT_MAX_RECORDS_PER_FAMILY,
    StateManager,
    NdwAcquirer,
)

logger = logging.getLogger(__name__)

DEFAULT_ENTRA_AUDIENCE = "https://eventgrid.azure.net/"


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() in {"1", "true", "yes", "on"}


def _topic_safe(value: object) -> str:
    """Sanitise a value for use as an MQTT topic segment."""
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for ch in ("/", "+", "#", "\x00"):
        text = text.replace(ch, "-")
    return "-".join(text.split()) or "unknown"


def _fetch_entra_token(audience: str, client_id: Optional[str] = None) -> str:
    params = {"api-version": "2018-02-01", "resource": audience}
    if client_id:
        params["client_id"] = client_id
    req = Request(
        "http://169.254.169.254/metadata/identity/oauth2/token?" + urlencode(params),
        headers={"Metadata": "true"},
    )
    with urlopen(req, timeout=30) as resp:
        payload = __import__("json").loads(resp.read().decode())
    token = payload.get("accessToken") or payload.get("access_token")
    if not token:
        raise RuntimeError("IMDS did not return an access token")
    return str(token)


def _build_mqtt_client(args: argparse.Namespace) -> tuple[mqtt.Client, str, int, Optional[str]]:
    """Return (paho_client, broker_host, broker_port, optional_entra_token)."""
    url = args.broker_url or f"mqtt://{args.host or 'localhost'}:{args.port or 1883}"
    if "://" not in url:
        url = f"mqtt://{url}"
    parsed = urlparse(url)
    host = parsed.hostname or "localhost"
    port = parsed.port or (8883 if parsed.scheme in ("mqtts", "ssl") else 1883)

    from paho.mqtt.client import CallbackAPIVersion, MQTTv5
    client = mqtt.Client(
        client_id=args.client_id or "",
        callback_api_version=CallbackAPIVersion.VERSION2,
        protocol=MQTTv5,
    )

    entra_token: Optional[str] = None
    auth_mode = (args.auth_mode or os.getenv("MQTT_AUTH_MODE", "password")).lower()
    if auth_mode == "entra":
        audience = args.entra_audience or DEFAULT_ENTRA_AUDIENCE
        entra_token = _fetch_entra_token(audience, args.entra_client_id)
    else:
        username = args.username or parsed.username or ""
        password = args.password or parsed.password or ""
        if username or password:
            client.username_pw_set(username, password)

    if parsed.scheme in ("mqtts", "ssl") or _env_bool("MQTT_TLS"):
        client.tls_set()

    return client, host, port, entra_token


async def _run_feed(args: argparse.Namespace) -> None:
    paho_client, host, port, entra_token = _build_mqtt_client(args)

    avg_client = NLNDWAVGMqttMqttClient(paho_client)
    drip_client = NLNDWDRIPMqttMqttClient(paho_client)
    msi_client = NLNDWMSIMqttMqttClient(paho_client)
    sit_client = NLNDWSituationsMqttMqttClient(paho_client)

    await avg_client.connect(host, port, token=entra_token)

    acquirer = NdwAcquirer(
        base_url=args.base_url,
        max_records_per_family=args.max_records_per_family,
    )
    state = StateManager(args.state_file)

    last_ref = 0.0
    last_sit = 0.0

    while True:
        now = time.monotonic()

        # Reference data
        if now - last_ref >= args.reference_refresh_interval:
            await _emit_reference(acquirer, avg_client, drip_client, msi_client)
            last_ref = time.monotonic()

        # Telemetry
        await _emit_speed(acquirer, state, avg_client)
        await _emit_traveltime(acquirer, state, avg_client)
        await _emit_drip_states(acquirer, state, drip_client)
        await _emit_msi_states(acquirer, state, msi_client)

        # Situations (lower frequency)
        if now - last_sit >= args.situation_interval:
            await _emit_situations(acquirer, state, sit_client)
            last_sit = time.monotonic()

        state.save()

        if args.once:
            break
        await asyncio.sleep(args.poll_interval)

    await avg_client.disconnect()


async def _emit_reference(
    acquirer: NdwAcquirer,
    avg_client: NLNDWAVGMqttMqttClient,
    drip_client: NLNDWDRIPMqttMqttClient,
    msi_client: NLNDWMSIMqttMqttClient,
) -> None:
    # Measurement sites
    try:
        point_sites, route_sites = acquirer.fetch_measurement_sites()
    except Exception:
        logger.exception("Failed to fetch measurement sites")
        point_sites, route_sites = [], []

    for rec in point_sites:
        road = _topic_safe(rec.get("road_name"))
        data = PointMeasurementSite(
            measurement_site_id=rec["measurement_site_id"],
            name=rec["name"],
            measurement_site_type=rec["measurement_site_type"],
            period=rec["period"],
            latitude=rec["latitude"],
            longitude=rec["longitude"],
            road_name=rec["road_name"],
            lane_count=rec["lane_count"],
            carriageway_type=rec["carriageway_type"],
        )
        try:
            await avg_client.publish_nl_ndw_avg_point_measurement_site_mqtt(
                measurement_site_id=rec["measurement_site_id"],
                road=road,
                data=data,
            )
        except Exception:
            logger.exception("MQTT publish failed for PointMeasurementSite %s", rec["measurement_site_id"])

    for rec in route_sites:
        road = _topic_safe(rec.get("road_name"))
        data = RouteMeasurementSite(
            measurement_site_id=rec["measurement_site_id"],
            name=rec["name"],
            measurement_site_type=rec["measurement_site_type"],
            period=rec["period"],
            start_latitude=rec["start_latitude"],
            start_longitude=rec["start_longitude"],
            end_latitude=rec["end_latitude"],
            end_longitude=rec["end_longitude"],
            road_name=rec["road_name"],
            length_metres=rec["length_metres"],
        )
        try:
            await avg_client.publish_nl_ndw_avg_route_measurement_site_mqtt(
                measurement_site_id=rec["measurement_site_id"],
                road=road,
                data=data,
            )
        except Exception:
            logger.exception("MQTT publish failed for RouteMeasurementSite %s", rec["measurement_site_id"])

    logger.info("Emitted %d point + %d route measurement site events via MQTT",
                len(point_sites), len(route_sites))

    # DRIP signs
    try:
        drip_signs, _ = acquirer.fetch_drip()
    except Exception:
        logger.exception("Failed to fetch DRIP signs")
        drip_signs = []

    for rec in drip_signs:
        road = _topic_safe(rec.get("road_name"))
        data = DripSign(
            vms_controller_id=rec["vms_controller_id"],
            vms_index=rec["vms_index"],
            vms_type=rec["vms_type"],
            latitude=rec["latitude"],
            longitude=rec["longitude"],
            road_name=rec["road_name"],
            description=rec["description"],
        )
        try:
            await drip_client.publish_nl_ndw_drip_drip_sign_mqtt(
                vms_controller_id=rec["vms_controller_id"],
                vms_index=rec["vms_index"],
                road=road,
                data=data,
            )
        except Exception:
            logger.exception("MQTT publish failed for DripSign %s", rec["vms_controller_id"])

    logger.info("Emitted %d DripSign reference events via MQTT", len(drip_signs))

    # MSI signs
    try:
        msi_signs, _ = acquirer.fetch_msi()
    except Exception:
        logger.exception("Failed to fetch MSI signs")
        msi_signs = []

    for rec in msi_signs:
        road = _topic_safe(rec.get("road_name"))
        data = MsiSign(
            sign_id=rec["sign_id"],
            sign_type=rec["sign_type"],
            latitude=rec["latitude"],
            longitude=rec["longitude"],
            road_name=rec["road_name"],
            lane=rec["lane"],
            description=rec["description"],
        )
        try:
            await msi_client.publish_nl_ndw_msi_msi_sign_mqtt(
                sign_id=rec["sign_id"],
                road=road,
                data=data,
            )
        except Exception:
            logger.exception("MQTT publish failed for MsiSign %s", rec["sign_id"])

    logger.info("Emitted %d MsiSign reference events via MQTT", len(msi_signs))


async def _emit_speed(
    acquirer: NdwAcquirer,
    state: StateManager,
    avg_client: NLNDWAVGMqttMqttClient,
) -> None:
    try:
        records = acquirer.fetch_speed_observations()
    except Exception:
        logger.exception("Failed to fetch speed observations")
        return

    count = 0
    for rec in records:
        sid = rec["measurement_site_id"]
        mtime = rec["measurement_time"]
        if state.state.get("speed", {}).get(sid) == mtime:
            continue
        data = TrafficObservation(
            measurement_site_id=sid,
            measurement_time=mtime,
            average_speed=rec["average_speed"],
            vehicle_flow_rate=rec["vehicle_flow_rate"],
            number_of_lanes_with_data=rec["number_of_lanes_with_data"],
        )
        try:
            await avg_client.publish_nl_ndw_avg_traffic_observation_mqtt(
                measurement_site_id=sid,
                road="unknown",
                data=data,
            )
            state.state.setdefault("speed", {})[sid] = mtime
            count += 1
        except Exception:
            logger.exception("MQTT publish failed for TrafficObservation %s", sid)

    logger.info("Emitted %d TrafficObservation events via MQTT", count)


async def _emit_traveltime(
    acquirer: NdwAcquirer,
    state: StateManager,
    avg_client: NLNDWAVGMqttMqttClient,
) -> None:
    try:
        records = acquirer.fetch_traveltime_observations()
    except Exception:
        logger.exception("Failed to fetch travel time observations")
        return

    count = 0
    for rec in records:
        sid = rec["measurement_site_id"]
        mtime = rec["measurement_time"]
        if state.state.get("traveltime", {}).get(sid) == mtime:
            continue
        data = TravelTimeObservation(
            measurement_site_id=sid,
            measurement_time=mtime,
            duration=rec["duration"],
            reference_duration=rec["reference_duration"],
            accuracy=rec["accuracy"],
            data_quality=rec["data_quality"],
            number_of_input_values=rec["number_of_input_values"],
        )
        try:
            await avg_client.publish_nl_ndw_avg_travel_time_observation_mqtt(
                measurement_site_id=sid,
                road="unknown",
                data=data,
            )
            state.state.setdefault("traveltime", {})[sid] = mtime
            count += 1
        except Exception:
            logger.exception("MQTT publish failed for TravelTimeObservation %s", sid)

    logger.info("Emitted %d TravelTimeObservation events via MQTT", count)


async def _emit_drip_states(
    acquirer: NdwAcquirer,
    state: StateManager,
    drip_client: NLNDWDRIPMqttMqttClient,
) -> None:
    try:
        _, states = acquirer.fetch_drip()
    except Exception:
        logger.exception("Failed to fetch DRIP display states")
        return

    count = 0
    for rec in states:
        key = f"{rec['vms_controller_id']}/{rec['vms_index']}"
        pub_time = rec["publication_time"]
        if state.state.get("drip", {}).get(key) == pub_time:
            continue
        data = DripDisplayState(
            vms_controller_id=rec["vms_controller_id"],
            vms_index=rec["vms_index"],
            publication_time=pub_time,
            active=rec["active"],
            vms_text=rec["vms_text"],
            pictogram_code=rec["pictogram_code"],
            state=rec["state"],
        )
        try:
            await drip_client.publish_nl_ndw_drip_drip_display_state_mqtt(
                vms_controller_id=rec["vms_controller_id"],
                vms_index=rec["vms_index"],
                road="unknown",
                data=data,
            )
            state.state.setdefault("drip", {})[key] = pub_time
            count += 1
        except Exception:
            logger.exception("MQTT publish failed for DripDisplayState %s", key)

    logger.info("Emitted %d DripDisplayState events via MQTT", count)


async def _emit_msi_states(
    acquirer: NdwAcquirer,
    state: StateManager,
    msi_client: NLNDWMSIMqttMqttClient,
) -> None:
    try:
        _, states = acquirer.fetch_msi()
    except Exception:
        logger.exception("Failed to fetch MSI display states")
        return

    count = 0
    for rec in states:
        sid = rec["sign_id"]
        pub_time = rec["publication_time"]
        if state.state.get("msi", {}).get(sid) == pub_time:
            continue
        data = MsiDisplayState(
            sign_id=sid,
            publication_time=pub_time,
            image_code=rec["image_code"],
            state=rec["state"],
            speed_limit=rec["speed_limit"],
        )
        try:
            await msi_client.publish_nl_ndw_msi_msi_display_state_mqtt(
                sign_id=sid,
                road="unknown",
                data=data,
            )
            state.state.setdefault("msi", {})[sid] = pub_time
            count += 1
        except Exception:
            logger.exception("MQTT publish failed for MsiDisplayState %s", sid)

    logger.info("Emitted %d MsiDisplayState events via MQTT", count)


async def _emit_situations(
    acquirer: NdwAcquirer,
    state: StateManager,
    sit_client: NLNDWSituationsMqttMqttClient,
) -> None:
    for feed_file, feed_type in SITUATION_FEEDS:
        try:
            records = acquirer.fetch_situations(feed_file, feed_type)
        except Exception:
            logger.exception("Failed to fetch situation feed %s", feed_file)
            continue

        count = 0
        for rec in records:
            rid = rec["situation_record_id"]
            vtime = rec["version_time"]
            if state.state.get("situation", {}).get(rid) == vtime:
                continue
            road = _topic_safe(rec.get("road_name"))
            try:
                if feed_type == "roadwork":
                    data = Roadwork(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        road_name=rec.get("road_name"), description=rec.get("description"),
                        location_description=rec.get("location_description"),
                        probability=rec.get("probability"), severity=rec.get("severity"),
                        management_type=rec.get("management_type"),
                    )
                    await sit_client.publish_nl_ndw_situations_roadwork_mqtt(
                        situation_record_id=rid, road=road, data=data)
                elif feed_type == "bridge_opening":
                    data = BridgeOpening(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        bridge_name=rec.get("bridge_name"), road_name=rec.get("road_name"),
                        description=rec.get("description"),
                    )
                    await sit_client.publish_nl_ndw_situations_bridge_opening_mqtt(
                        situation_record_id=rid, road=road, data=data)
                elif feed_type == "temporary_closure":
                    data = TemporaryClosure(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        road_name=rec.get("road_name"), description=rec.get("description"),
                        location_description=rec.get("location_description"),
                        severity=rec.get("severity"),
                    )
                    await sit_client.publish_nl_ndw_situations_temporary_closure_mqtt(
                        situation_record_id=rid, road=road, data=data)
                elif feed_type == "temporary_speed_limit":
                    data = TemporarySpeedLimit(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        road_name=rec.get("road_name"),
                        speed_limit_kmh=rec.get("speed_limit_kmh"),
                        description=rec.get("description"),
                        location_description=rec.get("location_description"),
                    )
                    await sit_client.publish_nl_ndw_situations_temporary_speed_limit_mqtt(
                        situation_record_id=rid, road=road, data=data)
                elif feed_type == "safety_related_message":
                    data = SafetyRelatedMessage(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        road_name=rec.get("road_name"),
                        message_type=rec.get("message_type"),
                        description=rec.get("description"),
                        urgency=rec.get("urgency"),
                    )
                    await sit_client.publish_nl_ndw_situations_safety_related_message_mqtt(
                        situation_record_id=rid, road=road, data=data)
                else:
                    continue
                state.state.setdefault("situation", {})[rid] = vtime
                count += 1
            except Exception:
                logger.exception("MQTT publish failed for %s situation %s", feed_type, rid)

        logger.info("Emitted %d %s situation events via MQTT", count, feed_type)


def _add_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("MQTT_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("MQTT_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "0")) or None)
    parser.add_argument("--client-id", default=os.getenv("MQTT_CLIENT_ID", ""))
    parser.add_argument("--username", default=os.getenv("MQTT_USERNAME"))
    parser.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("MQTT_TLS"))
    parser.add_argument("--auth-mode", choices=("password", "entra"), default=os.getenv("MQTT_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("MQTT_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE))
    parser.add_argument("--entra-client-id", default=os.getenv("MQTT_ENTRA_CLIENT_ID"))
    parser.add_argument("--base-url", default=os.getenv("NDW_BASE_URL", BASE_URL))
    parser.add_argument("--poll-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)))
    parser.add_argument("--reference-refresh-interval", type=int,
                        default=int(os.getenv("REFERENCE_REFRESH_INTERVAL", DEFAULT_REFERENCE_REFRESH_SECONDS)))
    parser.add_argument("--situation-interval", type=int,
                        default=int(os.getenv("SITUATION_INTERVAL", DEFAULT_SITUATION_INTERVAL_SECONDS)))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    parser.add_argument("--max-records-per-family", type=int,
                        default=int(os.getenv("MAX_RECORDS_PER_FAMILY", "0")) or None)
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE"))
    return parser


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = _add_args(argparse.ArgumentParser(description="NDW Road Traffic MQTT feeder"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_run_feed(args))


if __name__ == "__main__":
    main()
