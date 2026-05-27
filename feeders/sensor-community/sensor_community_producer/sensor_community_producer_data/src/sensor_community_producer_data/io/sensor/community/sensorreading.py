""" SensorReading dataclass. """

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
class SensorReading:
    """
    Latest Sensor.Community telemetry reading for one sensor at a specific timestamp, normalized across particulate, climate, pressure, and noise measurements.
    Attributes:
        sensor_id (int): Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key.
        timestamp (str): UTC timestamp published by Sensor.Community for the reading in the format YYYY-MM-DD HH:mm:ss.
        sensor_type_name (str): Upstream sensor hardware type name published under sensor.sensor_type.name for the device that emitted the reading.
        pm10_ug_m3 (typing.Optional[float]): Particulate matter mass concentration for PM10 in micrograms per cubic meter when the upstream feed publishes value type P1.
        pm2_5_ug_m3 (typing.Optional[float]): Particulate matter mass concentration for PM2.5 in micrograms per cubic meter when the upstream feed publishes value type P2.
        pm1_0_ug_m3 (typing.Optional[float]): Particulate matter mass concentration for PM1.0 in micrograms per cubic meter when the upstream feed publishes value type P0.
        pm4_0_ug_m3 (typing.Optional[float]): Particulate matter mass concentration for PM4.0 in micrograms per cubic meter when the upstream feed publishes value type P4.
        temperature_celsius (typing.Optional[float]): Ambient temperature measurement in degrees Celsius when the upstream feed publishes value type temperature.
        humidity_percent (typing.Optional[float]): Relative humidity in percent when the upstream feed publishes value type humidity.
        pressure_pa (typing.Optional[float]): Atmospheric pressure in pascals when the upstream feed publishes value type pressure.
        pressure_sealevel_pa (typing.Optional[float]): Atmospheric pressure reduced to sea level in pascals when the upstream feed publishes value type pressure_at_sealevel.
        noise_laeq_db (typing.Optional[float]): Equivalent continuous sound level in A-weighted decibels when the upstream feed publishes value type noise_LAeq.
        noise_la_min_db (typing.Optional[float]): Minimum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_min.
        noise_la_max_db (typing.Optional[float]): Maximum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_max."""
    
    sensor_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_id"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    sensor_type_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_type_name"))
    pm10_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_ug_m3"))
    pm2_5_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm2_5_ug_m3"))
    pm1_0_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm1_0_ug_m3"))
    pm4_0_ug_m3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm4_0_ug_m3"))
    temperature_celsius: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temperature_celsius"))
    humidity_percent: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="humidity_percent"))
    pressure_pa: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_pa"))
    pressure_sealevel_pa: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pressure_sealevel_pa"))
    noise_laeq_db: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="noise_laeq_db"))
    noise_la_min_db: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="noise_la_min_db"))
    noise_la_max_db: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="noise_la_max_db"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"SensorReading\", \"namespace\": \"io.sensor.community\", \"doc\": \"Latest Sensor.Community telemetry reading for one sensor at a specific timestamp, normalized across particulate, climate, pressure, and noise measurements.\", \"fields\": [{\"name\": \"sensor_id\", \"type\": \"int\", \"doc\": \"Stable integer identifier of the Sensor.Community sensor device. This value is used as the CloudEvents subject and Kafka key.\"}, {\"name\": \"timestamp\", \"type\": \"string\", \"doc\": \"UTC timestamp published by Sensor.Community for the reading in the format YYYY-MM-DD HH:mm:ss.\"}, {\"name\": \"sensor_type_name\", \"type\": \"string\", \"doc\": \"Upstream sensor hardware type name published under sensor.sensor_type.name for the device that emitted the reading.\"}, {\"name\": \"pm10_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Particulate matter mass concentration for PM10 in micrograms per cubic meter when the upstream feed publishes value type P1.\"}, {\"name\": \"pm2_5_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Particulate matter mass concentration for PM2.5 in micrograms per cubic meter when the upstream feed publishes value type P2.\"}, {\"name\": \"pm1_0_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Particulate matter mass concentration for PM1.0 in micrograms per cubic meter when the upstream feed publishes value type P0.\"}, {\"name\": \"pm4_0_ug_m3\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Particulate matter mass concentration for PM4.0 in micrograms per cubic meter when the upstream feed publishes value type P4.\"}, {\"name\": \"temperature_celsius\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Ambient temperature measurement in degrees Celsius when the upstream feed publishes value type temperature.\"}, {\"name\": \"humidity_percent\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Relative humidity in percent when the upstream feed publishes value type humidity.\"}, {\"name\": \"pressure_pa\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Atmospheric pressure in pascals when the upstream feed publishes value type pressure.\"}, {\"name\": \"pressure_sealevel_pa\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Atmospheric pressure reduced to sea level in pascals when the upstream feed publishes value type pressure_at_sealevel.\"}, {\"name\": \"noise_laeq_db\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Equivalent continuous sound level in A-weighted decibels when the upstream feed publishes value type noise_LAeq.\"}, {\"name\": \"noise_la_min_db\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Minimum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_min.\"}, {\"name\": \"noise_la_max_db\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"Maximum A-weighted sound level in decibels when the upstream feed publishes value type noise_LA_max.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.sensor_id=int(self.sensor_id)
        self.timestamp=str(self.timestamp)
        self.sensor_type_name=str(self.sensor_type_name)
        self.pm10_ug_m3=float(self.pm10_ug_m3) if self.pm10_ug_m3 else None
        self.pm2_5_ug_m3=float(self.pm2_5_ug_m3) if self.pm2_5_ug_m3 else None
        self.pm1_0_ug_m3=float(self.pm1_0_ug_m3) if self.pm1_0_ug_m3 else None
        self.pm4_0_ug_m3=float(self.pm4_0_ug_m3) if self.pm4_0_ug_m3 else None
        self.temperature_celsius=float(self.temperature_celsius) if self.temperature_celsius else None
        self.humidity_percent=float(self.humidity_percent) if self.humidity_percent else None
        self.pressure_pa=float(self.pressure_pa) if self.pressure_pa else None
        self.pressure_sealevel_pa=float(self.pressure_sealevel_pa) if self.pressure_sealevel_pa else None
        self.noise_laeq_db=float(self.noise_laeq_db) if self.noise_laeq_db else None
        self.noise_la_min_db=float(self.noise_la_min_db) if self.noise_la_min_db else None
        self.noise_la_max_db=float(self.noise_la_max_db) if self.noise_la_max_db else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SensorReading':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SensorReading']:
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
            return SensorReading.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return SensorReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')