"""AMQP 1.0 feeder application for the DMI observation triad.

Polls the DMI metObs, oceanObs, and lightning REST APIs and publishes their
reference and telemetry events as binary-mode AMQP 1.0 messages. Supports
generic AMQP brokers via SASL PLAIN and Azure Service Bus / Event Hubs via
Entra ID with AMQP CBS.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from dmi_core import (
    DmiApiKeys,
    DmiLightningAPI,
    DmiMetObsAPI,
    DmiOceanObsAPI,
    LIGHTNING_FEED_ROOT,
    METOBS_FEED_ROOT,
    OCEANOBS_FEED_ROOT,
    load_state,
    save_state,
)
from dmi_amqp_producer_data import (
    LightningSensor,
    LightningStrike,
    MetObsObservation,
    MetObsStation,
    OceanObservation,
    OceanStation,
    TidewaterPrediction,
    TidewaterStation,
)
from dmi_amqp_producer_amqp_producer.producer import (
    DkDmiLightningAmqpProducer,
    DkDmiMetObsAmqpProducer,
    DkDmiOceanObsAmqpProducer,
)

DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"

logger = logging.getLogger(__name__)

_REFERENCE_REFRESH_SECONDS = 6 * 3600


def _opt_float(value: Any) -> Optional[float]:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _opt_str(value: Any) -> Optional[str]:
    return None if value is None else str(value)


def _build_met_station(raw: Dict[str, Any]) -> MetObsStation:
    return MetObsStation(
        station_id=str(raw.get("stationId") or raw.get("id") or ""),
        wmo_station_id=_opt_str(raw.get("wmoStationId")),
        wmo_country_code=_opt_str(raw.get("wmoCountryCode")),
        name=str(raw.get("name") or ""),
        country=str(raw.get("country") or ""),
        owner=_opt_str(raw.get("owner")),
        region_id=_opt_str(raw.get("regionId")),
        type=_opt_str(raw.get("type")),
        status=_opt_str(raw.get("status")),
        parameter_id=list(raw.get("parameterId") or []) or None,
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        station_height=_opt_float(raw.get("stationHeight")),
        barometer_height=_opt_float(raw.get("barometerHeight")),
        anemometer_height=_opt_float(raw.get("anemometerHeight")),
        valid_from=_opt_str(raw.get("validFrom")),
        valid_to=_opt_str(raw.get("validTo")),
        operation_from=_opt_str(raw.get("operationFrom")),
        operation_to=_opt_str(raw.get("operationTo")),
        created=_opt_str(raw.get("created")),
        updated=_opt_str(raw.get("updated")),
    )


def _build_met_observation(raw: Dict[str, Any]) -> MetObsObservation:
    return MetObsObservation(
        observation_id=_opt_str(raw.get("id") or raw.get("observationId")),
        station_id=str(raw.get("stationId") or ""),
        parameter_id=str(raw.get("parameterId") or ""),
        observed=str(raw.get("observed") or ""),
        value=float(raw.get("value") or 0.0),
        latitude=_opt_float(raw.get("latitude")),
        longitude=_opt_float(raw.get("longitude")),
    )


def _build_ocean_station(raw: Dict[str, Any]) -> OceanStation:
    return OceanStation(
        station_id=str(raw.get("stationId") or raw.get("id") or ""),
        name=str(raw.get("name") or ""),
        country=str(raw.get("country") or ""),
        owner=_opt_str(raw.get("owner")),
        type=_opt_str(raw.get("type")),
        status=_opt_str(raw.get("status")),
        parameter_id=list(raw.get("parameterId") or []) or None,
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        valid_from=_opt_str(raw.get("validFrom")),
        valid_to=_opt_str(raw.get("validTo")),
        operation_from=_opt_str(raw.get("operationFrom")),
        operation_to=_opt_str(raw.get("operationTo")),
        created=_opt_str(raw.get("created")),
        updated=_opt_str(raw.get("updated")),
    )


def _build_tidewater_station(raw: Dict[str, Any]) -> TidewaterStation:
    return TidewaterStation(
        station_id=str(raw.get("stationId") or raw.get("id") or ""),
        name=str(raw.get("name") or ""),
        country=str(raw.get("country") or ""),
        owner=_opt_str(raw.get("owner")),
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        valid_from=_opt_str(raw.get("validFrom")),
        valid_to=_opt_str(raw.get("validTo")),
    )


def _build_ocean_observation(raw: Dict[str, Any]) -> OceanObservation:
    return OceanObservation(
        observation_id=_opt_str(raw.get("id") or raw.get("observationId")),
        station_id=str(raw.get("stationId") or ""),
        parameter_id=str(raw.get("parameterId") or ""),
        observed=str(raw.get("observed") or ""),
        value=float(raw.get("value") or 0.0),
        latitude=_opt_float(raw.get("latitude")),
        longitude=_opt_float(raw.get("longitude")),
    )


def _build_tidewater_prediction(raw: Dict[str, Any]) -> TidewaterPrediction:
    return TidewaterPrediction(
        prediction_id=_opt_str(raw.get("id") or raw.get("predictionId")),
        station_id=str(raw.get("stationId") or ""),
        prediction_type=_opt_str(raw.get("predictionType")),
        prediction_time=str(raw.get("predictionTime") or raw.get("observed") or ""),
        value=float(raw.get("value") or 0.0),
        latitude=_opt_float(raw.get("latitude")),
        longitude=_opt_float(raw.get("longitude")),
    )


def _build_lightning_sensor(raw: Dict[str, Any]) -> LightningSensor:
    return LightningSensor(
        sensor_id=str(raw.get("sensorId") or raw.get("id") or ""),
        name=str(raw.get("name") or ""),
        owner=_opt_str(raw.get("owner")),
        country=str(raw.get("country") or ""),
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
        active_from=_opt_str(raw.get("activeFrom")),
        active_to=_opt_str(raw.get("activeTo")),
    )


def _build_lightning_strike(raw: Dict[str, Any]) -> LightningStrike:
    sensors_raw = raw.get("sensors")
    if sensors_raw is None:
        sensors_value: Optional[str] = None
    elif isinstance(sensors_raw, (list, tuple)):
        sensors_value = ",".join(str(s) for s in sensors_raw)
    else:
        sensors_value = str(sensors_raw)
    return LightningStrike(
        strike_id=str(raw.get("id") or ""),
        observed=str(raw.get("observed") or ""),
        created=_opt_str(raw.get("created")),
        type=int(raw.get("type") or 0),
        amp=float(raw.get("amp") or 0.0),
        strokes=int(raw.get("strokes") or 0),
        sensors=sensors_value,
        latitude=float(raw.get("latitude") or 0.0),
        longitude=float(raw.get("longitude") or 0.0),
    )


def _retry_producer_init(factory, max_attempts=5, initial_delay=10):
    """Retry producer construction with exponential backoff for CBS/RBAC propagation."""
    for attempt in range(max_attempts):
        try:
            return factory()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            delay = initial_delay * (2 ** attempt)
            logging.warning("Producer init attempt %d/%d failed: %s. Retrying in %ds...",
                          attempt + 1, max_attempts, e, delay)
            import time; time.sleep(delay)
def _build_producer_kwargs(
    *,
    host: str,
    port: int,
    address: str,
    use_tls: bool,
    content_mode: str,
    auth_mode: str,
    username: Optional[str],
    password: Optional[str],
    entra_audience: str,
    entra_client_id: Optional[str],
) -> Dict[str, Any]:
    kwargs: Dict[str, Any] = {
        "host": host,
        "address": address,
        "port": port,
        "content_mode": content_mode,
        "use_tls": use_tls,
    }
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential

        credential = (
            ManagedIdentityCredential(client_id=entra_client_id)
            if entra_client_id
            else DefaultAzureCredential()
        )
        kwargs["credential"] = credential
        kwargs["entra_audience"] = entra_audience
    else:
        kwargs["username"] = username
        kwargs["password"] = password
    return kwargs


def _emit_reference(
    met_producer: DkDmiMetObsAmqpProducer,
    ocean_producer: DkDmiOceanObsAmqpProducer,
    lightning_producer: DkDmiLightningAmqpProducer,
    *,
    met_api: Optional[DmiMetObsAPI],
    ocean_api: Optional[DmiOceanObsAPI],
    lightning_api: Optional[DmiLightningAPI],
) -> int:
    count = 0
    if met_api is not None:
        for station in met_api.list_stations():
            station_id = str(station.get("stationId") or station.get("id") or "")
            if not station_id:
                continue
            met_producer.send_station(
                _feedurl=f"{METOBS_FEED_ROOT}/collections/station/items/{station_id}",
                _station_id=station_id,
                data=_build_met_station(station),
            )
            count += 1
    if ocean_api is not None:
        for station in ocean_api.list_stations():
            station_id = str(station.get("stationId") or station.get("id") or "")
            if not station_id:
                continue
            ocean_producer.send_station(
                _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/station/items/{station_id}",
                _station_id=station_id,
                data=_build_ocean_station(station),
            )
            count += 1
        for station in ocean_api.list_tidewater_stations():
            station_id = str(station.get("stationId") or station.get("id") or "")
            if not station_id:
                continue
            ocean_producer.send_tidewater_station(
                _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/tidewaterstation/items/{station_id}",
                _station_id=station_id,
                data=_build_tidewater_station(station),
            )
            count += 1
    if lightning_api is not None:
        for sensor in lightning_api.list_sensors():
            sensor_id = str(sensor.get("sensorId") or sensor.get("id") or "")
            if not sensor_id:
                continue
            lightning_producer.send_sensor(
                _feedurl=f"{LIGHTNING_FEED_ROOT}/collections/sensor/items/{sensor_id}",
                _sensor_id=sensor_id,
                data=_build_lightning_sensor(sensor),
            )
            count += 1
    return count


def _close_producers(*producers: Any) -> None:
    for producer in producers:
        try:
            producer.close()
        except Exception:  # pylint: disable=broad-except
            pass


def feed(
    api_keys: DmiApiKeys,
    met_producer: DkDmiMetObsAmqpProducer,
    ocean_producer: DkDmiOceanObsAmqpProducer,
    lightning_producer: DkDmiLightningAmqpProducer,
    polling_interval: int,
    *,
    state_file: str = "",
    once: bool = False,
) -> None:
    state = load_state(state_file)
    seen_met: Dict[str, str] = state.setdefault("metObs_latest", {})
    seen_ocean: Dict[str, str] = state.setdefault("oceanObs_latest", {})
    seen_tide: Dict[str, str] = state.setdefault("tidewater_latest", {})
    last_strike_observed: Dict[str, str] = state.setdefault("lightning_latest", {})

    met_api = DmiMetObsAPI(api_keys.met_obs)
    ocean_api = DmiOceanObsAPI(api_keys.ocean_obs)
    lightning_api = DmiLightningAPI(api_keys.lightning)

    logger.info(
        "DMI AMQP feeder starting (families=%s)",
        ",".join(
            name
            for name, present in (
                ("metObs", met_api is not None),
                ("oceanObs", ocean_api is not None),
                ("lightning", lightning_api is not None),
            )
            if present
        ),
    )

    ref_count = _emit_reference(
        met_producer,
        ocean_producer,
        lightning_producer,
        met_api=met_api,
        ocean_api=ocean_api,
        lightning_api=lightning_api,
    )
    logger.info("Reference data emitted: %d events", ref_count)
    last_reference_refresh = time.monotonic()

    period = os.getenv("DMI_OBSERVATION_PERIOD", "latest-hour")

    try:
        while True:
            try:
                cycle_start = datetime.now(timezone.utc)
                telemetry_count = 0
                if met_api is not None:
                    for obs in met_api.iter_observations(period=period):
                        sid = str(obs.get("stationId") or "")
                        pid = str(obs.get("parameterId") or "")
                        observed = str(obs.get("observed") or "")
                        if not sid or not pid or not observed:
                            continue
                        key = f"{sid}|{pid}"
                        if seen_met.get(key) == observed:
                            continue
                        seen_met[key] = observed
                        met_producer.send_observation(
                            _feedurl=f"{METOBS_FEED_ROOT}/collections/observation/items?stationId={sid}&parameterId={pid}",
                            _station_id=sid,
                            _parameter_id=pid,
                            data=_build_met_observation(obs),
                        )
                        telemetry_count += 1
                if ocean_api is not None:
                    for obs in ocean_api.iter_observations(period=period):
                        sid = str(obs.get("stationId") or "")
                        pid = str(obs.get("parameterId") or "")
                        observed = str(obs.get("observed") or "")
                        if not sid or not pid or not observed:
                            continue
                        key = f"{sid}|{pid}"
                        if seen_ocean.get(key) == observed:
                            continue
                        seen_ocean[key] = observed
                        ocean_producer.send_observation(
                            _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/observation/items?stationId={sid}&parameterId={pid}",
                            _station_id=sid,
                            _parameter_id=pid,
                            data=_build_ocean_observation(obs),
                        )
                        telemetry_count += 1
                    for pred in ocean_api.iter_tidewater(period=period):
                        sid = str(pred.get("stationId") or "")
                        when = str(pred.get("predictionTime") or pred.get("observed") or "")
                        if not sid or not when:
                            continue
                        if seen_tide.get(sid) == when:
                            continue
                        seen_tide[sid] = when
                        ocean_producer.send_tidewater_prediction(
                            _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/tidewater/items?stationId={sid}",
                            _station_id=sid,
                            data=_build_tidewater_prediction(pred),
                        )
                        telemetry_count += 1
                if lightning_api is not None:
                    last_seen = last_strike_observed.get("max_observed", "")
                    new_max = last_seen
                    for strike in lightning_api.iter_strikes(period=period):
                        strike_id = str(strike.get("id") or "")
                        observed = str(strike.get("observed") or "")
                        if not strike_id or not observed:
                            continue
                        if last_seen and observed <= last_seen:
                            continue
                        if observed > new_max:
                            new_max = observed
                        lightning_producer.send_strike(
                            _feedurl=f"{LIGHTNING_FEED_ROOT}/collections/observation/items/{strike_id}",
                            _strike_id=strike_id,
                            data=_build_lightning_strike(strike),
                        )
                        telemetry_count += 1
                    last_strike_observed["max_observed"] = new_max
                cycle_end = datetime.now(timezone.utc)
                elapsed = (cycle_end - cycle_start).total_seconds()
                effective = max(0.0, polling_interval - elapsed)
                logger.info(
                    "Sent %d telemetry events in %.2fs; sleeping until %s",
                    telemetry_count,
                    elapsed,
                    (datetime.now(timezone.utc) + timedelta(seconds=effective)).isoformat(),
                )
                save_state(state_file, state)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if time.monotonic() - last_reference_refresh >= _REFERENCE_REFRESH_SECONDS:
                    ref_count = _emit_reference(
                        met_producer,
                        ocean_producer,
                        lightning_producer,
                        met_api=met_api,
                        ocean_api=ocean_api,
                        lightning_api=lightning_api,
                    )
                    logger.info("Reference data refreshed: %d events", ref_count)
                    last_reference_refresh = time.monotonic()
                if effective > 0:
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting on keyboard interrupt")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("DMI polling cycle failed: %s", exc)
                time.sleep(polling_interval)
    finally:
        _close_producers(met_producer, ocean_producer, lightning_producer)


def _parse_broker_url(url: str) -> tuple[str, int, bool, Optional[str], Optional[str], Optional[str]]:
    parsed = urlparse(url if "://" in url else f"amqp://{url}")
    scheme = (parsed.scheme or "amqp").lower()
    tls = scheme in ("amqps", "ssl", "tls")
    port = parsed.port or (5671 if tls else 5672)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    path = (parsed.path or "").lstrip("/") or None
    return host, port, tls, user, pwd, path


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DMI observation triad → AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed DMI observations as AMQP 1.0 messages")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--port", type=int, default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "dmi"))
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true", default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("AMQP_CONTENT_MODE", "binary"), choices=["binary", "structured"])
    feed_parser.add_argument("--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra"])
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS), help=f"Entra token audience. Default: {DEFAULT_ENTRA_AUDIENCE_SERVICEBUS}. Use {DEFAULT_ENTRA_AUDIENCE_EVENTHUBS} for Event Hubs.")
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--metobs-api-key", type=str, default=None)
    feed_parser.add_argument("--oceanobs-api-key", type=str, default=None)
    feed_parser.add_argument("--lightning-api-key", type=str, default=None)
    feed_parser.add_argument("-i", "--polling-interval", type=int, default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--state-file", type=str, default=os.getenv("STATE_FILE", os.path.expanduser("~/.dmi_amqp_state.json")))
    feed_parser.add_argument("--once", action="store_true", default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

    address = args.address
    if args.broker_url:
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.port:
            port = args.port
        if args.tls:
            tls = True
        if path:
            address = path
    else:
        host = args.host or "localhost"
        tls = bool(args.tls) or args.auth_mode == "entra"
        port = args.port or (5671 if tls else 5672)
        username = args.username
        password = args.password

    if args.auth_mode == "entra":
        tls = True
        if not args.port:
            port = 5671

    if not address:
        parser.error("--address is required (or include it in --broker-url path)")

    api_keys = DmiApiKeys.from_env(
        met_obs=args.metobs_api_key,
        ocean_obs=args.oceanobs_api_key,
        lightning=args.lightning_api_key,
    )
    producer_kwargs = _build_producer_kwargs(
        host=host,
        port=port,
        address=address,
        use_tls=tls,
        content_mode=args.content_mode,
        auth_mode=args.auth_mode,
        username=username,
        password=password,
        entra_audience=args.entra_audience,
        entra_client_id=args.entra_client_id,
    )
    feed(
        api_keys,
        DkDmiMetObsAmqpProducer(**producer_kwargs),
        DkDmiOceanObsAmqpProducer(**producer_kwargs),
        DkDmiLightningAmqpProducer(**producer_kwargs),
        args.polling_interval,
        state_file=args.state_file,
        once=args.once,
    )


if __name__ == "__main__":
    main()
