"""DWD Open Data - transport-neutral module setup."""
from __future__ import annotations
import os
from typing import Dict, List, Optional, Set
from dwd_producer_data import StationMetadata, AirTemperature10Min, Precipitation10Min, Wind10Min, Solar10Min, HourlyObservation, ExtremeWind10Min, ExtremeTemperature10Min, Alert, RadarProductCatalog, RadarFileProduct, ForecastModelCatalog, IconD2ForecastFile
from dwd.modules.base import BaseModule
from dwd.modules.station_metadata import StationMetadataModule
from dwd.modules.station_obs_10min import StationObs10MinModule
from dwd.modules.station_obs_10min_extremes import StationObs10MinExtremesModule
from dwd.modules.station_obs_hourly import StationObsHourlyModule
from dwd.modules.weather_alerts import WeatherAlertsModule
from dwd.modules.radar_products import RadarProductsModule
from dwd.modules.icon_d2_forecast import IconD2ForecastModule
from dwd.util.http_client import DWDHttpClient
from dwd.util.state import load_state, save_state
MODULE_CLASSES = {"station_metadata": StationMetadataModule, "station_obs_10min": StationObs10MinModule, "station_obs_10min_extremes": StationObs10MinExtremesModule, "station_obs_hourly": StationObsHourlyModule, "weather_alerts": WeatherAlertsModule, "radar_products": RadarProductsModule, "icon_d2_forecast": IconD2ForecastModule}
__all__ = ["MODULE_CLASSES", "_optional_int_env", "_truthy_env", "parse_connection_string", "_resolve_modules", "_create_module", "StationMetadata", "AirTemperature10Min", "Precipitation10Min", "Wind10Min", "Solar10Min", "HourlyObservation", "ExtremeWind10Min", "ExtremeTemperature10Min", "Alert", "RadarProductCatalog", "RadarFileProduct", "ForecastModelCatalog", "IconD2ForecastFile", "DWDHttpClient", "load_state", "save_state", "StationMetadataModule", "StationObs10MinModule", "StationObs10MinExtremesModule", "StationObsHourlyModule", "WeatherAlertsModule", "RadarProductsModule", "IconD2ForecastModule"]
def _optional_int_env(var_name: str) -> Optional[int]:
    raw = os.getenv(var_name)
    if raw is None or raw.strip() == '': return None
    value = int(raw); return value or None
def _truthy_env(var_name: str) -> bool: return os.getenv(var_name, '').strip().lower() in ('1', 'true', 'yes')
def parse_connection_string(connection_string: str) -> Dict[str, str]:
    config_dict: Dict[str, str] = {}
    try:
        for part in connection_string.split(';'):
            if 'Endpoint' in part: config_dict['bootstrap.servers'] = part.split('=')[1].strip('"').strip().replace('sb://', '').replace('/', '') + ':9093'
            elif 'EntityPath' in part: config_dict['kafka_topic'] = part.split('=')[1].strip('"').strip()
            elif 'SharedAccessKeyName' in part: config_dict['sasl.username'] = '$ConnectionString'
            elif 'SharedAccessKey' in part: config_dict['sasl.password'] = connection_string.strip()
            elif 'BootstrapServer' in part: config_dict['bootstrap.servers'] = part.split('=', 1)[1].strip()
    except IndexError as e: raise ValueError('Invalid connection string format') from e
    if 'sasl.username' in config_dict: config_dict['security.protocol'] = 'SASL_SSL'; config_dict['sasl.mechanism'] = 'PLAIN'
    return config_dict
def _resolve_modules(http_client: DWDHttpClient, enabled_csv: Optional[str], disabled_csv: Optional[str], ten_min_params: Optional[str], station_filter: Optional[Set[str]]) -> List[BaseModule]:
    enabled = set(m.strip() for m in enabled_csv.split(',') if m.strip()) if enabled_csv else None; disabled = set(m.strip() for m in disabled_csv.split(',') if m.strip()) if disabled_csv else set(); modules: List[BaseModule] = []
    for key, cls in MODULE_CLASSES.items():
        if enabled is not None and key not in enabled: continue
        if key in disabled: continue
        if enabled is None:
            instance = _create_module(key, http_client, ten_min_params, station_filter)
            if instance.default_enabled: modules.append(instance)
        else: modules.append(_create_module(key, http_client, ten_min_params, station_filter))
    return modules
def _create_module(key: str, http_client: DWDHttpClient, ten_min_params: Optional[str], station_filter: Optional[Set[str]]) -> BaseModule:
    if key == 'station_obs_10min':
        categories = [p.strip() for p in ten_min_params.split(',')] if ten_min_params else None
        return StationObs10MinModule(http_client, categories=categories, station_filter=station_filter)
    if key == 'station_obs_10min_extremes': return StationObs10MinExtremesModule(http_client, station_filter=station_filter)
    if key == 'station_obs_hourly': return StationObsHourlyModule(http_client, station_filter=station_filter)
    if key == 'station_metadata': return StationMetadataModule(http_client)
    if key == 'weather_alerts': return WeatherAlertsModule(http_client)
    if key == 'radar_products': return RadarProductsModule(http_client)
    if key == 'icon_d2_forecast': return IconD2ForecastModule(http_client)
    raise ValueError(f'Unknown module: {key}')
