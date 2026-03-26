""" Zone dataclass. """

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
class Zone:
    """
    A Zone record.
    Attributes:
        zone_id (str): 
        name (str): 
        type (str): 
        state (str): 
        forecast_office (str): 
        timezone (str): 
        radar_station (str): """
    
    zone_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="zone_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="type"))
    state: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    forecast_office: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="forecast_office"))
    timezone: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timezone"))
    radar_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="radar_station"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Zone\", \"namespace\": \"Microsoft.OpenData.US.NOAA.NWS\", \"fields\": [{\"name\": \"zone_id\", \"type\": \"string\"}, {\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"type\", \"type\": \"string\"}, {\"name\": \"state\", \"type\": \"string\"}, {\"name\": \"forecast_office\", \"type\": \"string\"}, {\"name\": \"timezone\", \"type\": \"string\"}, {\"name\": \"radar_station\", \"type\": \"string\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.zone_id=str(self.zone_id)
        self.name=str(self.name)
        self.type=str(self.type)
        self.state=str(self.state)
        self.forecast_office=str(self.forecast_office)
        self.timezone=str(self.timezone)
        self.radar_station=str(self.radar_station)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Zone':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary.

        Returns:
            The dictionary representation of the dataclass.
        """
        asdict_result = dataclasses.asdict(self, dict_factory=self._dict_resolver)
        return asdict_result

    def _dict_resolver(self, data):
        """
        Helps resolving the Enum values to their actual values and fixes the key names.
        """ 
        def _resolve_enum(v):
            if isinstance(v,enum.Enum):
                return v.value
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/json': Encodes the data to JSON format.
        
        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'avro/binary':
            return self.to_avro_bytes()
        elif content_type in ['application/json', 'text/json']:
            return self.to_json().encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_avro_bytes(self) -> bytes:
        """
        Converts the dataclass to Avro binary format.
        
        Returns:
            The Avro binary representation of the dataclass.
        """
        writer = avro.io.DatumWriter(Zone.AvroType)
        buffer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(buffer)
        writer.write(self.to_serializer_dict(), encoder)
        return buffer.getvalue()

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Zone']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data by.
                Supported content types:
                    'avro/binary': Decodes the data from Avro binary format.
                    'application/json': Decodes the data from JSON format.
        Returns:
            The dataclass representation of the data.
        """
        if content_type_string:
            content_type = content_type_string.split(';')[0].strip()
            if content_type == 'avro/binary':
                reader = avro.io.DatumReader(Zone.AvroType)
                decoder = avro.io.BinaryDecoder(io.BytesIO(data))
                return Zone.from_serializer_dict(reader.read(decoder))
            elif content_type in ['application/json', 'text/json']:
                if isinstance(data, bytes):
                    data = data.decode('utf-8')
                return Zone.from_json(data)
        raise NotImplementedError(f"Unsupported content type: {content_type_string}")

    def is_content_type_avro_binary(self, content_type: str) -> bool:
        """Check if the content type indicates Avro binary encoding."""
        return content_type == 'avro/binary'
    
    def is_content_type_json(self, content_type: str) -> bool:
        """Check if the content type indicates JSON encoding."""
        return content_type in ['application/json', 'text/json']
