""" SensorInfo dataclass. """

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
class SensorInfo:
    """
    Reference data for a Sensor.Community sensor node including hardware type and latest known location metadata.
    Attributes:
        sensor_id (int): Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key.
        sensor_type_id (int): Numeric upstream identifier for the sensor hardware type, such as the Sensor.Community type id for SDS011 or BME280.
        sensor_type_name (str): Upstream sensor hardware type name published under sensor.sensor_type.name, for example SDS011, SPS30, BME280, or DHT22.
        sensor_type_manufacturer (str): Manufacturer name published by Sensor.Community for the sensor hardware type, taken from sensor.sensor_type.manufacturer.
        pin (str): Sensor pin designation reported by the upstream payload under sensor.pin.
        location_id (int): Stable integer identifier of the Sensor.Community location object associated with the reading.
        latitude (float): Latitude of the sensor location in WGS84 decimal degrees.
        longitude (float): Longitude of the sensor location in WGS84 decimal degrees.
        altitude (typing.Optional[float]): Altitude of the sensor location in meters above sea level when supplied by the upstream payload.
        country (str): ISO 3166-1 alpha-2 country code published in the Sensor.Community location record.
        indoor (bool): True when the upstream location.indoor flag marks the sensor as indoor; false when the sensor is marked as outdoor."""
    
    sensor_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_id"))
    sensor_type_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_type_id"))
    sensor_type_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_type_name"))
    sensor_type_manufacturer: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_type_manufacturer"))
    pin: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pin"))
    location_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_id"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    altitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude"))
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    indoor: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="indoor"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"SensorInfo\", \"namespace\": \"io.sensor.community\", \"doc\": \"Reference data for a Sensor.Community sensor node including hardware type and latest known location metadata.\", \"fields\": [{\"name\": \"sensor_id\", \"type\": \"int\", \"doc\": \"Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key.\"}, {\"name\": \"sensor_type_id\", \"type\": \"int\", \"doc\": \"Numeric upstream identifier for the sensor hardware type, such as the Sensor.Community type id for SDS011 or BME280.\"}, {\"name\": \"sensor_type_name\", \"type\": \"string\", \"doc\": \"Upstream sensor hardware type name published under sensor.sensor_type.name, for example SDS011, SPS30, BME280, or DHT22.\"}, {\"name\": \"sensor_type_manufacturer\", \"type\": \"string\", \"doc\": \"Manufacturer name published by Sensor.Community for the sensor hardware type, taken from sensor.sensor_type.manufacturer.\"}, {\"name\": \"pin\", \"type\": \"string\", \"doc\": \"Sensor pin designation reported by the upstream payload under sensor.pin.\"}, {\"name\": \"location_id\", \"type\": \"int\", \"doc\": \"Stable integer identifier of the Sensor.Community location object associated with the reading.\"}, {\"name\": \"latitude\", \"type\": \"double\", \"doc\": \"Latitude of the sensor location in WGS84 decimal degrees.\"}, {\"name\": \"longitude\", \"type\": \"double\", \"doc\": \"Longitude of the sensor location in WGS84 decimal degrees.\"}, {\"name\": \"altitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Altitude of the sensor location in meters above sea level when supplied by the upstream payload.\"}, {\"name\": \"country\", \"type\": \"string\", \"doc\": \"ISO 3166-1 alpha-2 country code published in the Sensor.Community location record.\"}, {\"name\": \"indoor\", \"type\": \"boolean\", \"doc\": \"True when the upstream location.indoor flag marks the sensor as indoor; false when the sensor is marked as outdoor.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.sensor_id=int(self.sensor_id)
        self.sensor_type_id=int(self.sensor_type_id)
        self.sensor_type_name=str(self.sensor_type_name)
        self.sensor_type_manufacturer=str(self.sensor_type_manufacturer)
        self.pin=str(self.pin)
        self.location_id=int(self.location_id)
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.altitude=float(self.altitude) if self.altitude else None
        self.country=str(self.country)
        self.indoor=bool(self.indoor)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SensorInfo':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SensorInfo']:
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
            return SensorInfo.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return SensorInfo.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')