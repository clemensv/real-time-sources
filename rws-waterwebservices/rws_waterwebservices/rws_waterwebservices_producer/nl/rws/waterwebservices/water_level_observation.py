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
    A water level observation from Rijkswaterstaat Waterwebservices.
    Attributes:
        location_code (str): Location code
        location_name (str): Location name
        timestamp (str): Measurement timestamp in ISO 8601
        value (float): Measured water level value in cm relative to NAP
        unit (str): Unit of measurement (cm)
        quality_code (str): Quality value code (00=good, 99=gap)
        status (str): Status (e.g., Ongecontroleerd)
        compartment (str): Compartment code (OW=surface water)
        parameter (str): Parameter code (WATHTE=water height)
    """

    location_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_code"))
    location_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_name"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    unit: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit"))
    quality_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="quality_code"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    compartment: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="compartment"))
    parameter: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter"))

    def __post_init__(self):
        self.location_code=str(self.location_code)
        self.location_name=str(self.location_name)
        self.timestamp=str(self.timestamp)
        self.value=float(self.value)
        self.unit=str(self.unit)
        self.quality_code=str(self.quality_code)
        self.status=str(self.status)
        self.compartment=str(self.compartment)
        self.parameter=str(self.parameter)

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
