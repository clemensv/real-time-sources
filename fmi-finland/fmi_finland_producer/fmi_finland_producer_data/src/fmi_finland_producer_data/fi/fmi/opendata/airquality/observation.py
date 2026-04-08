""" Observation dataclass. """

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
class Observation:
    """
    Hourly FMI air quality observation aggregated per station and timestamp.
    Attributes:
        fmisid (str): Stable FMI station identifier (fmisid) for the observing station.
        station_name (str): Station name resolved from station metadata or, if metadata lookup fails, the station identifier string.
        observation_time (str): Observation timestamp in UTC, formatted as an ISO-8601 instant such as 2024-01-15T13:00:00Z.
        aqindex (typing.Optional[float]): Finnish Air Quality Index 1-hour average.
        pm10_ug_m3 (typing.Optional[float]): PM10 particulate matter concentration 1-hour average in micrograms per cubic meter.
        pm2_5_ug_m3 (typing.Optional[float]): PM2.5 particulate matter concentration 1-hour average in micrograms per cubic meter.
        no2_ug_m3 (typing.Optional[float]): Nitrogen dioxide concentration 1-hour average in micrograms per cubic meter.
        o3_ug_m3 (typing.Optional[float]): Ozone concentration 1-hour average in micrograms per cubic meter.
        so2_ug_m3 (typing.Optional[float]): Sulfur dioxide concentration 1-hour average in micrograms per cubic meter.
        co_mg_m3 (typing.Optional[float]): Carbon monoxide concentration 1-hour average in milligrams per cubic meter."""
    
    fmisid: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fmisid"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    observation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    aqindex: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aqindex"))
    pm10_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_ug_m3"))
    pm2_5_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm2_5_ug_m3"))
    no2_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2_ug_m3"))
    o3_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3_ug_m3"))
    so2_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="so2_ug_m3"))
    co_mg_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="co_mg_m3"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Observation\", \"namespace\": \"fi.fmi.opendata.airquality\", \"doc\": \"Hourly FMI air quality observation aggregated per station and timestamp.\", \"fields\": [{\"name\": \"fmisid\", \"type\": \"string\", \"doc\": \"Stable FMI station identifier (fmisid) for the observing station.\"}, {\"name\": \"station_name\", \"type\": \"string\", \"doc\": \"Station name resolved from station metadata or, if metadata lookup fails, the station identifier string.\"}, {\"name\": \"observation_time\", \"type\": \"string\", \"doc\": \"Observation timestamp in UTC, formatted as an ISO-8601 instant such as 2024-01-15T13:00:00Z.\"}, {\"name\": \"aqindex\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Finnish Air Quality Index 1-hour average.\"}, {\"name\": \"pm10_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"PM10 particulate matter concentration 1-hour average in micrograms per cubic meter.\"}, {\"name\": \"pm2_5_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"PM2.5 particulate matter concentration 1-hour average in micrograms per cubic meter.\"}, {\"name\": \"no2_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Nitrogen dioxide concentration 1-hour average in micrograms per cubic meter.\"}, {\"name\": \"o3_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Ozone concentration 1-hour average in micrograms per cubic meter.\"}, {\"name\": \"so2_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Sulfur dioxide concentration 1-hour average in micrograms per cubic meter.\"}, {\"name\": \"co_mg_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Carbon monoxide concentration 1-hour average in milligrams per cubic meter.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.fmisid=str(self.fmisid)
        self.station_name=str(self.station_name)
        self.observation_time=str(self.observation_time)
        self.aqindex=float(self.aqindex) if self.aqindex else None
        self.pm10_ug_m3=float(self.pm10_ug_m3) if self.pm10_ug_m3 else None
        self.pm2_5_ug_m3=float(self.pm2_5_ug_m3) if self.pm2_5_ug_m3 else None
        self.no2_ug_m3=float(self.no2_ug_m3) if self.no2_ug_m3 else None
        self.o3_ug_m3=float(self.o3_ug_m3) if self.o3_ug_m3 else None
        self.so2_ug_m3=float(self.so2_ug_m3) if self.so2_ug_m3 else None
        self.co_mg_m3=float(self.co_mg_m3) if self.co_mg_m3 else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Observation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Observation']:
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
            return Observation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Observation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')