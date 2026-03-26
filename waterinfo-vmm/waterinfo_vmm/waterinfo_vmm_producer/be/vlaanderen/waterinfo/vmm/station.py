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
    A Station record from Waterinfo.be.
    Attributes:
        station_no (str): Station number/code
        station_name (str): Station name
        station_id (str): Numeric station identifier
        station_latitude (float): Latitude in WGS84
        station_longitude (float): Longitude in WGS84
        river_name (str): Name of the river or waterway
        stationparameter_name (str): Parameter measured (e.g., H for water level)
        ts_id (str): Time series identifier
        ts_unitname (str): Unit of measurement (e.g., meter)
    """

    station_no: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_no"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_latitude"))
    station_longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_longitude"))
    river_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="river_name"))
    stationparameter_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stationparameter_name"))
    ts_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ts_id"))
    ts_unitname: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ts_unitname"))

    def __post_init__(self):
        self.station_no=str(self.station_no)
        self.station_name=str(self.station_name)
        self.station_id=str(self.station_id)
        self.station_latitude=float(self.station_latitude)
        self.station_longitude=float(self.station_longitude)
        self.river_name=str(self.river_name)
        self.stationparameter_name=str(self.stationparameter_name)
        self.ts_id=str(self.ts_id)
        self.ts_unitname=str(self.ts_unitname)

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
