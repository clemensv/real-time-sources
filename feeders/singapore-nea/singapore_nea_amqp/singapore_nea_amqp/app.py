
"""AMQP 1.0 companion feeder for singapore-nea."""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import time as _time
from datetime import datetime, timezone
from typing import Any, Optional
from urllib.parse import urlparse

try:
    from proton import symbol
except Exception:  # pragma: no cover
    symbol = lambda value: value  # type: ignore

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
SOURCE_ID = "singapore-nea"
PY_MODULE = "singapore_nea"
ENV_PREFIX = "SINGAPORE_NEA"

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


def _station_region(latitude: float, longitude: float) -> str:
    """Assign a Singapore geographic region based on station coordinates."""
    if latitude > 1.385:
        return "north"
    if latitude < 1.300:
        return "south"
    if longitude > 103.885:
        return "east"
    if longitude < 103.775:
        return "west"
    return "central"


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


def _extract_producer_kwargs(args) -> dict:
    """Extract AMQP connection kwargs from parsed args."""
    if args.broker_url:
        host, port, tls, url_user, url_pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or url_user
        password = args.password or url_pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        address = path or args.address
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password
        address = args.address
    kwargs: dict[str, Any] = dict(
        host=host, address=address, port=port,
        content_mode=args.content_mode, use_tls=tls,
    )
    if args.auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        kwargs.update(
            credential=ManagedIdentityCredential(client_id=args.entra_client_id) if args.entra_client_id else DefaultAzureCredential(),
            entra_audience=args.entra_audience,
        )
    elif args.auth_mode == "sas":
        if not args.sas_key_name or not args.sas_key:
            raise RuntimeError("AMQP auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        kwargs.update(sas_key_name=args.sas_key_name, sas_key=args.sas_key)
    else:
        kwargs.update(username=username, password=password)
    return kwargs


# ---------------------------------------------------------------------------
# Source-local AMQP send helpers
#
# WORKAROUND(xregistry/codegen#shadowedmethods): The generated AMQP producer
# classes declare multiple send_amqp overloads for different message types.
# Python only retains the LAST definition per class, so earlier overloads are
# silently shadowed at class-definition time:
#   SGGovNEAWeatherAmqpProducer  : Station (shadowed), WeatherObservation (live)
#   SGGovNEAAirQualityAmqpProducer: Region (shadowed), PSIReading (shadowed), PM25Reading (live)
# We replicate the CloudEvent + AMQP serialisation pattern for the shadowed
# variants using the producer's internal infrastructure. A codegen bug should
# be filed upstream (xregistry/codegen) to emit distinct method names per
# message type instead of overloading send_amqp.
# ---------------------------------------------------------------------------

def _build_and_send_amqp_message(
    producer: Any,
    data: Any,
    ce_type: str,
    subject: str,
    app_properties: dict[str, str],
    _time_val: Optional[Any] = None,
) -> None:
    """Build a CloudEvent AMQP message and send it via the producer's internals."""
    try:
        from proton import Message
        from cloudevents.http import CloudEvent
        from cloudevents.conversion import to_binary, to_structured
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("proton / cloudevents packages required for AMQP send") from exc

    now_str = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if _time_val is not None:
        if isinstance(_time_val, datetime):
            if _time_val.tzinfo is None:
                _time_val = _time_val.replace(tzinfo=timezone.utc)
            resolved_time = _time_val.isoformat().replace("+00:00", "Z")
        else:
            resolved_time = str(_time_val)
    else:
        resolved_time = now_str

    attributes = {
        "type": ce_type,
        "source": "https://api.data.gov.sg",
        "subject": subject,
        "time": resolved_time,
    }
    attributes = {k: v for k, v in attributes.items() if v is not None}

    byte_data = producer._serialize_payload(data, "application/json")
    cloud_event = CloudEvent(attributes, byte_data)

    if producer.content_mode == "structured":
        headers, body = to_structured(cloud_event)
        msg_body = (
            json.dumps(body).encode("utf-8")
            if isinstance(body, dict)
            else (body if isinstance(body, bytes) else str(body).encode("utf-8"))
        )
        amqp_msg = Message(body=msg_body, inferred=True)
        amqp_msg.content_type = getattr(producer, "format_type", None) or headers.get("content-type")
    else:
        headers, body = to_binary(cloud_event)
        if isinstance(body, str):
            body = body.encode("utf-8")
        amqp_msg = Message(body=body, inferred=True)
        amqp_msg.content_type = "application/json"
        if headers:
            amqp_msg.properties = producer._ce_headers_to_amqp_properties(headers)

    ts = producer._coerce_amqp_timestamp(resolved_time)
    if ts is not None:
        amqp_msg.creation_time = ts
    amqp_msg.subject = subject

    if amqp_msg.properties is None:
        amqp_msg.properties = {}
    amqp_msg.properties.update(app_properties)  # type: ignore[attr-defined]

    if getattr(producer, "_handler", None) is not None:
        producer._send_via_reactor(amqp_msg)
    else:
        producer._send_via_blocking_sender(amqp_msg)


def _send_station_amqp(producer, data, station_id: str, region: str, event: str) -> None:
    """Send a Station event (shadowed send_amqp overload workaround)."""
    _build_and_send_amqp_message(
        producer, data,
        ce_type="SG.Gov.NEA.Weather.Station",
        subject=station_id,
        app_properties={"region": region, "event": event},
    )


def _send_region_amqp(producer, data, region: str, station_id: str, event: str) -> None:
    """Send a Region event (shadowed send_amqp overload workaround)."""
    _build_and_send_amqp_message(
        producer, data,
        ce_type="SG.Gov.NEA.AirQuality.Region",
        subject=region,
        app_properties={"station_id": station_id, "event": event},
    )


def _send_psireading_amqp(
    producer, data, region: str, station_id: str, event: str, ts: Optional[Any] = None
) -> None:
    """Send a PSIReading event (shadowed send_amqp overload workaround)."""
    _build_and_send_amqp_message(
        producer, data,
        ce_type="SG.Gov.NEA.AirQuality.PSIReading",
        subject=region,
        app_properties={"station_id": station_id, "event": event},
        _time_val=ts,
    )



def _build_both_producers(args):
    """Build weather + air quality AMQP producers."""
    from singapore_nea_amqp_producer_amqp_producer.producer import (
        SGGovNEAWeatherAmqpProducer,
        SGGovNEAAirQualityAmqpProducer,
    )
    kwargs = _extract_producer_kwargs(args)
    weather_producer = _apply_partition_key_workaround(SGGovNEAWeatherAmqpProducer(**kwargs))
    aq_producer = _apply_partition_key_workaround(SGGovNEAAirQualityAmqpProducer(**kwargs))
    return weather_producer, aq_producer


def _emit_sample_events(weather_producer, aq_producer) -> int:
    """Send one sample event per message type via AMQP (sample/test mode)."""
    from singapore_nea_amqp_producer_data import Station, WeatherObservation, Region, PSIReading, PM25Reading

    now = datetime.now(timezone.utc)
    sent = 0

    station = Station(
        station_id="S109", device_id="S109", name="Ang Mo Kio Avenue 5",
        latitude=1.3764, longitude=103.8492, data_types="air_temperature,rainfall",
    )
    _send_station_amqp(weather_producer, station, "S109", "central", "info")
    sent += 1

    observation = WeatherObservation(
        station_id="S109", station_name="Ang Mo Kio Avenue 5", observation_time=now,
        air_temperature=30.5, rainfall=0.0, relative_humidity=75.0,
        wind_speed=2.1, wind_direction=180.0,
    )
    weather_producer.send_amqp(
        data=observation, _station_id="S109", _region="central", _event="weather", _time=now,
    )
    sent += 1

    region = Region(region="central", latitude=1.357, longitude=103.82)
    _send_region_amqp(aq_producer, region, "central", "central", "info")
    sent += 1

    psi = PSIReading(
        region="central", timestamp=now, update_timestamp=now,
        psi_twenty_four_hourly=52, o3_sub_index=10, pm10_sub_index=20,
        pm10_twenty_four_hourly=25, pm25_sub_index=30, pm25_twenty_four_hourly=12,
        co_sub_index=5, co_eight_hour_max=1, so2_sub_index=2,
        so2_twenty_four_hourly=3, no2_one_hour_max=8, o3_eight_hour_max=10,
    )
    _send_psireading_amqp(aq_producer, psi, "central", "central", "psi", now)
    sent += 1

    pm25 = PM25Reading(region="central", timestamp=now, update_timestamp=now, pm25_one_hourly=11)
    aq_producer.send_amqp(
        data=pm25, _region="central", _station_id="central", _event="pm25", _time=now,
    )
    sent += 1

    return sent


async def _run_live(args: argparse.Namespace) -> None:
    """Live acquisition loop: fetch real NEA data and send via AMQP."""
    from singapore_nea_core import (
        NEAWeatherAPI,
        NEAAirQualityAPI,
        merge_observations,
        fetch_psi_readings,
        fetch_pm25_readings,
        load_state,
        save_state,
        split_state,
        compose_state,
        AIR_QUALITY_REFERENCE_REFRESH_INTERVAL,
    )
    from singapore_nea_amqp_producer_data import Station, WeatherObservation, Region, PSIReading, PM25Reading
    from singapore_nea_amqp_producer_amqp_producer.producer import (
        SGGovNEAWeatherAmqpProducer,
        SGGovNEAAirQualityAmqpProducer,
    )

    producer_kwargs = _extract_producer_kwargs(args)
    weather_producer = _apply_partition_key_workaround(SGGovNEAWeatherAmqpProducer(**producer_kwargs))
    aq_producer = _apply_partition_key_workaround(SGGovNEAAirQualityAmqpProducer(**producer_kwargs))

    polling_interval = getattr(args, "polling_interval", 300)
    aq_polling_interval = int(os.getenv("AIRQUALITY_POLLING_INTERVAL", "3600"))

    weather_api = NEAWeatherAPI(polling_interval=polling_interval)
    aq_api = NEAAirQualityAPI(polling_interval=aq_polling_interval)

    previous_state = load_state(args.state_file)
    weather_state, psi_state, pm25_state = split_state(previous_state)

    # Emit station reference data at startup
    stations = weather_api.get_all_stations()
    for sid, sd in stations.items():
        station = Station(
            station_id=sd.station_id, device_id=sd.device_id, name=sd.name,
            latitude=sd.latitude, longitude=sd.longitude, data_types=sd.data_types,
        )
        _send_station_amqp(weather_producer, station, sid, _station_region(sd.latitude, sd.longitude), "info")
    logger.info("Sent %d weather station reference events via AMQP", len(stations))

    # Emit region reference data at startup
    regions = aq_api.get_regions()
    for region_name, rd in regions.items():
        region = Region(region=rd.region, latitude=rd.latitude, longitude=rd.longitude)
        _send_region_amqp(aq_producer, region, region_name, region_name, "info")
    logger.info("Sent %d region reference events via AMQP", len(regions))

    now = _time.monotonic()
    next_weather_poll = now
    next_aq_poll = now
    next_aq_region_refresh = now + AIR_QUALITY_REFERENCE_REFRESH_INTERVAL
    did_weather = False
    did_aq = False

    try:
        while True:
            now = _time.monotonic()
            next_due = min(next_weather_poll, next_aq_poll, next_aq_region_refresh)
            if now < next_due:
                await asyncio.sleep(max(1, min(int(next_due - now), 30)))
                continue

            state_changed = False

            if now >= next_weather_poll:
                did_weather = True
                next_weather_poll = now + polling_interval
                try:
                    all_stations, observations = merge_observations(weather_api)
                    sent = 0
                    for obs in observations:
                        key = f"{obs.station_id}:{obs.observation_time.isoformat()}"
                        if key in weather_state:
                            continue
                        observation = WeatherObservation(
                            station_id=obs.station_id, station_name=obs.station_name,
                            observation_time=obs.observation_time,
                            air_temperature=obs.air_temperature, rainfall=obs.rainfall,
                            relative_humidity=obs.relative_humidity,
                            wind_speed=obs.wind_speed, wind_direction=obs.wind_direction,
                        )
                        sd = all_stations.get(obs.station_id)
                        region_val = _station_region(sd.latitude, sd.longitude) if sd else "central"
                        weather_producer.send_amqp(
                            data=observation, _station_id=obs.station_id,
                            _region=region_val, _event="weather", _time=obs.observation_time,
                        )
                        weather_state[key] = obs.observation_time.isoformat()
                        sent += 1
                    logger.info("Sent %d weather observations via AMQP", sent)
                    state_changed = True
                except Exception as exc:  # pragma: no cover - runtime safety
                    logger.error("Error fetching/sending weather: %s", exc)

            if now >= next_aq_region_refresh:
                next_aq_region_refresh = now + AIR_QUALITY_REFERENCE_REFRESH_INTERVAL
                try:
                    regions = aq_api.get_regions()
                    for region_name, rd in regions.items():
                        region = Region(region=rd.region, latitude=rd.latitude, longitude=rd.longitude)
                        _send_region_amqp(aq_producer, region, region_name, region_name, "info")
                except Exception as exc:  # pragma: no cover - runtime safety
                    logger.error("Error refreshing regions: %s", exc)

            if now >= next_aq_poll:
                did_aq = True
                next_aq_poll = now + aq_polling_interval
                try:
                    psi_readings = fetch_psi_readings(aq_api, psi_state)
                    for psi_data in psi_readings:
                        psi_obj = PSIReading(
                            region=psi_data.region, timestamp=psi_data.timestamp,
                            update_timestamp=psi_data.update_timestamp,
                            psi_twenty_four_hourly=psi_data.psi_twenty_four_hourly,
                            o3_sub_index=psi_data.o3_sub_index,
                            pm10_sub_index=psi_data.pm10_sub_index,
                            pm10_twenty_four_hourly=psi_data.pm10_twenty_four_hourly,
                            pm25_sub_index=psi_data.pm25_sub_index,
                            pm25_twenty_four_hourly=psi_data.pm25_twenty_four_hourly,
                            co_sub_index=psi_data.co_sub_index,
                            co_eight_hour_max=psi_data.co_eight_hour_max,
                            so2_sub_index=psi_data.so2_sub_index,
                            so2_twenty_four_hourly=psi_data.so2_twenty_four_hourly,
                            no2_one_hour_max=psi_data.no2_one_hour_max,
                            o3_eight_hour_max=psi_data.o3_eight_hour_max,
                        )
                        _send_psireading_amqp(
                            aq_producer, psi_obj, psi_data.region, psi_data.region, "psi", psi_data.timestamp
                        )
                    pm25_readings = fetch_pm25_readings(aq_api, pm25_state)
                    for pm25_data in pm25_readings:
                        pm25_obj = PM25Reading(
                            region=pm25_data.region, timestamp=pm25_data.timestamp,
                            update_timestamp=pm25_data.update_timestamp,
                            pm25_one_hourly=pm25_data.pm25_one_hourly,
                        )
                        aq_producer.send_amqp(
                            data=pm25_obj, _region=pm25_data.region,
                            _station_id=pm25_data.region, _event="pm25", _time=pm25_data.timestamp,
                        )
                    logger.info(
                        "Sent %d PSI and %d PM2.5 readings via AMQP",
                        len(psi_readings), len(pm25_readings),
                    )
                    state_changed = True
                except Exception as exc:  # pragma: no cover - runtime safety
                    logger.error("Error fetching/sending air quality: %s", exc)

            if state_changed:
                save_state(args.state_file, compose_state(weather_state, psi_state, pm25_state))

            if args.once and did_weather and did_aq:
                logger.info("--once mode: exiting after first polling cycle")
                break
    finally:
        for p in [weather_producer, aq_producer]:
            close = getattr(p, "close", None)
            if close:
                close()


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
    parser.add_argument("--sample-mode", action="store_true", default=_env_bool(f"{ENV_PREFIX}_MOCK", False) or _env_bool(f"{ENV_PREFIX}_SAMPLE_MODE", False) or _env_bool(f"{ENV_PREFIX}_AMQP_SAMPLE", False))
    parser.add_argument("--feeds", default=os.getenv("PTWC_TSUNAMI_FEEDS", "PAAQ,PHEB"))
    parser.add_argument("--providers", default=os.getenv("NINA_BBK_PROVIDERS", "mowas,katwarn,biwapp,dwd,lhp,police"))
    parser.add_argument("--regions", default=os.getenv("EAWS_ALBINA_REGIONS", "AT-07-01"))
    parser.add_argument("--lang", default=os.getenv("EAWS_ALBINA_LANG", "en"))
    parser.add_argument("--resources", default=os.getenv("AUTOBAHN_RESOURCES", "all"))
    parser.add_argument("--roads", default=os.getenv("AUTOBAHN_ROADS", ""))
    parser.add_argument("--request-concurrency", type=int, default=int(os.getenv("AUTOBAHN_REQUEST_CONCURRENCY", "8")))
    parser.add_argument("--station-filter", default=os.getenv("STATION_FILTER", ""))
    parser.add_argument("--max-size", type=int, default=int(os.getenv("MAX_SIZE", "1000")))
    return parser


def _retry_producer_build(factory, max_attempts=5, initial_delay=10):
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
    if args.sample_mode:
        # Sample path: build both producers, send one event of each type, then close.
        weather_producer, aq_producer = await asyncio.get_running_loop().run_in_executor(
            None, lambda: _retry_producer_build(lambda: _build_both_producers(args))
        )
        try:
            sent = _emit_sample_events(weather_producer, aq_producer)
            logger.info("Published %d sample AMQP event(s)", sent)
        finally:
            for p in [weather_producer, aq_producer]:
                close = getattr(p, "close", None)
                if close:
                    close()
    else:
        # Live path: two producers (weather + air quality) with real NEA data.
        await _run_live(args)


def main() -> None:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    parser = _add_common_args(argparse.ArgumentParser(description=f"{SOURCE_ID} AMQP 1.0 bridge"))
    args = parser.parse_args()
    if args.feed_command != "feed":
        parser.error("only the 'feed' command is supported")
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
