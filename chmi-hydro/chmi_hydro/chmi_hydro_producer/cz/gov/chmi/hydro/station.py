""" Station dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Station:
    """
    A hydrological station from ČHMÚ.
    Attributes:
        station_id (str): Unique station identifier (e.g. 0-203-1-001000)
        dbc (str): Station database code
        station_name (str): Station name
        stream_name (str): River or stream name
        latitude (float): Latitude in WGS84
        longitude (float): Longitude in WGS84
        flood_level_1 (float): 1st degree flood warning water level in cm, or None
        flood_level_2 (float): 2nd degree flood warning water level in cm, or None
        flood_level_3 (float): 3rd degree flood warning water level in cm, or None
        flood_level_4 (float): Extreme flood warning water level in cm, or None
        has_forecast (bool): Whether the station provides forecast data
    """

    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    dbc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dbc"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    stream_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stream_name"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    flood_level_1: typing.Optional[float]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="flood_level_1"))
    flood_level_2: typing.Optional[float]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="flood_level_2"))
    flood_level_3: typing.Optional[float]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="flood_level_3"))
    flood_level_4: typing.Optional[float]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="flood_level_4"))
    has_forecast: bool=dataclasses.field(default=False, kw_only=True, metadata=dataclasses_json.config(field_name="has_forecast"))

    def __post_init__(self):
        self.station_id=str(self.station_id)
        self.dbc=str(self.dbc)
        self.station_name=str(self.station_name)
        self.stream_name=str(self.stream_name)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        if self.flood_level_1 is not None:
            self.flood_level_1=float(self.flood_level_1)
        if self.flood_level_2 is not None:
            self.flood_level_2=float(self.flood_level_2)
        if self.flood_level_3 is not None:
            self.flood_level_3=float(self.flood_level_3)
        if self.flood_level_4 is not None:
            self.flood_level_4=float(self.flood_level_4)
        self.has_forecast=bool(self.has_forecast)

    def to_byte_array(self, content_type_string: str) -> bytes:
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            return json.dumps(self.to_dict()).encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'Station':
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            return Station.from_dict(data)
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
