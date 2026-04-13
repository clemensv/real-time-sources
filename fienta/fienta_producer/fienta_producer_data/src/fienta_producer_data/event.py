""" Event dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Event:
    """
    Reference data for a Fienta public event. Emitted at bridge startup and refreshed periodically so downstream consumers can correlate sale-status change events with full event metadata. Sourced from the Fienta public events API at https://fienta.com/api/v1/public/events.
    
    Attributes:
        event_id (str)
        name (str)
        slug (typing.Optional[str])
        description (typing.Optional[str])
        start (str)
        end (typing.Optional[str])
        timezone (typing.Optional[str])
        url (str)
        language (typing.Optional[str])
        currency (typing.Optional[str])
        status (str)
        sale_status (str)
        is_online (typing.Optional[bool])
        is_free (typing.Optional[bool])
        location (typing.Optional[str])
        country (typing.Optional[str])
        region (typing.Optional[str])
        image_url (typing.Optional[str])
        organizer_name (typing.Optional[str])
        organizer_url (typing.Optional[str])
        categories (typing.Optional[typing.Any])
        created_at (typing.Optional[str])
        updated_at (typing.Optional[str])
    """
    
    
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    slug: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="slug"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    start: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start"))
    end: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end"))
    timezone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timezone"))
    url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    language: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="language"))
    currency: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="currency"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))
    sale_status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sale_status"))
    is_online: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_online"))
    is_free: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_free"))
    location: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location"))
    country: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    region: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="region"))
    image_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_url"))
    organizer_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizer_name"))
    organizer_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizer_url"))
    categories: typing.Optional[typing.Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="categories"))
    created_at: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created_at"))
    updated_at: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="updated_at"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Event':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
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
            if isinstance(v, enum.Enum):
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Event']:
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Event.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Event':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            event_id='fqdcajvabhgbfbvdoced',
            name='daagywylgwgmlgogixod',
            slug='rnpdmzfmrqmtlugutrwn',
            description='btiaccubbjoaugrlajgw',
            start='slitotirndozzlaynjcr',
            end='chezpltnpuuyhzpogcbd',
            timezone='ewsmwejvzgrryieoqlnq',
            url='nypzglwovhefgqdbqeht',
            language='cnwkolkybhfxsipzynli',
            currency='aftyamrewhtvzhqtkiln',
            status='yyzohusiyntyrwmpztby',
            sale_status='vglfwyrokskwitxovlpw',
            is_online=True,
            is_free=False,
            location='jkgnfofjtngbeapvnphx',
            country='qgmvousqbmuvgyaofjih',
            region='reirmbppmmaetzseupek',
            image_url='vqdtwqsjsoqcdvfaxfwg',
            organizer_name='jyakpxkkfbsiltdbrogm',
            organizer_url='ttxfatunrgnbjutbgbms',
            categories={"test": "test"},
            created_at='khmojnhebopzcmqzwqhm',
            updated_at='yayembxhzirmvzwvrqno'
        )