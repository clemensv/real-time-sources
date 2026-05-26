""" GoesMagnetometer dataclass. """

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
class GoesMagnetometer:
    """
    One-minute resolution magnetic field measurement from the GOES primary satellite magnetometer at geostationary orbit (~6.6 Earth radii), as reported by the SWPC goes/primary/magnetometers-7-day endpoint. The field is measured in the spacecraft-centered HEN coordinate system where Hp is parallel to Earth's rotation axis, He is perpendicular in the east-west direction, and Hn is radially earthward. During geomagnetic storms, Hp can drop dramatically or even become negative, indicating magnetopause compression.
    
    Attributes:
        time_tag (str)
        satellite (int)
        he (typing.Optional[float])
        hp (typing.Optional[float])
        hn (typing.Optional[float])
        total (typing.Optional[float])
        arcjet_flag (typing.Optional[bool])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"GoesMagnetometer\", \"doc\": \"One-minute resolution magnetic field measurement from the GOES primary satellite magnetometer at geostationary orbit (~6.6 Earth radii), as reported by the SWPC goes/primary/magnetometers-7-day endpoint. The field is measured in the spacecraft-centered HEN coordinate system where Hp is parallel to Earth's rotation axis, He is perpendicular in the east-west direction, and Hn is radially earthward. During geomagnetic storms, Hp can drop dramatically or even become negative, indicating magnetopause compression.\", \"fields\": [{\"name\": \"time_tag\", \"type\": \"string\", \"doc\": \"UTC date-time of the magnetic field measurement in ISO 8601 format.\"}, {\"name\": \"satellite\", \"type\": \"integer\", \"doc\": \"GOES satellite number providing the measurement (e.g., 19 for GOES-19).\"}, {\"name\": \"he\", \"type\": [\"double\", \"null\"], \"doc\": \"Magnetic field He component: perpendicular to the satellite-Earth direction and the dipole axis, positive eastward. Measures the east-west distortion of the geomagnetic field at geostationary orbit.\", \"default\": null}, {\"name\": \"hp\", \"type\": [\"double\", \"null\"], \"doc\": \"Magnetic field Hp component: parallel to Earth's dipole axis, positive northward. During quiet times Hp is typically 80-120 nT; during intense geomagnetic storms (G4-G5) it can drop below zero, indicating the magnetopause has been compressed inside geostationary orbit.\", \"default\": null}, {\"name\": \"hn\", \"type\": [\"double\", \"null\"], \"doc\": \"Magnetic field Hn component: along the satellite-Earth direction, positive radially earthward.\", \"default\": null}, {\"name\": \"total\", \"type\": [\"double\", \"null\"], \"doc\": \"Total magnetic field magnitude at geostationary orbit, computed as sqrt(He\u00b2 + Hp\u00b2 + Hn\u00b2). Typical quiet-time values are 100-120 nT.\", \"default\": null}, {\"name\": \"arcjet_flag\", \"type\": [\"boolean\", \"null\"], \"doc\": \"When true, the satellite's electric propulsion (arcjet) thrusters are firing, which causes magnetic field contamination. Magnetometer readings during arcjet events should be treated with caution as they may not reflect the ambient geomagnetic field.\", \"default\": null}]}"
    )
    
    
    time_tag: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_tag"))
    satellite: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="satellite"))
    he: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="he"))
    hp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hp"))
    hn: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hn"))
    total: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="total"))
    arcjet_flag: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="arcjet_flag"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'GoesMagnetometer':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'GoesMagnetometer':
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
        if 'time_tag' in converted and converted['time_tag'] is not None:
            value = converted['time_tag']
        if 'satellite' in converted and converted['satellite'] is not None:
            value = converted['satellite']
        if 'he' in converted and converted['he'] is not None:
            value = converted['he']
        if 'hp' in converted and converted['hp'] is not None:
            value = converted['hp']
        if 'hn' in converted and converted['hn'] is not None:
            value = converted['hn']
        if 'total' in converted and converted['total'] is not None:
            value = converted['total']
        if 'arcjet_flag' in converted and converted['arcjet_flag'] is not None:
            value = converted['arcjet_flag']
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['GoesMagnetometer']:
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
                    return GoesMagnetometer.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return GoesMagnetometer.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'GoesMagnetometer':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            time_tag='bsqemsukscorrsutpsws',
            satellite=int(58),
            he=float(69.57348905135422),
            hp=float(62.57000003508823),
            hn=float(9.883240088075551),
            total=float(51.44709638431231),
            arcjet_flag=True
        )