""" Station dataclass. """

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
class Station:
    """
    Station
    Attributes:
        code_station (str): 
        libelle_station (str): 
        code_site (typing.Optional[str]): 
        longitude_station (float): 
        latitude_station (float): 
        libelle_cours_eau (typing.Optional[str]): 
        libelle_commune (typing.Optional[str]): 
        code_departement (typing.Optional[str]): 
        en_service (typing.Optional[bool]): 
        date_ouverture_station (typing.Optional[str]): """
    
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Station\", \"doc\": \"Station\", \"fields\": [{\"name\": \"code_station\", \"type\": \"string\"}, {\"name\": \"libelle_station\", \"type\": \"string\"}, {\"name\": \"code_site\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"longitude_station\", \"type\": \"double\"}, {\"name\": \"latitude_station\", \"type\": \"double\"}, {\"name\": \"libelle_cours_eau\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"libelle_commune\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"code_departement\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"en_service\", \"type\": [\"null\", \"boolean\"], \"default\": null}, {\"name\": \"date_ouverture_station\", \"type\": [\"null\", \"string\"], \"default\": null}], \"namespace\": \"FR.Gov.Eaufrance.HubEau.Hydrometrie\"}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.code_station=str(self.code_station)
        self.libelle_station=str(self.libelle_station)
        self.code_site=str(self.code_site) if self.code_site else None
        self.longitude_station=float(self.longitude_station)
        self.latitude_station=float(self.latitude_station)
        self.libelle_cours_eau=str(self.libelle_cours_eau) if self.libelle_cours_eau else None
        self.libelle_commune=str(self.libelle_commune) if self.libelle_commune else None
        self.code_departement=str(self.code_departement) if self.code_departement else None
        self.en_service=bool(self.en_service) if self.en_service else None
        self.date_ouverture_station=str(self.date_ouverture_station) if self.date_ouverture_station else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
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
            return Station.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')