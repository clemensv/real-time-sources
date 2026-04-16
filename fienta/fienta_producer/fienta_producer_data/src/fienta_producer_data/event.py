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
    Reference data for a Fienta public event as exposed by the public events endpoint. Emitted at bridge startup and refreshed periodically so downstream consumers can correlate sale-status change events with the latest published event metadata from https://fienta.com/api/v1/public/events.
    
    Attributes:
        event_id (str)
        name (str)
        start (str)
        end (typing.Optional[str])
        duration_text (typing.Optional[str])
        time_notes (typing.Optional[str])
        event_status (str)
        sale_status (str)
        attendance_mode (typing.Optional[str])
        venue_name (typing.Optional[str])
        venue_id (typing.Optional[str])
        address (typing.Optional[str])
        postal_code (typing.Optional[str])
        description (typing.Optional[str])
        url (str)
        buy_tickets_url (typing.Optional[str])
        image_url (typing.Optional[str])
        image_small_url (typing.Optional[str])
        series_id (typing.Optional[str])
        organizer_name (typing.Optional[str])
        organizer_phone (typing.Optional[str])
        organizer_email (typing.Optional[str])
        organizer_id (typing.Optional[int])
        categories (typing.Optional[typing.List[str]])
    """
    
    
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    start: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start"))
    end: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end"))
    duration_text: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="duration_text"))
    time_notes: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_notes"))
    event_status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_status"))
    sale_status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sale_status"))
    attendance_mode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attendance_mode"))
    venue_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_name"))
    venue_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="venue_id"))
    address: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address"))
    postal_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="postal_code"))
    description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="description"))
    url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="url"))
    buy_tickets_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="buy_tickets_url"))
    image_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_url"))
    image_small_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="image_small_url"))
    series_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="series_id"))
    organizer_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizer_name"))
    organizer_phone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizer_phone"))
    organizer_email: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizer_email"))
    organizer_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizer_id"))
    categories: typing.Optional[typing.List[str]]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="categories"))

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
            event_id='djtzdgmvrzfdaarqwuty',
            name='xeiikcujtuykssjnktwy',
            start='ocyyjreshixminugpgnu',
            end='tkeujtjmfvmelsyicpwp',
            duration_text='lupwdecaoveupkopxtvz',
            time_notes='rwscjbrhpvyvjkpkqtmq',
            event_status='flnodrcloslkrcmbuvcz',
            sale_status='zeqkfwwrddshwopllhyb',
            attendance_mode='mqumguhqnkymugrsvocn',
            venue_name='qfqouzrktkqdtteusffe',
            venue_id='hbpxmejndrjqkpodhioo',
            address='ikkdryklkxczehmocugh',
            postal_code='qvfbnxatzwllfprfxbpi',
            description='htpimvsvhmknjgkwnmas',
            url='zravhrfceljvqzaaidrl',
            buy_tickets_url='dthexgqyljrmlkqqawbb',
            image_url='btpudhqhndqgbhcfwyka',
            image_small_url='leiskeyjttzibshozgmr',
            series_id='egclyjqxbmokuigaldbs',
            organizer_name='bxyzplbtindbzwurjaby',
            organizer_phone='ipziyovqbtxewxzlnshn',
            organizer_email='wwurmymyvddbqmnptgjr',
            organizer_id=int(94),
            categories=['kiuewsrpqkvwbrfkejin', 'pghtppfesottjgizyjkx']
        )