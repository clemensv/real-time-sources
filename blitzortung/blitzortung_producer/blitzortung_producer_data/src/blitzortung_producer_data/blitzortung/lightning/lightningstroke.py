""" LightningStroke dataclass. """

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
from blitzortung_producer_data.blitzortung.lightning.detectorparticipation import DetectorParticipation


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class LightningStroke:
    """
    Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed.
    Attributes:
        source_id (int): Upstream live-source identifier from the src field.
        stroke_id (str): Source-scoped stroke identifier from the upstream id field, stringified for key and subject resolution.
        event_time (str): ISO-8601 UTC timestamp derived from the upstream time field.
        event_timestamp_ms (int): Original upstream time value in Unix epoch milliseconds.
        latitude (float): Latitude of the located lightning stroke in decimal degrees.
        longitude (float): Longitude of the located lightning stroke in decimal degrees.
        server_id (typing.Optional[int]): Upstream server identifier from the srv field.
        server_delay_ms (typing.Optional[int]): Delay between the upstream server computing the stroke and sending it to the live client, in milliseconds.
        accuracy_diameter_m (typing.Optional[float]): Estimated accuracy diameter in meters from the upstream dev field.
        detector_participations (typing.List[DetectorParticipation]): Detector participation entries expanded from the upstream sta object."""
    
    source_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_id"))
    stroke_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stroke_id"))
    event_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_time"))
    event_timestamp_ms: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_timestamp_ms"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    server_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="server_id"))
    server_delay_ms: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="server_delay_ms"))
    accuracy_diameter_m: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="accuracy_diameter_m"))
    detector_participations: typing.List[DetectorParticipation]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="detector_participations"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"LightningStroke\", \"namespace\": \"Blitzortung.Lightning\", \"doc\": \"Live lightning-stroke event from the public LightningMaps / Blitzortung websocket feed.\", \"fields\": [{\"name\": \"source_id\", \"type\": \"int\", \"doc\": \"Upstream live-source identifier from the src field.\"}, {\"name\": \"stroke_id\", \"type\": \"string\", \"doc\": \"Source-scoped stroke identifier from the upstream id field, stringified for key and subject resolution.\"}, {\"name\": \"event_time\", \"type\": \"string\", \"doc\": \"ISO-8601 UTC timestamp derived from the upstream time field.\"}, {\"name\": \"event_timestamp_ms\", \"type\": \"long\", \"doc\": \"Original upstream time value in Unix epoch milliseconds.\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Latitude of the located lightning stroke in decimal degrees.\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Longitude of the located lightning stroke in decimal degrees.\"}, {\"name\": \"server_id\", \"type\": [\"null\", \"int\"], \"default\": null, \"doc\": \"Upstream server identifier from the srv field.\"}, {\"name\": \"server_delay_ms\", \"type\": [\"null\", \"int\"], \"default\": null, \"doc\": \"Delay between the upstream server computing the stroke and sending it to the live client, in milliseconds.\"}, {\"name\": \"accuracy_diameter_m\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Estimated accuracy diameter in meters from the upstream dev field.\"}, {\"name\": \"detector_participations\", \"type\": {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"DetectorParticipation\", \"doc\": \"One detector entry expanded from the upstream sta object on a live stroke.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"int\", \"doc\": \"Detector station identifier from the key of the upstream sta object.\"}, {\"name\": \"status\", \"type\": \"int\", \"doc\": \"Opaque integer status flag from the value of the upstream sta object.\"}]}}, \"default\": [], \"doc\": \"Detector participation entries expanded from the upstream sta object.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.source_id=int(self.source_id)
        self.stroke_id=str(self.stroke_id)
        self.event_time=str(self.event_time)
        self.event_timestamp_ms=int(self.event_timestamp_ms)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.server_id=int(self.server_id) if self.server_id else None
        self.server_delay_ms=int(self.server_delay_ms) if self.server_delay_ms else None
        self.accuracy_diameter_m=float(self.accuracy_diameter_m) if self.accuracy_diameter_m else None
        self.detector_participations=self.detector_participations if isinstance(self.detector_participations, list) else [v if isinstance(v, DetectorParticipation) else DetectorParticipation.from_serializer_dict(v) if v else None for v in self.detector_participations] if self.detector_participations else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'LightningStroke':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['LightningStroke']:
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
            return LightningStroke.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return LightningStroke.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')