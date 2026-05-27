""" SolarWindMagField dataclass. """

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
class SolarWindMagField:
    """
    One-minute resolution interplanetary magnetic field (IMF) vector measurement from the DSCOVR satellite magnetometer at the L1 Lagrange point, as reported by the SWPC solar-wind/mag-7-day endpoint. Provides the full magnetic field vector in Geocentric Solar Magnetospheric (GSM) coordinates plus total magnitude. The Bz GSM component is the primary indicator of geomagnetic storm potential.
    
    Attributes:
        observation_time (str)
        bx_gsm (typing.Optional[float])
        by_gsm (typing.Optional[float])
        bz_gsm (typing.Optional[float])
        lon_gsm (typing.Optional[float])
        lat_gsm (typing.Optional[float])
        bt (typing.Optional[float])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"SolarWindMagField\", \"doc\": \"One-minute resolution interplanetary magnetic field (IMF) vector measurement from the DSCOVR satellite magnetometer at the L1 Lagrange point, as reported by the SWPC solar-wind/mag-7-day endpoint. Provides the full magnetic field vector in Geocentric Solar Magnetospheric (GSM) coordinates plus total magnitude. The Bz GSM component is the primary indicator of geomagnetic storm potential.\", \"fields\": [{\"name\": \"observation_time\", \"type\": \"string\", \"doc\": \"UTC date-time of the magnetic field measurement, in 'YYYY-MM-DD HH:MM:SS.fff' format.\"}, {\"name\": \"bx_gsm\", \"type\": [\"double\", \"null\"], \"doc\": \"IMF X-component in GSM coordinates, directed from Earth toward the Sun along the Earth-Sun line.\", \"default\": null}, {\"name\": \"by_gsm\", \"type\": [\"double\", \"null\"], \"doc\": \"IMF Y-component in GSM coordinates, perpendicular to the Earth-Sun line in the magnetic equatorial plane. Influences the dawn-dusk electric field in the magnetosphere.\", \"default\": null}, {\"name\": \"bz_gsm\", \"type\": [\"double\", \"null\"], \"doc\": \"IMF Z-component in GSM coordinates (north-south). Sustained negative (southward) Bz is the primary driver of geomagnetic storms through magnetic reconnection at the dayside magnetopause. Values below -10 nT can produce G2+ storms.\", \"default\": null}, {\"name\": \"lon_gsm\", \"type\": [\"double\", \"null\"], \"doc\": \"IMF longitude angle in GSM coordinates, measured in the GSM X-Y plane from the Earth-Sun line.\", \"default\": null}, {\"name\": \"lat_gsm\", \"type\": [\"double\", \"null\"], \"doc\": \"IMF latitude angle in GSM coordinates, measured from the GSM X-Y plane toward the Z-axis.\", \"default\": null}, {\"name\": \"bt\", \"type\": [\"double\", \"null\"], \"doc\": \"Total interplanetary magnetic field magnitude, computed as the vector sum sqrt(Bx\u00b2 + By\u00b2 + Bz\u00b2). Typical quiet-time values are 3-6 nT; values above 20 nT indicate strong solar wind magnetic driving.\", \"default\": null}]}"
    )
    
    
    observation_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="observation_time"))
    bx_gsm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bx_gsm"))
    by_gsm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="by_gsm"))
    bz_gsm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bz_gsm"))
    lon_gsm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lon_gsm"))
    lat_gsm: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat_gsm"))
    bt: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bt"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SolarWindMagField':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'SolarWindMagField':
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
        if 'bx_gsm' in converted and converted['bx_gsm'] is not None:
            value = converted['bx_gsm']
        if 'by_gsm' in converted and converted['by_gsm'] is not None:
            value = converted['by_gsm']
        if 'bz_gsm' in converted and converted['bz_gsm'] is not None:
            value = converted['bz_gsm']
        if 'lon_gsm' in converted and converted['lon_gsm'] is not None:
            value = converted['lon_gsm']
        if 'lat_gsm' in converted and converted['lat_gsm'] is not None:
            value = converted['lat_gsm']
        if 'bt' in converted and converted['bt'] is not None:
            value = converted['bt']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SolarWindMagField']:
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
                    return SolarWindMagField.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return SolarWindMagField.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SolarWindMagField':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            observation_time='gwvoydgdcvadbarnfhhq',
            bx_gsm=float(66.91980255724458),
            by_gsm=float(95.64498378357837),
            bz_gsm=float(94.51207457199006),
            lon_gsm=float(30.504143784455074),
            lat_gsm=float(74.31077110802451),
            bt=float(64.83062311356784)
        )