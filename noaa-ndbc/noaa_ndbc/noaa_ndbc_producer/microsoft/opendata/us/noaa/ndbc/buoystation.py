""" BuoyStation dataclass. """

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
import avro.schema
import avro.name
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class BuoyStation:
    """
    A BuoyStation record.
    Attributes:
        station_id (str): NDBC station identifier
        owner (str): Station owner organization
        station_type (str): Station type (e.g., Weather Buoy, C-MAN Station)
        hull (str): Hull type
        name (str): Station name and location description
        latitude (float): Station latitude in decimal degrees
        longitude (float): Station longitude in decimal degrees
        timezone (str): Station timezone"""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    owner: str=dataclasses.field(kw_only=True, default="", metadata=dataclasses_json.config(field_name="owner"))
    station_type: str=dataclasses.field(kw_only=True, default="", metadata=dataclasses_json.config(field_name="station_type"))
    hull: str=dataclasses.field(kw_only=True, default="", metadata=dataclasses_json.config(field_name="hull"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    latitude: float=dataclasses.field(kw_only=True, default=0.0, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, default=0.0, metadata=dataclasses_json.config(field_name="longitude"))
    timezone: str=dataclasses.field(kw_only=True, default="", metadata=dataclasses_json.config(field_name="timezone"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"BuoyStation\", \"namespace\": \"Microsoft.OpenData.US.NOAA.NDBC\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\"}, {\"name\": \"owner\", \"type\": \"string\"}, {\"name\": \"station_type\", \"type\": \"string\"}, {\"name\": \"hull\", \"type\": \"string\"}, {\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"latitude\", \"type\": \"double\"}, {\"name\": \"longitude\", \"type\": \"double\"}, {\"name\": \"timezone\", \"type\": \"string\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the BuoyStation dataclass """
        self.station_id = str(self.station_id)
        self.owner = str(self.owner)
        self.station_type = str(self.station_type)
        self.hull = str(self.hull)
        self.name = str(self.name)
        self.latitude = float(self.latitude)
        self.longitude = float(self.longitude)
        self.timezone = str(self.timezone)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BuoyStation':
        """ Converts a dictionary to a dataclass instance """
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """ Converts a dataclass instance to a dictionary """
        return dataclasses.asdict(self)

    def to_byte_array(self, content_type: str) -> bytes:
        """ Converts the dataclass to a byte array """
        if content_type == "application/json":
            return json.dumps(self.to_serializer_dict()).encode("utf-8")
        if "avro" in content_type:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(BuoyStation.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
            data = stream.getvalue()
            if "gzip" in content_type:
                return gzip.compress(data)
            return data
        raise ValueError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type: str = "application/json") -> 'BuoyStation':
        """ Converts the data to a dataclass instance """
        if content_type == "application/json":
            if isinstance(data, str):
                data = json.loads(data)
            return cls.from_serializer_dict(data)
        if "avro" in content_type:
            if "gzip" in content_type:
                data = gzip.decompress(data)
            stream = io.BytesIO(data)
            reader = avro.io.DatumReader(BuoyStation.AvroType)
            decoder = avro.io.BinaryDecoder(stream)
            return cls.from_serializer_dict(reader.read(decoder))
        raise ValueError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        """ Converts the dataclass to a JSON string """
        return json.dumps(self.to_serializer_dict())
