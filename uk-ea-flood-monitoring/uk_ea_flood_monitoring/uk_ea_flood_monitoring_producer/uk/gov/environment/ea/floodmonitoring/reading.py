""" Reading dataclass. """

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
class Reading:
    """
    A Reading record.
    Attributes:
        station_reference (str): Station reference for this reading
        date_time (str): Timestamp of the reading in ISO 8601 format
        measure (str): Measure identifier URI
        value (float): Reading value
    """

    station_reference: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_reference"))
    date_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_time"))
    measure: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="measure"))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_reference=str(self.station_reference)
        self.date_time=str(self.date_time)
        self.measure=str(self.measure)
        self.value=float(self.value)

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Serializes this object to a byte array.

        Args:
            content_type_string (str): The content type string.

        Returns:
            bytes: The serialized byte array.
        """
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            return json.dumps(self.to_dict()).encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'Reading':
        """
        Deserializes this object from a data structure.

        Args:
            data: The data to deserialize.
            content_type_string (str): The content type string.

        Returns:
            Reading: The deserialized object.
        """
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            return Reading.from_dict(data)
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
