""" RoadEvent dataclass. """

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
class RoadEvent:
    """
    Real-time road situation record from the French national non-conceded road network.
    Attributes:
        situation_id (str): Unique identifier of the parent DATEX II situation.
        record_id (str): Unique identifier of this situation record within the parent situation.
        version (str): Version number of the parent situation.
        severity (typing.Optional[str]): Overall severity of the parent situation.
        record_type (str): DATEX II xsi:type of the situation record.
        probability (typing.Optional[str]): Probability of occurrence of the event.
        latitude (typing.Optional[float]): WGS84 latitude of the event location.
        longitude (typing.Optional[float]): WGS84 longitude of the event location.
        road_number (typing.Optional[str]): Road identifier (e.g. N20, A10).
        town_name (typing.Optional[str]): Name of the nearest town.
        direction (typing.Optional[str]): Direction of traffic affected.
        description (typing.Optional[str]): Human-readable description of the event.
        location_description (typing.Optional[str]): Human-readable description of the event location.
        source_name (typing.Optional[str]): Name of the publishing organization.
        validity_status (typing.Optional[str]): Validity status of the situation record.
        overall_start_time (typing.Optional[str]): ISO 8601 start time of the event validity period.
        overall_end_time (typing.Optional[str]): ISO 8601 end time of the event validity period.
        creation_time (str): ISO 8601 timestamp when the situation record was first created.
        observation_time (typing.Optional[str]): ISO 8601 timestamp of the most recent observation."""
    
    situation_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="situation_id"))
    record_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="record_id"))
    version: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    severity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    record_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="record_type"))
    probability: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="probability"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    road_number: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="road_number"))
    town_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="town_name"))
    direction: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    location_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_description"))
    source_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_name"))
    validity_status: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="validity_status"))
    overall_start_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="overall_start_time"))
    overall_end_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="overall_end_time"))
    creation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="creation_time"))
    observation_time: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"RoadEvent\", \"namespace\": \"fr.gouv.transport.bison_fute\", \"doc\": \"Real-time road situation record from the French national non-conceded road network.\", \"fields\": [{\"name\": \"situation_id\", \"type\": \"string\", \"doc\": \"Unique identifier of the parent DATEX II situation.\"}, {\"name\": \"record_id\", \"type\": \"string\", \"doc\": \"Unique identifier of this situation record within the parent situation.\"}, {\"name\": \"version\", \"type\": \"string\", \"doc\": \"Version number of the parent situation.\"}, {\"name\": \"severity\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Overall severity of the parent situation.\"}, {\"name\": \"record_type\", \"type\": \"string\", \"doc\": \"DATEX II xsi:type of the situation record.\"}, {\"name\": \"probability\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Probability of occurrence of the event.\"}, {\"name\": \"latitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS84 latitude of the event location.\"}, {\"name\": \"longitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS84 longitude of the event location.\"}, {\"name\": \"road_number\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Road identifier (e.g. N20, A10).\"}, {\"name\": \"town_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Name of the nearest town.\"}, {\"name\": \"direction\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Direction of traffic affected.\"}, {\"name\": \"description\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Human-readable description of the event.\"}, {\"name\": \"location_description\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Human-readable description of the event location.\"}, {\"name\": \"source_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Name of the publishing organization.\"}, {\"name\": \"validity_status\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Validity status of the situation record.\"}, {\"name\": \"overall_start_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 8601 start time of the event validity period.\"}, {\"name\": \"overall_end_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 8601 end time of the event validity period.\"}, {\"name\": \"creation_time\", \"type\": \"string\", \"doc\": \"ISO 8601 timestamp when the situation record was first created.\"}, {\"name\": \"observation_time\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 8601 timestamp of the most recent observation.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.situation_id=str(self.situation_id)
        self.record_id=str(self.record_id)
        self.version=str(self.version)
        self.severity=str(self.severity) if self.severity else None
        self.record_type=str(self.record_type)
        self.probability=str(self.probability) if self.probability else None
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None
        self.road_number=str(self.road_number) if self.road_number else None
        self.town_name=str(self.town_name) if self.town_name else None
        self.direction=str(self.direction) if self.direction else None
        self.description=str(self.description) if self.description else None
        self.location_description=str(self.location_description) if self.location_description else None
        self.source_name=str(self.source_name) if self.source_name else None
        self.validity_status=str(self.validity_status) if self.validity_status else None
        self.overall_start_time=str(self.overall_start_time) if self.overall_start_time else None
        self.overall_end_time=str(self.overall_end_time) if self.overall_end_time else None
        self.creation_time=str(self.creation_time)
        self.observation_time=str(self.observation_time) if self.observation_time else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'RoadEvent':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['RoadEvent']:
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
            return RoadEvent.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return RoadEvent.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')