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
import avro.schema
import avro.name
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WaterLevelReading:
    """
    Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal.
    Attributes:
        station_id (str): Unique integer identifier of the river station.
        title (str): Human-readable name of the river station at the time of the reading.
        basin (str): Name of the river basin the station belongs to.
        water_level (typing.Optional[float]): Current water level at the station in meters. Null when no reading available.
        danger_level (typing.Optional[float]): Configured danger water level threshold in meters. Null when not configured.
        warning_level (typing.Optional[float]): Configured warning water level threshold in meters. Null when not configured.
        status (str): Current alert status: 'BELOW WARNING LEVEL', 'WARNING', or 'DANGER'.
        trend (str): Direction of water level change: 'STEADY', 'RISING', or 'FALLING'.
        water_level_on (str): ISO 8601 timestamp of when the water level was measured."""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    title: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    basin: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))
    water_level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level"))
    danger_level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="danger_level"))
    warning_level: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="warning_level"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    trend: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trend"))
    water_level_on: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_level_on"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"WaterLevelReading\", \"namespace\": \"np.gov.bipad.hydrology\", \"doc\": \"Real-time water level telemetry reading from a BIPAD river monitoring station in Nepal.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Unique integer identifier of the river station.\"}, {\"name\": \"title\", \"type\": \"string\", \"doc\": \"Human-readable name of the river station at the time of the reading.\"}, {\"name\": \"basin\", \"type\": \"string\", \"doc\": \"Name of the river basin the station belongs to.\"}, {\"name\": \"water_level\", \"type\": [\"null\", \"double\"], \"doc\": \"Current water level at the station in meters. Null when no reading available.\", \"default\": null}, {\"name\": \"danger_level\", \"type\": [\"null\", \"double\"], \"doc\": \"Configured danger water level threshold in meters. Null when not configured.\", \"default\": null}, {\"name\": \"warning_level\", \"type\": [\"null\", \"double\"], \"doc\": \"Configured warning water level threshold in meters. Null when not configured.\", \"default\": null}, {\"name\": \"status\", \"type\": \"string\", \"doc\": \"Current alert status: 'BELOW WARNING LEVEL', 'WARNING', or 'DANGER'.\"}, {\"name\": \"trend\", \"type\": \"string\", \"doc\": \"Direction of water level change: 'STEADY', 'RISING', or 'FALLING'.\"}, {\"name\": \"water_level_on\", \"type\": \"string\", \"doc\": \"ISO 8601 timestamp of when the water level was measured.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.title=str(self.title)
        self.basin=str(self.basin)
        self.water_level=float(self.water_level) if self.water_level else None
        self.danger_level=float(self.danger_level) if self.danger_level else None
        self.warning_level=float(self.warning_level) if self.warning_level else None
        self.status=str(self.status)
        self.trend=str(self.trend)
        self.water_level_on=str(self.water_level_on)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaterLevelReading':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaterLevelReading']:
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
            return WaterLevelReading.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WaterLevelReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')