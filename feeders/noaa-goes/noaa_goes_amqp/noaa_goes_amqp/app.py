
"""AMQP 1.0 companion feeder for noaa-goes."""
from __future__ import annotations

import argparse
import asyncio
import importlib
import inspect
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
SOURCE_ID = "noaa-goes"
PY_MODULE = "noaa_goes"
ENV_PREFIX = "NOAA_GOES"

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
    if getattr(producer, "_send_queue", None) is not None:
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


class AmqpSendShim:
    """
    WORKAROUND(xregistry/codegen#XXX): The generated AMQP producer for noaa-goes
    defines ``send_amqp`` multiple times in one class body — once per event type
    (GoesXrayFlux, GoesProtonFlux, GoesElectronFlux, GoesMagnetometer,
    SpaceWeatherAlert, XrayFlare).  Python silently overwrites each definition
    with the next, so only the *last* definition (XrayFlare) survives at runtime.
    Calling ``producer.send_amqp(data=GoesXrayFlux(...), ...)`` would therefore
    build the wrong CloudEvent type/subject.

    This shim bypasses the broken overloaded name by replicating the send logic
    for each event type using the producer's internal machinery:
    ``_serialize_payload``, ``_ce_headers_to_amqp_properties``,
    ``_coerce_amqp_timestamp``, ``_send_via_reactor`` / ``_send_via_blocking_sender``.
    Each helper method below constructs the correct CloudEvent attributes and
    AMQP message independently.
    """

    def __init__(self, producer: Any) -> None:
        self._p = producer
        self.sent = 0

    def _send(
        self,
        type_attr: str,
        source: str,
        subject: str,
        data: Any,
        content_type: str = "application/json",
        extra_app_props: Optional[dict] = None,
    ) -> None:
        from proton import Message
        from cloudevents.http import CloudEvent
        from cloudevents.conversion import to_binary, to_structured

        p = self._p
        now_str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        attributes = {
            "type": type_attr,
            "source": source,
            "subject": subject,
            "time": now_str,
        }
        byte_data = p._serialize_payload(data, content_type)
        cloud_event = CloudEvent(attributes, byte_data)
        if p.content_mode == "structured":
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode("utf-8")
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode("utf-8")
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = p.format_type or headers.get("content-type")
        else:
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode("utf-8")
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = p._ce_headers_to_amqp_properties(headers)
        ts = p._coerce_amqp_timestamp(now_str)
        if ts is not None:
            amqp_msg.creation_time = ts
        amqp_msg.subject = subject
        if extra_app_props:
            if amqp_msg.properties is None:
                amqp_msg.properties = {}
            amqp_msg.properties.update(extra_app_props)  # type: ignore[attr-defined]
        if getattr(p, "_handler", None) is not None:
            p._send_via_reactor(amqp_msg)
        else:
            p._send_via_blocking_sender(amqp_msg)
        self.sent += 1

    def send_xray_flux(self, data: Any, satellite: str, energy: str, time_tag: str, event: str = "xrs") -> None:
        self._send(
            "Microsoft.OpenData.US.NOAA.SWPC.GoesXrayFlux",
            "https://services.swpc.noaa.gov",
            f"{_topic_segment(satellite)}/{_topic_segment(energy)}/{_topic_segment(time_tag)}",
            data,
            extra_app_props={"event": str(event)},
        )

    def send_proton_flux(self, data: Any, satellite: str, energy: str, time_tag: str, event: str = "sgps") -> None:
        self._send(
            "Microsoft.OpenData.US.NOAA.SWPC.GoesProtonFlux",
            "https://services.swpc.noaa.gov",
            f"{_topic_segment(satellite)}/{_topic_segment(energy)}/{_topic_segment(time_tag)}",
            data,
            extra_app_props={"event": str(event)},
        )

    def send_electron_flux(self, data: Any, satellite: str, energy: str, time_tag: str, event: str = "exis") -> None:
        self._send(
            "Microsoft.OpenData.US.NOAA.SWPC.GoesElectronFlux",
            "https://services.swpc.noaa.gov",
            f"{_topic_segment(satellite)}/{_topic_segment(energy)}/{_topic_segment(time_tag)}",
            data,
            extra_app_props={"event": str(event)},
        )

    def send_magnetometer(self, data: Any, satellite: str, time_tag: str, event: str = "magnetometer") -> None:
        self._send(
            "Microsoft.OpenData.US.NOAA.SWPC.GoesMagnetometer",
            "https://services.swpc.noaa.gov",
            f"{_topic_segment(satellite)}/{_topic_segment(time_tag)}",
            data,
            extra_app_props={"event": str(event)},
        )

    def send_space_weather_alert(self, data: Any, product_id: str) -> None:
        self._send(
            "Microsoft.OpenData.US.NOAA.SWPC.SpaceWeatherAlert",
            "https://services.swpc.noaa.gov",
            _topic_segment(product_id),
            data,
        )

    def send_xray_flare(self, data: Any, satellite: str, begin_time: str, flare_class: str) -> None:
        self._send(
            "Microsoft.OpenData.US.NOAA.SWPC.XrayFlare",
            "https://services.swpc.noaa.gov",
            f"{_topic_segment(satellite)}/{_topic_segment(begin_time)}",
            data,
            extra_app_props={"flare_class": str(flare_class)},
        )

    def close(self) -> None:
        close = getattr(self._p, "close", None)
        if close:
            close()


def _emit_sample_events(shim: AmqpSendShim) -> int:
    """Emit one sample event of each GOES AMQP event type via the shim."""
    from noaa_goes_amqp_producer_data import (
        GoesXrayFlux, GoesProtonFlux, GoesElectronFlux,
        GoesMagnetometer, SpaceWeatherAlert, XrayFlare,
    )
    ts = "2026-01-01T00:00:00Z"
    sat = "18"
    shim.send_xray_flux(
        GoesXrayFlux(time_tag=ts, satellite=18, flux=1.2e-6, energy="0.1-0.8nm"),
        satellite=sat, energy="0.1-0.8nm", time_tag=ts,
    )
    shim.send_proton_flux(
        GoesProtonFlux(time_tag=ts, satellite=18, flux=3.0, energy=">=10MeV"),
        satellite=sat, energy=">=10MeV", time_tag=ts,
    )
    shim.send_electron_flux(
        GoesElectronFlux(time_tag=ts, satellite=18, flux=900.0, energy=">=2MeV"),
        satellite=sat, energy=">=2MeV", time_tag=ts,
    )
    shim.send_magnetometer(
        GoesMagnetometer(time_tag=ts, satellite=18, he=1.0, hp=2.0, hn=3.0, total=3.7, arcjet_flag=False),
        satellite=sat, time_tag=ts,
    )
    shim.send_space_weather_alert(
        SpaceWeatherAlert(product_id="ALTXMF-20260101", issue_datetime="2026 Jan 01 0000 UTC", message="Synthetic SWPC alert."),
        product_id="ALTXMF-20260101",
    )
    shim.send_xray_flare(
        XrayFlare(
            time_tag=ts, begin_time="2026-01-01T00:00:00Z", begin_class="C9.0",
            max_time=ts, max_class="M1.0", max_xrlong=1e-5, max_ratio=0.2,
            max_ratio_time=ts, current_int_xrlong=1e-3,
            end_time="2026-01-01T00:10:00Z", end_class="C2.0", satellite=18,
        ),
        satellite=sat, begin_time="2026-01-01T00:00:00Z", flare_class="M1.0",
    )
    return shim.sent


async def _run_live(args: argparse.Namespace, shim: AmqpSendShim) -> None:
    """Fetch real SWPC/GOES data and emit via the AMQP shim."""
    from noaa_goes_core import SWPCFetcher
    from noaa_goes_amqp_producer_data import (
        GoesXrayFlux, GoesProtonFlux, GoesElectronFlux,
        GoesMagnetometer, SpaceWeatherAlert, XrayFlare,
    )

    fetcher = SWPCFetcher(last_polled_file=args.state_file)
    logger.info("Starting live SWPC/GOES AMQP poller for %s", SOURCE_ID)

    while True:
        count = 0
        try:
            state = fetcher.load_state()

            # --- Space weather alerts ---
            for alert_data in fetcher.poll_alerts():
                pid = alert_data.get("product_id", "")
                if not pid or pid == state.get("last_alert_id"):
                    continue
                shim.send_space_weather_alert(
                    SpaceWeatherAlert(
                        product_id=pid,
                        issue_datetime=alert_data.get("issue_datetime", ""),
                        message=alert_data.get("message", ""),
                    ),
                    product_id=pid,
                )
                state["last_alert_id"] = pid
                count += 1

            # --- GOES X-ray flux ---
            rows = fetcher.poll_goes_xrays()
            last_time = state.get("last_xray_time", "")
            filtered = [r for r in rows if str(r.get("time_tag", "")) > last_time]
            if filtered:
                state["last_xray_time"] = max(str(r.get("time_tag", "")) for r in filtered)
            for row in filtered:
                tt = str(row.get("time_tag", ""))
                sat = fetcher._safe_int(row.get("satellite"))
                energy = str(row.get("energy", ""))
                flux_val = fetcher._safe_float(row.get("flux"))
                if not tt or sat is None or flux_val is None:
                    continue
                shim.send_xray_flux(
                    GoesXrayFlux(time_tag=tt, satellite=sat, flux=flux_val, energy=energy),
                    satellite=str(sat), energy=energy, time_tag=tt,
                )
                count += 1

            # --- GOES proton flux ---
            rows = fetcher.poll_goes_protons()
            last_time = state.get("last_proton_time", "")
            filtered = [r for r in rows if str(r.get("time_tag", "")) > last_time]
            if filtered:
                state["last_proton_time"] = max(str(r.get("time_tag", "")) for r in filtered)
            for row in filtered:
                tt = str(row.get("time_tag", ""))
                sat = fetcher._safe_int(row.get("satellite"))
                energy = str(row.get("energy", ""))
                flux_val = fetcher._safe_float(row.get("flux"))
                if not tt or sat is None or flux_val is None:
                    continue
                shim.send_proton_flux(
                    GoesProtonFlux(time_tag=tt, satellite=sat, flux=flux_val, energy=energy),
                    satellite=str(sat), energy=energy, time_tag=tt,
                )
                count += 1

            # --- GOES electron flux ---
            rows = fetcher.poll_goes_electrons()
            last_time = state.get("last_electron_time", "")
            filtered = [r for r in rows if str(r.get("time_tag", "")) > last_time]
            if filtered:
                state["last_electron_time"] = max(str(r.get("time_tag", "")) for r in filtered)
            for row in filtered:
                tt = str(row.get("time_tag", ""))
                sat = fetcher._safe_int(row.get("satellite"))
                energy = str(row.get("energy", ""))
                flux_val = fetcher._safe_float(row.get("flux"))
                if not tt or sat is None or flux_val is None:
                    continue
                shim.send_electron_flux(
                    GoesElectronFlux(time_tag=tt, satellite=sat, flux=flux_val, energy=energy),
                    satellite=str(sat), energy=energy, time_tag=tt,
                )
                count += 1

            # --- GOES magnetometer ---
            for row in fetcher.poll_goes_magnetometers():
                tt = str(row.get("time_tag", ""))
                if not tt or tt <= state.get("last_magnetometer_time", ""):
                    continue
                sat = fetcher._safe_int(row.get("satellite"))
                if sat is None:
                    continue
                shim.send_magnetometer(
                    GoesMagnetometer(
                        time_tag=tt,
                        satellite=sat,
                        he=fetcher._safe_float(row.get("He")),
                        hp=fetcher._safe_float(row.get("Hp")),
                        hn=fetcher._safe_float(row.get("Hn")),
                        total=fetcher._safe_float(row.get("total")),
                        arcjet_flag=row.get("arcjet_flag"),
                    ),
                    satellite=str(sat), time_tag=tt,
                )
                state["last_magnetometer_time"] = tt
                count += 1

            # --- X-ray flares ---
            for row in fetcher.poll_xray_flares():
                tt = str(row.get("time_tag", ""))
                begin = str(row.get("begin_time", ""))
                if not tt or not begin or tt <= state.get("last_flare_time", ""):
                    continue
                sat = fetcher._safe_int(row.get("satellite"))
                if sat is None:
                    continue
                flare_class = str(row.get("max_class") or row.get("begin_class") or "unknown")
                shim.send_xray_flare(
                    XrayFlare(
                        time_tag=tt,
                        begin_time=begin,
                        begin_class=row.get("begin_class"),
                        max_time=row.get("max_time"),
                        max_class=row.get("max_class"),
                        max_xrlong=fetcher._safe_float(row.get("max_xrlong")),
                        max_ratio=fetcher._safe_float(row.get("max_ratio")),
                        max_ratio_time=row.get("max_ratio_time"),
                        current_int_xrlong=fetcher._safe_float(row.get("current_int_xrlong")),
                        end_time=row.get("end_time"),
                        end_class=row.get("end_class"),
                        satellite=sat,
                    ),
                    satellite=str(sat), begin_time=begin, flare_class=flare_class,
                )
                state["last_flare_time"] = tt
                count += 1

            fetcher.save_state(state)
            if count:
                logger.info("Emitted %d AMQP event(s) for %s", count, SOURCE_ID)

        except Exception as exc:
            logger.error("Error in live polling loop: %s", exc)

        if args.once:
            break
        await asyncio.sleep(args.polling_interval)


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
    parser.add_argument("--mock-mode", action="store_true", default=_env_bool(f"{ENV_PREFIX}_MOCK", False) or _env_bool(f"{ENV_PREFIX}_SAMPLE_MODE", False) or _env_bool(f"{ENV_PREFIX}_AMQP_MOCK", False))
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
            time.sleep(delay)


async def _async_main(args: argparse.Namespace) -> None:
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
    shim = AmqpSendShim(producer)
    try:
        if args.mock_mode:
            _emit_sample_events(shim)
            logger.info("Published %d mock AMQP event(s)", shim.sent)
        else:
            await _run_live(args, shim)
    finally:
        shim.close()


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()

