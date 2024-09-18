""" Agency dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Agency:
    """
    Information about the transit agencies.
    Attributes:
        agencyId (str): Identifies a transit brand which is often synonymous with a transit agency.
        agencyName (str): Full name of the transit agency.
        agencyUrl (str): URL of the transit agency.
        agencyTimezone (str): Timezone where the transit agency is located.
        agencyLang (typing.Optional[str]): Primary language used by this transit agency.
        agencyPhone (typing.Optional[str]): A voice telephone number for the specified agency.
        agencyFareUrl (typing.Optional[str]): URL of a web page that allows a rider to purchase tickets or other fare instruments for that agency online.
        agencyEmail (typing.Optional[str]): Email address actively monitored by the agency’s customer service department."""
    
    agencyId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyId"))
    agencyName: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyName"))
    agencyUrl: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyUrl"))
    agencyTimezone: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyTimezone"))
    agencyLang: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyLang"))
    agencyPhone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyPhone"))
    agencyFareUrl: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyFareUrl"))
    agencyEmail: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyEmail"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.agencyId=str(self.agencyId)
        self.agencyName=str(self.agencyName)
        self.agencyUrl=str(self.agencyUrl)
        self.agencyTimezone=str(self.agencyTimezone)
        self.agencyLang=str(self.agencyLang) if self.agencyLang else None
        self.agencyPhone=str(self.agencyPhone) if self.agencyPhone else None
        self.agencyFareUrl=str(self.agencyFareUrl) if self.agencyFareUrl else None
        self.agencyEmail=str(self.agencyEmail) if self.agencyEmail else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Agency':
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
                    'application/json': Encodes the data to JSON format.
                Supported content type extensions:
                    '+gzip': Compresses the byte array using gzip, e.g. 'application/json+gzip'.

        Returns:
            The byte array representation of the dataclass.        
        """
        content_type = content_type_string.split(';')[0].strip()
        result = None
        if content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member

        if result is not None and content_type.endswith('+gzip'):
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Agency']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
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
        if content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Agency.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')