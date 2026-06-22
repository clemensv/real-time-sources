"""Madrid Real-Time Traffic (Informo) - transport-neutral acquisition."""
from __future__ import annotations
import os, time, xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
from madrid_traffic_producer_data import MeasurementPoint, TrafficReading
PM_XML_URL = "https://informo.madrid.es/informo/tmadrid/pm.xml"
POLL_INTERVAL_SECONDS = 300
REFERENCE_REFRESH_SECONDS = 3600
USER_AGENT = os.environ.get("USER_AGENT") or ("real-time-sources-madrid-traffic/0.1.0 " "(+https://github.com/clemensv/real-time-sources; " + os.environ.get("USER_AGENT_CONTACT", "clemensv@microsoft.com") + ")")
__all__ = ["PM_XML_URL","POLL_INTERVAL_SECONDS","REFERENCE_REFRESH_SECONDS","USER_AGENT","parse_european_float","safe_int","round_to_5min","parse_pm_xml","build_measurement_point","build_traffic_reading","MadridTrafficPoller"]
def parse_european_float(value: str) -> Optional[float]:
    if not value or not value.strip(): return None
    try: return float(value.strip().replace(',', '.'))
    except (ValueError, TypeError): return None
def safe_int(value: str) -> Optional[int]:
    if not value or not value.strip(): return None
    try: return int(value.strip())
    except (ValueError, TypeError): return None
def round_to_5min(dt: datetime) -> datetime: return dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0)
def parse_pm_xml(xml_text: str) -> Tuple[List[dict], Optional[str]]:
    root = ET.fromstring(xml_text); fecha_hora = None; fecha_hora_elem = root.find('fecha_hora')
    if fecha_hora_elem is not None and fecha_hora_elem.text: fecha_hora = fecha_hora_elem.text.strip()
    sensors = []
    for pm in root.findall('pm'):
        sensor = {}
        for child in pm: sensor[child.tag] = child.text.strip() if child.text else ''
        sensors.append(sensor)
    return sensors, fecha_hora
def build_measurement_point(sensor: dict) -> MeasurementPoint:
    return MeasurementPoint(sensor_id=sensor.get('idelem', ''), description=sensor.get('descripcion', ''), element_type=sensor.get('tipo_elem', None), subarea=sensor.get('subarea', None) or None, longitude=parse_european_float(sensor.get('st_x', '')), latitude=parse_european_float(sensor.get('st_y', '')), saturation_intensity=safe_int(sensor.get('intensidadSat', '')))
def build_traffic_reading(sensor: dict, timestamp: datetime) -> TrafficReading:
    return TrafficReading(sensor_id=sensor.get('idelem', ''), intensity=safe_int(sensor.get('intensidad', '')), occupancy=safe_int(sensor.get('ocupacion', '')), load=safe_int(sensor.get('carga', '')), service_level=safe_int(sensor.get('nivelServicio', '')), error_flag=sensor.get('error', None) or None, timestamp=timestamp)
class MadridTrafficPoller:
    def __init__(self): self._last_dedup_key = None; self._last_reference_time = 0.0
    def fetch_xml(self) -> Optional[str]:
        try:
            response = requests.get(PM_XML_URL, headers={'User-Agent': USER_AGENT}, timeout=60); response.raise_for_status(); return response.text
        except Exception as err: print(f'Error fetching Madrid traffic data: {err}'); return None
    def get_reference_data(self, sensors): return [build_measurement_point(s) for s in sensors if s.get('idelem')]
    def get_traffic_readings(self, sensors, poll_time):
        timestamp = round_to_5min(poll_time); dedup_key = timestamp.isoformat()
        if dedup_key == self._last_dedup_key: return dedup_key, []
        readings = []
        for sensor in sensors:
            error = sensor.get('error', 'N')
            if error and error.upper() in ('S', 'Y'): continue
            reading = build_traffic_reading(sensor, timestamp)
            if reading.sensor_id: readings.append(reading)
        self._last_dedup_key = dedup_key
        return dedup_key, readings
