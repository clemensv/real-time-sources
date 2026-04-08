""" ReservoirReading dataclass. """

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
class ReservoirReading:
    """
    A single sensor reading from a CDEC reservoir station. The California Data Exchange Center (CDEC) publishes hourly and sub-hourly observations for over 2,600 stations across California. Each reading captures one measurement for a specific station, sensor type, and timestamp.
    Attributes:
        station_id (str): Three-letter CDEC station identifier (e.g. SHA for Shasta Dam, ORO for Oroville Dam, FOL for Folsom Dam). This is the primary key for the monitoring station and is immutable.
        sensor_num (int): CDEC numeric sensor identifier. Standard sensor numbers: 15=STORAGE (acre-feet), 6=RESERVOIR ELEVATION (feet), 76=INFLOW (cubic feet per second), 23=OUTFLOW (cubic feet per second), 1=RIVER STAGE (feet).
        sensor_type (str): Human-readable sensor type label as returned by the CDEC API (e.g. 'STORAGE', 'RES ELE', 'INFLOW', 'OUTFLOW', 'STAGE').
        value (typing.Optional[float]): Observed measurement value in the units specified by the 'units' field. Null when no observation is available or when the upstream reports the sentinel value -9999.
        units (str): Engineering units of the measurement as reported by CDEC (e.g. 'AF' for acre-feet, 'FEET' for feet, 'CFS' for cubic feet per second).
        date (str): Observation timestamp as reported by CDEC in PST (Pacific Standard Time, UTC-8). Format from the API is 'YYYY-M-D H:MM' and is normalized to ISO 8601 format 'YYYY-MM-DDTHH:MM:SS-08:00'. CDEC always reports in PST regardless of daylight saving time.
        dur_code (str): Duration code indicating the measurement interval. 'H' for hourly observations, 'D' for daily observations, 'E' for event-based (15-minute or irregular).
        data_flag (str): Quality flag character applied to the observation by CDEC. A single space ' ' means no flag (normal data). Other values indicate provisional, edited, or suspect data."""
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    sensor_num: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_num"))
    sensor_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sensor_type"))
    value: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    units: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="units"))
    date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date"))
    dur_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dur_code"))
    data_flag: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_flag"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"ReservoirReading\", \"namespace\": \"gov.ca.water.cdec\", \"doc\": \"A single sensor reading from a CDEC reservoir station. The California Data Exchange Center (CDEC) publishes hourly and sub-hourly observations for over 2,600 stations across California. Each reading captures one measurement for a specific station, sensor type, and timestamp.\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"Three-letter CDEC station identifier (e.g. SHA for Shasta Dam, ORO for Oroville Dam, FOL for Folsom Dam). This is the primary key for the monitoring station and is immutable.\"}, {\"name\": \"sensor_num\", \"type\": \"int\", \"doc\": \"CDEC numeric sensor identifier. Standard sensor numbers: 15=STORAGE (acre-feet), 6=RESERVOIR ELEVATION (feet), 76=INFLOW (cubic feet per second), 23=OUTFLOW (cubic feet per second), 1=RIVER STAGE (feet).\"}, {\"name\": \"sensor_type\", \"type\": \"string\", \"doc\": \"Human-readable sensor type label as returned by the CDEC API (e.g. 'STORAGE', 'RES ELE', 'INFLOW', 'OUTFLOW', 'STAGE').\"}, {\"name\": \"value\", \"type\": [\"null\", \"double\"], \"doc\": \"Observed measurement value in the units specified by the 'units' field. Null when no observation is available or when the upstream reports the sentinel value -9999.\"}, {\"name\": \"units\", \"type\": \"string\", \"doc\": \"Engineering units of the measurement as reported by CDEC (e.g. 'AF' for acre-feet, 'FEET' for feet, 'CFS' for cubic feet per second).\"}, {\"name\": \"date\", \"type\": \"string\", \"doc\": \"Observation timestamp as reported by CDEC in PST (Pacific Standard Time, UTC-8). Format from the API is 'YYYY-M-D H:MM' and is normalized to ISO 8601 format 'YYYY-MM-DDTHH:MM:SS-08:00'. CDEC always reports in PST regardless of daylight saving time.\"}, {\"name\": \"dur_code\", \"type\": \"string\", \"doc\": \"Duration code indicating the measurement interval. 'H' for hourly observations, 'D' for daily observations, 'E' for event-based (15-minute or irregular).\"}, {\"name\": \"data_flag\", \"type\": \"string\", \"doc\": \"Quality flag character applied to the observation by CDEC. A single space ' ' means no flag (normal data). Other values indicate provisional, edited, or suspect data.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.sensor_num=int(self.sensor_num)
        self.sensor_type=str(self.sensor_type)
        self.value=float(self.value) if self.value else None
        self.units=str(self.units)
        self.date=str(self.date)
        self.dur_code=str(self.dur_code)
        self.data_flag=str(self.data_flag)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'ReservoirReading':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['ReservoirReading']:
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
            return ReservoirReading.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return ReservoirReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')