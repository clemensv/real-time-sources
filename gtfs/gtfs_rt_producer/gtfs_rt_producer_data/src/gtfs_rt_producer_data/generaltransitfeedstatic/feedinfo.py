""" FeedInfo dataclass. """

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
class FeedInfo:
    """
    Provides information about the GTFS feed itself.
    Attributes:
        feedPublisherName (str): Full name of the organization that publishes the feed.
        feedPublisherUrl (str): URL of the feed publishing organization's website.
        feedLang (str): Default language for the text in this feed.
        defaultLang (typing.Optional[str]): Specifies the language used when the data consumer doesn’t know the language of the user.
        feedStartDate (typing.Optional[str]): The start date for the dataset.
        feedEndDate (typing.Optional[str]): The end date for the dataset.
        feedVersion (typing.Optional[str]): Version string that indicates the current version of their GTFS dataset.
        feedContactEmail (typing.Optional[str]): Email address for communication with the data publisher.
        feedContactUrl (typing.Optional[str]): URL for a web page that allows a feed consumer to contact the data publisher."""
    
    feedPublisherName: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedPublisherName"))
    feedPublisherUrl: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedPublisherUrl"))
    feedLang: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedLang"))
    defaultLang: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="defaultLang"))
    feedStartDate: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedStartDate"))
    feedEndDate: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedEndDate"))
    feedVersion: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedVersion"))
    feedContactEmail: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedContactEmail"))
    feedContactUrl: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="feedContactUrl"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.feedPublisherName=str(self.feedPublisherName)
        self.feedPublisherUrl=str(self.feedPublisherUrl)
        self.feedLang=str(self.feedLang)
        self.defaultLang=str(self.defaultLang) if self.defaultLang else None
        self.feedStartDate=str(self.feedStartDate) if self.feedStartDate else None
        self.feedEndDate=str(self.feedEndDate) if self.feedEndDate else None
        self.feedVersion=str(self.feedVersion) if self.feedVersion else None
        self.feedContactEmail=str(self.feedContactEmail) if self.feedContactEmail else None
        self.feedContactUrl=str(self.feedContactUrl) if self.feedContactUrl else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FeedInfo':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['FeedInfo']:
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
                return FeedInfo.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')