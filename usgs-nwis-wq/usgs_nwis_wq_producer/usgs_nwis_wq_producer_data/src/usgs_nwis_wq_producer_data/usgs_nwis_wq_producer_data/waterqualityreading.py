""" WaterQualityReading dataclass. """

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
class WaterQualityReading:
    """
    A WaterQualityReading record.
    Attributes:
        site_number (str): 
        site_name (str): 
        parameter_code (str): 
        parameter_name (str): 
        value (typing.Optional[float]): 
        unit (str): 
        qualifier (typing.Optional[str]): 
        date_time (str): """
    
    site_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_number"))
    site_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_name"))
    parameter_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_code"))
    parameter_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_name"))
    value: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    unit: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit"))
    qualifier: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="qualifier"))
    date_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_time"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"$id\": \"gov.usgs.waterservices.wq.WaterQualityReading\", \"type\": \"record\", \"name\": \"WaterQualityReading\", \"description\": \"A single water quality observation from a USGS continuous monitoring sensor. The USGS Instantaneous Values Service returns time series of sensor readings in WaterML 2.0 JSON format. Each reading represents one measurement at a specific date_time for one parameter at one site.\", \"fields\": [{\"name\": \"site_number\", \"type\": \"string\", \"description\": \"USGS site identification number for the monitoring location that produced this reading (e.g. '01646500').\"}, {\"name\": \"site_name\", \"type\": \"string\", \"description\": \"Official USGS station name for the monitoring location.\"}, {\"name\": \"parameter_code\", \"type\": \"string\", \"description\": \"Five-digit USGS parameter code identifying the measured quantity. Key water quality codes: 00010 (water temperature \u00b0C), 00300 (dissolved oxygen mg/L), 00400 (pH), 00095 (specific conductance \u00b5S/cm), 63680 (turbidity FNU), 99133 (nitrate+nitrite mg/L as N).\"}, {\"name\": \"parameter_name\", \"type\": \"string\", \"description\": \"Human-readable name of the measured parameter as provided in the USGS variable description (e.g. 'Temperature, water, degrees Celsius').\"}, {\"name\": \"value\", \"type\": [\"double\", \"null\"], \"description\": \"Numeric sensor reading for the parameter at the given date_time. Null when the sensor did not return a valid numeric value (e.g. equipment malfunction, ice-affected, or the USGS noDataValue sentinel -999999.0).\"}, {\"name\": \"unit\", \"type\": \"string\", \"description\": \"Unit of measurement for the reading as reported by the USGS (e.g. 'deg C', 'mg/l', 'uS/cm @25C', 'FNU', 'mg/l as N').\"}, {\"name\": \"qualifier\", \"type\": [\"string\", \"null\"], \"description\": \"USGS data qualifier code indicating the quality or status of the reading. Common values: 'P' (provisional), 'A' (approved), 'e' (estimated). Null when no qualifier is provided.\"}, {\"name\": \"date_time\", \"type\": \"string\", \"description\": \"ISO 8601 date-time string of the observation in UTC (e.g. '2024-11-15T16:45:00+00:00'). Converted from the site-local timestamp using the timezone information provided in the WaterML 2.0 response.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.site_number=str(self.site_number)
        self.site_name=str(self.site_name)
        self.parameter_code=str(self.parameter_code)
        self.parameter_name=str(self.parameter_name)
        self.value=float(self.value) if self.value else None
        self.unit=str(self.unit)
        self.qualifier=str(self.qualifier) if self.qualifier else None
        self.date_time=str(self.date_time)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaterQualityReading':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaterQualityReading']:
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
            return WaterQualityReading.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WaterQualityReading.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')