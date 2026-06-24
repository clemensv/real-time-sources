"""AMQP 1.0 companion feeder for nws-forecasts."""
from __future__ import annotations

import argparse
import asyncio
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

try:
    from proton import Message
    from cloudevents.http import CloudEvent
    from cloudevents.conversion import to_binary, to_structured
    _AMQP_AVAILABLE = True
except ImportError:
    _AMQP_AVAILABLE = False

try:
    from nws_forecasts_core import (
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_STATE_FILE,
        DEFAULT_ZONES,
        NWSForecastFetcher,
        NWSForecastZone,
        NWSLandZoneForecast,
        NWSMarineZoneForecast,
        build_retrying_session,
        parse_zone_list,
    )
except ImportError:
    from nws_forecasts_core.nws_forecasts import (  # type: ignore[no-redef]
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_STATE_FILE,
        DEFAULT_ZONES,
        NWSForecastFetcher,
        NWSForecastZone,
        NWSLandZoneForecast,
        NWSMarineZoneForecast,
        build_retrying_session,
        parse_zone_list,
    )

from nws_forecasts_amqp_producer_data import (
    ForecastZone,
    LandForecastPeriod,
    LandZoneForecast,
    MarineForecastPeriod,
    MarineZoneForecast,
    ZoneTypeenum,
)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "nws-forecasts"
PY_MODULE = "nws_forecasts"
ENV_PREFIX = "NWS_FORECASTS"

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


def _build_amqp_producer(args):
    import importlib
    mod = importlib.import_module(f"{PY_MODULE}_amqp_producer_amqp_producer.producer")
    producer_class = getattr(mod, "MicrosoftOpenDataUSNOAANWSForecastsAmqpProducer")

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
    producer = producer_class(**kwargs)
    return _apply_partition_key_workaround(producer)


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


# ---------------------------------------------------------------------------
# Source-local shim for the generated send_amqp method collision.
#
# The generated MicrosoftOpenDataUSNOAANWSForecastsAmqpProducer defines
# ``send_amqp`` three times (once for ForecastZone, LandZoneForecast, and
# MarineZoneForecast).  Python resolves duplicate method names in a class
# body to the LAST definition, so only the MarineZoneForecast overload
# survives at runtime; the ForecastZone and LandZoneForecast overloads are
# silently dropped.  This shim works around the codegen bug by building each
# AMQP message directly via the underlying producer infrastructure
# (_serialize_payload, _ce_headers_to_amqp_properties, _coerce_amqp_timestamp,
# and the send primitives), one distinctly-named method per event type.
# ---------------------------------------------------------------------------

CE_TYPE_ZONE = "Microsoft.OpenData.US.NOAA.NWS.ForecastZone"
CE_TYPE_LAND = "Microsoft.OpenData.US.NOAA.NWS.LandZoneForecast"
CE_TYPE_MARINE = "Microsoft.OpenData.US.NOAA.NWS.MarineZoneForecast"
CE_SOURCE_ZONE_LAND = "https://api.weather.gov"
CE_SOURCE_MARINE = "https://tgftp.nws.noaa.gov/data/forecasts/marine/coastal/pz/"


class NWSAmqpProducerShim:
    """Shim exposing distinctly-named send methods for each NWS event type.

    The generated producer class defines ``send_amqp`` three times (once per
    data class).  Python keeps only the last definition; the two earlier
    ForecastZone and LandZoneForecast overloads are unreachable through the
    normal producer API.  This class builds AMQP messages directly via the
    producer's internal helpers, bypassing the overloaded method entirely.
    """

    def __init__(self, producer: Any) -> None:
        self._p = producer

    def _send_one(
        self,
        ce_type: str,
        ce_source: str,
        zone_id: str,
        state: str,
        zone_type: str,
        event: str,
        data: Any,
        content_type: str = "application/json",
    ) -> None:
        attributes = {
            "type": ce_type,
            "source": ce_source,
            "subject": zone_id,
            "time": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        byte_data = self._p._serialize_payload(data, content_type)
        cloud_event = CloudEvent(attributes, byte_data)

        if self._p.content_mode == "structured":
            headers, body = to_structured(cloud_event)
            if isinstance(body, dict):
                msg_body = json.dumps(body).encode("utf-8")
            elif isinstance(body, bytes):
                msg_body = body
            else:
                msg_body = str(body).encode("utf-8")
            amqp_msg = Message(body=msg_body, inferred=True)
            amqp_msg.content_type = self._p.format_type or headers.get("content-type")
        else:
            headers, body = to_binary(cloud_event)
            if isinstance(body, str):
                body = body.encode("utf-8")
            amqp_msg = Message(body=body, inferred=True)
            amqp_msg.content_type = content_type
            if headers:
                amqp_msg.properties = self._p._ce_headers_to_amqp_properties(headers)

        ts = self._p._coerce_amqp_timestamp(attributes.get("time"))
        if ts is not None:
            amqp_msg.creation_time = ts

        amqp_msg.subject = zone_id
        props = dict(amqp_msg.properties or {})
        props.update({"state": state, "zone_type": zone_type, "event": event})
        amqp_msg.properties = props

        if getattr(self._p, "_handler", None) is not None:
            self._p._send_via_reactor(amqp_msg)
        else:
            self._p._send_via_blocking_sender(amqp_msg)

    def send_forecast_zone(
        self, zone_id: str, state: str, zone_type: str, data: ForecastZone
    ) -> None:
        self._send_one(CE_TYPE_ZONE, CE_SOURCE_ZONE_LAND, zone_id, state, zone_type, "info", data)

    def send_land_zone_forecast(
        self, zone_id: str, state: str, zone_type: str, data: LandZoneForecast
    ) -> None:
        self._send_one(CE_TYPE_LAND, CE_SOURCE_ZONE_LAND, zone_id, state, zone_type, "land-forecast", data)

    def send_marine_zone_forecast(
        self, zone_id: str, state: str, zone_type: str, data: MarineZoneForecast
    ) -> None:
        self._send_one(CE_TYPE_MARINE, CE_SOURCE_MARINE, zone_id, state, zone_type, "marine-forecast", data)

    def close(self) -> None:
        close = getattr(self._p, "close", None)
        if close:
            close()


# ---------------------------------------------------------------------------
# Data conversion helpers: core dataclasses → AMQP producer_data dataclasses
# ---------------------------------------------------------------------------

def _to_amqp_zone(zone: NWSForecastZone) -> ForecastZone:
    return ForecastZone(
        zone_id=zone.zone_id,
        zone_type=ZoneTypeenum(zone.zone_type),
        name=zone.name,
        state=zone.state,
        forecast_office_url=zone.forecast_office_url,
        grid_identifier=zone.grid_identifier,
        awips_location_identifier=zone.awips_location_identifier,
        cwa_ids=zone.cwa_ids,
        forecast_office_urls=zone.forecast_office_urls,
        time_zones=zone.time_zones,
        observation_station_ids=zone.observation_station_ids,
        radar_station=zone.radar_station,
        effective_date=zone.effective_date,
        expiration_date=zone.expiration_date,
    )


def _to_amqp_land(forecast: NWSLandZoneForecast) -> LandZoneForecast:
    return LandZoneForecast(
        zone_id=forecast.zone_id,
        updated=forecast.updated,
        periods=[
            LandForecastPeriod(
                period_number=p.period_number,  # type: ignore[arg-type]
                period_name=p.period_name,
                detailed_forecast=p.detailed_forecast,
            )
            for p in forecast.periods
        ],
    )


def _to_amqp_marine(forecast: NWSMarineZoneForecast) -> MarineZoneForecast:
    return MarineZoneForecast(
        zone_id=forecast.zone_id,
        zone_name=forecast.zone_name,  # type: ignore[arg-type]
        product_title=forecast.product_title,
        office_name=forecast.office_name,
        issued_at_text=forecast.issued_at_text,  # type: ignore[arg-type]
        expires_text=forecast.expires_text,
        wmo_header=forecast.wmo_header,
        bulletin_awips_id=forecast.bulletin_awips_id,
        synopsis=forecast.synopsis,
        periods=[
            MarineForecastPeriod(
                period_name=p.period_name,
                forecast_text=p.forecast_text,
            )
            for p in forecast.periods
        ],
        bulletin_text=forecast.bulletin_text,  # type: ignore[arg-type]
    )


# ---------------------------------------------------------------------------
# Live acquisition loop
# ---------------------------------------------------------------------------

async def _run_live(args: argparse.Namespace, shim: NWSAmqpProducerShim) -> None:
    """Real NWS forecast acquisition loop emitting via AMQP."""
    zones = parse_zone_list(args.zones)

    def on_zone(zone_id: str, zone: NWSForecastZone) -> None:
        amqp_zone = _to_amqp_zone(zone)
        shim.send_forecast_zone(
            zone_id=zone_id,
            state=_topic_segment(zone.state),
            zone_type=_topic_segment(zone.zone_type),
            data=amqp_zone,
        )

    def on_land(zone_id: str, forecast: NWSLandZoneForecast) -> None:
        zone = fetcher.zone_cache.get(zone_id)
        state = _topic_segment(zone.state) if zone else "unknown"
        zone_type = _topic_segment(zone.zone_type) if zone else "public"
        shim.send_land_zone_forecast(
            zone_id=zone_id,
            state=state,
            zone_type=zone_type,
            data=_to_amqp_land(forecast),
        )

    def on_marine(zone_id: str, forecast: NWSMarineZoneForecast) -> None:
        zone = fetcher.zone_cache.get(zone_id)
        state = _topic_segment(zone.state) if zone else "unknown"
        zone_type = _topic_segment(zone.zone_type) if zone else "marine"
        shim.send_marine_zone_forecast(
            zone_id=zone_id,
            state=state,
            zone_type=zone_type,
            data=_to_amqp_marine(forecast),
        )

    fetcher = NWSForecastFetcher(
        zones=zones,
        state_file=args.state_file,
        poll_interval_seconds=args.polling_interval,
        on_zone=on_zone,
        on_land_forecast=on_land,
        on_marine_forecast=on_marine,
    )

    logger.info("Starting NWS AMQP feeder for zones: %s", ", ".join(zones))
    await asyncio.get_running_loop().run_in_executor(
        None, lambda: fetcher.run(once=args.once)
    )


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
    parser.add_argument("--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", str(DEFAULT_POLL_INTERVAL_SECONDS))))
    parser.add_argument("--state-file", default=os.getenv("STATE_FILE", DEFAULT_STATE_FILE))
    parser.add_argument("--zones", default=os.getenv("NWS_FORECAST_ZONES", DEFAULT_ZONES))
    parser.add_argument("--once", action="store_true", default=_env_bool("ONCE_MODE", False))
    parser.add_argument("--mock-mode", action="store_true", default=_env_bool(f"{ENV_PREFIX}_MOCK", False) or _env_bool(f"{ENV_PREFIX}_SAMPLE_MODE", False) or _env_bool(f"{ENV_PREFIX}_AMQP_MOCK", False))
    return parser


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
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
    shim = NWSAmqpProducerShim(producer)
    try:
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
