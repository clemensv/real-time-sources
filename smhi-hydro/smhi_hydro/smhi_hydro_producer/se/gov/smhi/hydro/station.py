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
    A hydrological station from SMHI.
    Attributes:
        station_id (str): Unique station identifier
        name (str): Station name
        owner (str): Station owner (e.g. SMHI)
        measuring_stations (str): Station type (CORE or ADDITIONAL)
        region (int): Region number
        catchment_name (str): Catchment area name (river/watercourse)
        catchment_number (int): Catchment area number
        catchment_size (float): Catchment area size in km²
        latitude (float): Latitude in WGS84
        longitude (float): Longitude in WGS84
    """

    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    owner: str=dataclasses.field(default="", kw_only=True, metadata=dataclasses_json.config(field_name="owner"))
    measuring_stations: str=dataclasses.field(default="", kw_only=True, metadata=dataclasses_json.config(field_name="measuring_stations"))
    region: int=dataclasses.field(default=0, kw_only=True, metadata=dataclasses_json.config(field_name="region"))
    catchment_name: str=dataclasses.field(default="", kw_only=True, metadata=dataclasses_json.config(field_name="catchment_name"))
    catchment_number: int=dataclasses.field(default=0, kw_only=True, metadata=dataclasses_json.config(field_name="catchment_number"))
    catchment_size: float=dataclasses.field(default=0.0, kw_only=True, metadata=dataclasses_json.config(field_name="catchment_size"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))

    def __post_init__(self):
        self.station_id=str(self.station_id)
        self.name=str(self.name)
        self.owner=str(self.owner)
        self.measuring_stations=str(self.measuring_stations)
        self.region=int(self.region)
        self.catchment_name=str(self.catchment_name)
        self.catchment_number=int(self.catchment_number)
        self.catchment_size=float(self.catchment_size)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)

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
