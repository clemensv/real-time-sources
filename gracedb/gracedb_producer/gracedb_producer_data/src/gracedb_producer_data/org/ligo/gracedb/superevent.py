""" Superevent dataclass. """

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
class Superevent:
    """
    A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.
    Attributes:
        superevent_id (str): Unique identifier for the superevent assigned by GraceDB, e.g. 'S240414a' for production events or 'MS260408x' for MDC (mock data challenge) events.
        category (str): Category of the superevent. 'Production' for real observing-run candidates, 'MDC' for mock data challenge injections, 'Test' for engineering/test events.
        created (str): ISO-8601 UTC timestamp when the superevent was first created in GraceDB, e.g. '2026-04-08 23:59:34 UTC'.
        t_start (float): GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the start of the superevent time window.
        t_0 (float): GPS time (seconds since 1980-01-06T00:00:00 UTC) of the central trigger time for this superevent.
        t_end (float): GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the end of the superevent time window.
        far (float): False alarm rate in Hz. Lower values indicate a more significant event.
        time_coinc_far (typing.Optional[float]): Time-coincidence false alarm rate in Hz from the RAVEN pipeline. Null if no external coincidence was evaluated.
        space_coinc_far (typing.Optional[float]): Space-and-time-coincidence false alarm rate in Hz from the RAVEN pipeline. Null if no external coincidence was evaluated.
        labels_json (str): JSON-encoded array of label strings attached to this superevent.
        preferred_event_id (typing.Optional[str]): GraceDB event ID of the preferred pipeline event associated with this superevent. Null if no preferred event has been selected.
        pipeline (typing.Optional[str]): Name of the detection pipeline that produced the preferred event, e.g. 'gstlal', 'MBTAOnline', 'SPIIR', 'PyCBC'. Null if not set.
        group (typing.Optional[str]): Physics group of the preferred event: 'CBC' (compact binary coalescence), 'Burst' (unmodeled transient), or 'Test'. Null if not set.
        instruments (typing.Optional[str]): Comma-separated list of detector instruments that contributed to the preferred event, e.g. 'H1,L1,V1'. Null if not set.
        gw_id (typing.Optional[str]): Official gravitational wave event name assigned after confirmation. Null if the event has not been confirmed or named.
        submitter (str): Username or service account that submitted the superevent to GraceDB.
        em_type (typing.Optional[str]): Identifier of the associated electromagnetic event from an external trigger. Null if no external EM association exists.
        search (typing.Optional[str]): Search type of the preferred event: 'AllSky', 'MDC', 'BBH', 'EarlyWarning'. Null if not set.
        far_is_upper_limit (typing.Optional[bool]): Whether the reported FAR value is an upper limit rather than an exact estimate. Null if not set.
        nevents (typing.Optional[int]): Number of pipeline events aggregated into this superevent. Null if not available.
        self_uri (str): HATEOAS self link for the superevent resource in the GraceDB REST API."""
    
    superevent_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="superevent_id"))
    category: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category"))
    created: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created"))
    t_start: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="t_start"))
    t_0: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="t_0"))
    t_end: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="t_end"))
    far: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="far"))
    time_coinc_far: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_coinc_far"))
    space_coinc_far: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="space_coinc_far"))
    labels_json: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="labels_json"))
    preferred_event_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="preferred_event_id"))
    pipeline: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pipeline"))
    group: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="group"))
    instruments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instruments"))
    gw_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gw_id"))
    submitter: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="submitter"))
    em_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="em_type"))
    search: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="search"))
    far_is_upper_limit: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="far_is_upper_limit"))
    nevents: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nevents"))
    self_uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="self_uri"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Superevent\", \"namespace\": \"org.ligo.gracedb\", \"doc\": \"A gravitational wave candidate superevent from the LIGO/Virgo/KAGRA collaboration, published via GraceDB. A superevent aggregates one or more pipeline detections into a single candidate and carries significance, classification, and alert-lifecycle metadata.\", \"fields\": [{\"name\": \"superevent_id\", \"type\": \"string\", \"doc\": \"Unique identifier for the superevent assigned by GraceDB, e.g. 'S240414a' for production events or 'MS260408x' for MDC (mock data challenge) events.\"}, {\"name\": \"category\", \"type\": \"string\", \"doc\": \"Category of the superevent. 'Production' for real observing-run candidates, 'MDC' for mock data challenge injections, 'Test' for engineering/test events.\"}, {\"name\": \"created\", \"type\": \"string\", \"doc\": \"ISO-8601 UTC timestamp when the superevent was first created in GraceDB, e.g. '2026-04-08 23:59:34 UTC'.\"}, {\"name\": \"t_start\", \"type\": \"double\", \"doc\": \"GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the start of the superevent time window.\"}, {\"name\": \"t_0\", \"type\": \"double\", \"doc\": \"GPS time (seconds since 1980-01-06T00:00:00 UTC) of the central trigger time for this superevent.\"}, {\"name\": \"t_end\", \"type\": \"double\", \"doc\": \"GPS time (seconds since 1980-01-06T00:00:00 UTC) marking the end of the superevent time window.\"}, {\"name\": \"far\", \"type\": \"double\", \"doc\": \"False alarm rate in Hz. Lower values indicate a more significant event.\"}, {\"name\": \"time_coinc_far\", \"type\": [\"double\", \"null\"], \"doc\": \"Time-coincidence false alarm rate in Hz from the RAVEN pipeline. Null if no external coincidence was evaluated.\"}, {\"name\": \"space_coinc_far\", \"type\": [\"double\", \"null\"], \"doc\": \"Space-and-time-coincidence false alarm rate in Hz from the RAVEN pipeline. Null if no external coincidence was evaluated.\"}, {\"name\": \"labels_json\", \"type\": \"string\", \"doc\": \"JSON-encoded array of label strings attached to this superevent.\"}, {\"name\": \"preferred_event_id\", \"type\": [\"string\", \"null\"], \"doc\": \"GraceDB event ID of the preferred pipeline event associated with this superevent. Null if no preferred event has been selected.\"}, {\"name\": \"pipeline\", \"type\": [\"string\", \"null\"], \"doc\": \"Name of the detection pipeline that produced the preferred event, e.g. 'gstlal', 'MBTAOnline', 'SPIIR', 'PyCBC'. Null if not set.\"}, {\"name\": \"group\", \"type\": [\"string\", \"null\"], \"doc\": \"Physics group of the preferred event: 'CBC' (compact binary coalescence), 'Burst' (unmodeled transient), or 'Test'. Null if not set.\"}, {\"name\": \"instruments\", \"type\": [\"string\", \"null\"], \"doc\": \"Comma-separated list of detector instruments that contributed to the preferred event, e.g. 'H1,L1,V1'. Null if not set.\"}, {\"name\": \"gw_id\", \"type\": [\"string\", \"null\"], \"doc\": \"Official gravitational wave event name assigned after confirmation. Null if the event has not been confirmed or named.\"}, {\"name\": \"submitter\", \"type\": \"string\", \"doc\": \"Username or service account that submitted the superevent to GraceDB.\"}, {\"name\": \"em_type\", \"type\": [\"string\", \"null\"], \"doc\": \"Identifier of the associated electromagnetic event from an external trigger. Null if no external EM association exists.\"}, {\"name\": \"search\", \"type\": [\"string\", \"null\"], \"doc\": \"Search type of the preferred event: 'AllSky', 'MDC', 'BBH', 'EarlyWarning'. Null if not set.\"}, {\"name\": \"far_is_upper_limit\", \"type\": [\"boolean\", \"null\"], \"doc\": \"Whether the reported FAR value is an upper limit rather than an exact estimate. Null if not set.\"}, {\"name\": \"nevents\", \"type\": [\"int\", \"null\"], \"doc\": \"Number of pipeline events aggregated into this superevent. Null if not available.\"}, {\"name\": \"self_uri\", \"type\": \"string\", \"doc\": \"HATEOAS self link for the superevent resource in the GraceDB REST API.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.superevent_id=str(self.superevent_id)
        self.category=str(self.category)
        self.created=str(self.created)
        self.t_start=float(self.t_start)
        self.t_0=float(self.t_0)
        self.t_end=float(self.t_end)
        self.far=float(self.far)
        self.time_coinc_far=float(self.time_coinc_far) if self.time_coinc_far else None
        self.space_coinc_far=float(self.space_coinc_far) if self.space_coinc_far else None
        self.labels_json=str(self.labels_json)
        self.preferred_event_id=str(self.preferred_event_id) if self.preferred_event_id else None
        self.pipeline=str(self.pipeline) if self.pipeline else None
        self.group=str(self.group) if self.group else None
        self.instruments=str(self.instruments) if self.instruments else None
        self.gw_id=str(self.gw_id) if self.gw_id else None
        self.submitter=str(self.submitter)
        self.em_type=str(self.em_type) if self.em_type else None
        self.search=str(self.search) if self.search else None
        self.far_is_upper_limit=bool(self.far_is_upper_limit) if self.far_is_upper_limit else None
        self.nevents=int(self.nevents) if self.nevents else None
        self.self_uri=str(self.self_uri)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Superevent':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Superevent']:
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
            return Superevent.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Superevent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')