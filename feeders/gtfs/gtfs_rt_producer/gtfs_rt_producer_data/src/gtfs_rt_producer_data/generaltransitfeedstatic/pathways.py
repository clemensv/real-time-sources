""" Pathways dataclass. """

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
class Pathways:
    """
    Defines pathways.
    Attributes:
        pathwayId (str): Identifies a pathway.
        fromStopId (str): Identifies a stop or station where the pathway begins.
        toStopId (str): Identifies a stop or station where the pathway ends.
        pathwayMode (int): Type of pathway between the specified (from_stop_id, to_stop_id) pair.
        isBidirectional (int): When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id).
        length (typing.Optional[float]): Length of the pathway, in meters.
        traversalTime (typing.Optional[int]): Average time, in seconds, needed to walk through the pathway.
        stairCount (typing.Optional[int]): Number of stairs of the pathway.
        maxSlope (typing.Optional[float]): Maximum slope of the pathway, in percent.
        minWidth (typing.Optional[float]): Minimum width of the pathway, in meters.
        signpostedAs (typing.Optional[str]): Signposting information for the pathway.
        reversedSignpostedAs (typing.Optional[str]): Reversed signposting information for the pathway."""
    
    pathwayId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pathwayId"))
    fromStopId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fromStopId"))
    toStopId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="toStopId"))
    pathwayMode: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pathwayMode"))
    isBidirectional: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="isBidirectional"))
    length: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="length"))
    traversalTime: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="traversalTime"))
    stairCount: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stairCount"))
    maxSlope: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="maxSlope"))
    minWidth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minWidth"))
    signpostedAs: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="signpostedAs"))
    reversedSignpostedAs: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reversedSignpostedAs"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Pathways\", \"namespace\": \"GeneralTransitFeedStatic\", \"doc\": \"Defines pathways.\", \"fields\": [{\"name\": \"pathwayId\", \"type\": \"string\", \"doc\": \"Identifies a pathway.\"}, {\"name\": \"fromStopId\", \"type\": \"string\", \"doc\": \"Identifies a stop or station where the pathway begins.\"}, {\"name\": \"toStopId\", \"type\": \"string\", \"doc\": \"Identifies a stop or station where the pathway ends.\"}, {\"name\": \"pathwayMode\", \"type\": \"int\", \"doc\": \"Type of pathway between the specified (from_stop_id, to_stop_id) pair.\"}, {\"name\": \"isBidirectional\", \"type\": \"int\", \"doc\": \"When 1, the pathway can be used in both directions. When 0, the pathway can only be used from (from_stop_id) to (to_stop_id).\"}, {\"name\": \"length\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Length of the pathway, in meters.\"}, {\"name\": \"traversalTime\", \"type\": [\"null\", \"int\"], \"default\": null, \"doc\": \"Average time, in seconds, needed to walk through the pathway.\"}, {\"name\": \"stairCount\", \"type\": [\"null\", \"int\"], \"default\": null, \"doc\": \"Number of stairs of the pathway.\"}, {\"name\": \"maxSlope\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Maximum slope of the pathway, in percent.\"}, {\"name\": \"minWidth\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Minimum width of the pathway, in meters.\"}, {\"name\": \"signpostedAs\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Signposting information for the pathway.\"}, {\"name\": \"reversedSignpostedAs\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Reversed signposting information for the pathway.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.pathwayId=str(self.pathwayId)
        self.fromStopId=str(self.fromStopId)
        self.toStopId=str(self.toStopId)
        self.pathwayMode=int(self.pathwayMode)
        self.isBidirectional=int(self.isBidirectional)
        self.length=float(self.length) if self.length else None
        self.traversalTime=int(self.traversalTime) if self.traversalTime else None
        self.stairCount=int(self.stairCount) if self.stairCount else None
        self.maxSlope=float(self.maxSlope) if self.maxSlope else None
        self.minWidth=float(self.minWidth) if self.minWidth else None
        self.signpostedAs=str(self.signpostedAs) if self.signpostedAs else None
        self.reversedSignpostedAs=str(self.reversedSignpostedAs) if self.reversedSignpostedAs else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Pathways':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Pathways']:
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
            return Pathways.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Pathways.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')