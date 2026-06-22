
"""AMQP 1.0 feeder for Entur Norway SIRI real-time transit data."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import inspect
import logging
import os
import time
import uuid
from typing import Optional
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

from entur_norway_core import EnturNorwayBridge, _has_more_data

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "entur-norway"
PY_MODULE = "entur_norway"

logger = logging.getLogger(__name__)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


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


async def _run_live(args: argparse.Namespace, producer) -> None:
    """Acquire live Entur Norway SIRI data and publish via AMQP."""
    bridge = EnturNorwayBridge()
    poll_interval = args.polling_interval
    max_size = args.max_size

    et_requestor_id = str(uuid.uuid4())
    vm_requestor_id = str(uuid.uuid4())
    sx_requestor_id = str(uuid.uuid4())
    first_run = True

    while True:
        poll_start = time.monotonic()

        # ── ET: Estimated Timetable ────────────────────────────────────────────
        et_req_id: Optional[str] = None if first_run else et_requestor_id
        et_count = 0
        more_et = True
        while more_et:
            et_root = await asyncio.to_thread(bridge.fetch_siri, "et", et_req_id, max_size)
            if et_root is None:
                break
            more_et = _has_more_data(et_root)
            et_req_id = et_requestor_id
            for op_day, sj_id, evj in bridge.parse_et_journeys(et_root):
                try:
                    producer.send_estimated_vehicle_journey(
                        data=evj,
                        _operating_day=op_day,
                        _service_journey_id=sj_id,
                        _operator_ref=evj.operator_ref,
                        _line_ref=evj.line_ref,
                    )
                    et_count += 1
                except Exception as exc:
                    logger.error("Error sending EstimatedVehicleJourney %s/%s: %s", op_day, sj_id, exc)

        # ── VM: Vehicle Monitoring ─────────────────────────────────────────────
        vm_req_id: Optional[str] = None if first_run else vm_requestor_id
        vm_count = 0
        more_vm = True
        while more_vm:
            vm_root = await asyncio.to_thread(bridge.fetch_siri, "vm", vm_req_id, max_size)
            if vm_root is None:
                break
            more_vm = _has_more_data(vm_root)
            vm_req_id = vm_requestor_id
            for op_day, sj_id, mvj in bridge.parse_vm_journeys(vm_root):
                try:
                    producer.send_monitored_vehicle_journey(
                        data=mvj,
                        _operating_day=op_day,
                        _service_journey_id=sj_id,
                        _operator_ref=mvj.operator_ref,
                        _line_ref=mvj.line_ref,
                    )
                    vm_count += 1
                except Exception as exc:
                    logger.error("Error sending MonitoredVehicleJourney %s/%s: %s", op_day, sj_id, exc)

        # ── SX: Situation Exchange ─────────────────────────────────────────────
        sx_req_id: Optional[str] = None if first_run else sx_requestor_id
        sx_count = 0
        more_sx = True
        while more_sx:
            sx_root = await asyncio.to_thread(bridge.fetch_siri, "sx", sx_req_id, max_size)
            if sx_root is None:
                break
            more_sx = _has_more_data(sx_root)
            sx_req_id = sx_requestor_id
            for sit_num, sit in bridge.parse_sx_situations(sx_root):
                try:
                    producer.send_pt_situation_element(
                        data=sit,
                        _situation_number=sit_num,
                        _severity=sit.severity,
                    )
                    sx_count += 1
                except Exception as exc:
                    logger.error("Error sending PtSituationElement %s: %s", sit_num, exc)

        elapsed = time.monotonic() - poll_start
        logger.info(
            "Published Entur ET=%d VM=%d SX=%d in %.1fs",
            et_count, vm_count, sx_count, elapsed,
        )
        first_run = False

        if args.once:
            break
        await asyncio.sleep(max(0, poll_interval - elapsed))


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
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "30")))
    parser.add_argument("--max-size", type=int, default=int(os.getenv("MAX_SIZE", "1000")))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
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
            logger.warning(
                "Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                attempt + 1, max_attempts, e, delay,
            )
            import time as _time; _time.sleep(delay)


async def _async_main(args: argparse.Namespace) -> None:
    producer = _retry_producer_init(lambda: _build_amqp_producer(args))
    try:
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

