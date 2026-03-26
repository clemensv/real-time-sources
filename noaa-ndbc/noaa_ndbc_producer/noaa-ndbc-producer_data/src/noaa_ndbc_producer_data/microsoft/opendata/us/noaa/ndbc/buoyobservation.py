""" BuoyObservation dataclass. """

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
class BuoyObservation:
    """
    A BuoyObservation record.
    Attributes:
        station_id (str): 
        latitude (float): 
        longitude (float): 
        timestamp (str): 
        wind_direction (float): 
        wind_speed (float): 
        gust (float): 
        wave_height (float): 
        dominant_wave_period (float): 
        average_wave_period (float): 
        mean_wave_direction (float): 
        pressure (float): 
        air_temperature (float): 
        water_temperature (float): 
        dewpoint (float): """
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    wind_direction: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_direction"))
    wind_speed: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    gust: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gust"))
    wave_height: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wave_height"))
    dominant_wave_period: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dominant_wave_period"))
    average_wave_period: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="average_wave_period"))
    mean_wave_direction: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mean_wave_direction"))
    pressure: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure"))
    air_temperature: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_temperature"))
    water_temperature: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water_temperature"))
    dewpoint: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dewpoint"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"BuoyObservation\", \"namespace\": \"Microsoft.OpenData.US.NOAA.NDBC\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\"}, {\"name\": \"latitude\", \"type\": \"double\"}, {\"name\": \"longitude\", \"type\": \"double\"}, {\"name\": \"timestamp\", \"type\": \"string\"}, {\"name\": \"wind_direction\", \"type\": \"double\"}, {\"name\": \"wind_speed\", \"type\": \"double\"}, {\"name\": \"gust\", \"type\": \"double\"}, {\"name\": \"wave_height\", \"type\": \"double\"}, {\"name\": \"dominant_wave_period\", \"type\": \"double\"}, {\"name\": \"average_wave_period\", \"type\": \"double\"}, {\"name\": \"mean_wave_direction\", \"type\": \"double\"}, {\"name\": \"pressure\", \"type\": \"double\"}, {\"name\": \"air_temperature\", \"type\": \"double\"}, {\"name\": \"water_temperature\", \"type\": \"double\"}, {\"name\": \"dewpoint\", \"type\": \"double\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.timestamp=str(self.timestamp)
        self.wind_direction=float(self.wind_direction)
        self.wind_speed=float(self.wind_speed)
        self.gust=float(self.gust)
        self.wave_height=float(self.wave_height)
        self.dominant_wave_period=float(self.dominant_wave_period)
        self.average_wave_period=float(self.average_wave_period)
        self.mean_wave_direction=float(self.mean_wave_direction)
        self.pressure=float(self.pressure)
        self.air_temperature=float(self.air_temperature)
        self.water_temperature=float(self.water_temperature)
        self.dewpoint=float(self.dewpoint)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'BuoyObservation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['BuoyObservation']:
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
            return BuoyObservation.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return BuoyObservation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')