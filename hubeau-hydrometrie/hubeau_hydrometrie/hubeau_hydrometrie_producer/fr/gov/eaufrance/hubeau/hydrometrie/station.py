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
    A Station record.
    Attributes:
        code_station (str): Unique station code (10 characters)
        libelle_station (str): Station name/label
        code_site (str): Parent site code (8 characters)
        longitude_station (float): Longitude in WGS84
        latitude_station (float): Latitude in WGS84
        libelle_cours_eau (str): River/waterway name
        libelle_commune (str): Municipality name
        code_departement (str): Department code
        en_service (bool): Whether the station is currently active
        date_ouverture_station (str): Station opening date in ISO 8601
    """

    code_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_station"))
    libelle_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_station"))
    code_site: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_site"))
    longitude_station: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude_station"))
    latitude_station: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude_station"))
    libelle_cours_eau: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_cours_eau"))
    libelle_commune: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_commune"))
    code_departement: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_departement"))
    en_service: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="en_service"))
    date_ouverture_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_ouverture_station"))

    def __post_init__(self):
        self.code_station=str(self.code_station)
        self.libelle_station=str(self.libelle_station)
        self.code_site=str(self.code_site)
        self.longitude_station=float(self.longitude_station)
        self.latitude_station=float(self.latitude_station)
        self.libelle_cours_eau=str(self.libelle_cours_eau)
        self.libelle_commune=str(self.libelle_commune)
        self.code_departement=str(self.code_departement)
        self.en_service=bool(self.en_service)
        self.date_ouverture_station=str(self.date_ouverture_station)

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
