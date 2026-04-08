""" TrafficSituation dataclass. """

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
class TrafficSituation:
    """
    Current traffic situation from the NDW DATEX II v3 actueel_beeld feed.
    Attributes:
        situation_id (str): Unique identifier of the traffic situation.
        version_time (str): Timestamp of the latest version of this situation in ISO 8601 format (UTC).
        severity (typing.Optional[str]): Overall severity: low, medium, high, highest, unknown.
        record_type (typing.Optional[str]): DATEX II situation record type.
        cause_type (typing.Optional[str]): Cause of the traffic situation.
        start_time (typing.Optional[str]): Start time of the situation validity period in ISO 8601 format.
        end_time (typing.Optional[str]): End time of the situation validity period in ISO 8601 format.
        information_status (str): Status of the information: real, test, or exercise."""
    
    situation_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_id"))
    version_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version_time"))
    severity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    record_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="record_type"))
    cause_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cause_type"))
    start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time"))
    end_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_time"))
    information_status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="information_status"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"TrafficSituation\", \"namespace\": \"nl.ndw.traffic\", \"doc\": \"Current traffic situation from the NDW DATEX II v3 actueel_beeld feed.\", \"fields\": [{\"name\": \"situation_id\", \"type\": \"string\", \"doc\": \"Unique identifier of the traffic situation.\"}, {\"name\": \"version_time\", \"type\": \"string\", \"doc\": \"Timestamp of the latest version of this situation in ISO 8601 format (UTC).\"}, {\"name\": \"severity\", \"type\": [\"null\", \"string\"], \"doc\": \"Overall severity: low, medium, high, highest, unknown.\", \"default\": null}, {\"name\": \"record_type\", \"type\": [\"null\", \"string\"], \"doc\": \"DATEX II situation record type.\", \"default\": null}, {\"name\": \"cause_type\", \"type\": [\"null\", \"string\"], \"doc\": \"Cause of the traffic situation.\", \"default\": null}, {\"name\": \"start_time\", \"type\": [\"null\", \"string\"], \"doc\": \"Start time of the situation validity period in ISO 8601 format.\", \"default\": null}, {\"name\": \"end_time\", \"type\": [\"null\", \"string\"], \"doc\": \"End time of the situation validity period in ISO 8601 format.\", \"default\": null}, {\"name\": \"information_status\", \"type\": \"string\", \"doc\": \"Status of the information: real, test, or exercise.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.situation_id=str(self.situation_id)
        self.version_time=str(self.version_time)
        self.severity=str(self.severity) if self.severity else None
        self.record_type=str(self.record_type) if self.record_type else None
        self.cause_type=str(self.cause_type) if self.cause_type else None
        self.start_time=str(self.start_time) if self.start_time else None
        self.end_time=str(self.end_time) if self.end_time else None
        self.information_status=str(self.information_status)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'TrafficSituation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['TrafficSituation']:
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
            return TrafficSituation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return TrafficSituation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')