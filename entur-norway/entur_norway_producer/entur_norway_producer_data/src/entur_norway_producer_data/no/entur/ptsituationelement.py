""" PtSituationElement dataclass. """

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
from entur_norway_producer_data.no.entur.validityperiod import ValidityPeriod


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PtSituationElement:
    """
    Real-time transit disruption or service alert from the Entur SIRI-SX feed.
    Attributes:
        situation_number (str): Unique situation identifier (SituationNumber). Example: RUT:SituationNumber:12345.
        version (typing.Optional[str]): Situation version number.
        creation_time (str): ISO 8601 UTC creation time (CreationTime).
        source_type (typing.Optional[str]): Source type: directReport, email, phone, post, feed, radio, tv, web, pager, text, other.
        source_name (typing.Optional[str]): Name of originating source or organisation.
        progress (typing.Optional[str]): Publication progress: open, published, closing, closed.
        severity (typing.Optional[str]): SIRI Severity: unknown, noImpact, verySlight, slight, normal, severe, verySevere, undefined.
        keywords (typing.Optional[str]): Space-separated keywords from the SIRI Keywords element.
        summary (typing.Optional[str]): Short public summary text from Summary element.
        description (typing.Optional[str]): Full public description text from Description element.
        validity_periods (typing.List[ValidityPeriod]): One or more active validity windows for this situation.
        affects_line_refs (typing.List[str]): LineRef values from AffectedLine elements.
        affects_stop_point_refs (typing.List[str]): StopPointRef values from AffectedStopPoint elements."""
    
    situation_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_number"))
    version: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    creation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="creation_time"))
    source_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_type"))
    source_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_name"))
    progress: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="progress"))
    severity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    keywords: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="keywords"))
    summary: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="summary"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    validity_periods: typing.List[ValidityPeriod]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="validity_periods"))
    affects_line_refs: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="affects_line_refs"))
    affects_stop_point_refs: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="affects_stop_point_refs"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"PtSituationElement\", \"namespace\": \"no.entur\", \"doc\": \"Real-time transit disruption or service alert from the Entur SIRI-SX feed.\", \"fields\": [{\"name\": \"situation_number\", \"type\": \"string\", \"doc\": \"Unique situation identifier (SituationNumber). Example: RUT:SituationNumber:12345.\"}, {\"name\": \"version\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Situation version number.\"}, {\"name\": \"creation_time\", \"type\": \"string\", \"doc\": \"ISO 8601 UTC creation time (CreationTime).\"}, {\"name\": \"source_type\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Source type: directReport, email, phone, post, feed, radio, tv, web, pager, text, other.\"}, {\"name\": \"source_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Name of originating source or organisation.\"}, {\"name\": \"progress\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Publication progress: open, published, closing, closed.\"}, {\"name\": \"severity\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"SIRI Severity: unknown, noImpact, verySlight, slight, normal, severe, verySevere, undefined.\"}, {\"name\": \"keywords\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Space-separated keywords from the SIRI Keywords element.\"}, {\"name\": \"summary\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Short public summary text from Summary element.\"}, {\"name\": \"description\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Full public description text from Description element.\"}, {\"name\": \"validity_periods\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"ValidityPeriod\", \"namespace\": \"no.entur\", \"doc\": \"An active validity window for a situation.\", \"fields\": [{\"name\": \"start_time\", \"type\": \"string\", \"doc\": \"ISO 8601 UTC start time.\"}, {\"name\": \"end_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 8601 UTC end time, null if open-ended.\"}]}}, \"doc\": \"One or more active validity windows for this situation.\"}, {\"name\": \"affects_line_refs\", \"type\": {\"type\": \"array\", \"items\": \"string\"}, \"doc\": \"LineRef values from AffectedLine elements.\"}, {\"name\": \"affects_stop_point_refs\", \"type\": {\"type\": \"array\", \"items\": \"string\"}, \"doc\": \"StopPointRef values from AffectedStopPoint elements.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.situation_number=str(self.situation_number)
        self.version=str(self.version) if self.version else None
        self.creation_time=str(self.creation_time)
        self.source_type=str(self.source_type) if self.source_type else None
        self.source_name=str(self.source_name) if self.source_name else None
        self.progress=str(self.progress) if self.progress else None
        self.severity=str(self.severity) if self.severity else None
        self.keywords=str(self.keywords) if self.keywords else None
        self.summary=str(self.summary) if self.summary else None
        self.description=str(self.description) if self.description else None
        self.validity_periods=self.validity_periods if isinstance(self.validity_periods, list) else [v if isinstance(v, ValidityPeriod) else ValidityPeriod.from_serializer_dict(v) if v else None for v in self.validity_periods] if self.validity_periods else None
        self.affects_line_refs=self.affects_line_refs if isinstance(self.affects_line_refs, list) else [str(v) for v in self.affects_line_refs] if self.affects_line_refs else None
        self.affects_stop_point_refs=self.affects_stop_point_refs if isinstance(self.affects_stop_point_refs, list) else [str(v) for v in self.affects_stop_point_refs] if self.affects_stop_point_refs else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PtSituationElement':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PtSituationElement']:
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
            return PtSituationElement.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return PtSituationElement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')