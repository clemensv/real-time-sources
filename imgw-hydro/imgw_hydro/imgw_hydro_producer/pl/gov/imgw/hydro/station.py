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
    A hydrological station from IMGW-PIB.
    Attributes:
        id_stacji (str): Station identifier
        stacja (str): Station name
        rzeka (str): River name
        wojewodztwo (str): Voivodeship (province)
        longitude (float): Longitude in WGS84
        latitude (float): Latitude in WGS84
    """

    id_stacji: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id_stacji"))
    stacja: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stacja"))
    rzeka: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rzeka"))
    wojewodztwo: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wojewodztwo"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))

    def __post_init__(self):
        self.id_stacji=str(self.id_stacji)
        self.stacja=str(self.stacja)
        self.rzeka=str(self.rzeka)
        self.wojewodztwo=str(self.wojewodztwo)
        self.longitude=float(self.longitude)
        self.latitude=float(self.latitude)

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
