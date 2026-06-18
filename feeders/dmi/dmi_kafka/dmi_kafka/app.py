"""Kafka feeder application for the DMI observation triad.

Polls the three DMI Open Data v2 products (metObs, oceanObs, lightning) and
multiplexes every CloudEvent onto a single Kafka topic ``dmi``. Reference
events (Station / OceanStation / TidewaterStation / LightningSensor) are
emitted at startup and re-emitted on a slow refresh cadence; telemetry events
(MetObsObservation / OceanObservation / TidewaterPrediction / LightningStrike)
are emitted on every polling cycle, with dedupe based on the upstream
``observed`` timestamp.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from confluent_kafka import Producer

from dmi_core import (
    DmiApiKeys,
    DmiLightningAPI,
    DmiMetObsAPI,
    DmiOceanObsAPI,
    LIGHTNING_FEED_ROOT,
    METOBS_FEED_ROOT,
    OCEANOBS_FEED_ROOT,
    build_kafka_config,
    load_state,
    parse_kafka_connection_string,
    save_state,
)
from dmi_producer_data import (
    LightningSensor,
    LightningStrike,
    MetObsObservation,
    MetObsStation,
    OceanObservation,
    OceanStation,
    TidewaterPrediction,
    TidewaterStation,
)
from dmi_producer_kafka_producer.producer import (
    DkDmiLightningKafkaEventProducer,
    DkDmiMetObsKafkaEventProducer,
    DkDmiOceanObsKafkaEventProducer,
)

logger = logging.getLogger(__name__)

# Reference data is slowly-changing; re-emit every six hours.
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


def _emit_reference(
    api_keys: DmiApiKeys,
    met_producer: DkDmiMetObsKafkaEventProducer,
    ocean_producer: DkDmiOceanObsKafkaEventProducer,
    lightning_producer: DkDmiLightningKafkaEventProducer,
    *,
    met_api: Optional[DmiMetObsAPI],
    ocean_api: Optional[DmiOceanObsAPI],
    lightning_api: Optional[DmiLightningAPI],
    kafka_producer: Producer,
) -> int:
    count = 0
    if met_api is not None:
        for station in met_api.list_stations():
            station_id = str(station.get("stationId") or station.get("id") or "")
            if not station_id:
                continue
            met_producer.send_dk_dmi_met_obs_kafka_station(
                _feedurl=f"{METOBS_FEED_ROOT}/collections/station/items/{station_id}",
                _station_id=station_id,
                data=_build_met_station(station),
                flush_producer=False,
            )
            count += 1
    if ocean_api is not None:
        for station in ocean_api.list_stations():
            station_id = str(station.get("stationId") or station.get("id") or "")
            if not station_id:
                continue
            ocean_producer.send_dk_dmi_ocean_obs_kafka_station(
                _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/station/items/{station_id}",
                _station_id=station_id,
                data=_build_ocean_station(station),
                flush_producer=False,
            )
            count += 1
        for station in ocean_api.list_tidewater_stations():
            station_id = str(station.get("stationId") or station.get("id") or "")
            if not station_id:
                continue
            ocean_producer.send_dk_dmi_ocean_obs_kafka_tidewater_station(
                _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/tidewaterstation/items/{station_id}",
                _station_id=station_id,
                data=_build_tidewater_station(station),
                flush_producer=False,
            )
            count += 1
    if lightning_api is not None:
        for sensor in lightning_api.list_sensors():
            sensor_id = str(sensor.get("sensorId") or sensor.get("id") or "")
            if not sensor_id:
                continue
            lightning_producer.send_dk_dmi_lightning_kafka_sensor(
                _feedurl=f"{LIGHTNING_FEED_ROOT}/collections/sensor/items/{sensor_id}",
                _sensor_id=sensor_id,
                data=_build_lightning_sensor(sensor),
                flush_producer=False,
            )
            count += 1
    kafka_producer.flush()
    return count


async def feed(
    api_keys: DmiApiKeys,
    kafka_config: Dict[str, str],
    kafka_topic: str,
    polling_interval: int,
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

    kafka_producer = Producer(kafka_config)
    met_producer = DkDmiMetObsKafkaEventProducer(kafka_producer, kafka_topic)
    ocean_producer = DkDmiOceanObsKafkaEventProducer(kafka_producer, kafka_topic)
    lightning_producer = DkDmiLightningKafkaEventProducer(kafka_producer, kafka_topic)

    logger.info(
        "DMI Kafka feeder starting (topic=%s, bootstrap=%s, families=%s)",
        kafka_topic,
        kafka_config.get("bootstrap.servers"),
        ",".join(
            n
            for n, present in (
                ("metObs", met_api is not None),
                ("oceanObs", ocean_api is not None),
                ("lightning", lightning_api is not None),
            )
            if present
        ),
    )

    ref_count = _emit_reference(
        api_keys, met_producer, ocean_producer, lightning_producer,
        met_api=met_api, ocean_api=ocean_api, lightning_api=lightning_api,
        kafka_producer=kafka_producer,
    )
    logger.info("Reference data emitted: %d events", ref_count)
    last_reference_refresh = time.monotonic()

    period = os.getenv("DMI_OBSERVATION_PERIOD", "latest-hour")

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
                    met_producer.send_dk_dmi_met_obs_kafka_observation(
                        _feedurl=f"{METOBS_FEED_ROOT}/collections/observation/items?stationId={sid}&parameterId={pid}",
                        _station_id=sid,
                        _parameter_id=pid,
                        data=_build_met_observation(obs),
                        flush_producer=False,
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
                    ocean_producer.send_dk_dmi_ocean_obs_kafka_observation(
                        _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/observation/items?stationId={sid}&parameterId={pid}",
                        _station_id=sid,
                        _parameter_id=pid,
                        data=_build_ocean_observation(obs),
                        flush_producer=False,
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
                    ocean_producer.send_dk_dmi_ocean_obs_kafka_tidewater_prediction(
                        _feedurl=f"{OCEANOBS_FEED_ROOT}/collections/tidewater/items?stationId={sid}",
                        _station_id=sid,
                        data=_build_tidewater_prediction(pred),
                        flush_producer=False,
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
                    lightning_producer.send_dk_dmi_lightning_kafka_strike(
                        _feedurl=f"{LIGHTNING_FEED_ROOT}/collections/observation/items/{strike_id}",
                        _strike_id=strike_id,
                        data=_build_lightning_strike(strike),
                        flush_producer=False,
                    )
                    telemetry_count += 1
                last_strike_observed["max_observed"] = new_max
            kafka_producer.flush()
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
                    api_keys, met_producer, ocean_producer, lightning_producer,
                    met_api=met_api, ocean_api=ocean_api, lightning_api=lightning_api,
                    kafka_producer=kafka_producer,
                )
                logger.info("Reference data refreshed: %d events", ref_count)
                last_reference_refresh = time.monotonic()
            if effective > 0:
                await asyncio.sleep(effective)
        except KeyboardInterrupt:
            logger.info("Exiting on keyboard interrupt")
            break
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("DMI polling cycle failed: %s", exc)
            await asyncio.sleep(polling_interval)
    kafka_producer.flush()


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="DMI observation triad → Apache Kafka bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed DMI observations as CloudEvents to Kafka")
    feed_parser.add_argument("--kafka-bootstrap-servers", type=str,
                             default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    feed_parser.add_argument("--kafka-topic", type=str,
                             default=os.getenv("KAFKA_TOPIC", "dmi"))
    feed_parser.add_argument("--sasl-username", type=str, default=os.getenv("SASL_USERNAME"))
    feed_parser.add_argument("--sasl-password", type=str, default=os.getenv("SASL_PASSWORD"))
    feed_parser.add_argument("-c", "--connection-string", type=str,
                             default=os.getenv("CONNECTION_STRING"))
    feed_parser.add_argument("--metobs-api-key", type=str, default=None)
    feed_parser.add_argument("--oceanobs-api-key", type=str, default=None)
    feed_parser.add_argument("--lightning-api-key", type=str, default=None)
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "300")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.dmi_state.json")))
    feed_parser.add_argument("--once", action="store_true",
                             default=os.getenv("ONCE_MODE", "").lower() in ("1", "true", "yes"))
    return parser


def main(argv: Optional[list] = None) -> None:
    logging.basicConfig(level=logging.DEBUG if sys.gettrace() else logging.INFO)
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    if args.command != "feed":
        parser.print_help()
        return

    if args.connection_string:
        cfg = parse_kafka_connection_string(args.connection_string)
        bootstrap = cfg.get("bootstrap.servers")
        topic = cfg.get("kafka_topic") or args.kafka_topic
        user = cfg.get("sasl.username")
        pwd = cfg.get("sasl.password")
    else:
        bootstrap = args.kafka_bootstrap_servers
        topic = args.kafka_topic
        user = args.sasl_username
        pwd = args.sasl_password

    if not bootstrap:
        print("Error: Kafka bootstrap servers must be provided via CLI or connection string.")
        sys.exit(1)
    if not topic:
        print("Error: Kafka topic must be provided via CLI or connection string.")
        sys.exit(1)

    tls_enabled = os.getenv("KAFKA_ENABLE_TLS", "true").lower() not in ("false", "0", "no")
    kafka_config = build_kafka_config(
        bootstrap_servers=bootstrap,
        sasl_username=user,
        sasl_password=pwd,
        tls_enabled=tls_enabled,
    )

    api_keys = DmiApiKeys.from_env(
        met_obs=args.metobs_api_key,
        ocean_obs=args.oceanobs_api_key,
        lightning=args.lightning_api_key,
    )

    asyncio.run(
        feed(
            api_keys,
            kafka_config,
            topic,
            args.polling_interval,
            args.state_file,
            args.once,
        )
    )


if __name__ == "__main__":
    main()
