""" SolarWindSummary dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
from __future__ import annotations
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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SolarWindSummary:
    """
    Latest solar wind conditions summary from the DSCOVR satellite at the L1 Lagrange point (~1.5 million km sunward of Earth), combining proton bulk speed from the summary/solar-wind-speed endpoint and interplanetary magnetic field from the summary/solar-wind-mag-field endpoint. Provides a single snapshot of current conditions, updated approximately every minute.
    
    Attributes:
        observation_time (str)
        wind_speed (float)
        bt (float)
        bz (float)
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"SolarWindSummary\", \"doc\": \"Latest solar wind conditions summary from the DSCOVR satellite at the L1 Lagrange point (~1.5 million km sunward of Earth), combining proton bulk speed from the summary/solar-wind-speed endpoint and interplanetary magnetic field from the summary/solar-wind-mag-field endpoint. Provides a single snapshot of current conditions, updated approximately every minute.\", \"fields\": [{\"name\": \"observation_time\", \"type\": \"string\", \"doc\": \"UTC date-time of the solar wind measurement from DSCOVR, in ISO 8601 format.\"}, {\"name\": \"wind_speed\", \"type\": \"double\", \"doc\": \"Solar wind proton bulk speed measured by DSCOVR at L1. Typical slow-wind values are 300-400 km/s; fast streams and CME passages can reach 500-1000+ km/s.\"}, {\"name\": \"bt\", \"type\": \"double\", \"doc\": \"Interplanetary magnetic field total magnitude (Bt) measured by the DSCOVR magnetometer at L1. Quiet-time values are typically 3-6 nT; values above 20 nT indicate strong solar wind driving.\"}, {\"name\": \"bz\", \"type\": \"double\", \"doc\": \"Interplanetary magnetic field north-south component in Geocentric Solar Magnetospheric (GSM) coordinates (Bz GSM). Sustained negative (southward) Bz is the primary driver of geomagnetic storms via magnetic reconnection at Earth's magnetopause.\"}]}"
    )
    
    
    observation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    wind_speed: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_speed"))
    bt: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bt"))
    bz: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bz"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SolarWindSummary':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'SolarWindSummary':
        """
        Converts a dictionary from Avro deserialization to a dataclass instance.
        Handles conversion of string representations back to Python types for
        extended logical types.
        
        Args:
            data: The dictionary from Avro deserialization.
        
        Returns:
            The dataclass representation.
        """
        # Convert string values back to Python types for Avro string-based logical types
        converted = data.copy()
        if 'observation_time' in converted and converted['observation_time'] is not None:
            value = converted['observation_time']
        if 'wind_speed' in converted and converted['wind_speed'] is not None:
            value = converted['wind_speed']
        if 'bt' in converted and converted['bt'] is not None:
            value = converted['bt']
        if 'bz' in converted and converted['bz'] is not None:
            value = converted['bz']
        
        return cls(**converted)

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
            if isinstance(v, enum.Enum):
                return v.value
            return v
        def _fix_key(k):
            return k[:-1] if k.endswith('_') else k
        return {_fix_key(k): _resolve_enum(v) for k, v in iter(data)}

    def to_avro_dict(self) -> dict:
        """
        Converts the dataclass to a dictionary suitable for Avro serialization.
        Handles conversion of Python types to Avro-compatible string representations
        for extended logical types.

        Returns:
            The dictionary representation suitable for Avro serialization.
        """
        result = self.to_serializer_dict()
        converted = result.copy()
        
        # Convert specific fields based on their source types
        
        return converted

    def to_byte_array(self, content_type_string: str) -> bytes:
        """
        Converts the dataclass to a byte array based on the content type string.
        
        Args:
            content_type_string: The content type string to convert the dataclass to.
                Supported content types:
                    'application/json': Encodes the data to JSON format.
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
            # Convert to Avro binary format using the embedded schema
            writer = avro.io.DatumWriter(self.AvroType)
            with io.BytesIO() as stream:
                encoder = avro.io.BinaryEncoder(stream)
                writer.write(self.to_avro_dict(), encoder)
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SolarWindSummary']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'application/json': Attempts to decode the data from JSON encoded format.
                    'avro/binary': Attempts to decode the data from Avro binary format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            if isinstance(data, bytes):
                # Decode from Avro binary format using the embedded schema
                reader = avro.io.DatumReader(cls.AvroType)
                with io.BytesIO(data) as stream:
                    decoder = avro.io.BinaryDecoder(stream)
                    _record = reader.read(decoder)
                    return SolarWindSummary.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return SolarWindSummary.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SolarWindSummary':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            observation_time='taqgyskupscuctikloed',
            wind_speed=float(98.58846776477817),
            bt=float(89.877628090897),
            bz=float(77.17509888591293)
        )