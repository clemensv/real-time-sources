""" Venue dataclass. """

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
class Venue:
    """
    Reference data for a Ticketmaster venue.
    Attributes:
        entity_id (str): Stable Ticketmaster venue identifier.
        name (str): Human-readable name of the venue.
        url (typing.Optional[str]): URL to the venue page on Ticketmaster.com.
        locale (typing.Optional[str]): BCP-47 locale string.
        timezone (typing.Optional[str]): IANA timezone database name.
        city (typing.Optional[str]): City name.
        state_code (typing.Optional[str]): ISO 3166-2 state or province code.
        country_code (typing.Optional[str]): ISO 3166-1 alpha-2 country code.
        address (typing.Optional[str]): Street address line 1.
        postal_code (typing.Optional[str]): Postal or ZIP code.
        latitude (typing.Optional[float]): WGS-84 latitude in decimal degrees.
        longitude (typing.Optional[float]): WGS-84 longitude in decimal degrees."""
    
    entity_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="entity_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    locale: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="locale"))
    timezone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timezone"))
    city: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="city"))
    state_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_code"))
    country_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_code"))
    address: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address"))
    postal_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="postal_code"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"Venue\", \"namespace\": \"Ticketmaster.Reference\", \"doc\": \"Reference data for a Ticketmaster venue.\", \"fields\": [{\"name\": \"entity_id\", \"type\": \"string\", \"doc\": \"Stable Ticketmaster venue identifier.\"}, {\"name\": \"name\", \"type\": \"string\", \"doc\": \"Human-readable name of the venue.\"}, {\"name\": \"url\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"URL to the venue page on Ticketmaster.com.\"}, {\"name\": \"locale\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"BCP-47 locale string.\"}, {\"name\": \"timezone\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"IANA timezone database name.\"}, {\"name\": \"city\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"City name.\"}, {\"name\": \"state_code\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 3166-2 state or province code.\"}, {\"name\": \"country_code\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"ISO 3166-1 alpha-2 country code.\"}, {\"name\": \"address\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Street address line 1.\"}, {\"name\": \"postal_code\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Postal or ZIP code.\"}, {\"name\": \"latitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS-84 latitude in decimal degrees.\"}, {\"name\": \"longitude\", \"type\": [\"null\", \"double\"], \"default\": null, \"doc\": \"WGS-84 longitude in decimal degrees.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.entity_id=str(self.entity_id)
        self.name=str(self.name)
        self.url=str(self.url) if self.url else None
        self.locale=str(self.locale) if self.locale else None
        self.timezone=str(self.timezone) if self.timezone else None
        self.city=str(self.city) if self.city else None
        self.state_code=str(self.state_code) if self.state_code else None
        self.country_code=str(self.country_code) if self.country_code else None
        self.address=str(self.address) if self.address else None
        self.postal_code=str(self.postal_code) if self.postal_code else None
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Venue':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Venue']:
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
            return Venue.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Venue.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')