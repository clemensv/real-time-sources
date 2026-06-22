"""
NOAA SWPC Space Weather Poller
Polls the Space Weather Prediction Center endpoints for space weather data
and sends it to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import sys
import time
import logging
from typing import Dict, List, Optional
import argparse
from noaa_goes_core import SWPCFetcher
from noaa_goes_producer_data import (
    SpaceWeatherAlert, PlanetaryKIndex, SolarWindSummary,
    SolarWindPlasma, SolarWindMagField,
    GoesXrayFlux, GoesProtonFlux, GoesElectronFlux,
    GoesMagnetometer, XrayFlare,
)
from noaa_goes_producer_kafka_producer.producer import (
    MicrosoftOpenDataUSNOAASWPCAlertsEventProducer,
    MicrosoftOpenDataUSNOAASWPCObservationsEventProducer,
    MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer,
    MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer,
    MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer,
)

logger = logging.getLogger(__name__)


class SWPCPoller(SWPCFetcher):
    """
    Polls the NOAA Space Weather Prediction Center API endpoints and sends
    space weather data to Kafka as CloudEvents.
    """

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        super().__init__(last_polled_file)
        self.kafka_topic = kafka_topic
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.alerts_producer = MicrosoftOpenDataUSNOAASWPCAlertsEventProducer(kafka_producer, kafka_topic)
        self.observations_producer = MicrosoftOpenDataUSNOAASWPCObservationsEventProducer(kafka_producer, kafka_topic)
        self.particle_flux_producer = MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer(kafka_producer, kafka_topic)
        self.magnetometer_producer = MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer(kafka_producer, kafka_topic)
        self.flares_producer = MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer(kafka_producer, kafka_topic)
        self.kafka_producer = kafka_producer

    def poll_and_send(self, once: bool = False):
        logger.info("Starting SWPC Space Weather poller, polling every %ds", self.POLL_INTERVAL_SECONDS)
        logger.info("  Kafka topic: %s", self.kafka_topic)

        while True:
            try:
                state = self.load_state()
                new_count = 0

                new_count += self._send_alerts(state)
                new_count += self._send_k_index(state)
                new_count += self._send_solar_wind_summary(state)
                new_count += self._send_plasma(state)
                new_count += self._send_mag(state)
                new_count += self._send_goes_xrays(state)
                new_count += self._send_goes_protons(state)
                new_count += self._send_goes_electrons(state)
                new_count += self._send_goes_magnetometers(state)
                new_count += self._send_xray_flares(state)

                if new_count > 0:
                    self.kafka_producer.flush()
                    logger.info("Sent %d new record(s) to Kafka", new_count)

                self.save_state(state)

            except Exception as e:
                logger.error("Error in polling loop: %s", e)

            if once:
                logger.info("--once mode: exiting after first polling cycle")
                break

            time.sleep(self.POLL_INTERVAL_SECONDS)

    def _send_alerts(self, state: Dict) -> int:
        alerts = self.poll_alerts()
        last_alert_id = state.get("last_alert_id")
        count = 0
        for alert_data in alerts:
            product_id = alert_data.get("product_id", "")
            if not product_id or product_id == last_alert_id:
                continue
            alert = SpaceWeatherAlert(
                product_id=product_id,
                issue_datetime=alert_data.get("issue_datetime", ""),
                message=alert_data.get("message", "")
            )
            self.alerts_producer.send_microsoft_open_data_us_noaa_swpc_space_weather_alert(
                product_id, alert, flush_producer=False)
            state["last_alert_id"] = product_id
            count += 1
        return count

    def _send_k_index(self, state: Dict) -> int:
        rows = self.poll_k_index()
        last_time = state.get("last_kindex_time")
        count = 0
        for row in rows:
            time_tag = str(row.get("time_tag", ""))
            if not time_tag or time_tag == last_time:
                continue
            kindex = PlanetaryKIndex(
                observation_time=time_tag,
                kp=float(row.get("Kp", 0)),
                a_running=float(row.get("a_running", 0)),
                station_count=int(row.get("station_count", 0))
            )
            self.observations_producer.send_microsoft_open_data_us_noaa_swpc_planetary_kindex(
                time_tag, kindex, flush_producer=False)
            state["last_kindex_time"] = time_tag
            count += 1
        return count

    def _send_solar_wind_summary(self, state: Dict) -> int:
        records = self.poll_solar_wind()
        last_time = state.get("last_solar_wind_time")
        count = 0
        for record in records:
            ts = record.get("timestamp", "")
            if not ts or ts == last_time:
                continue
            summary = SolarWindSummary(
                observation_time=ts,
                wind_speed=record.get("wind_speed", 0.0),
                bt=record.get("bt", 0.0),
                bz=record.get("bz", 0.0)
            )
            self.observations_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_summary(
                ts, summary, flush_producer=False)
            state["last_solar_wind_time"] = ts
            count += 1
        return count

    def _send_plasma(self, state: Dict) -> int:
        rows = self.poll_plasma()
        last_time = state.get("last_plasma_time")
        count = 0
        for row in rows:
            tt = row.get("time_tag", "")
            if not tt or tt <= (last_time or ""):
                continue
            plasma = SolarWindPlasma(
                observation_time=tt,
                density=self._safe_float(row.get("density")),
                speed=self._safe_float(row.get("speed")),
                temperature=self._safe_float(row.get("temperature")),
            )
            self.observations_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_plasma(
                tt, plasma, flush_producer=False)
            state["last_plasma_time"] = tt
            count += 1
        return count

    def _send_mag(self, state: Dict) -> int:
        rows = self.poll_mag()
        last_time = state.get("last_mag_time")
        count = 0
        for row in rows:
            tt = row.get("time_tag", "")
            if not tt or tt <= (last_time or ""):
                continue
            mag = SolarWindMagField(
                observation_time=tt,
                bx_gsm=self._safe_float(row.get("bx_gsm")),
                by_gsm=self._safe_float(row.get("by_gsm")),
                bz_gsm=self._safe_float(row.get("bz_gsm")),
                lon_gsm=self._safe_float(row.get("lon_gsm")),
                lat_gsm=self._safe_float(row.get("lat_gsm")),
                bt=self._safe_float(row.get("bt")),
            )
            self.observations_producer.send_microsoft_open_data_us_noaa_swpc_solar_wind_mag_field(
                tt, mag, flush_producer=False)
            state["last_mag_time"] = tt
            count += 1
        return count

    def _send_goes_flux(self, rows: List[dict], state_key: str,
                        data_cls, send_fn) -> int:
        last_time = state_key  # reused below
        count = 0
        for row in rows:
            tt = str(row.get("time_tag", ""))
            sat = self._safe_int(row.get("satellite"))
            energy = str(row.get("energy", ""))
            flux_val = self._safe_float(row.get("flux"))
            if not tt or sat is None or flux_val is None:
                continue
            obj = data_cls(
                time_tag=tt,
                satellite=sat,
                flux=flux_val,
                energy=energy,
            )
            send_fn(str(sat), energy, tt, obj, flush_producer=False)
            count += 1
        return count

    def _send_goes_xrays(self, state: Dict) -> int:
        rows = self.poll_goes_xrays()
        last_time = state.get("last_xray_time")
        filtered = [r for r in rows if str(r.get("time_tag", "")) > (last_time or "")]
        if filtered:
            state["last_xray_time"] = max(str(r.get("time_tag", "")) for r in filtered)
        return self._send_goes_flux(
            filtered, "last_xray_time",
            GoesXrayFlux,
            self.particle_flux_producer.send_microsoft_open_data_us_noaa_swpc_goes_xray_flux,
        )

    def _send_goes_protons(self, state: Dict) -> int:
        rows = self.poll_goes_protons()
        last_time = state.get("last_proton_time")
        filtered = [r for r in rows if str(r.get("time_tag", "")) > (last_time or "")]
        if filtered:
            state["last_proton_time"] = max(str(r.get("time_tag", "")) for r in filtered)
        return self._send_goes_flux(
            filtered, "last_proton_time",
            GoesProtonFlux,
            self.particle_flux_producer.send_microsoft_open_data_us_noaa_swpc_goes_proton_flux,
        )

    def _send_goes_electrons(self, state: Dict) -> int:
        rows = self.poll_goes_electrons()
        last_time = state.get("last_electron_time")
        filtered = [r for r in rows if str(r.get("time_tag", "")) > (last_time or "")]
        if filtered:
            state["last_electron_time"] = max(str(r.get("time_tag", "")) for r in filtered)
        return self._send_goes_flux(
            filtered, "last_electron_time",
            GoesElectronFlux,
            self.particle_flux_producer.send_microsoft_open_data_us_noaa_swpc_goes_electron_flux,
        )

    def _send_goes_magnetometers(self, state: Dict) -> int:
        rows = self.poll_goes_magnetometers()
        last_time = state.get("last_magnetometer_time")
        count = 0
        for row in rows:
            tt = str(row.get("time_tag", ""))
            if not tt or tt <= (last_time or ""):
                continue
            sat = self._safe_int(row.get("satellite"))
            if sat is None:
                continue
            obj = GoesMagnetometer(
                time_tag=tt,
                satellite=sat,
                he=self._safe_float(row.get("He")),
                hp=self._safe_float(row.get("Hp")),
                hn=self._safe_float(row.get("Hn")),
                total=self._safe_float(row.get("total")),
                arcjet_flag=row.get("arcjet_flag"),
            )
            self.magnetometer_producer.send_microsoft_open_data_us_noaa_swpc_goes_magnetometer(
                str(sat), tt, obj, flush_producer=False)
            state["last_magnetometer_time"] = tt
            count += 1
        return count

    def _send_xray_flares(self, state: Dict) -> int:
        rows = self.poll_xray_flares()
        last_time = state.get("last_flare_time")
        count = 0
        for row in rows:
            tt = str(row.get("time_tag", ""))
            begin = str(row.get("begin_time", ""))
            if not tt or not begin or tt <= (last_time or ""):
                continue
            sat = self._safe_int(row.get("satellite"))
            if sat is None:
                continue
            obj = XrayFlare(
                time_tag=tt,
                begin_time=begin,
                begin_class=row.get("begin_class"),
                max_time=row.get("max_time"),
                max_class=row.get("max_class"),
                max_xrlong=self._safe_float(row.get("max_xrlong")),
                max_ratio=self._safe_float(row.get("max_ratio")),
                max_ratio_time=row.get("max_ratio_time"),
                current_int_xrlong=self._safe_float(row.get("current_int_xrlong")),
                end_time=row.get("end_time"),
                end_class=row.get("end_class"),
                satellite=sat,
            )
            self.flares_producer.send_microsoft_open_data_us_noaa_swpc_xray_flare(
                str(sat), begin, obj, flush_producer=False)
            state["last_flare_time"] = tt
            count += 1
        return count


def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part:
                config_dict['bootstrap.servers'] = part.split('=')[1].strip(
                    '"').replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part:
                config_dict['kafka_topic'] = part.split('=')[1].strip('"')
            elif 'SharedAccessKeyName' in part:
                config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part:
                config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part:
                config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e:
        raise ValueError("Invalid connection string format") from e
    if 'sasl.username' in config_dict:
        config_dict['security.protocol'] = 'SASL_SSL'
        config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict


def main():
    parser = argparse.ArgumentParser(description="NOAA SWPC Space Weather Poller")
    parser.add_argument('--last-polled-file', type=str,
                        help="File to store last-polled timestamps for deduplication")
    parser.add_argument('--kafka-bootstrap-servers', type=str,
                        help="Comma separated list of Kafka bootstrap servers")
    parser.add_argument('--kafka-topic', type=str,
                        help="Kafka topic to send messages to")
    parser.add_argument('--sasl-username', type=str,
                        help="Username for SASL PLAIN authentication")
    parser.add_argument('--sasl-password', type=str,
                        help="Password for SASL PLAIN authentication")
    parser.add_argument('--connection-string', type=str,
                        help='Microsoft Event Hubs or Microsoft Fabric Event Stream connection string')
    parser.add_argument('--once', action='store_true',
                        default=os.getenv('ONCE_MODE', '').lower() in ('1', 'true', 'yes'),
                        help='Exit after one polling cycle (also via ONCE_MODE env var). '
                             'Useful for scheduled execution in Fabric notebooks.')

    _argv = sys.argv[1:]
    if _argv and _argv[0] == 'feed':
        _argv = _argv[1:]
    args = parser.parse_args(_argv)
    logging.basicConfig(level=logging.INFO)

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('SWPC_LAST_POLLED_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.getenv('STATE_FILE')
        if not args.last_polled_file:
            args.last_polled_file = os.path.expanduser('~/.swpc_last_polled.json')

    if args.connection_string:
        config_params = parse_connection_string(args.connection_string)
        kafka_bootstrap_servers = config_params.get('bootstrap.servers')
        kafka_topic = config_params.get('kafka_topic')
        sasl_username = config_params.get('sasl.username')
        sasl_password = config_params.get('sasl.password')
    else:
        kafka_bootstrap_servers = args.kafka_bootstrap_servers
        kafka_topic = args.kafka_topic
        sasl_username = args.sasl_username
        sasl_password = args.sasl_password

    if not kafka_bootstrap_servers:
        print("Error: Kafka bootstrap servers must be provided either through the command line or connection string.")
        sys.exit(1)
    if not kafka_topic:
        print("Error: Kafka topic must be provided either through the command line or connection string.")
        sys.exit(1)
    tls_enabled = os.getenv('KAFKA_ENABLE_TLS', 'true').lower() not in ('false', '0', 'no')
    kafka_config = {
        'bootstrap.servers': kafka_bootstrap_servers,
    }
    if sasl_username and sasl_password:
        kafka_config.update({
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL' if tls_enabled else 'SASL_PLAINTEXT',
            'sasl.username': sasl_username,
            'sasl.password': sasl_password
        })
    elif tls_enabled:
        kafka_config['security.protocol'] = 'SSL'

    poller = SWPCPoller(
        kafka_config=kafka_config,
        kafka_topic=kafka_topic,
        last_polled_file=args.last_polled_file
    )
    poller.poll_and_send(once=args.once)


if __name__ == "__main__":
    main()
