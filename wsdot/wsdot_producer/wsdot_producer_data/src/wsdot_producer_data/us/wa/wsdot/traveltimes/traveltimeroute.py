""" TravelTimeRoute dataclass. """

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
class TravelTimeRoute:
    """
    Travel time route.
    Attributes:
        travel_time_id (str): 
        name (str): 
        description (str): 
        distance (float): 
        average_time (int): 
        current_time (int): 
        time_updated (str): 
        start_description (typing.Optional[str]): 
        start_road_name (typing.Optional[str]): 
        start_direction (typing.Optional[str]): 
        start_milepost (typing.Optional[float]): 
        start_latitude (float): 
        start_longitude (float): 
        end_description (typing.Optional[str]): 
        end_road_name (typing.Optional[str]): 
        end_direction (typing.Optional[str]): 
        end_milepost (typing.Optional[float]): 
        end_latitude (float): 
        end_longitude (float): """
    
    travel_time_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="travel_time_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    description: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    distance: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="distance"))
    average_time: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_time"))
    current_time: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="current_time"))
    time_updated: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_updated"))
    start_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_description"))
    start_road_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_road_name"))
    start_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_direction"))
    start_milepost: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_milepost"))
    start_latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_latitude"))
    start_longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_longitude"))
    end_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_description"))
    end_road_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_road_name"))
    end_direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_direction"))
    end_milepost: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_milepost"))
    end_latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_latitude"))
    end_longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_longitude"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"TravelTimeRoute\", \"namespace\": \"us.wa.wsdot.traveltimes\", \"doc\": \"Travel time route.\", \"fields\": [{\"name\": \"travel_time_id\", \"type\": \"string\"}, {\"name\": \"name\", \"type\": \"string\"}, {\"name\": \"description\", \"type\": \"string\"}, {\"name\": \"distance\", \"type\": \"double\"}, {\"name\": \"average_time\", \"type\": \"int\"}, {\"name\": \"current_time\", \"type\": \"int\"}, {\"name\": \"time_updated\", \"type\": \"string\"}, {\"name\": \"start_description\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"start_road_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"start_direction\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"start_milepost\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"start_latitude\", \"type\": \"double\"}, {\"name\": \"start_longitude\", \"type\": \"double\"}, {\"name\": \"end_description\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"end_road_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"end_direction\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"end_milepost\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"end_latitude\", \"type\": \"double\"}, {\"name\": \"end_longitude\", \"type\": \"double\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.travel_time_id=str(self.travel_time_id)
        self.name=str(self.name)
        self.description=str(self.description)
        self.distance=float(self.distance)
        self.average_time=int(self.average_time)
        self.current_time=int(self.current_time)
        self.time_updated=str(self.time_updated)
        self.start_description=str(self.start_description) if self.start_description else None
        self.start_road_name=str(self.start_road_name) if self.start_road_name else None
        self.start_direction=str(self.start_direction) if self.start_direction else None
        self.start_milepost=float(self.start_milepost) if self.start_milepost else None
        self.start_latitude=float(self.start_latitude)
        self.start_longitude=float(self.start_longitude)
        self.end_description=str(self.end_description) if self.end_description else None
        self.end_road_name=str(self.end_road_name) if self.end_road_name else None
        self.end_direction=str(self.end_direction) if self.end_direction else None
        self.end_milepost=float(self.end_milepost) if self.end_milepost else None
        self.end_latitude=float(self.end_latitude)
        self.end_longitude=float(self.end_longitude)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TravelTimeRoute':
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
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
                    'application/json': Encodes the data to JSON format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
            result = stream.getvalue()
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member

        if result is not None and content_type.endswith('+gzip'):
            # Handle string result from to_json()
            if isinstance(result, str):
                result = result.encode('utf-8')
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TravelTimeRoute']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'avro/binary': Attempts to decode the data from Avro binary encoded format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary encoded format.
                    'avro/json': Attempts to decode the data from Avro JSON encoded format.
                    'application/vnd.apache.avro+json': Attempts to decode the data from Avro JSON encoded format.
                    'application/json': Attempts to decode the data from JSON encoded format.
                Supported content type extensions:
                    '+gzip': First decompresses the data using gzip, e.g. 'application/json+gzip'.
        Returns:
            The dataclass representation of the data.
        """
        if data is None:
            return None
        if isinstance(data, cls):
            return data
        if isinstance(data, dict):
            return cls.from_serializer_dict(data)

        content_type = (content_type_string or 'application/octet-stream').split(';')[0].strip()

        if content_type.endswith('+gzip'):
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for gzip decompression')
            with gzip.GzipFile(fileobj=stream, mode='rb') as gzip_file:
                data = gzip_file.read()
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return TravelTimeRoute.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return TravelTimeRoute.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')