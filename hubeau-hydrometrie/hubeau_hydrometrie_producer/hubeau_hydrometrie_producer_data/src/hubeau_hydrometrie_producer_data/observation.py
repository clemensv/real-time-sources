""" Observation dataclass. """

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
from marshmallow import fields
import json
import avro.schema
import avro.io
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Observation:
    """
    Measurement payload for water height and discharge observations in the Hub'Eau Hydrométrie source.
    
    Attributes:
        code_station (str)
        date_obs (datetime.datetime)
        resultat_obs (float)
        grandeur_hydro (str)
        libelle_methode_obs (typing.Optional[str])
        libelle_qualification_obs (typing.Optional[str])
        basin (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Observation\", \"doc\": \"Measurement payload for water height and discharge observations in the Hub'Eau Hydrom\u00e9trie source.\", \"fields\": [{\"name\": \"code_station\", \"type\": \"string\", \"doc\": \"Permanent hydrometry-station code assigned by the French monitoring network. Use it as the stable identity for station records and related observations.\"}, {\"name\": \"date_obs\", \"type\": {\"type\": \"string\", \"logicalType\": \"timestamp-millis\"}, \"doc\": \"Observation timestamp published by Hub'Eau for this measurement.\"}, {\"name\": \"resultat_obs\", \"type\": \"double\", \"doc\": \"Measured hydrometric value. Interpret the quantity and unit from `grandeur_hydro`, such as discharge or water height.\"}, {\"name\": \"grandeur_hydro\", \"type\": \"string\", \"doc\": \"Hydrometric quantity code identifying what `resultat_obs` measures, such as discharge or water height.\"}, {\"name\": \"libelle_methode_obs\", \"type\": [\"string\", \"null\"], \"doc\": \"Provider label for the observation method used to produce the measurement.\", \"default\": null}, {\"name\": \"libelle_qualification_obs\", \"type\": [\"string\", \"null\"], \"doc\": \"Provider quality label describing how Hub'Eau qualifies the observation.\", \"default\": null}, {\"name\": \"basin\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for hubeau-hydrometrie.\", \"default\": null}]}"
    )
    
    
    code_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_station"))
    date_obs: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_obs", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    resultat_obs: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="resultat_obs"))
    grandeur_hydro: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="grandeur_hydro"))
    libelle_methode_obs: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_methode_obs"))
    libelle_qualification_obs: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_qualification_obs"))
    basin: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Observation':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Observation':
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
        if 'code_station' in converted and converted['code_station'] is not None:
            value = converted['code_station']
        if 'date_obs' in converted and converted['date_obs'] is not None:
            value = converted['date_obs']
            if isinstance(value, str):
                converted['date_obs'] = datetime.datetime.fromisoformat(value)
        if 'resultat_obs' in converted and converted['resultat_obs'] is not None:
            value = converted['resultat_obs']
        if 'grandeur_hydro' in converted and converted['grandeur_hydro'] is not None:
            value = converted['grandeur_hydro']
        if 'libelle_methode_obs' in converted and converted['libelle_methode_obs'] is not None:
            value = converted['libelle_methode_obs']
        if 'libelle_qualification_obs' in converted and converted['libelle_qualification_obs'] is not None:
            value = converted['libelle_qualification_obs']
        if 'basin' in converted and converted['basin'] is not None:
            value = converted['basin']
        
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
        if 'date_obs' in converted and converted['date_obs'] is not None:
            value = converted['date_obs']
            if isinstance(value, datetime.datetime):
                converted['date_obs'] = value.isoformat()
        
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Observation']:
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
                    return Observation.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Observation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Observation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            code_station='ndtwlwpksfnvhrtvtlca',
            date_obs=datetime.datetime.now(datetime.timezone.utc),
            resultat_obs=float(72.79030439576368),
            grandeur_hydro='jcedzcwcswndbqvxchqi',
            libelle_methode_obs='jquvqomtjrigduhnuebk',
            libelle_qualification_obs='pzkgiualetajvcifsppi',
            basin='hurazvczaejqewotalfu'
        )