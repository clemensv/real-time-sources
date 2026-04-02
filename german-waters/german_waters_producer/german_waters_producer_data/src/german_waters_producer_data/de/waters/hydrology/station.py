""" Station dataclass. """

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
class Station:
    """
    Station
    Attributes:
        station_id (str): 
        station_name (str): 
        water_body (str): 
        state (typing.Optional[str]): 
        region (typing.Optional[str]): 
        provider (str): 
        latitude (typing.Optional[float]): 
        longitude (typing.Optional[float]): 
        river_km (typing.Optional[float]): 
        altitude (typing.Optional[float]): 
        station_type (typing.Optional[str]): 
        warn_level_cm (typing.Optional[float]): 
        alarm_level_cm (typing.Optional[float]): 
        warn_level_m3s (typing.Optional[float]): 
        alarm_level_m3s (typing.Optional[float]): """
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    station_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_name"))
    water_body: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_body"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))
    provider: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="provider"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    river_km: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="river_km"))
    altitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude"))
    station_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_type"))
    warn_level_cm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="warn_level_cm"))
    alarm_level_cm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alarm_level_cm"))
    warn_level_m3s: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="warn_level_m3s"))
    alarm_level_m3s: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alarm_level_m3s"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Station\", \"doc\": \"Station\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\"}, {\"name\": \"station_name\", \"type\": \"string\"}, {\"name\": \"water_body\", \"type\": \"string\"}, {\"name\": \"state\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"region\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"provider\", \"type\": \"string\"}, {\"name\": \"latitude\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"longitude\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"river_km\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"altitude\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"station_type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"warn_level_cm\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"alarm_level_cm\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"warn_level_m3s\", \"type\": [\"null\", \"double\"], \"default\": null}, {\"name\": \"alarm_level_m3s\", \"type\": [\"null\", \"double\"], \"default\": null}], \"namespace\": \"DE.Waters.Hydrology\"}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.station_name=str(self.station_name)
        self.water_body=str(self.water_body)
        self.state=str(self.state) if self.state else None
        self.region=str(self.region) if self.region else None
        self.provider=str(self.provider)
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None
        self.river_km=float(self.river_km) if self.river_km else None
        self.altitude=float(self.altitude) if self.altitude else None
        self.station_type=str(self.station_type) if self.station_type else None
        self.warn_level_cm=float(self.warn_level_cm) if self.warn_level_cm else None
        self.alarm_level_cm=float(self.alarm_level_cm) if self.alarm_level_cm else None
        self.warn_level_m3s=float(self.warn_level_m3s) if self.warn_level_m3s else None
        self.alarm_level_m3s=float(self.alarm_level_m3s) if self.alarm_level_m3s else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
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
            return Station.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')