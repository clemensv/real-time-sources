"""
NOAA SWPC Space Weather Poller
Polls the Space Weather Prediction Center endpoints for space weather data
and sends it to a Kafka topic as CloudEvents.
"""

# pylint: disable=line-too-long

import os
import json
import sys
import time
import logging
from typing import Dict, List, Optional
import argparse
import requests
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


class SWPCPoller:
    """
    Polls the NOAA Space Weather Prediction Center API endpoints and sends
    space weather data to Kafka as CloudEvents.
    """
    ALERTS_URL = "https://services.swpc.noaa.gov/products/alerts.json"
    K_INDEX_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    SOLAR_WIND_SPEED_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json"
    SOLAR_WIND_MAG_FIELD_URL = "https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json"
    PLASMA_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
    MAG_URL = "https://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json"
    XRAYS_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"
    PROTONS_URL = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"
    ELECTRONS_URL = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-3-day.json"
    MAGNETOMETERS_URL = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json"
    FLARES_URL = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json"
    POLL_INTERVAL_SECONDS = 60

    def __init__(self, kafka_config: Dict[str, str], kafka_topic: str, last_polled_file: str):
        self.kafka_topic = kafka_topic
        self.last_polled_file = last_polled_file
        from confluent_kafka import Producer as KafkaProducer
        kafka_producer = KafkaProducer(kafka_config)
        self.alerts_producer = MicrosoftOpenDataUSNOAASWPCAlertsEventProducer(kafka_producer, kafka_topic)
        self.observations_producer = MicrosoftOpenDataUSNOAASWPCObservationsEventProducer(kafka_producer, kafka_topic)
        self.particle_flux_producer = MicrosoftOpenDataUSNOAASWPCGOESParticleFluxEventProducer(kafka_producer, kafka_topic)
        self.magnetometer_producer = MicrosoftOpenDataUSNOAASWPCGOESMagnetometerEventProducer(kafka_producer, kafka_topic)
        self.flares_producer = MicrosoftOpenDataUSNOAASWPCSolarFlaresEventProducer(kafka_producer, kafka_topic)
        self.kafka_producer = kafka_producer

    def load_state(self) -> Dict:
        try:
            if os.path.exists(self.last_polled_file):
                with open(self.last_polled_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_state(self, state: Dict):
        try:
            os.makedirs(os.path.dirname(self.last_polled_file) if os.path.dirname(self.last_polled_file) else '.', exist_ok=True)
            with open(self.last_polled_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error("Error saving state: %s", e)

    def _get_json(self, url: str) -> Optional[list]:
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else [data] if isinstance(data, dict) else []
        except Exception as err:
            logger.warning("Error fetching %s: %s", url, err)
            return None

    def poll_alerts(self) -> List[dict]:
        result = self._get_json(self.ALERTS_URL)
        return result if result is not None else []

    def poll_k_index(self) -> List[dict]:
        result = self._get_json(self.K_INDEX_URL)
        if result is None:
            return []
        return [row for row in result if isinstance(row, dict)]

    def poll_solar_wind(self) -> List[dict]:
        try:
            speed_response = requests.get(self.SOLAR_WIND_SPEED_URL, timeout=30)
            speed_response.raise_for_status()
            speed_data = speed_response.json()
            mag_response = requests.get(self.SOLAR_WIND_MAG_FIELD_URL, timeout=30)
            mag_response.raise_for_status()
            mag_data = mag_response.json()
            if isinstance(speed_data, list) and speed_data:
                speed_data = speed_data[0]
            if isinstance(mag_data, list) and mag_data:
                mag_data = mag_data[0]
            timestamp = speed_data.get("time_tag") or speed_data.get("TimeStamp") or mag_data.get("time_tag") or mag_data.get("TimeStamp") or ""
            wind_speed = speed_data.get("proton_speed") or speed_data.get("WindSpeed") or 0
            bt = mag_data.get("bt") or mag_data.get("Bt") or 0
            bz = mag_data.get("bz_gsm") or mag_data.get("Bz") or 0
            return [{
                "timestamp": timestamp,
                "wind_speed": float(wind_speed) if wind_speed else 0.0,
                "bt": float(bt) if bt else 0.0,
                "bz": float(bz) if bz else 0.0
            }]
        except Exception as err:
            logger.warning("Error fetching solar wind summary: %s", err)
            return []

    def _parse_csv_json(self, url: str) -> List[dict]:
        """Parse CSV-in-JSON (array of arrays with header row) into list of dicts."""
        result = self._get_json(url)
        if not result or len(result) < 2:
            return []
        headers = result[0]
        rows = []
        for row in result[1:]:
            if isinstance(row, list) and len(row) == len(headers):
                rows.append(dict(zip(headers, row)))
        return rows

    def poll_plasma(self) -> List[dict]:
        return self._parse_csv_json(self.PLASMA_URL)

    def poll_mag(self) -> List[dict]:
        return self._parse_csv_json(self.MAG_URL)

    def poll_goes_xrays(self) -> List[dict]:
        result = self._get_json(self.XRAYS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_goes_protons(self) -> List[dict]:
        result = self._get_json(self.PROTONS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_goes_electrons(self) -> List[dict]:
        result = self._get_json(self.ELECTRONS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_goes_magnetometers(self) -> List[dict]:
        result = self._get_json(self.MAGNETOMETERS_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def poll_xray_flares(self) -> List[dict]:
        result = self._get_json(self.FLARES_URL)
        return [r for r in (result or []) if isinstance(r, dict)]

    def _safe_float(self, val) -> Optional[float]:
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    def _safe_int(self, val) -> Optional[int]:
        if val is None:
            return None
        try:
            return int(val)
        except (ValueError, TypeError):
            return None

    def poll_and_send(self):
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

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    if not args.connection_string:
        args.connection_string = os.getenv('CONNECTION_STRING')
    if not args.last_polled_file:
        args.last_polled_file = os.getenv('SWPC_LAST_POLLED_FILE')
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
    poller.poll_and_send()


if __name__ == "__main__":
    main()
