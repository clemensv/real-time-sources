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
        station_reference (str): Unique station reference identifier
        label (str): Station name
        river_name (str): Name of the river at the station
        catchment_name (str): Name of the catchment area
        town (str): Nearest town to the station
        lat (float): Latitude of the station in WGS84
        long (float): Longitude of the station in WGS84
        notation (str): Station notation identifier
        status (str): Station status URI
        date_opened (str): Date the station was opened
    """

    station_reference: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_reference"))
    label: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="label"))
    river_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="river_name"))
    catchment_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="catchment_name"))
    town: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="town"))
    lat: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat"))
    long: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="long"))
    notation: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="notation"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    date_opened: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_opened"))

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_reference=str(self.station_reference)
        self.label=str(self.label)
        self.river_name=str(self.river_name)
        self.catchment_name=str(self.catchment_name)
        self.town=str(self.town)
        self.lat=float(self.lat)
        self.long=float(self.long)
        self.notation=str(self.notation)
        self.status=str(self.status)
        self.date_opened=str(self.date_opened)

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
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'Station':
        """
        Deserializes this object from a data structure.

        Args:
            data: The data to deserialize.
            content_type_string (str): The content type string.

        Returns:
            Station: The deserialized object.
        """
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
