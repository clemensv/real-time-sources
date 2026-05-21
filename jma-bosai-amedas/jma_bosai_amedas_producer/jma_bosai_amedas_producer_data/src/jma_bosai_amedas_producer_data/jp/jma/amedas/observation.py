""" Observation dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import json
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import avro.schema
import avro.name
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Observation:
    """
    Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.
    Attributes:
        station_code (str): JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map.
        observed_at (str): Observation snapshot timestamp converted from JMA latest_time.txt to UTC and serialized as RFC3339. AMeDAS map snapshots are published every ten minutes.
        observed_at_local (str): Original JMA latest_time.txt timestamp in Japan Standard Time with +09:00 offset, serialized as RFC3339.
        temp (typing.Optional[float]): Air temperature observed automatically by AMeDAS, expressed in degrees Celsius. JMA documents temperature as air temperature displayed in 0.1 °C units.
        temp_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        humidity (typing.Optional[float]): Relative humidity of the air observed automatically by AMeDAS, expressed as percent. JMA documents humidity as relative humidity displayed in 1 percent units.
        humidity_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        pressure (typing.Optional[float]): Station pressure from JMA Bosai AMeDAS where available, expressed in hectopascals.
        pressure_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        normal_pressure (typing.Optional[float]): Sea-level adjusted pressure (normalPressure in the Bosai payload) where available, expressed in hectopascals.
        normal_pressure_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        wind_speed (typing.Optional[float]): Wind speed averaged over the ten minutes before observation time, expressed in meters per second. JMA documents wind speed as the speed of the wind over the preceding ten minutes.
        wind_speed_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        wind_direction (typing.Optional[float]): Wind direction from which the wind blows, converted by the bridge from JMA 16-direction codes to degrees clockwise from true north.
        wind_direction_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        wind_gust (typing.Optional[float]): Maximum instantaneous wind speed (gust) for the observation interval from the JMA Bosai per-station point payload, expressed in meters per second. The bridge enriches map observations with this value only for configured point-detail stations.
        wind_gust_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the gust tuple in the Bosai AMeDAS per-station point payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA non-normal quality states as represented by the Bosai web application.
        wind_gust_direction (typing.Optional[float]): Direction from which the maximum instantaneous wind gust blew, converted by the bridge from JMA 16-direction codes in gustDirection to degrees clockwise from true north. The field is present only when point-detail enrichment is configured and JMA publishes a gust direction.
        wind_gust_time (typing.Optional[str]): UTC RFC3339 timestamp for the maximum instantaneous wind gust time from the JMA Bosai per-station gustTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.
        max_temp (typing.Optional[float]): Maximum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations.
        max_temp_time (typing.Optional[str]): UTC RFC3339 timestamp for the maximum air temperature time from the JMA Bosai per-station maxTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.
        min_temp (typing.Optional[float]): Minimum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations.
        min_temp_time (typing.Optional[str]): UTC RFC3339 timestamp for the minimum air temperature time from the JMA Bosai per-station minTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.
        precipitation10m (typing.Optional[float]): Precipitation amount for the previous 10 minutes, expressed in millimeters of liquid water equivalent. JMA documents precipitation as rain or snow amount melted to water and displayed in 0.5 mm units.
        precipitation10m_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        precipitation1h (typing.Optional[float]): Precipitation amount for the previous 1 hour, expressed in millimeters of liquid water equivalent.
        precipitation1h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        precipitation3h (typing.Optional[float]): Precipitation amount for the previous 3 hours, expressed in millimeters of liquid water equivalent.
        precipitation3h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        precipitation24h (typing.Optional[float]): Precipitation amount for the previous 24 hours, expressed in millimeters of liquid water equivalent.
        precipitation24h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        sun10m (typing.Optional[float]): Sunshine duration for the previous 10 minutes, expressed in minutes. JMA publishes this ten-minute map field in minutes, so its unit intentionally differs from the hourly sun1h field.
        sun10m_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        sun1h (typing.Optional[float]): Sunshine duration for the previous 1 hour, expressed in hours as published by the Bosai AMeDAS map. JMA publishes this hourly field in hours, so its unit intentionally differs from the ten-minute sun10m field.
        sun1h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        snow (typing.Optional[float]): Snow depth, the height of snow on the ground, expressed in centimeters. JMA documents snow depth as the height from the ground surface to the top of accumulated snow.
        snow_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        snow1h (typing.Optional[float]): Change in snow depth over the previous 1 hour, expressed in centimeters.
        snow1h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        snow6h (typing.Optional[float]): Change in snow depth over the previous 6 hours, expressed in centimeters.
        snow6h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        snow12h (typing.Optional[float]): Change in snow depth over the previous 12 hours, expressed in centimeters.
        snow12h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        snow24h (typing.Optional[float]): Change in snow depth over the previous 24 hours, expressed in centimeters.
        snow24h_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        visibility (typing.Optional[float]): Horizontal visibility where published by JMA Bosai AMeDAS, expressed in meters.
        visibility_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        cloud (typing.Optional[float]): Cloud amount code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish cloud information.
        cloud_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.
        weather (typing.Optional[float]): Present weather code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish weather information.
        weather_qc_flag (typing.Optional[int]): JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application."""
    
    station_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_code"))
    observed_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observed_at"))
    observed_at_local: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observed_at_local"))
    temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp"))
    temp_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp_qc_flag"))
    humidity: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity"))
    humidity_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity_qc_flag"))
    pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure"))
    pressure_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_qc_flag"))
    normal_pressure: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="normal_pressure"))
    normal_pressure_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="normal_pressure_qc_flag"))
    wind_speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    wind_speed_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed_qc_flag"))
    wind_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_direction_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction_qc_flag"))
    wind_gust: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust"))
    wind_gust_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_qc_flag"))
    wind_gust_direction: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_direction"))
    wind_gust_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_gust_time"))
    max_temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_temp"))
    max_temp_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_temp_time"))
    min_temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="min_temp"))
    min_temp_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="min_temp_time"))
    precipitation10m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation10m"))
    precipitation10m_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation10m_qc_flag"))
    precipitation1h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation1h"))
    precipitation1h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation1h_qc_flag"))
    precipitation3h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation3h"))
    precipitation3h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation3h_qc_flag"))
    precipitation24h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation24h"))
    precipitation24h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="precipitation24h_qc_flag"))
    sun10m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun10m"))
    sun10m_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun10m_qc_flag"))
    sun1h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun1h"))
    sun1h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sun1h_qc_flag"))
    snow: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow"))
    snow_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow_qc_flag"))
    snow1h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow1h"))
    snow1h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow1h_qc_flag"))
    snow6h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow6h"))
    snow6h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow6h_qc_flag"))
    snow12h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow12h"))
    snow12h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow12h_qc_flag"))
    snow24h: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow24h"))
    snow24h_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="snow24h_qc_flag"))
    visibility: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility"))
    visibility_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visibility_qc_flag"))
    cloud: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud"))
    cloud_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cloud_qc_flag"))
    weather: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="weather"))
    weather_qc_flag: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="weather_qc_flag"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Observation\", \"namespace\": \"JP.JMA.Amedas\", \"doc\": \"Telemetry event for one JMA AMeDAS station observation in a ten-minute Bosai map snapshot. Each measurement value is nullable because JMA publishes different fields by station capability and by observation availability.\", \"fields\": [{\"name\": \"station_code\", \"type\": \"string\", \"doc\": \"JMA AMeDAS five-digit station code used as the stable identifier in the Bosai AMeDAS station table and observation map.\"}, {\"name\": \"observed_at\", \"type\": \"string\", \"doc\": \"Observation snapshot timestamp converted from JMA latest_time.txt to UTC and serialized as RFC3339. AMeDAS map snapshots are published every ten minutes.\"}, {\"name\": \"observed_at_local\", \"type\": \"string\", \"doc\": \"Original JMA latest_time.txt timestamp in Japan Standard Time with +09:00 offset, serialized as RFC3339.\"}, {\"name\": \"temp\", \"type\": [\"null\", \"double\"], \"doc\": \"Air temperature observed automatically by AMeDAS, expressed in degrees Celsius. JMA documents temperature as air temperature displayed in 0.1 \u00b0C units.\", \"default\": null}, {\"name\": \"temp_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"humidity\", \"type\": [\"null\", \"double\"], \"doc\": \"Relative humidity of the air observed automatically by AMeDAS, expressed as percent. JMA documents humidity as relative humidity displayed in 1 percent units.\", \"default\": null}, {\"name\": \"humidity_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"pressure\", \"type\": [\"null\", \"double\"], \"doc\": \"Station pressure from JMA Bosai AMeDAS where available, expressed in hectopascals.\", \"default\": null}, {\"name\": \"pressure_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"normal_pressure\", \"type\": [\"null\", \"double\"], \"doc\": \"Sea-level adjusted pressure (normalPressure in the Bosai payload) where available, expressed in hectopascals.\", \"default\": null}, {\"name\": \"normal_pressure_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"wind_speed\", \"type\": [\"null\", \"double\"], \"doc\": \"Wind speed averaged over the ten minutes before observation time, expressed in meters per second. JMA documents wind speed as the speed of the wind over the preceding ten minutes.\", \"default\": null}, {\"name\": \"wind_speed_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"wind_direction\", \"type\": [\"null\", \"double\"], \"doc\": \"Wind direction from which the wind blows, converted by the bridge from JMA 16-direction codes to degrees clockwise from true north.\", \"default\": null}, {\"name\": \"wind_direction_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"wind_gust\", \"type\": [\"null\", \"double\"], \"doc\": \"Maximum instantaneous wind speed (gust) for the observation interval from the JMA Bosai per-station point payload, expressed in meters per second. The bridge enriches map observations with this value only for configured point-detail stations.\", \"default\": null}, {\"name\": \"wind_gust_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the gust tuple in the Bosai AMeDAS per-station point payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"wind_gust_direction\", \"type\": [\"null\", \"double\"], \"doc\": \"Direction from which the maximum instantaneous wind gust blew, converted by the bridge from JMA 16-direction codes in gustDirection to degrees clockwise from true north. The field is present only when point-detail enrichment is configured and JMA publishes a gust direction.\", \"default\": null}, {\"name\": \"wind_gust_time\", \"type\": [\"null\", \"string\"], \"doc\": \"UTC RFC3339 timestamp for the maximum instantaneous wind gust time from the JMA Bosai per-station gustTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.\", \"default\": null}, {\"name\": \"max_temp\", \"type\": [\"null\", \"double\"], \"doc\": \"Maximum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations.\", \"default\": null}, {\"name\": \"max_temp_time\", \"type\": [\"null\", \"string\"], \"doc\": \"UTC RFC3339 timestamp for the maximum air temperature time from the JMA Bosai per-station maxTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.\", \"default\": null}, {\"name\": \"min_temp\", \"type\": [\"null\", \"double\"], \"doc\": \"Minimum air temperature from the JMA Bosai per-station point payload, expressed in degrees Celsius. The bridge enriches map observations with this value only for configured point-detail stations.\", \"default\": null}, {\"name\": \"min_temp_time\", \"type\": [\"null\", \"string\"], \"doc\": \"UTC RFC3339 timestamp for the minimum air temperature time from the JMA Bosai per-station minTempTime object. JMA publishes hour and minute in local time; the bridge resolves the date relative to the observation timestamp and converts it to UTC.\", \"default\": null}, {\"name\": \"precipitation10m\", \"type\": [\"null\", \"double\"], \"doc\": \"Precipitation amount for the previous 10 minutes, expressed in millimeters of liquid water equivalent. JMA documents precipitation as rain or snow amount melted to water and displayed in 0.5 mm units.\", \"default\": null}, {\"name\": \"precipitation10m_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"precipitation1h\", \"type\": [\"null\", \"double\"], \"doc\": \"Precipitation amount for the previous 1 hour, expressed in millimeters of liquid water equivalent.\", \"default\": null}, {\"name\": \"precipitation1h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"precipitation3h\", \"type\": [\"null\", \"double\"], \"doc\": \"Precipitation amount for the previous 3 hours, expressed in millimeters of liquid water equivalent.\", \"default\": null}, {\"name\": \"precipitation3h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"precipitation24h\", \"type\": [\"null\", \"double\"], \"doc\": \"Precipitation amount for the previous 24 hours, expressed in millimeters of liquid water equivalent.\", \"default\": null}, {\"name\": \"precipitation24h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"sun10m\", \"type\": [\"null\", \"double\"], \"doc\": \"Sunshine duration for the previous 10 minutes, expressed in minutes. JMA publishes this ten-minute map field in minutes, so its unit intentionally differs from the hourly sun1h field.\", \"default\": null}, {\"name\": \"sun10m_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"sun1h\", \"type\": [\"null\", \"double\"], \"doc\": \"Sunshine duration for the previous 1 hour, expressed in hours as published by the Bosai AMeDAS map. JMA publishes this hourly field in hours, so its unit intentionally differs from the ten-minute sun10m field.\", \"default\": null}, {\"name\": \"sun1h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"snow\", \"type\": [\"null\", \"double\"], \"doc\": \"Snow depth, the height of snow on the ground, expressed in centimeters. JMA documents snow depth as the height from the ground surface to the top of accumulated snow.\", \"default\": null}, {\"name\": \"snow_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"snow1h\", \"type\": [\"null\", \"double\"], \"doc\": \"Change in snow depth over the previous 1 hour, expressed in centimeters.\", \"default\": null}, {\"name\": \"snow1h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"snow6h\", \"type\": [\"null\", \"double\"], \"doc\": \"Change in snow depth over the previous 6 hours, expressed in centimeters.\", \"default\": null}, {\"name\": \"snow6h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"snow12h\", \"type\": [\"null\", \"double\"], \"doc\": \"Change in snow depth over the previous 12 hours, expressed in centimeters.\", \"default\": null}, {\"name\": \"snow12h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"snow24h\", \"type\": [\"null\", \"double\"], \"doc\": \"Change in snow depth over the previous 24 hours, expressed in centimeters.\", \"default\": null}, {\"name\": \"snow24h_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"visibility\", \"type\": [\"null\", \"double\"], \"doc\": \"Horizontal visibility where published by JMA Bosai AMeDAS, expressed in meters.\", \"default\": null}, {\"name\": \"visibility_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"cloud\", \"type\": [\"null\", \"double\"], \"doc\": \"Cloud amount code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish cloud information.\", \"default\": null}, {\"name\": \"cloud_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}, {\"name\": \"weather\", \"type\": [\"null\", \"double\"], \"doc\": \"Present weather code from JMA Bosai AMeDAS where available. The Bosai map exposes this as a numeric measurement tuple for stations that publish weather information.\", \"default\": null}, {\"name\": \"weather_qc_flag\", \"type\": [\"null\", \"int\"], \"doc\": \"JMA quality-control flag accompanying the measurement tuple in the Bosai AMeDAS map payload. A value of 0 indicates normal data; values 1 through 9 indicate JMA error, correction, missing, estimated, or other non-normal quality states as represented by the Bosai web application.\", \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_code=str(self.station_code)
        self.observed_at=str(self.observed_at)
        self.observed_at_local=str(self.observed_at_local)
        self.temp=float(self.temp) if self.temp else None
        self.temp_qc_flag=int(self.temp_qc_flag) if self.temp_qc_flag else None
        self.humidity=float(self.humidity) if self.humidity else None
        self.humidity_qc_flag=int(self.humidity_qc_flag) if self.humidity_qc_flag else None
        self.pressure=float(self.pressure) if self.pressure else None
        self.pressure_qc_flag=int(self.pressure_qc_flag) if self.pressure_qc_flag else None
        self.normal_pressure=float(self.normal_pressure) if self.normal_pressure else None
        self.normal_pressure_qc_flag=int(self.normal_pressure_qc_flag) if self.normal_pressure_qc_flag else None
        self.wind_speed=float(self.wind_speed) if self.wind_speed else None
        self.wind_speed_qc_flag=int(self.wind_speed_qc_flag) if self.wind_speed_qc_flag else None
        self.wind_direction=float(self.wind_direction) if self.wind_direction else None
        self.wind_direction_qc_flag=int(self.wind_direction_qc_flag) if self.wind_direction_qc_flag else None
        self.wind_gust=float(self.wind_gust) if self.wind_gust else None
        self.wind_gust_qc_flag=int(self.wind_gust_qc_flag) if self.wind_gust_qc_flag else None
        self.wind_gust_direction=float(self.wind_gust_direction) if self.wind_gust_direction else None
        self.wind_gust_time=str(self.wind_gust_time) if self.wind_gust_time else None
        self.max_temp=float(self.max_temp) if self.max_temp else None
        self.max_temp_time=str(self.max_temp_time) if self.max_temp_time else None
        self.min_temp=float(self.min_temp) if self.min_temp else None
        self.min_temp_time=str(self.min_temp_time) if self.min_temp_time else None
        self.precipitation10m=float(self.precipitation10m) if self.precipitation10m else None
        self.precipitation10m_qc_flag=int(self.precipitation10m_qc_flag) if self.precipitation10m_qc_flag else None
        self.precipitation1h=float(self.precipitation1h) if self.precipitation1h else None
        self.precipitation1h_qc_flag=int(self.precipitation1h_qc_flag) if self.precipitation1h_qc_flag else None
        self.precipitation3h=float(self.precipitation3h) if self.precipitation3h else None
        self.precipitation3h_qc_flag=int(self.precipitation3h_qc_flag) if self.precipitation3h_qc_flag else None
        self.precipitation24h=float(self.precipitation24h) if self.precipitation24h else None
        self.precipitation24h_qc_flag=int(self.precipitation24h_qc_flag) if self.precipitation24h_qc_flag else None
        self.sun10m=float(self.sun10m) if self.sun10m else None
        self.sun10m_qc_flag=int(self.sun10m_qc_flag) if self.sun10m_qc_flag else None
        self.sun1h=float(self.sun1h) if self.sun1h else None
        self.sun1h_qc_flag=int(self.sun1h_qc_flag) if self.sun1h_qc_flag else None
        self.snow=float(self.snow) if self.snow else None
        self.snow_qc_flag=int(self.snow_qc_flag) if self.snow_qc_flag else None
        self.snow1h=float(self.snow1h) if self.snow1h else None
        self.snow1h_qc_flag=int(self.snow1h_qc_flag) if self.snow1h_qc_flag else None
        self.snow6h=float(self.snow6h) if self.snow6h else None
        self.snow6h_qc_flag=int(self.snow6h_qc_flag) if self.snow6h_qc_flag else None
        self.snow12h=float(self.snow12h) if self.snow12h else None
        self.snow12h_qc_flag=int(self.snow12h_qc_flag) if self.snow12h_qc_flag else None
        self.snow24h=float(self.snow24h) if self.snow24h else None
        self.snow24h_qc_flag=int(self.snow24h_qc_flag) if self.snow24h_qc_flag else None
        self.visibility=float(self.visibility) if self.visibility else None
        self.visibility_qc_flag=int(self.visibility_qc_flag) if self.visibility_qc_flag else None
        self.cloud=float(self.cloud) if self.cloud else None
        self.cloud_qc_flag=int(self.cloud_qc_flag) if self.cloud_qc_flag else None
        self.weather=float(self.weather) if self.weather else None
        self.weather_qc_flag=int(self.weather_qc_flag) if self.weather_qc_flag else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Observation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        return asdict_result

    def _dict_resolver(self, data):
        """
        Helps resolving the Enum values to their actual values and fixes the key names.
        """ 
        def _resolve_enum(v):
            if isinstance(v,enum.Enum):
                return v.value
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
                    'application/json': Encodes the data to JSON format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
            result = stream.getvalue()
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member

        if result is not None and content_type.endswith('+gzip'):
            # Handle string result from to_json()
            if isinstance(result, str):
                result = result.encode('utf-8')
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Observation']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'avro/binary': Attempts to decode the data from Avro binary encoded format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary encoded format.
                    'avro/json': Attempts to decode the data from Avro JSON encoded format.
                    'application/vnd.apache.avro+json': Attempts to decode the data from Avro JSON encoded format.
                    'application/json': Attempts to decode the data from JSON encoded format.
                Supported content type extensions:
                    '+gzip': First decompresses the data using gzip, e.g. 'application/json+gzip'.
        Returns:
            The dataclass representation of the data.
        """
        if data is None:
            return None
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            return cls.from_serializer_dict(data)

        content_type = (content_type_string or 'application/octet-stream').split(';')[0].strip()

        if content_type.endswith('+gzip'):
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for gzip decompression')
            with gzip.GzipFile(fileobj=stream, mode='rb') as gzip_file:
                data = gzip_file.read()
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return Observation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Observation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')