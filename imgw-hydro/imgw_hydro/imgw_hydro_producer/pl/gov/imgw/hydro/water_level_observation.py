""" WaterLevelObservation dataclass. """

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
class WaterLevelObservation:
    """
    A water level observation from IMGW-PIB.
    Attributes:
        station_id (str): Station identifier
        station_name (str): Station name
        river (str): River name
        voivodeship (str): Voivodeship (province)
        water_level (float): Water level in cm
        water_level_timestamp (str): Water level measurement timestamp
        water_temperature (float): Water temperature in degrees C, or None
        water_temperature_timestamp (str): Water temperature measurement timestamp, or None
        discharge (float): Discharge in m3/s, or None
        discharge_timestamp (str): Discharge measurement timestamp, or None
        ice_phenomenon_code (str): Ice phenomenon code, or None
        overgrowth_code (str): Vegetation overgrowth code, or None
    """

    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    river: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="river"))
    voivodeship: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="voivodeship"))
    water_level: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level"))
    water_level_timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level_timestamp"))
    water_temperature: typing.Optional[float]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="water_temperature"))
    water_temperature_timestamp: typing.Optional[str]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="water_temperature_timestamp"))
    discharge: typing.Optional[float]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="discharge"))
    discharge_timestamp: typing.Optional[str]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="discharge_timestamp"))
    ice_phenomenon_code: typing.Optional[str]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="ice_phenomenon_code"))
    overgrowth_code: typing.Optional[str]=dataclasses.field(default=None, kw_only=True, metadata=dataclasses_json.config(field_name="overgrowth_code"))

    def __post_init__(self):
        self.station_id=str(self.station_id)
        self.station_name=str(self.station_name)
        self.river=str(self.river)
        self.voivodeship=str(self.voivodeship)
        self.water_level=float(self.water_level)
        self.water_level_timestamp=str(self.water_level_timestamp)
        if self.water_temperature is not None:
            self.water_temperature=float(self.water_temperature)
        if self.water_temperature_timestamp is not None:
            self.water_temperature_timestamp=str(self.water_temperature_timestamp)
        if self.discharge is not None:
            self.discharge=float(self.discharge)
        if self.discharge_timestamp is not None:
            self.discharge_timestamp=str(self.discharge_timestamp)
        if self.ice_phenomenon_code is not None:
            self.ice_phenomenon_code=str(self.ice_phenomenon_code)
        if self.overgrowth_code is not None:
            self.overgrowth_code=str(self.overgrowth_code)

    def to_byte_array(self, content_type_string: str) -> bytes:
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            return json.dumps(self.to_dict()).encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'WaterLevelObservation':
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            return WaterLevelObservation.from_dict(data)
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
