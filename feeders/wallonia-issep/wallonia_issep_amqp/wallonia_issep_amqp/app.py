"""AMQP feeder application for Wallonia ISSeP Air Quality → Unified Namespace.

Reuses the upstream HTTP client logic from the existing ``wallonia_issep``
Kafka bridge and pushes CloudEvents into AMQP 1.0 using the xrcg-generated
:class:`BeIssepAirqualitySensorsAmqpProducer`.

Topic tree: ``air-quality/be/issep/wallonia-issep/{province}/{configuration_id}/{info|observation}``.
"""

from __future__ import annotations

import argparse
import time
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from wallonia_issep.wallonia_issep import WalloniaISsePAPI, _load_state, _save_state
from wallonia_issep_amqp_producer_data import Observation, SensorConfiguration
from wallonia_issep_amqp_producer_amqp_producer.producer import BeIssepAirqualitySensorsAmqpProducer

logger = logging.getLogger(__name__)


def _publish_configurations(
    producer: BeIssepAirqualitySensorsAmqpProducer,
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
        producer.send_sensor_configuration(
            _configuration_id=config.configuration_id,
            _province=province,
            data=data,
        )
    logger.info("Published %d sensor configuration info events", len(configs))
    return len(configs)


def _build_observation_data(obs) -> Observation:
    """Build an AMQP Observation dataclass from a normalized upstream observation."""
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


def _publish_observations(
    api: WalloniaISsePAPI,
    producer: BeIssepAirqualitySensorsAmqpProducer,
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
            producer.send_observation(
                _configuration_id=obs.configuration_id,
                _province=getattr(obs, "province", None) or "unknown",
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


def _publish_mock(producer: BeIssepAirqualitySensorsAmqpProducer) -> None:
    config = SensorConfiguration(configuration_id="12345", province="mock-province")
    observation = Observation(configuration_id="12345", province="mock-province", moment=datetime.now(timezone.utc).isoformat(), co=1, no=1, no2=1, o3no2=1, ppbno=1.0, ppbno_statut=0, ppbno2=1.0, ppbno2_statut=0, ppbo3=1.0, ppbo3_statut=0, ugpcmno=1.0, ugpcmno_statut=0, ugpcmno2=1.0, ugpcmno2_statut=0, ugpcmo3=1.0, ugpcmo3_statut=0, bme_t=20.0, bme_t_statut=0, bme_pres=1013, bme_pres_statut=0, bme_rh=50.0, bme_rh_statut=0, pm1=1.0, pm1_statut=0, pm25=1.0, pm25_statut=0, pm4=1.0, pm4_statut=0, pm10=1.0, pm10_statut=0, vbat=4.0, vbat_statut=0, mwh_bat=0.0, mwh_pv=0.0, co_rf=1.0, no_rf=1.0, no2_rf=1.0, o3no2_rf=1.0, o3_rf=1.0, pm10_rf=1.0)
    producer.send_sensor_configuration(data=config, _configuration_id="12345", _province="mock-province")
    producer.send_observation(data=observation, _configuration_id="12345", _province="mock-province")


def feed(
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
    address: str = "wallonia-issep",
    auth_mode: str = "password",
    entra_audience: str = "https://servicebus.azure.net/.default",
    entra_client_id: Optional[str] = None,
    sas_key_name: Optional[str] = None,
    sas_key: Optional[str] = None,
) -> None:
    """Run the AMQP feed loop."""
    state = _load_state(state_file)
    producer = _retry_producer_init(lambda: _build_producer(host=broker_host, port=broker_port, address=address, use_tls=tls, content_mode=content_mode, auth_mode=auth_mode, username=username, password=password, entra_audience=entra_audience, entra_client_id=entra_client_id, sas_key_name=sas_key_name, sas_key=sas_key))
    if os.getenv("MOCK_MODE", "").lower() in ("1", "true", "yes"):
        _publish_mock(producer)
        producer.close()
        return


    # Initial full fetch: publish both reference data and observations
    all_records = api.fetch_all_records()
    logger.info("Publishing sensor configuration info events under air-quality/be/issep/wallonia-issep/...")
    _publish_configurations(producer, all_records)

    # Publish observations from the initial batch (treats all as new)
    new_records = api.filter_new_records(all_records, state)
    init_count = 0
    for record in new_records:
        try:
            obs = api.normalize_observation(record)
            data = _build_observation_data(obs)
            producer.send_observation(
                _configuration_id=obs.configuration_id,
                _province=getattr(obs, "province", None) or "unknown",
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
        producer.close()
        return

    try:
        while True:
            try:
                start_time = datetime.now(timezone.utc)
                count, _ = _publish_observations(api, producer, state)
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
                    time.sleep(effective)
            except KeyboardInterrupt:
                logger.info("Exiting...")
                break
            except Exception as exc:  # pylint: disable=broad-except
                logger.error("Error during polling cycle: %s", exc)
                time.sleep(polling_interval)
    finally:
        producer.close()



DEFAULT_ENTRA_AUDIENCE_SERVICEBUS = "https://servicebus.azure.net/.default"
DEFAULT_ENTRA_AUDIENCE_EVENTHUBS = "https://eventhubs.azure.net/.default"


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
def _build_producer(*, host: str, port: int, address: str, use_tls: bool, content_mode: str, auth_mode: str, username: Optional[str], password: Optional[str], entra_audience: str, entra_client_id: Optional[str], sas_key_name: Optional[str], sas_key: Optional[str]) -> BeIssepAirqualitySensorsAmqpProducer:
    if auth_mode == "entra":
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        credential = ManagedIdentityCredential(client_id=entra_client_id) if entra_client_id else DefaultAzureCredential()
        return BeIssepAirqualitySensorsAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, credential=credential, entra_audience=entra_audience, use_tls=use_tls)  # type: ignore[arg-type]
    if auth_mode == "sas":
        if not sas_key_name or not sas_key:
            raise RuntimeError("auth-mode=sas requires AMQP_SAS_KEY_NAME and AMQP_SAS_KEY")
        return BeIssepAirqualitySensorsAmqpProducer(host=host, address=address, port=port, content_mode=content_mode, sas_key_name=sas_key_name, sas_key=sas_key, use_tls=use_tls)  # type: ignore[arg-type]
    return BeIssepAirqualitySensorsAmqpProducer(host=host, address=address, port=port, username=username, password=password, content_mode=content_mode, use_tls=use_tls)  # type: ignore[arg-type]

def _parse_broker_url(url: str) -> tuple:
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
    parser = argparse.ArgumentParser(description="Wallonia ISSeP air quality → AMQP 1.0 bridge.")
    subparsers = parser.add_subparsers(dest="command")
    feed_parser = subparsers.add_parser("feed", help="Feed sensor data as CloudEvents to AMQP")
    feed_parser.add_argument("--broker-url", type=str, default=os.getenv("AMQP_BROKER_URL"))
    feed_parser.add_argument("--broker-host", type=str, default=os.getenv("AMQP_HOST"))
    feed_parser.add_argument("--broker-port", type=int,
                             default=int(os.getenv("AMQP_PORT", "0")) or None)
    feed_parser.add_argument("--username", type=str, default=os.getenv("AMQP_USERNAME"))
    feed_parser.add_argument("--password", type=str, default=os.getenv("AMQP_PASSWORD"))
    feed_parser.add_argument("--tls", action="store_true",
                             default=os.getenv("AMQP_TLS", "").lower() in ("1", "true", "yes"))
    feed_parser.add_argument("--client-id", type=str, default=os.getenv("AMQP_CLIENT_ID"))
    feed_parser.add_argument("--content-mode", type=str, default=os.getenv("AMQP_CONTENT_MODE", "binary"),
                             choices=["binary", "structured"])
    feed_parser.add_argument("--address", type=str, default=os.getenv("AMQP_ADDRESS", "wallonia-issep"))
    feed_parser.add_argument("--auth-mode", type=str, default=os.getenv("AMQP_AUTH_MODE", "password"), choices=["password", "entra", "sas"])
    feed_parser.add_argument("--entra-audience", type=str, default=os.getenv("AMQP_ENTRA_AUDIENCE", DEFAULT_ENTRA_AUDIENCE_SERVICEBUS))
    feed_parser.add_argument("--entra-client-id", type=str, default=os.getenv("AMQP_ENTRA_CLIENT_ID"))
    feed_parser.add_argument("--sas-key-name", type=str, default=os.getenv("AMQP_SAS_KEY_NAME"))
    feed_parser.add_argument("--sas-key", type=str, default=os.getenv("AMQP_SAS_KEY"))
    feed_parser.add_argument("-i", "--polling-interval", type=int,
                             default=int(os.getenv("POLLING_INTERVAL", "600")))
    feed_parser.add_argument("--state-file", type=str,
                             default=os.getenv("STATE_FILE", os.path.expanduser("~/.wallonia_issep_amqp_state.json")))
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
        host, port, tls, user, pwd, path = _parse_broker_url(args.broker_url)
        username = args.username or user
        password = args.password or pwd
        if args.broker_port:
            port = args.broker_port
        address = path or args.address
        if args.tls:
            tls = True
    else:
        host = args.broker_host or "localhost"
        tls = bool(args.tls)
        port = args.broker_port or (5671 if tls else 5672)
        username = args.username
        password = args.password
        address = args.address

    api = WalloniaISsePAPI()
    feed(
            api, host, port, args.polling_interval,
            username=username, password=password, tls=tls,
            client_id=args.client_id, state_file=args.state_file,
            once=args.once, content_mode=args.content_mode,
            address=address, auth_mode=args.auth_mode, entra_audience=args.entra_audience,
            entra_client_id=args.entra_client_id, sas_key_name=args.sas_key_name, sas_key=args.sas_key,
        )


if __name__ == "__main__":
    main()
