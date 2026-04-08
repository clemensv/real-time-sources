""" Timeseries dataclass. """

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
from irceline_belgium_producer_data.be.irceline.statusinterval import StatusInterval


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Timeseries:
    """
    Reference event for one IRCELINE station-timeseries combination.
    Attributes:
        timeseries_id (str): Stable numeric timeseries identifier from id.
        label (str): Descriptive upstream timeseries label.
        uom (str): Published unit of measurement.
        station_id (str): Linked numeric station identifier from station.properties.id.
        station_label (str): Linked station label from station.properties.label.
        latitude (typing.Optional[float]): Linked station latitude from station.geometry.coordinates[1].
        longitude (typing.Optional[float]): Linked station longitude from station.geometry.coordinates[0].
        phenomenon_id (typing.Optional[str]): Measured phenomenon identifier from parameters.phenomenon.id.
        phenomenon_label (typing.Optional[str]): Measured phenomenon label from parameters.phenomenon.label.
        category_id (typing.Optional[str]): Category identifier from parameters.category.id.
        category_label (typing.Optional[str]): Category label from parameters.category.label.
        status_intervals (typing.Optional[typing.List[StatusInterval]]): Optional ordered array of status interval bands from the expanded timeseries metadata."""
    
    timeseries_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timeseries_id"))
    label: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="label"))
    uom: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uom"))
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_label: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_label"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    phenomenon_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="phenomenon_id"))
    phenomenon_label: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="phenomenon_label"))
    category_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category_id"))
    category_label: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="category_label"))
    status_intervals: typing.Optional[typing.List[StatusInterval]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status_intervals"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Timeseries\", \"namespace\": \"be.irceline\", \"doc\": \"Reference event for one IRCELINE station-timeseries combination.\", \"fields\": [{\"name\": \"timeseries_id\", \"type\": \"string\", \"doc\": \"Stable numeric timeseries identifier from id.\"}, {\"name\": \"label\", \"type\": \"string\", \"doc\": \"Descriptive upstream timeseries label.\"}, {\"name\": \"uom\", \"type\": \"string\", \"doc\": \"Published unit of measurement.\"}, {\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Linked numeric station identifier from station.properties.id.\"}, {\"name\": \"station_label\", \"type\": \"string\", \"doc\": \"Linked station label from station.properties.label.\"}, {\"name\": \"latitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Linked station latitude from station.geometry.coordinates[1].\"}, {\"name\": \"longitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Linked station longitude from station.geometry.coordinates[0].\"}, {\"name\": \"phenomenon_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Measured phenomenon identifier from parameters.phenomenon.id.\"}, {\"name\": \"phenomenon_label\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Measured phenomenon label from parameters.phenomenon.label.\"}, {\"name\": \"category_id\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Category identifier from parameters.category.id.\"}, {\"name\": \"category_label\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Category label from parameters.category.label.\"}, {\"name\": \"status_intervals\", \"type\": [\"null\", {\"type\": \"array\", \"items\": {\"type\": \"record\", \"name\": \"StatusInterval\", \"doc\": \"One threshold band from the IRCELINE statusIntervals expansion.\", \"fields\": [{\"name\": \"lower\", \"type\": \"string\", \"doc\": \"Inclusive lower threshold boundary.\"}, {\"name\": \"upper\", \"type\": \"string\", \"doc\": \"Exclusive upper threshold boundary.\"}, {\"name\": \"name\", \"type\": \"string\", \"doc\": \"Human-readable band label.\"}, {\"name\": \"color\", \"type\": \"string\", \"doc\": \"Hex RGB display color.\"}]}}], \"default\": null, \"doc\": \"Optional ordered array of status interval bands from the expanded timeseries metadata.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.timeseries_id=str(self.timeseries_id)
        self.label=str(self.label)
        self.uom=str(self.uom)
        self.station_id=str(self.station_id)
        self.station_label=str(self.station_label)
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None
        self.phenomenon_id=str(self.phenomenon_id) if self.phenomenon_id else None
        self.phenomenon_label=str(self.phenomenon_label) if self.phenomenon_label else None
        self.category_id=str(self.category_id) if self.category_id else None
        self.category_label=str(self.category_label) if self.category_label else None
        self.status_intervals=self.status_intervals if isinstance(self.status_intervals, list) else [v if isinstance(v, StatusInterval) else StatusInterval.from_serializer_dict(v) if v else None for v in self.status_intervals] if self.status_intervals else None if self.status_intervals else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Timeseries':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Timeseries']:
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
            return Timeseries.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Timeseries.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')