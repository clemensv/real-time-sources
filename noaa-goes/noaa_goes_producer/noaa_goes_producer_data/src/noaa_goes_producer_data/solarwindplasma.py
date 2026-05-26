""" SolarWindPlasma dataclass. """

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
class SolarWindPlasma:
    """
    One-minute resolution solar wind plasma measurement from the DSCOVR satellite Faraday Cup instrument at the L1 Lagrange point, as reported by the SWPC solar-wind/plasma-7-day endpoint. Includes proton density, bulk speed, and ion temperature. DSCOVR provides approximately 15-45 minutes of advance warning before solar wind structures reach Earth's magnetosphere.
    
    Attributes:
        observation_time (str)
        density (typing.Optional[float])
        speed (typing.Optional[float])
        temperature (typing.Optional[float])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"SolarWindPlasma\", \"doc\": \"One-minute resolution solar wind plasma measurement from the DSCOVR satellite Faraday Cup instrument at the L1 Lagrange point, as reported by the SWPC solar-wind/plasma-7-day endpoint. Includes proton density, bulk speed, and ion temperature. DSCOVR provides approximately 15-45 minutes of advance warning before solar wind structures reach Earth's magnetosphere.\", \"fields\": [{\"name\": \"observation_time\", \"type\": \"string\", \"doc\": \"UTC date-time of the plasma measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format.\"}, {\"name\": \"density\", \"type\": [\"double\", \"null\"], \"doc\": \"Solar wind proton number density measured by the DSCOVR Faraday Cup. Typical quiet-time values are 3-10 n/cm\u00b3; values above 20 n/cm\u00b3 may indicate a coronal mass ejection passage or a compressed solar wind region.\", \"default\": null}, {\"name\": \"speed\", \"type\": [\"double\", \"null\"], \"doc\": \"Solar wind proton bulk speed measured by DSCOVR. Typical quiet-time values are 300-400 km/s (slow wind); high-speed streams reach 500-800 km/s and CME-driven shocks can exceed 1000 km/s.\", \"default\": null}, {\"name\": \"temperature\", \"type\": [\"double\", \"null\"], \"doc\": \"Solar wind ion temperature measured by DSCOVR. Typical values are 10,000-200,000 K; elevated temperatures often accompany high-speed streams and interplanetary shock passages.\", \"default\": null}]}"
    )
    
    
    observation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    density: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="density"))
    speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="speed"))
    temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temperature"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SolarWindPlasma':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'SolarWindPlasma':
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
        if 'density' in converted and converted['density'] is not None:
            value = converted['density']
        if 'speed' in converted and converted['speed'] is not None:
            value = converted['speed']
        if 'temperature' in converted and converted['temperature'] is not None:
            value = converted['temperature']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SolarWindPlasma']:
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
                    return SolarWindPlasma.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return SolarWindPlasma.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SolarWindPlasma':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            observation_time='gedslmkgjolzdeudqbgp',
            density=float(15.58535269627952),
            speed=float(57.32898680419414),
            temperature=float(17.239556668857624)
        )