"""MQTT feeder application for Wallonia ISSeP Air Quality → Unified Namespace.

Reuses the upstream HTTP client logic from the existing ``wallonia_issep``
Kafka bridge and pushes CloudEvents into MQTT 5.0 using the xrcg-generated
:class:`BeIssepAirqualitySensorsMqttMqttClient`.

Topic tree: ``air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/{info|observation}``.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion, MQTTv5

from wallonia_issep.wallonia_issep import WalloniaISsePAPI, _load_state, _save_state
from wallonia_issep_mqtt_producer_data import Observation, SensorConfiguration
from wallonia_issep_mqtt_producer_mqtt_client.client import BeIssepAirqualitySensorsMqttMqttClient

logger = logging.getLogger(__name__)


async def _publish_configurations(
    mqtt_client: BeIssepAirqualitySensorsMqttMqttClient,
    records: List[Dict[str, Any]],
) -> int:
    """Extract and publish sensor configuration reference events."""
    configs = WalloniaISsePAPI.extract_configurations(records)
    for config in configs:
        province = getattr(config, "province", None) or "unknown"
        data = SensorConfiguration(
            configuration_id=config.configuration_id,
            province=province,
        )
        await mqtt_client.publish_be_issep_airquality_sensors_mqtt_sensor_configuration(
            configuration_id=config.configuration_id,
            province=province,
            data=data,
        )
    logger.info("Published %d sensor configuration info events", len(configs))
    return len(configs)


def _build_observation_data(obs) -> Observation:
    """Build an MQTT Observation dataclass from a normalized upstream observation."""
    return Observation(
        configuration_id=obs.configuration_id,
        province=getattr(obs, "province", None) or "unknown",
        moment=obs.moment,
        co=obs.co,
        no=obs.no,
        no2=obs.no2,
        o3no2=obs.o3no2,
        ppbno=obs.ppbno,
        ppbno_statut=obs.ppbno_statut,
        ppbno2=obs.ppbno2,
        ppbno2_statut=obs.ppbno2_statut,
        ppbo3=obs.ppbo3,
        ppbo3_statut=obs.ppbo3_statut,
        ugpcmno=obs.ugpcmno,
        ugpcmno_statut=obs.ugpcmno_statut,
        ugpcmno2=obs.ugpcmno2,
        ugpcmno2_statut=obs.ugpcmno2_statut,
        ugpcmo3=obs.ugpcmo3,
        ugpcmo3_statut=obs.ugpcmo3_statut,
        bme_t=obs.bme_t,
        bme_t_statut=obs.bme_t_statut,
        bme_pres=obs.bme_pres,
        bme_pres_statut=obs.bme_pres_statut,
        bme_rh=obs.bme_rh,
        bme_rh_statut=obs.bme_rh_statut,
        pm1=obs.pm1,
        pm1_statut=obs.pm1_statut,
        pm25=obs.pm25,
        pm25_statut=obs.pm25_statut,
        pm4=obs.pm4,
        pm4_statut=obs.pm4_statut,
        pm10=obs.pm10,
        pm10_statut=obs.pm10_statut,
        vbat=obs.vbat,
        vbat_statut=obs.vbat_statut,
        mwh_bat=obs.mwh_bat,
        mwh_pv=obs.mwh_pv,
        co_rf=obs.co_rf,
        no_rf=obs.no_rf,
        no2_rf=obs.no2_rf,
        o3no2_rf=obs.o3no2_rf,
        o3_rf=obs.o3_rf,
        pm10_rf=obs.pm10_rf,
    )


async def _publish_observations(
    api: WalloniaISsePAPI,
    mqtt_client: BeIssepAirqualitySensorsMqttMqttClient,
    state: Dict[str, str],
) -> tuple:
    """Poll and publish new observation events."""
    all_records = api.fetch_all_records()
    new_records = api.filter_new_records(all_records, state)
    count = 0
    for record in new_records:
        try:
            obs = api.normalize_observation(record)
            data = _build_observation_data(obs)
            await mqtt_client.publish_be_issep_airquality_sensors_mqtt_observation(
                configuration_id=obs.configuration_id,
                province=getattr(obs, "province", None) or "unknown",
                data=data,
            )
            count += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning(
                "Could not publish observation for config %s: %s",
                record.get("id_configuration"),
                exc,
            )
    return count, all_records


async def feed(
    api: WalloniaISsePAPI,
    broker_host: str,
    broker_port: int,
    polling_interval: int,
    *,
    username: Optional[str] = None,
    password: Optional[str] = None,
    tls: bool = False,
    client_id: Optional[str] = None,
    state_file: str = "",
    once: bool = False,
    content_mode: str = "binary",
) -> None:
    """Run the MQTT feed loop."""
    state = _load_state(state_file)

    paho_client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id or "",
        protocol=MQTTv5,
    )
    if username:
        paho_client.username_pw_set(username, password or "")
    if tls:
        paho_client.tls_set()

    loop = asyncio.get_running_loop()
    mqtt_client = BeIssepAirqualitySensorsMqttMqttClient(
        client=paho_client,
        content_mode=content_mode,  # type: ignore[arg-type]
        loop=loop,
    )

    logger.info("Connecting to MQTT broker %s:%s (tls=%s)", broker_host, broker_port, tls)
    await mqtt_client.connect(broker_host, broker_port)

    # Initial full fetch: publish both reference data and observations
    all_records = api.fetch_all_records()
    logger.info("Publishing sensor configuration info events under air-quality/be/issep/wallonia-issep/...")
    await _publish_configurations(mqtt_client, all_records)

    # Publish observations from the initial batch (treats all as new)
    new_records = api.filter_new_records(all_records, state)
    init_count = 0
    for record in new_records:
        try:
            obs = api.normalize_observation(record)
            data = _build_observation_data(obs)
            await mqtt_client.publish_be_issep_airquality_sensors_mqtt_observation(
                configuration_id=obs.configuration_id,
                province=getattr(obs, "province", None) or "unknown",
                data=data,
            )
            init_count += 1
        except Exception as exc:  # pylint: disable=broad-except
            logger.warning("Could not publish initial observation for config %s: %s",
                           record.get("id_configuration"), exc)
    logger.info("Published %d initial observations", init_count)
    _save_state(state_file, state)

    if once:
        logger.info("--once mode: exiting after initial cycle")
        await mqtt_client.disconnect()
        return

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count, _ = await _publish_observations(api, mqtt_client, state)
                end_time = datetime.now(timezone.utc)
                effective = max(0, polling_interval - (end_time - start_time).total_seconds())
                logger.info(
                    "Published %d observations in %.1fs. Sleeping %.1fs.",
                    count,
                    (end_time - start_time).total_seconds(),
                    effective,
                )
                _save_state(state_file, state)
                if once:
                    logger.info("--once mode: exiting after first polling cycle")
                    break
                if effective > 0:
                    await asyncio.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                await asyncio.sleep(polling_interval)
    finally:
        await mqtt_client.disconnect()


def _parse_broker_url(url: str) -> tuple:
    parsed = urlparse(url if "://" in url else f"mqtt://{url}")
    scheme = (parsed.scheme or "mqtt").lower()
    tls = scheme in ("mqtts", "ssl", "tls")
    port = parsed.port or (8883 if tls else 1883)
    host = parsed.hostname or "localhost"
    user = parsed.username or None
    pwd = parsed.password or None
    return host, port, tls, user, pwd


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Wallonia ISSeP air quality → MQTT/UNS bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed sensor data as CloudEvents to MQTT")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("MQTT_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("MQTT_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("MQTT_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("MQTT_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("MQTT_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("MQTT_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("MQTT_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("MQTT_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.wallonia_issep_mqtt_state.json")))
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

    if args.broker_url:
        host, port, tls, user, pwd = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (8883 if tls else 1883)
        username = args.username
        password = args.password

    api = WalloniaISsePAPI()
    asyncio.run(
        feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
        )
    )


if __name__ == "__main__":
    main()
