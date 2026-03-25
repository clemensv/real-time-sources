""" DischargeObservation dataclass. """

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
class DischargeObservation:
    """
    A discharge observation from SMHI.
    Attributes:
        station_id (str): Station identifier
        station_name (str): Station name
        catchment_name (str): Catchment area name (river/watercourse)
        timestamp (str): Measurement timestamp (ISO 8601)
        discharge (float): Discharge (flow rate) in m³/s
        quality (str): Data quality flag (e.g. O = original)
    """

    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    catchment_name: str=dataclasses.field(default="", kw_only=True, metadata=dataclasses_json.config(field_name="catchment_name"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    discharge: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discharge"))
    quality: str=dataclasses.field(default="", kw_only=True, metadata=dataclasses_json.config(field_name="quality"))

    def __post_init__(self):
        self.station_id=str(self.station_id)
        self.station_name=str(self.station_name)
        self.catchment_name=str(self.catchment_name)
        self.timestamp=str(self.timestamp)
        self.discharge=float(self.discharge)
        self.quality=str(self.quality)

    def to_byte_array(self, content_type_string: str) -> bytes:
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            return json.dumps(self.to_dict()).encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'DischargeObservation':
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            return DischargeObservation.from_dict(data)
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
