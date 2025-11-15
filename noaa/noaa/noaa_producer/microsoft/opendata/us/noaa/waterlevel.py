""" WaterLevel dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
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
from noaa.noaa_producer.microsoft.opendata.us.noaa.qualitylevel import QualityLevel


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WaterLevel:
    """
    A WaterLevel record.
    Attributes:
        station_id (str): {"description": "7 character station ID, or a currents station ID."}
        timestamp (str): {"description": "Timestamp of the water level measurement"}
        value (float): {"description": "Value of the water level"}
        stddev (float): {"description": "Standard deviation of 1-second samples used to compute the water level height"}
        outside_sigma_band (bool): {"description": "Flag indicating if the water level is outside a 3-sigma band. Possible values: 'false' (not outside), 'true' (outside)."}
        flat_tolerance_limit (bool): {"description": "Flag indicating if the flat tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."}
        rate_of_change_limit (bool): {"description": "Flag indicating if the rate of change tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."}
        max_min_expected_height (bool): {"description": "Flag indicating if the max/min expected water level height is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded)."}
        quality (QualityLevel): """
    
    station_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_id"))
    timestamp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    value: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    stddev: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="stddev"))
    outside_sigma_band: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="outside_sigma_band"))
    flat_tolerance_limit: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="flat_tolerance_limit"))
    rate_of_change_limit: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="rate_of_change_limit"))
    max_min_expected_height: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_min_expected_height"))
    quality: QualityLevel=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="quality"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"WaterLevel\", \"fields\": [{\"name\": \"station_id\", \"type\": \"string\", \"doc\": \"{'description': '7 character station ID, or a currents station ID.'}\"}, {\"name\": \"timestamp\", \"type\": \"string\", \"logicalType\": \"timestamp-millis\", \"doc\": \"{'description': 'Timestamp of the water level measurement'}\"}, {\"name\": \"value\", \"type\": \"double\", \"doc\": \"{'description': 'Value of the water level'}\"}, {\"name\": \"stddev\", \"type\": \"double\", \"doc\": \"{'description': 'Standard deviation of 1-second samples used to compute the water level height'}\"}, {\"name\": \"outside_sigma_band\", \"type\": \"boolean\", \"doc\": \"{'description': 'Flag indicating if the water level is outside a 3-sigma band. Possible values: 'false' (not outside), 'true' (outside).'}\"}, {\"name\": \"flat_tolerance_limit\", \"type\": \"boolean\", \"doc\": \"{'description': 'Flag indicating if the flat tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded).'}\"}, {\"name\": \"rate_of_change_limit\", \"type\": \"boolean\", \"doc\": \"{'description': 'Flag indicating if the rate of change tolerance limit is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded).'}\"}, {\"name\": \"max_min_expected_height\", \"type\": \"boolean\", \"doc\": \"{'description': 'Flag indicating if the max/min expected water level height is exceeded. Possible values: 'false' (not exceeded), 'true' (exceeded).'}\"}, {\"name\": \"quality\", \"type\": {\"type\": \"enum\", \"name\": \"QualityLevel\", \"symbols\": [\"Preliminary\", \"Verified\"], \"doc\": \"Quality Assurance/Quality Control level\"}}], \"altnames\": {\"kql\": \"WaterLevel\"}, \"namespace\": \"Microsoft.OpenData.US.NOAA\"}"
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.station_id=str(self.station_id)
        self.timestamp=str(self.timestamp)
        self.value=float(self.value)
        self.stddev=float(self.stddev)
        self.outside_sigma_band=bool(self.outside_sigma_band)
        self.flat_tolerance_limit=bool(self.flat_tolerance_limit)
        self.rate_of_change_limit=bool(self.rate_of_change_limit)
        self.max_min_expected_height=bool(self.max_min_expected_height)
        self.quality=QualityLevel(self.quality)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WaterLevel':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WaterLevel']:
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
            return WaterLevel.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WaterLevel.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')