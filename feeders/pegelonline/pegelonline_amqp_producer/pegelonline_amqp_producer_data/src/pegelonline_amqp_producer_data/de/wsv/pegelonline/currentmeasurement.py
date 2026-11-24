""" CurrentMeasurement dataclass. """

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
class CurrentMeasurement:
    """
    Latest 15-minute water-level reading for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Carries only the W (water-level) timeseries; other timeseries (Q discharge, LT water temperature) are not emitted by this source.
    Attributes:
        station_id (str): Stable UUID of the gauge this reading was taken at. References the `station_id` of the corresponding Station reference event. Used as the CloudEvents `subject` and the Kafka partition key so all readings for a given gauge land on the same partition / topic key.
        timestamp (str): Wall-clock time the upstream reading was taken, in ISO 8601 / RFC 3339 with an explicit UTC offset. PegelOnline publishes the value in Europe/Berlin local time, so the offset shifts between `+01:00` (CET) and `+02:00` (CEST) across the DST boundary — preserve the offset when storing. Sourced from the upstream `timestamp` field.
        value (float): Water-level reading on the W (water-level) timeseries, in centimetres above the gauge's Pegelnullpunkt (PNP — a geodetically fixed datum specific to each gauge, see https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Typical operational range is 0–1500 cm; flood events at major Rhine gauges can exceed 1000 cm. Negative readings are valid at gauges whose normal pool is below PNP (e.g. tidal Elbe at low water). Unit: cm. [minimum: -1000, maximum: 2500]
        stateMnwMhw (typing.Optional[str]): Categorical classification of the current water level against the gauge's long-term mean low water (MNW) and mean high water (MHW) reference values, as computed by the upstream feed. Omitted by upstream when the gauge has no MNW/MHW reference series configured (treat absence as 'unknown').
        stateNswHsw (typing.Optional[str]): Categorical classification of the current water level against the highest navigable water level (HSW) reference for the reach, as computed by the upstream feed. Drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Note: upstream never emits 'low' on this series — HSW is an upper bound only. Omitted by upstream when the gauge has no HSW reference (treat absence as 'unknown').
        trend (typing.Optional[int]): Short-term trend of the water level relative to the previous reading, as classified by the upstream feed. First-class signal for flood-monitoring dashboards. Sourced from the upstream `trend` field; omitted when upstream cannot compute a trend (e.g. first reading after a gap)."""


    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    stateMnwMhw: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stateMnwMhw"))
    stateNswHsw: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stateNswHsw"))
    trend: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="trend"))

    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"CurrentMeasurement\", \"namespace\": \"de.wsv.pegelonline\", \"doc\": \"Latest 15-minute water-level reading for one WSV PegelOnline gauge. Sourced from `GET /stations/{uuid}/W/currentmeasurement.json` on the PegelOnline REST API v2. Carries only the W (water-level) timeseries; other timeseries (Q discharge, LT water temperature) are not emitted by this source.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Stable UUID of the gauge this reading was taken at. References the `station_id` of the corresponding Station reference event. Used as the CloudEvents `subject` and the Kafka partition key so all readings for a given gauge land on the same partition / topic key.\"}, {\"name\": \"timestamp\", \"type\": {\"type\": \"string\", \"x-original-logical-type\": \"rfc3339-timestamp-millis\"}, \"doc\": \"Wall-clock time the upstream reading was taken, in ISO 8601 / RFC 3339 with an explicit UTC offset. PegelOnline publishes the value in Europe/Berlin local time, so the offset shifts between `+01:00` (CET) and `+02:00` (CEST) across the DST boundary \u2014 preserve the offset when storing. Sourced from the upstream `timestamp` field.\"}, {\"name\": \"value\", \"type\": \"double\", \"doc\": \"Water-level reading on the W (water-level) timeseries, in centimetres above the gauge's Pegelnullpunkt (PNP \u2014 a geodetically fixed datum specific to each gauge, see https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json). Typical operational range is 0\u20131500 cm; flood events at major Rhine gauges can exceed 1000 cm. Negative readings are valid at gauges whose normal pool is below PNP (e.g. tidal Elbe at low water). Unit: cm. [minimum: -1000, maximum: 2500]\"}, {\"name\": \"stateMnwMhw\", \"type\": [\"null\", \"string\"], \"doc\": \"Categorical classification of the current water level against the gauge's long-term mean low water (MNW) and mean high water (MHW) reference values, as computed by the upstream feed. Omitted by upstream when the gauge has no MNW/MHW reference series configured (treat absence as 'unknown').\", \"default\": null}, {\"name\": \"stateNswHsw\", \"type\": [\"null\", \"string\"], \"doc\": \"Categorical classification of the current water level against the highest navigable water level (HSW) reference for the reach, as computed by the upstream feed. Drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Note: upstream never emits 'low' on this series \u2014 HSW is an upper bound only. Omitted by upstream when the gauge has no HSW reference (treat absence as 'unknown').\", \"default\": null}, {\"name\": \"trend\", \"type\": [\"int\", \"null\"], \"doc\": \"Short-term trend of the water level relative to the previous reading, as classified by the upstream feed. First-class signal for flood-monitoring dashboards. Sourced from the upstream `trend` field; omitted when upstream cannot compute a trend (e.g. first reading after a gap).\", \"default\": null}]}"), avro.name.Names()
    )


    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.timestamp=str(self.timestamp)
        self.value=float(self.value)
        self.stateMnwMhw=(str(self.stateMnwMhw)) if self.stateMnwMhw is not None else None
        self.stateNswHsw=(str(self.stateNswHsw)) if self.stateNswHsw is not None else None
        self.trend=(int(self.trend)) if self.trend is not None else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'CurrentMeasurement':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
        """
        data = dict(data)
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
            if isinstance(result, str):
                result = result.encode('utf-8')

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['CurrentMeasurement']:
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
            return CurrentMeasurement.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return CurrentMeasurement.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')