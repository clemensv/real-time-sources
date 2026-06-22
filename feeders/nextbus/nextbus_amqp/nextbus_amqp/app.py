
"""AMQP 1.0 companion feeder for nextbus."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import logging
import os
import time
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "nextbus"
PY_MODULE = "nextbus"
ENV_PREFIX = "NEXTBUS"

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _topic_segment(value: Any) -> str:
    text = (str(value) if value is not None else "unknown").strip() or "unknown"
    for forbidden in ("/", "+", "#", "\x00"):
        text = text.replace(forbidden, "-")
    return "-".join(text.split()) or "unknown"


def _parse_broker_url(url: str):
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    return parsed.hostname or "localhost", parsed.port or (5671 if tls else 5672), tls, parsed.username, parsed.password, (parsed.path or "").lstrip("/") or None


def _producer_class():
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer")
    classes = [obj for _, obj in vars(mod).items() if inspect.isclass(obj) and any(name.startswith("send_") for name in dir(obj))]
    if not classes:
        raise RuntimeError(f"No AMQP producer class found in {mod.__name__}")
    classes.sort(key=lambda cls: (len([name for name in dir(cls) if name.startswith("send_")]), cls.__name__), reverse=True)
    return classes[0]


def _apply_partition_key_workaround(producer):
    # WORKAROUND(xregistry/codegen#294): xrcg declares AMQP message_annotations
    # but does not emit them yet. Stamp x-opt-partition-key from CE subject.
    def stamp(msg):
        props = dict(getattr(msg, "properties", None) or {})
        ce_subject = props.get("cloudEvents:subject") or getattr(msg, "subject", None)
        if ce_subject:
            annotations = dict(getattr(msg, "annotations", None) or {})
            annotations[symbol("x-opt-partition-key")] = str(ce_subject)
            msg.annotations = annotations
        return msg
    if getattr(producer, "_sender", None) is not None:
        original_send = producer._sender.send
        producer._sender.send = lambda msg, *a, **kw: original_send(stamp(msg), *a, **kw)
    if hasattr(producer, "_send_via_reactor"):
        original_reactor_send = producer._send_via_reactor
        producer._send_via_reactor = lambda msg: original_reactor_send(stamp(msg))
    return producer


def _build_amqp_producer(args):
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
    kwargs = dict(host=host, address=address, port=port, content_mode=args.content_mode, use_tls=tls)
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(), entra_audience=args.entra_audience)
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return _apply_partition_key_workaround(_producer_class()(**kwargs))


class NextbusAmqpSendAdapter:
    """Source-local workaround for send_amqp name collision in generated producer.

    The generated NextbusAmqpProducer declares 4 overloads of send_amqp
    (one per data class: VehiclePosition, RouteConfig, Schedule, Message).
    Python silently overwrites all but the last definition, so only the
    Message variant survives at runtime.  This adapter exposes one typed
    send method per event family and manually constructs the correct
    CloudEvent subject / CE type before delegating to the producer's
    internal send infrastructure (_send_via_reactor or
    _send_via_blocking_sender), bypassing the broken send_amqp overloads.
    """

    _SOURCE = "https://retro.umoiq.com/service/publicXMLFeed"

    def __init__(self, producer: Any) -> None:
        self.producer = producer

    def _send(self, data: Any, ce_type: str, subject: str, event_time: Any = None) -> None:
        from cloudevents.http import CloudEvent
        from cloudevents.conversion import to_binary, to_structured
        from proton import Message, symbol as _sym
        import json

        ts = (
            datetime.utcfromtimestamp(event_time).isoformat() + "Z"
            if isinstance(event_time, float)
            else str(event_time)
            if event_time is not None
            else datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )
        attributes = {
            "type": ce_type,
            "source": self._SOURCE,
            "subject": subject,
            "time": ts,
        }
        byte_data = self.producer._serialize_payload(data, "application/json")
        cloud_event = CloudEvent(attributes, byte_data)

        if self.producer.content_mode == "structured":
            headers, body = to_structured(cloud_event)
            msg_body = json.dumps(body).encode("utf-8") if isinstance(body, dict) else (body if isinstance(body, bytes) else str(body).encode("utf-8"))
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self.producer.format_type or headers.get("content-type")
        else:
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode("utf-8")
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = "application/json"
            if headers:
                amqp_msg.properties = self.producer._ce_headers_to_amqp_properties(headers)

        amqp_msg.subject = subject
        amqp_msg.annotations = {_sym("x-opt-partition-key"): subject[:128]}

        if getattr(self.producer, "_handler", None) is not None:
            self.producer._send_via_reactor(amqp_msg)
        else:
            self.producer._send_via_blocking_sender(amqp_msg)

    def send_vehicle_position(self, data: Any, agency_id: str, route_tag: str, vehicle_id: str, event_time: Any = None) -> None:
        subject = f"{agency_id}/{route_tag}/vehicle/{vehicle_id}"
        self._send(data, "nextbus.VehiclePosition", subject, event_time)

    def send_route_config(self, data: Any, agency_id: str, route_tag: str, stop_or_vehicle_id: str, event_time: Any = None) -> None:
        subject = f"{agency_id}/{route_tag}/route-config/{stop_or_vehicle_id}"
        self._send(data, "nextbus.RouteConfig", subject, event_time)

    def send_schedule(self, data: Any, agency_id: str, route_tag: str, stop_or_vehicle_id: str, event_time: Any = None) -> None:
        subject = f"{agency_id}/{route_tag}/schedule/{stop_or_vehicle_id}"
        self._send(data, "nextbus.Schedule", subject, event_time)

    def send_message(self, data: Any, agency_id: str, route_tag: str, stop_or_vehicle_id: str, event_time: Any = None) -> None:
        subject = f"{agency_id}/{route_tag}/message/{stop_or_vehicle_id}"
        self._send(data, "nextbus.Message", subject, event_time)



def _emit_sample_corpus(sender: NextbusAmqpSendAdapter) -> int:
    """Emit one sample event of each NextBus event type via the AMQP sender.

    Used by --sample-mode (formerly --mock-mode).  Uses NextbusAmqpSendAdapter
    directly — no dispatch-table, no manifest parsing needed.
    """
    from nextbus_amqp_producer_data import VehiclePosition, RouteConfig, Schedule, Message

    agency = "sample-agency"
    route = "sample-route"
    vehicle = "sample-vehicle"
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    sender.send_vehicle_position(
        VehiclePosition(agency_id=agency, route_tag=route, vehicle_id=vehicle,
                        stop_or_vehicle_id=vehicle, event_type="vehicle",
                        lat="37.77", lon="-122.41", timestamp=0.0),
        agency, route, vehicle,
    )
    sender.send_route_config(
        RouteConfig(agency_id=agency, route_tag=route, stop_or_vehicle_id=route,
                    event_type="route-config", route_config="{}"),
        agency, route, route,
    )
    sender.send_schedule(
        Schedule(agency_id=agency, route_tag=route, stop_or_vehicle_id=route,
                 event_type="schedule", schedule="{}"),
        agency, route, route,
    )
    sender.send_message(
        Message(agency_id=agency, route_tag=route, stop_or_vehicle_id=route,
                event_type="message", message="{}"),
        agency, route, route,
    )
    return 4


async def _run_live(args: argparse.Namespace, producer: Any) -> None:
    """Real NextBus acquisition loop: fetch from upstream API and send via AMQP.

    Uses nextbus_core for all HTTP acquisition (zero transport dependency).
    Uses NextbusAmqpSendAdapter to work around the send_amqp name collision in
    the generated producer (all four overloads share one name; only the last
    survives at Python class definition time).
    """
    from nextbus_core import (
        get_route_config_updates,
        get_schedule_updates,
        get_message_updates,
        get_vehicle_positions,
    )
    from nextbus_amqp_producer_data import VehiclePosition, RouteConfig, Schedule, Message

    agency_tag = getattr(args, "agency", None) or os.getenv("AGENCY")
    if not agency_tag:
        logger.error("No agency tag configured; set --agency or AGENCY env var")
        return

    route = getattr(args, "route", "*") or "*"
    polling_interval = args.polling_interval if hasattr(args, "polling_interval") else 300
    sender = NextbusAmqpSendAdapter(producer)

    last_vehicle_time: Optional[float] = None
    last_ref_time: Optional[float] = None
    sent_total = 0

    while True:
        current_time = time.monotonic()

        # Reference data (route configs, schedules, messages) — refreshed every hour
        if last_ref_time is None or current_time - last_ref_time >= 3600:
            try:
                for rc in get_route_config_updates(agency_tag):
                    data = RouteConfig(
                        agency_id=rc["agency"],
                        route_tag=rc["routeTag"],
                        stop_or_vehicle_id=rc["routeTag"],
                        event_type="route-config",
                        route_config=rc["routeConfig"],
                    )
                    sender.send_route_config(data, rc["agency"], rc["routeTag"], rc["routeTag"])
                    sent_total += 1
                    logger.info("Sent RouteConfig for %s/%s", agency_tag, rc["routeTag"])

                for sched in get_schedule_updates(agency_tag):
                    data_s = Schedule(
                        agency_id=sched["agency"],
                        route_tag=sched["routeTag"],
                        stop_or_vehicle_id=sched["routeTag"],
                        event_type="schedule",
                        schedule=sched["schedule"],
                    )
                    sender.send_schedule(data_s, sched["agency"], sched["routeTag"], sched["routeTag"])
                    sent_total += 1
                    logger.info("Sent Schedule for %s/%s", agency_tag, sched["routeTag"])

                for msg in get_message_updates(agency_tag):
                    data_m = Message(
                        agency_id=msg["agency"],
                        route_tag=msg["routeTag"],
                        stop_or_vehicle_id=msg["routeTag"],
                        event_type="message",
                        message=msg["messages"],
                    )
                    sender.send_message(data_m, msg["agency"], msg["routeTag"], msg["routeTag"])
                    sent_total += 1
                    logger.info("Sent Message for %s/%s", agency_tag, msg["routeTag"])
            except Exception as ref_err:
                logger.warning("Reference data fetch error: %s", ref_err)
            last_ref_time = current_time

        # Vehicle positions
        try:
            positions, last_vehicle_time = get_vehicle_positions(agency_tag, route, last_vehicle_time)
            for vp in positions:
                veh_data = VehiclePosition(
                    agency_id=vp["agency"],
                    route_tag=vp.get("routeTag") or "",
                    vehicle_id=vp["id"],
                    stop_or_vehicle_id=vp["id"],
                    event_type="vehicle",
                    lat=vp.get("lat"),
                    lon=vp.get("lon"),
                    timestamp=vp["timestamp"],
                )
                sender.send_vehicle_position(
                    veh_data,
                    vp["agency"],
                    vp.get("routeTag") or "",
                    vp["id"],
                    event_time=vp["timestamp"],
                )
                sent_total += 1
            if positions:
                logger.info("Sent %d vehicle positions for %s", len(positions), agency_tag)
        except Exception as vp_err:
            logger.warning("Vehicle positions fetch error: %s", vp_err)

        logger.debug("Total AMQP events sent so far: %d", sent_total)
        if args.once:
            break
        await asyncio.sleep(polling_interval)


def _add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("feed_command", nargs="?", default="feed")
    parser.add_argument("--broker-url", default=os.getenv("AMQP_BROKER_URL"))
    parser.add_argument("--host", default=os.getenv("AMQP_HOST"))
    parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    parser.add_argument("--address", default=os.getenv("AMQP_ADDRESS", SOURCE_ID))
    parser.add_argument("--username", default=os.getenv("AMQP_USERNAME"))
    parser.add_argument("--password", default=os.getenv("AMQP_PASSWORD"))
    parser.add_argument("--tls", action="store_true", default=_env_bool("AMQP_TLS", False))
    parser.add_argument("--content-mode", choices=("binary", "structured"), default=os.getenv("AMQP_CONTENT_MODE", "binary"))
    parser.add_argument("--auth-mode", choices=("password", "entra", "sas"), default=os.getenv("AMQP_AUTH_MODE", "password"))
    parser.add_argument("--entra-audience", default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    parser.add_argument("--entra-client-id", default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    parser.add_argument("--sas-key-name", default=os.getenv("AMQP_SAS_KEY_NAME"))
    parser.add_argument("--sas-key", default=os.getenv("AMQP_SAS_KEY"))
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", os.path.expanduser(f"~/.{PY_MODULE}_amqp_state.json")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    parser.add_argument("--sample-mode", action="store_true", default=_env_bool(f"{ENV_PREFIX}_SAMPLE_MODE", False) or _env_bool(f"{ENV_PREFIX}_AMQP_SAMPLE", False))
    # NextBus-specific acquisition args
    parser.add_argument("--agency", default=os.getenv("AGENCY"), help="NextBus agency tag to poll (required for live mode)")
    parser.add_argument("--route", default=os.getenv("ROUTE", "*"), help="NextBus route tag, or '*' for all routes (default: *)")
    return parser



def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logger.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)

async def _async_main(args: argparse.Namespace) -> None:
    # Retry producer connection with backoff (RBAC propagation can take minutes)
    producer = None
    for _attempt in range(6):
        try:
            producer = _retry_producer_init(lambda: _build_amqp_producer(args))
            break
        except Exception as _conn_err:
            logger.warning("AMQP connection attempt %d failed: %s", _attempt + 1, _conn_err)
            if _attempt < 5:
                await asyncio.sleep(15 * (_attempt + 1))
    if producer is None:
        logger.error("Failed to connect to AMQP broker after 6 attempts")
        return
    sender = NextbusAmqpSendAdapter(producer)
    try:
        if args.sample_mode:
            count = _emit_sample_corpus(sender)
            logger.info("Published %d sample AMQP event(s)", count)
        else:
            await _run_live(args, producer)
    finally:
        close = getattr(producer, "close", None)
        if close:
            close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
