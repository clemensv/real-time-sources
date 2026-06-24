"""NWS forecast zone bridge – Kafka transport wrapper."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from typing import Dict, List, Optional

import requests
from confluent_kafka import Producer

try:
    from nws_forecasts_core import (
        DEFAULT_POLL_INTERVAL_SECONDS,
        DEFAULT_REFERENCE_REFRESH_SECONDS,
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
        DEFAULT_REFERENCE_REFRESH_SECONDS,
        DEFAULT_STATE_FILE,
        DEFAULT_ZONES,
        NWSForecastFetcher,
        NWSForecastZone,
        NWSLandZoneForecast,
        NWSMarineZoneForecast,
        build_retrying_session,
        parse_zone_list,
    )

from nws_forecasts_producer_data import (
    ForecastZone,
    LandForecastPeriod,
    LandZoneForecast,
    MarineForecastPeriod,
    MarineZoneForecast,
    ZoneTypeenum,
)
from nws_forecasts_producer_kafka_producer.producer import (
    MicrosoftOpenDataUSNOAANWSForecastsEventProducer,
)


LOGGER = logging.getLogger(__name__)


def parse_connection_string(connection_string: str, enable_tls: bool = True) -> Dict[str, str]:
    """Parse Event Hubs/Fabric or BootstrapServer connection strings into Kafka config."""
    parts: Dict[str, str] = {}
    for item in connection_string.split(";"):
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        parts[key] = value

    if "Endpoint" in parts:
        endpoint = parts["Endpoint"].replace("sb://", "").rstrip("/")
        config = {
            "bootstrap.servers": f"{endpoint}:9093",
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": "$ConnectionString",
            "sasl.password": connection_string.strip(),
        }
    elif "BootstrapServer" in parts:
        config = {
            "bootstrap.servers": parts["BootstrapServer"],
            "security.protocol": "SSL" if enable_tls else "PLAINTEXT",
        }
    else:
        raise ValueError("Connection string must contain Endpoint or BootstrapServer.")

    if "EntityPath" in parts:
        config["kafka_topic"] = parts["EntityPath"]
    return config


def build_kafka_config(args: argparse.Namespace) -> tuple[Dict[str, str], str]:
    """Build Kafka config and resolve the destination topic."""
    if args.connection_string:
        config = parse_connection_string(args.connection_string, enable_tls=args.kafka_enable_tls)
        parsed_topic = config.pop("kafka_topic", None)
        topic = args.kafka_topic or parsed_topic
        if not topic:
            raise ValueError("Kafka topic must be provided in KAFKA_TOPIC or EntityPath.")
        config["socket.keepalive.enable"] = "true"
        config["connections.max.idle.ms"] = "540000"
        return config, topic

    if not args.kafka_bootstrap_servers or not args.kafka_topic:
        raise ValueError("Provide CONNECTION_STRING or both KAFKA_BOOTSTRAP_SERVERS and KAFKA_TOPIC.")

    config: Dict[str, str] = {
        "bootstrap.servers": args.kafka_bootstrap_servers,
        "security.protocol": "SASL_SSL" if args.sasl_username and args.kafka_enable_tls else (
            "SASL_PLAINTEXT" if args.sasl_username else ("SSL" if args.kafka_enable_tls else "PLAINTEXT")
        ),
        "socket.keepalive.enable": "true",
        "connections.max.idle.ms": "540000",
    }
    if args.sasl_username:
        config["sasl.mechanisms"] = "PLAIN"
        config["sasl.username"] = args.sasl_username
        if not args.sasl_password:
            raise ValueError("SASL_PASSWORD is required when SASL_USERNAME is set.")
        config["sasl.password"] = args.sasl_password
    return config, args.kafka_topic


def _to_producer_zone(zone: NWSForecastZone) -> ForecastZone:
    """Convert a transport-neutral NWSForecastZone to a generated ForecastZone."""
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


def _to_producer_land(forecast: NWSLandZoneForecast) -> LandZoneForecast:
    """Convert a transport-neutral NWSLandZoneForecast to a generated LandZoneForecast."""
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


def _to_producer_marine(forecast: NWSMarineZoneForecast) -> MarineZoneForecast:
    """Convert a transport-neutral NWSMarineZoneForecast to a generated MarineZoneForecast."""
    return MarineZoneForecast(
        zone_id=forecast.zone_id,
        zone_name=str(forecast.zone_name) if forecast.zone_name is not None else None,  # type: ignore[arg-type]
        product_title=forecast.product_title,
        office_name=forecast.office_name,
        issued_at_text=str(forecast.issued_at_text) if forecast.issued_at_text is not None else None,  # type: ignore[arg-type]
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
        bulletin_text=str(forecast.bulletin_text) if forecast.bulletin_text is not None else None,  # type: ignore[arg-type]
    )


class NWSForecastPoller:
    """Kafka transport wrapper over the transport-neutral NWS forecast fetcher."""

    def __init__(
        self,
        kafka_config: Dict[str, str],
        kafka_topic: str,
        zones: List[str],
        state_file: str,
        poll_interval_seconds: int = DEFAULT_POLL_INTERVAL_SECONDS,
        reference_refresh_seconds: int = DEFAULT_REFERENCE_REFRESH_SECONDS,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.kafka_client = Producer(kafka_config)
        self.producer = MicrosoftOpenDataUSNOAANWSForecastsEventProducer(self.kafka_client, kafka_topic)
        self._fetcher = NWSForecastFetcher(
            zones=zones,
            state_file=state_file,
            poll_interval_seconds=poll_interval_seconds,
            reference_refresh_seconds=reference_refresh_seconds,
            session=session,
            on_zone=self._on_zone,
            on_land_forecast=self._on_land_forecast,
            on_marine_forecast=self._on_marine_forecast,
            flush_callback=self._flush,
        )

    def _on_zone(self, zone_id: str, zone: NWSForecastZone) -> None:
        self.producer.send_microsoft_open_data_us_noaa_nws_forecast_zone(
            zone_id, _to_producer_zone(zone), flush_producer=False
        )

    def _on_land_forecast(self, zone_id: str, forecast: NWSLandZoneForecast) -> None:
        self.producer.send_microsoft_open_data_us_noaa_nws_land_zone_forecast(
            zone_id, _to_producer_land(forecast), flush_producer=False
        )

    def _on_marine_forecast(self, zone_id: str, forecast: NWSMarineZoneForecast) -> None:
        self.producer.send_microsoft_open_data_us_noaa_nws_marine_zone_forecast(
            zone_id, _to_producer_marine(forecast), flush_producer=False
        )

    def _flush(self) -> None:
        self._flush_with_retry()

    def _flush_with_retry(self, timeout: int = 30, retries: int = 3, context: str = "messages") -> None:
        """Flush Kafka producer with retries and exponential backoff."""
        for attempt in range(1, retries + 1):
            remaining = self.kafka_client.flush(timeout=timeout)
            if remaining == 0:
                return
            if attempt < retries:
                backoff = 2 ** attempt
                LOGGER.warning(
                    "Kafka flush left %d %s unsent (attempt %d/%d), retrying in %ds...",
                    remaining, context, attempt, retries, backoff,
                )
                time.sleep(backoff)
            else:
                raise RuntimeError(
                    f"Kafka flush left {remaining} {context} unsent after {retries} attempts."
                )

    def _emit_reference_with_backoff(self) -> None:
        try:
            self._fetcher.emit_reference_data()
        except RuntimeError as exc:
            LOGGER.warning("Reference data emission failed (will retry next refresh): %s", exc)

    def run(self, once: bool = False) -> None:
        self._fetcher.run(once=once, emit_reference_with_backoff=self._emit_reference_with_backoff)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NWS forecast zone bridge")
    parser.add_argument("--zones", default=os.getenv("NWS_FORECAST_ZONES", DEFAULT_ZONES))
    parser.add_argument("--state-file", default=os.getenv("NWS_FORECAST_STATE_FILE", DEFAULT_STATE_FILE))
    parser.add_argument(
        "--poll-interval-seconds",
        type=int,
        default=int(os.getenv("NWS_FORECAST_POLL_INTERVAL_SECONDS", DEFAULT_POLL_INTERVAL_SECONDS)),
    )
    parser.add_argument(
        "--reference-refresh-seconds",
        type=int,
        default=int(os.getenv("NWS_FORECAST_REFERENCE_REFRESH_SECONDS", DEFAULT_REFERENCE_REFRESH_SECONDS)),
    )
    parser.add_argument("--connection-string", default=os.getenv("CONNECTION_STRING"))
    parser.add_argument("--kafka-bootstrap-servers", default=os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    parser.add_argument("--kafka-topic", default=os.getenv("KAFKA_TOPIC"))
    parser.add_argument("--sasl-username", default=os.getenv("SASL_USERNAME"))
    parser.add_argument("--sasl-password", default=os.getenv("SASL_PASSWORD"))
    parser.add_argument(
        "--kafka-enable-tls",
        default=os.getenv("KAFKA_ENABLE_TLS", "true").lower() != "false",
        type=lambda value: str(value).lower() != "false",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        default=os.getenv("ONCE_MODE", "false").lower() == "true",
        help="Run a single polling cycle and exit (used by Fabric notebook hosting).",
    )
    return parser


def main() -> None:
    logging.basicConfig(
        level=logging.INFO if sys.gettrace() is None else logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    args = build_argument_parser().parse_args()
    kafka_config, kafka_topic = build_kafka_config(args)
    poller = NWSForecastPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        zones=parse_zone_list(args.zones),
        state_file=args.state_file,
        poll_interval_seconds=args.poll_interval_seconds,
        reference_refresh_seconds=args.reference_refresh_seconds,
    )
    poller.run(once=args.once)


if __name__ == "__main__":
    main()
