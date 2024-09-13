""" Alert dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.translatedstring import TranslatedString
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.timerange import TimeRange
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.effect import Effect
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.entityselector import EntitySelector
from gtfs_rt_producer_data.generaltransitfeedrealtime.alert.alert_types.cause import Cause


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Alert:
    """
    An alert, indicating some sort of incident in the public transit network.
    Attributes:
        active_period (typing.List[TimeRange]): Time when the alert should be shown to the user. If missing, the alert will be shown as long as it appears in the feed. If multiple ranges are given, the alert will be shown during all of them.
        informed_entity (typing.List[EntitySelector]): Entities whose users we should notify of this alert.
        cause (typing.Optional[Cause]): 
        effect (typing.Optional[Effect]): 
        url (typing.Optional[TranslatedString]): The URL which provides additional information about the alert.
        header_text (typing.Optional[TranslatedString]): Alert header. Contains a short summary of the alert text as plain-text. Full description for the alert as plain-text. The information in the
        description_text (typing.Optional[TranslatedString]): description should add to the information of the header."""
    
    active_period: typing.List[TimeRange]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="active_period"))
    informed_entity: typing.List[EntitySelector]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="informed_entity"))
    cause: typing.Optional[Cause]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cause"))
    effect: typing.Optional[Effect]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="effect"))
    url: typing.Optional[TranslatedString]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    header_text: typing.Optional[TranslatedString]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="header_text"))
    description_text: typing.Optional[TranslatedString]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description_text"))    
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.active_period=self.active_period if isinstance(self.active_period, list) else [v if isinstance(v, TimeRange) else TimeRange.from_serializer_dict(v) if v else None for v in self.active_period] if self.active_period else None
        self.informed_entity=self.informed_entity if isinstance(self.informed_entity, list) else [v if isinstance(v, EntitySelector) else EntitySelector.from_serializer_dict(v) if v else None for v in self.informed_entity] if self.informed_entity else None
        self.cause=Cause(self.cause) if self.cause else None
        self.effect=Effect(self.effect) if self.effect else None
        self.url=self.url if isinstance(self.url, TranslatedString) else TranslatedString.from_serializer_dict(self.url) if self.url else None if self.url else None
        self.header_text=self.header_text if isinstance(self.header_text, TranslatedString) else TranslatedString.from_serializer_dict(self.header_text) if self.header_text else None if self.header_text else None
        self.description_text=self.description_text if isinstance(self.description_text, TranslatedString) else TranslatedString.from_serializer_dict(self.description_text) if self.description_text else None if self.description_text else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Alert':
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
            result = self.to_json()

        if result is not None and content_type.endswith('+gzip'):
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Alert']:
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
                return Alert.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')