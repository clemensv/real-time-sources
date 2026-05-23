""" LightningStroke dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
from __future__ import annotations
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import json
import avro.schema
import avro.io
from blitzortung_producer_data.detectorparticipation import DetectorParticipation


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class LightningStroke:
    """
    One located lightning stroke from the public LightningMaps / Blitzortung live websocket feed. The stroke identity is the tuple of source_id and stroke_id because the upstream browser client tracks the last seen stroke id separately for each source stream.
    
    Attributes:
        source_id (int)
        stroke_id (str)
        event_time (str)
        event_timestamp_ms (int)
        latitude (float)
        longitude (float)
        server_id (typing.Optional[int])
        server_delay_ms (typing.Optional[int])
        accuracy_diameter_m (typing.Optional[float])
        detector_participations (typing.List[DetectorParticipation])
        geohash5 (str)
        geohash7 (str)
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "[{\"type\": \"record\", \"name\": \"LightningStroke\", \"doc\": \"One located lightning stroke from the public LightningMaps / Blitzortung live websocket feed. The stroke identity is the tuple of source_id and stroke_id because the upstream browser client tracks the last seen stroke id separately for each source stream.\", \"fields\": [{\"name\": \"source_id\", \"type\": \"int\", \"doc\": \"Upstream live-source identifier from the src field. The public LightningMaps websocket treats stroke ids as source-scoped, so this field is part of the stable event identity. [minimum: 0]\"}, {\"name\": \"stroke_id\", \"type\": \"string\", \"doc\": \"Source-scoped stroke identifier from the upstream id field, stringified so the Kafka key and CloudEvents subject can be resolved directly from the payload.\"}, {\"name\": \"event_time\", \"type\": \"string\", \"doc\": \"ISO-8601 UTC timestamp derived from the upstream time field, which the public live websocket emits in Unix epoch milliseconds.\"}, {\"name\": \"event_timestamp_ms\", \"type\": \"long\", \"doc\": \"Original upstream time value in Unix epoch milliseconds from the public live websocket. [minimum: 0]\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Latitude of the located lightning stroke in decimal degrees from the upstream lat field. [minimum: -90.0, maximum: 90.0]\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Longitude of the located lightning stroke in decimal degrees from the upstream lon field. [minimum: -180.0, maximum: 180.0]\"}, {\"name\": \"server_id\", \"type\": [\"int\", \"null\"], \"doc\": \"Upstream server identifier from the srv field that produced the current live batch. The public documentation reviewed during implementation does not publish a stable human-readable enumeration for these ids. [minimum: 0]\", \"default\": null}, {\"name\": \"server_delay_ms\", \"type\": [\"int\", \"null\"], \"doc\": \"Delay between the upstream server receiving or computing the stroke and sending it to the live client, in milliseconds, from the public del field. [minimum: 0]\", \"default\": null}, {\"name\": \"accuracy_diameter_m\", \"type\": [\"double\", \"null\"], \"doc\": \"Estimated accuracy diameter in meters from the upstream dev field. The public LightningMaps client renders an accuracy circle with radius dev/2, which indicates the value is expressed as a diameter rather than a raw algorithm score. [minimum: 0.0]\", \"default\": null}, {\"name\": \"detector_participations\", \"type\": {\"type\": \"array\", \"items\": \"DetectorParticipation\"}, \"doc\": \"Detector participation entries expanded from the upstream sta object when the client asks the public live feed to include station details. An empty array means the upstream batch did not include detector participation details for this stroke.\"}, {\"name\": \"geohash5\", \"type\": \"string\", \"doc\": \"5-character geohash of the located stroke (~40 km cell at the equator), derived in the bridge from latitude and longitude. Used as the {geohash5} MQTT topic segment for geographic wildcards. [pattern: ^[0-9b-hjkmnp-z]{5}$]\"}, {\"name\": \"geohash7\", \"type\": \"string\", \"doc\": \"7-character geohash of the located stroke (~153 m cell), derived from latitude and longitude. Used as the {geohash7} MQTT topic segment for fine-grained geographic wildcards. [pattern: ^[0-9b-hjkmnp-z]{7}$]\"}]}, {\"type\": \"record\", \"name\": \"DetectorParticipation\", \"doc\": \"One detector entry expanded from the upstream sta object on a live stroke. The public feed exposes integer status flags per station, but the public documentation does not currently publish a bit-level meaning for those status codes, so this contract preserves the upstream integer verbatim.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"int\", \"doc\": \"Detector station identifier from the key of the upstream sta object. [minimum: 0]\"}, {\"name\": \"status\", \"type\": \"int\", \"doc\": \"Opaque integer status flag from the value of the upstream sta object. The public live feed exposes the value, but the public documentation reviewed during implementation does not publish a stable bit-level interpretation. [minimum: 0]\"}]}]"
    )
    
    
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
    geohash5: str=dataclasses.field(default="00000", kw_only=True, metadata=dataclasses_json.config(field_name="geohash5"))
    geohash7: str=dataclasses.field(default="0000000", kw_only=True, metadata=dataclasses_json.config(field_name="geohash7"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'LightningStroke':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'LightningStroke':
        """
        Converts a dictionary from Avro deserialization to a dataclass instance.
        Handles conversion of string representations back to Python types for
        extended logical types.
        
        Args:
            data: The dictionary from Avro deserialization.
        
        Returns:
            The dataclass representation.
        """
        # Convert string values back to Python types for Avro string-based logical types
        converted = data.copy()
        if 'source_id' in converted and converted['source_id'] is not None:
            value = converted['source_id']
        if 'stroke_id' in converted and converted['stroke_id'] is not None:
            value = converted['stroke_id']
        if 'event_time' in converted and converted['event_time'] is not None:
            value = converted['event_time']
        if 'event_timestamp_ms' in converted and converted['event_timestamp_ms'] is not None:
            value = converted['event_timestamp_ms']
        if 'latitude' in converted and converted['latitude'] is not None:
            value = converted['latitude']
        if 'longitude' in converted and converted['longitude'] is not None:
            value = converted['longitude']
        if 'server_id' in converted and converted['server_id'] is not None:
            value = converted['server_id']
        if 'server_delay_ms' in converted and converted['server_delay_ms'] is not None:
            value = converted['server_delay_ms']
        if 'accuracy_diameter_m' in converted and converted['accuracy_diameter_m'] is not None:
            value = converted['accuracy_diameter_m']
        if 'detector_participations' in converted and converted['detector_participations'] is not None:
            value = converted['detector_participations']
        if 'geohash5' in converted and converted['geohash5'] is not None:
            value = converted['geohash5']
        if 'geohash7' in converted and converted['geohash7'] is not None:
            value = converted['geohash7']
        
        return cls(**converted)

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
            if isinstance(v, enum.Enum):
                return v.value
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_avro_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary suitable for Avro serialization.
        Handles conversion of Python types to Avro-compatible string representations
        for extended logical types.

        Returns:
            The dictionary representation suitable for Avro serialization.
        """
        result = self.to_serializer_dict()
        converted = result.copy()
        
        # Convert specific fields based on their source types
        
        return converted

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'application/json': Encodes the data to JSON format.
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
            # Convert to Avro binary format using the embedded schema
            writer = avro.io.DatumWriter(self.AvroType)
            with io.BytesIO() as stream:
                encoder = avro.io.BinaryEncoder(stream)
                writer.write(self.to_avro_dict(), encoder)
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
                    'application/json': Attempts to decode the data from JSON encoded format.
                    'avro/binary': Attempts to decode the data from Avro binary format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            if isinstance(data, bytes):
                # Decode from Avro binary format using the embedded schema
                reader = avro.io.DatumReader(cls.AvroType)
                with io.BytesIO(data) as stream:
                    decoder = avro.io.BinaryDecoder(stream)
                    _record = reader.read(decoder)
                    return LightningStroke.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return LightningStroke.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'LightningStroke':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            source_id=int(81),
            stroke_id='nymikanyecdzhmmrechg',
            event_time='dmemuavsjphuipqdzvxb',
            event_timestamp_ms=int(48),
            latitude=float(70.64115031622048),
            longitude=float(89.46994491723731),
            server_id=int(16),
            server_delay_ms=int(83),
            accuracy_diameter_m=float(39.37401912582803),
            detector_participations=[None],
            geohash5='vdzypgvcrqigzvrdslil',
            geohash7='espheibxrbwqysakyhlb'
        )