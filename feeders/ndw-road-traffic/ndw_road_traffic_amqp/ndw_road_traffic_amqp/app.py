"""AMQP 1.0 companion feeder for ndw-road-traffic.

Polls NDW open-data XML feeds and sends CloudEvents via AMQP 1.0 using the
family-specific generated AMQP producer classes.

KNOWN BLOCKER — xrcg send_amqp name collision (xregistry/codegen#482):
  Each generated AMQP producer class (NLNDWAVGAmqpProducer, etc.) contains
  multiple methods all named `send_amqp`, one per message type.  Python only
  retains the *last* definition, making the earlier ones unreachable.
  Workaround: build and dispatch AMQP messages directly via the producer's
  lower-level `_send_via_reactor` / `_send_via_blocking_sender` methods plus
  `_serialize_payload` and `_ce_headers_to_amqp_properties`, bypassing the
  colliding `send_amqp` name entirely.  The workaround is localised to the
  `_send_direct` helper below and can be removed once the codegen emits
  distinct method names per message type.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

from proton import Message, symbol

from ndw_road_traffic_amqp_producer_amqp_producer.producer import (
    NLNDWAVGAmqpProducer,
    NLNDWDRIPAmqpProducer,
    NLNDWMSIAmqpProducer,
    NLNDWSituationsAmqpProducer,
)
from ndw_road_traffic_amqp_producer_data import (
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

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "ndw-road-traffic"


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() in {"1", "true", "yes", "on"}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# WORKAROUND(xregistry/codegen#482): send_amqp name collision
#
# xrcg generates multiple methods all named `send_amqp` inside a single
# producer class (one per message type). Python retains only the last.
# We bypass the collision by building the AMQP Message directly and calling
# the producer's internal low-level send path.  This is intentionally
# minimal: we only replicate the attribute-assembly logic that every
# send_amqp body shares.
# ---------------------------------------------------------------------------

def _send_direct(
    producer: Any,
    ce_type: str,
    source: str,
    subject: str,
    data: Any,
    content_type: str = "application/json",
) -> None:
    """Send a single CloudEvent via AMQP bypassing the send_amqp name collision."""
    from cloudevents.http import CloudEvent
    from cloudevents.conversion import to_binary, to_structured

    attributes = {
        "type": ce_type,
        "source": source,
        "subject": subject,
        "time": _now_utc(),
    }

    byte_data = producer._serialize_payload(data, content_type)
    cloud_event = CloudEvent(attributes, byte_data)

    if getattr(producer, "content_mode", "structured") == "structured":
        headers, body = to_structured(cloud_event)
        msg_body = body if isinstance(body, bytes) else str(body).encode("utf-8")
        amqp_msg = Message(body=msg_body, inferred=True)
        amqp_msg.content_type = getattr(producer, "format_type", "application/json")
    else:
        headers, body = to_binary(cloud_event)
        if isinstance(body, str):
            body = body.encode("utf-8")
        amqp_msg = Message(body=body, inferred=True)
        amqp_msg.content_type = content_type
        if headers:
            amqp_msg.properties = producer._ce_headers_to_amqp_properties(headers)

    amqp_msg.subject = subject
    amqp_msg.annotations = {symbol("x-opt-partition-key"): subject[:128]}

    if getattr(producer, "_handler", None) is not None:
        producer._send_via_reactor(amqp_msg)
    else:
        producer._send_via_blocking_sender(amqp_msg)


# ---------------------------------------------------------------------------
# AMQP producer factory helpers
# ---------------------------------------------------------------------------

def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return (
        parsed.hostname or "localhost",
        parsed.port or (5671 if tls else 5672),
        tls,
        parsed.username,
        parsed.password,
        (parsed.path or "").lstrip("/") or None,
    )


def _build_producer(cls, args: argparse.Namespace):
    address = args.address
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        address = path or address
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password

    kwargs: dict[str, Any] = dict(
        host=host,
        address=address,
        port=port,
        content_mode=args.content_mode,
        use_tls=tls,
    )
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs["credential"] = (
            ManagedIdentityCredential(client_id=args.entra_client_id)
            if args.entra_client_id
            else DefaultAzureCredential()
        )
        kwargs["entra_audience"] = args.entra_audience
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs["sas_key_name"] = args.sas_key_name
        kwargs["sas_key"] = args.sas_key
    else:
        kwargs["username"] = username
        kwargs["password"] = password

    return cls(**kwargs)


def _retry_build(cls, args, max_attempts=5, initial_delay=10):
    for attempt in range(max_attempts):
        try:
            return _build_producer(cls, args)
        except Exception as exc:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning("Producer init attempt %d/%d failed: %s; retrying in %ds",
                           attempt + 1, max_attempts, exc, delay)
            time.sleep(delay)


# ---------------------------------------------------------------------------
# Emission helpers
# ---------------------------------------------------------------------------

_AVG_BASE = "https://opendata.ndw.nu"
_DRIP_SRC = f"{_AVG_BASE}/dynamische_route_informatie_paneel.xml.gz"
_MSI_SRC = f"{_AVG_BASE}/Matrixsignaalinformatie.xml.gz"

_SITUATION_SOURCES = {
    "roadwork": f"{_AVG_BASE}/planningsfeed_wegwerkzaamheden_en_evenementen.xml.gz",
    "bridge_opening": f"{_AVG_BASE}/planningsfeed_brugopeningen.xml.gz",
    "temporary_closure": f"{_AVG_BASE}/tijdelijke_verkeersmaatregelen_afsluitingen.xml.gz",
    "temporary_speed_limit": f"{_AVG_BASE}/tijdelijke_verkeersmaatregelen_maximum_snelheden.xml.gz",
    "safety_related_message": f"{_AVG_BASE}/veiligheidsgerelateerde_berichten_srti.xml.gz",
}

_SITUATION_TYPES = {
    "roadwork": "NL.NDW.Situations.Roadwork",
    "bridge_opening": "NL.NDW.Situations.BridgeOpening",
    "temporary_closure": "NL.NDW.Situations.TemporaryClosure",
    "temporary_speed_limit": "NL.NDW.Situations.TemporarySpeedLimit",
    "safety_related_message": "NL.NDW.Situations.SafetyRelatedMessage",
}


def _emit_measurement_sites(avg_prod, acquirer):
    try:
        point_sites, route_sites = acquirer.fetch_measurement_sites()
    except Exception:
        logger.exception("Failed to fetch measurement sites")
        return

    src = f"{_AVG_BASE}/measurement_current.xml.gz"
    for rec in point_sites:
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
        subject = f"measurement-sites/{rec['measurement_site_id']}"
        try:
            _send_direct(avg_prod, "NL.NDW.AVG.PointMeasurementSite", src, subject, data)
        except Exception:
            logger.exception("AMQP send failed for PointMeasurementSite %s", rec["measurement_site_id"])

    for rec in route_sites:
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
        subject = f"measurement-sites/{rec['measurement_site_id']}"
        try:
            _send_direct(avg_prod, "NL.NDW.AVG.RouteMeasurementSite", src, subject, data)
        except Exception:
            logger.exception("AMQP send failed for RouteMeasurementSite %s", rec["measurement_site_id"])

    logger.info("Emitted %d point + %d route measurement site events via AMQP",
                len(point_sites), len(route_sites))


def _emit_drip_signs(drip_prod, acquirer):
    try:
        signs, _ = acquirer.fetch_drip()
    except Exception:
        logger.exception("Failed to fetch DRIP signs")
        return

    for rec in signs:
        data = DripSign(
            vms_controller_id=rec["vms_controller_id"],
            vms_index=rec["vms_index"],
            vms_type=rec["vms_type"],
            latitude=rec["latitude"],
            longitude=rec["longitude"],
            road_name=rec["road_name"],
            description=rec["description"],
        )
        subject = f"drips/{rec['vms_controller_id']}/{rec['vms_index']}"
        try:
            _send_direct(drip_prod, "NL.NDW.DRIP.DripSign", _DRIP_SRC, subject, data)
        except Exception:
            logger.exception("AMQP send failed for DripSign %s", rec["vms_controller_id"])

    logger.info("Emitted %d DripSign reference events via AMQP", len(signs))


def _emit_msi_signs(msi_prod, acquirer):
    try:
        signs, _ = acquirer.fetch_msi()
    except Exception:
        logger.exception("Failed to fetch MSI signs")
        return

    for rec in signs:
        data = MsiSign(
            sign_id=rec["sign_id"],
            sign_type=rec["sign_type"],
            latitude=rec["latitude"],
            longitude=rec["longitude"],
            road_name=rec["road_name"],
            lane=rec["lane"],
            description=rec["description"],
        )
        subject = f"msi-signs/{rec['sign_id']}"
        try:
            _send_direct(msi_prod, "NL.NDW.MSI.MsiSign", _MSI_SRC, subject, data)
        except Exception:
            logger.exception("AMQP send failed for MsiSign %s", rec["sign_id"])

    logger.info("Emitted %d MsiSign reference events via AMQP", len(signs))


def _emit_speed(avg_prod, state, acquirer):
    try:
        records = acquirer.fetch_speed_observations()
    except Exception:
        logger.exception("Failed to fetch speed observations")
        return 0

    src = f"{_AVG_BASE}/trafficspeed.xml.gz"
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
        subject = f"measurement-sites/{sid}"
        try:
            _send_direct(avg_prod, "NL.NDW.AVG.TrafficObservation", src, subject, data)
            state.state.setdefault("speed", {})[sid] = mtime
            count += 1
        except Exception:
            logger.exception("AMQP send failed for TrafficObservation %s", sid)

    logger.info("Emitted %d TrafficObservation events via AMQP", count)
    return count


def _emit_traveltime(avg_prod, state, acquirer):
    try:
        records = acquirer.fetch_traveltime_observations()
    except Exception:
        logger.exception("Failed to fetch travel time observations")
        return 0

    src = f"{_AVG_BASE}/traveltime.xml.gz"
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
        subject = f"measurement-sites/{sid}"
        try:
            _send_direct(avg_prod, "NL.NDW.AVG.TravelTimeObservation", src, subject, data)
            state.state.setdefault("traveltime", {})[sid] = mtime
            count += 1
        except Exception:
            logger.exception("AMQP send failed for TravelTimeObservation %s", sid)

    logger.info("Emitted %d TravelTimeObservation events via AMQP", count)
    return count


def _emit_drip_states(drip_prod, state, acquirer):
    try:
        _, states = acquirer.fetch_drip()
    except Exception:
        logger.exception("Failed to fetch DRIP display states")
        return 0

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
        subject = f"drips/{rec['vms_controller_id']}/{rec['vms_index']}"
        try:
            _send_direct(drip_prod, "NL.NDW.DRIP.DripDisplayState", _DRIP_SRC, subject, data)
            state.state.setdefault("drip", {})[key] = pub_time
            count += 1
        except Exception:
            logger.exception("AMQP send failed for DripDisplayState %s", key)

    logger.info("Emitted %d DripDisplayState events via AMQP", count)
    return count


def _emit_msi_states(msi_prod, state, acquirer):
    try:
        _, states = acquirer.fetch_msi()
    except Exception:
        logger.exception("Failed to fetch MSI display states")
        return 0

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
        subject = f"msi-signs/{sid}"
        try:
            _send_direct(msi_prod, "NL.NDW.MSI.MsiDisplayState", _MSI_SRC, subject, data)
            state.state.setdefault("msi", {})[sid] = pub_time
            count += 1
        except Exception:
            logger.exception("AMQP send failed for MsiDisplayState %s", sid)

    logger.info("Emitted %d MsiDisplayState events via AMQP", count)
    return count


def _emit_situations(sit_prod, state, acquirer):
    for feed_file, feed_type in SITUATION_FEEDS:
        try:
            records = acquirer.fetch_situations(feed_file, feed_type)
        except Exception:
            logger.exception("Failed to fetch situation feed %s", feed_file)
            continue

        src = _SITUATION_SOURCES.get(feed_type, _AVG_BASE)
        ce_type = _SITUATION_TYPES.get(feed_type, f"NL.NDW.Situations.{feed_type}")

        count = 0
        for rec in records:
            rid = rec["situation_record_id"]
            vtime = rec["version_time"]
            if state.state.get("situation", {}).get(rid) == vtime:
                continue
            subject = f"situations/{rid}"
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
                elif feed_type == "bridge_opening":
                    data = BridgeOpening(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        bridge_name=rec.get("bridge_name"), road_name=rec.get("road_name"),
                        description=rec.get("description"),
                    )
                elif feed_type == "temporary_closure":
                    data = TemporaryClosure(
                        situation_record_id=rid, version_time=vtime,
                        validity_status=rec.get("validity_status"),
                        start_time=rec.get("start_time"), end_time=rec.get("end_time"),
                        road_name=rec.get("road_name"), description=rec.get("description"),
                        location_description=rec.get("location_description"),
                        severity=rec.get("severity"),
                    )
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
                else:
                    continue
                _send_direct(sit_prod, ce_type, src, subject, data)
                state.state.setdefault("situation", {})[rid] = vtime
                count += 1
            except Exception:
                logger.exception("AMQP send failed for %s situation %s", feed_type, rid)

        logger.info("Emitted %d %s situation events via AMQP", count, feed_type)


# ---------------------------------------------------------------------------
# Main feed loop
# ---------------------------------------------------------------------------

async def _async_main(args: argparse.Namespace) -> None:
    avg_prod = _retry_build(NLNDWAVGAmqpProducer, args)
    drip_prod = _retry_build(NLNDWDRIPAmqpProducer, args)
    msi_prod = _retry_build(NLNDWMSIAmqpProducer, args)
    sit_prod = _retry_build(NLNDWSituationsAmqpProducer, args)

    acquirer = NdwAcquirer(
        base_url=args.base_url,
        max_records_per_family=args.max_records_per_family,
    )
    state = StateManager(args.state_file)

    last_ref = 0.0
    last_sit = 0.0

    try:
        while True:
            now = time.monotonic()

            if now - last_ref >= args.reference_refresh_interval:
                _emit_measurement_sites(avg_prod, acquirer)
                _emit_drip_signs(drip_prod, acquirer)
                _emit_msi_signs(msi_prod, acquirer)
                last_ref = time.monotonic()

            _emit_speed(avg_prod, state, acquirer)
            _emit_traveltime(avg_prod, state, acquirer)
            _emit_drip_states(drip_prod, state, acquirer)
            _emit_msi_states(msi_prod, state, acquirer)

            if now - last_sit >= args.situation_interval:
                _emit_situations(sit_prod, state, acquirer)
                last_sit = time.monotonic()

            state.save()

            if args.once:
                break
            await asyncio.sleep(args.poll_interval)
    finally:
        for prod in (avg_prod, drip_prod, msi_prod, sit_prod):
            try:
                close = getattr(prod, "close", None)
                if close:
                    close()
            except Exception:
                pass


def _add_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", SOURCE_ID))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS"))
    parser.add_argument("--content-mode", choices=("binary", "structured"),
                        default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"),
                        default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience",
                        default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--base-url", default=os.getenv("NDW_BASE_URL", BASE_URL))
    parser.add_argument("--poll-interval", type=int,
                        default=int(os.getenv("POLLING_INTERVAL", DEFAULT_POLL_INTERVAL_SECONDS)))
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
    parser = _add_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
