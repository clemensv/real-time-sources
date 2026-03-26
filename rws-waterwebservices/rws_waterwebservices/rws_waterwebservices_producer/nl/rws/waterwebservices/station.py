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
    A Station record from Rijkswaterstaat Waterwebservices.
    Attributes:
        code (str): Location code (e.g., hoekvanholland)
        name (str): Location name (e.g., Hoek van Holland)
        latitude (float): Latitude in ETRS89/WGS84
        longitude (float): Longitude in ETRS89/WGS84
        coordinate_system (str): Coordinate system (e.g., ETRS89)
    """

    code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    coordinate_system: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coordinate_system"))

    def __post_init__(self):
        self.code=str(self.code)
        self.name=str(self.name)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.coordinate_system=str(self.coordinate_system)

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
