""" DailyIndex dataclass. """

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
class DailyIndex:
    """
    Daily Air Quality Index bulletin record for a LAQN site and pollutant species within the latest London-wide index publication.
    Attributes:
        site_code (str): Stable LAQN site code for the monitoring site to which the daily index applies.
        bulletin_date (str): Bulletin date and time published by LAQN for the daily index, encoded as YYYY-MM-DD HH:MM:SS.
        species_code (str): Stable LAQN pollutant code for the species to which the daily index applies.
        air_quality_index (int): LAQN Daily Air Quality Index value from 1 to 10.
        air_quality_band (str): Textual Daily Air Quality Index band published by LAQN: Low, Moderate, High, or Very High.
        index_source (str): Origin of the daily index published by LAQN, typically Measurement or Forecast."""
    
    site_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_code"))
    bulletin_date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bulletin_date"))
    species_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="species_code"))
    air_quality_index: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_quality_index"))
    air_quality_band: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="air_quality_band"))
    index_source: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="index_source"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"DailyIndex\", \"namespace\": \"uk.kcl.laqn\", \"doc\": \"Daily Air Quality Index bulletin record for a LAQN site and pollutant species within the latest London-wide index publication.\", \"fields\": [{\"name\": \"site_code\", \"type\": \"string\", \"doc\": \"Stable LAQN site code for the monitoring site to which the daily index applies.\"}, {\"name\": \"bulletin_date\", \"type\": \"string\", \"doc\": \"Bulletin date and time published by LAQN for the daily index, encoded as YYYY-MM-DD HH:MM:SS.\"}, {\"name\": \"species_code\", \"type\": \"string\", \"doc\": \"Stable LAQN pollutant code for the species to which the daily index applies.\"}, {\"name\": \"air_quality_index\", \"type\": \"int\", \"doc\": \"LAQN Daily Air Quality Index value from 1 to 10.\"}, {\"name\": \"air_quality_band\", \"type\": \"string\", \"doc\": \"Textual Daily Air Quality Index band published by LAQN: Low, Moderate, High, or Very High.\"}, {\"name\": \"index_source\", \"type\": \"string\", \"doc\": \"Origin of the daily index published by LAQN, typically Measurement or Forecast.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.site_code=str(self.site_code)
        self.bulletin_date=str(self.bulletin_date)
        self.species_code=str(self.species_code)
        self.air_quality_index=int(self.air_quality_index)
        self.air_quality_band=str(self.air_quality_band)
        self.index_source=str(self.index_source)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'DailyIndex':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['DailyIndex']:
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
            return DailyIndex.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return DailyIndex.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')