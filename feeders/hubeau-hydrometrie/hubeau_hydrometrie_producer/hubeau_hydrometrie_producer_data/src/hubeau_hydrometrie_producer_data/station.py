""" Station dataclass. """

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
class Station:
    """
    Reference details for one monitoring station or site in the Hub'Eau Hydrométrie source.
    
    Attributes:
        code_station (str)
        libelle_station (str)
        code_site (typing.Optional[str])
        longitude_station (float)
        latitude_station (float)
        libelle_cours_eau (typing.Optional[str])
        libelle_commune (typing.Optional[str])
        code_departement (typing.Optional[str])
        en_service (typing.Optional[bool])
        date_ouverture_station (typing.Optional[str])
        basin (typing.Optional[str])
    """
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Station\", \"doc\": \"Reference details for one monitoring station or site in the Hub'Eau Hydrom\u00e9trie source.\", \"fields\": [{\"name\": \"code_station\", \"type\": \"string\", \"doc\": \"Permanent hydrometry-station code assigned by the French monitoring network. Use it as the stable identity for station records and related observations.\"}, {\"name\": \"libelle_station\", \"type\": \"string\", \"doc\": \"Display label for the hydrometry station as published by Hub'Eau. It is useful for maps and UI labels but should not be used as a stable key.\"}, {\"name\": \"code_site\", \"type\": [\"string\", \"null\"], \"doc\": \"Optional Hub'Eau site code grouping one or more stations at the same monitoring location.\", \"default\": null}, {\"name\": \"longitude_station\", \"type\": \"double\", \"doc\": \"Longitude of the station in WGS 84 coordinates.\"}, {\"name\": \"latitude_station\", \"type\": \"double\", \"doc\": \"Latitude of the station in WGS 84 coordinates.\"}, {\"name\": \"libelle_cours_eau\", \"type\": [\"string\", \"null\"], \"doc\": \"Name of the river or watercourse monitored by the station.\", \"default\": null}, {\"name\": \"libelle_commune\", \"type\": [\"string\", \"null\"], \"doc\": \"Municipality where the station is located.\", \"default\": null}, {\"name\": \"code_departement\", \"type\": [\"string\", \"null\"], \"doc\": \"French department code for the station location.\", \"default\": null}, {\"name\": \"en_service\", \"type\": [\"boolean\", \"null\"], \"doc\": \"Whether Hub'Eau marks the station as currently in service.\", \"default\": null}, {\"name\": \"date_ouverture_station\", \"type\": [\"string\", \"null\"], \"doc\": \"Date when the station began operating, when the upstream catalog provides it.\", \"default\": null}, {\"name\": \"basin\", \"type\": [\"null\", \"string\"], \"doc\": \"Stable routing axis used by MQTT and AMQP transport templates for hubeau-hydrometrie.\", \"default\": null}]}"
    )
    
    
    code_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_station"))
    libelle_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_station"))
    code_site: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_site"))
    longitude_station: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude_station"))
    latitude_station: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude_station"))
    libelle_cours_eau: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_cours_eau"))
    libelle_commune: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_commune"))
    code_departement: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_departement"))
    en_service: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="en_service"))
    date_ouverture_station: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_ouverture_station"))
    basin: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
        """
        return cls(**data)
    @classmethod
    def from_avro_dict(cls, data: dict) -> 'Station':
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
        if 'libelle_station' in converted and converted['libelle_station'] is not None:
            value = converted['libelle_station']
        if 'code_site' in converted and converted['code_site'] is not None:
            value = converted['code_site']
        if 'longitude_station' in converted and converted['longitude_station'] is not None:
            value = converted['longitude_station']
        if 'latitude_station' in converted and converted['latitude_station'] is not None:
            value = converted['latitude_station']
        if 'libelle_cours_eau' in converted and converted['libelle_cours_eau'] is not None:
            value = converted['libelle_cours_eau']
        if 'libelle_commune' in converted and converted['libelle_commune'] is not None:
            value = converted['libelle_commune']
        if 'code_departement' in converted and converted['code_departement'] is not None:
            value = converted['code_departement']
        if 'en_service' in converted and converted['en_service'] is not None:
            value = converted['en_service']
        if 'date_ouverture_station' in converted and converted['date_ouverture_station'] is not None:
            value = converted['date_ouverture_station']
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
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
                    return Station.from_avro_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for Avro deserialization')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Station':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            code_station='zbqfvhewzmsqlrtdqtns',
            libelle_station='wqtzljltvrvcmdljkhvh',
            code_site='gqmgsbclqiomzjhjianl',
            longitude_station=float(88.3803467684087),
            latitude_station=float(73.5754581161012),
            libelle_cours_eau='vmuuufyfxddrtpsmacji',
            libelle_commune='nuzlblhmntkpdqxoqkny',
            code_departement='issdkeevxollrdztndmn',
            en_service=True,
            date_ouverture_station='xxuflkfmzkbgvarrarix',
            basin='exaxgfvbaypphnzkqwfe'
        )