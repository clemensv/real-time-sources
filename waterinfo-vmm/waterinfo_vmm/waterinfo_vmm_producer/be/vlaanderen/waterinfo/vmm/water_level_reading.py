""" WaterLevelReading dataclass. """

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
class WaterLevelReading:
    """
    A WaterLevelReading record from Waterinfo.be.
    Attributes:
        ts_id (str): Time series identifier
        station_no (str): Station number/code
        station_name (str): Station name
        timestamp (str): Measurement timestamp in ISO 8601 UTC
        value (float): Measured value
        unit_name (str): Unit of measurement
        parameter_name (str): Parameter code (H = water level, Q = discharge)
    """

    ts_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ts_id"))
    station_no: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_no"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    unit_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit_name"))
    parameter_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_name"))

    def __post_init__(self):
        self.ts_id=str(self.ts_id)
        self.station_no=str(self.station_no)
        self.station_name=str(self.station_name)
        self.timestamp=str(self.timestamp)
        self.value=float(self.value)
        self.unit_name=str(self.unit_name)
        self.parameter_name=str(self.parameter_name)

    def to_byte_array(self, content_type_string: str) -> bytes:
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            return json.dumps(self.to_dict()).encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'WaterLevelReading':
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            return WaterLevelReading.from_dict(data)
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
