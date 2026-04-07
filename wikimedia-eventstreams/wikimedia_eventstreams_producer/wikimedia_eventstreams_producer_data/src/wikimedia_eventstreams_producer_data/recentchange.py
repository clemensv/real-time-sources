""" RecentChange dataclass. """

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
from wikimedia_eventstreams_producer_data.unnamedclass import UnnamedClass


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class RecentChange:
    """
    Normalized representation of Wikimedia's mediawiki/recentchange event schema. This contract preserves the documented recentchange payload while renaming the upstream $schema field to schema_uri and serializing the variant log_params field into log_params_json for stable generated types.
    
    Attributes:
        event_id (str)
        event_time (str)
        schema_uri (str)
        meta (UnnamedClass)
        id (typing.Optional[str])
        type (str)
        namespace (int)
        title (str)
        title_url (typing.Optional[str])
        comment (typing.Optional[str])
        timestamp (int)
        user (str)
        bot (typing.Optional[bool])
        minor (typing.Optional[bool])
        patrolled (typing.Optional[bool])
        length (typing.Optional[UnnamedClass])
        revision (typing.Optional[UnnamedClass])
        server_url (typing.Optional[str])
        server_name (typing.Optional[str])
        server_script_path (typing.Optional[str])
        wiki (str)
        parsedcomment (typing.Optional[str])
        notify_url (typing.Optional[str])
        log_type (typing.Optional[str])
        log_action (typing.Optional[str])
        log_action_comment (typing.Optional[str])
        log_id (typing.Optional[str])
        log_params_json (typing.Optional[str])
    """
    
    
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    event_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_time"))
    schema_uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="schema_uri"))
    meta: UnnamedClass=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="meta"))
    id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="type"))
    namespace: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="namespace"))
    title: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title"))
    title_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title_url"))
    comment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="comment"))
    timestamp: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timestamp"))
    user: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="user"))
    bot: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bot"))
    minor: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minor"))
    patrolled: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="patrolled"))
    length: typing.Optional[UnnamedClass]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="length"))
    revision: typing.Optional[UnnamedClass]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="revision"))
    server_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="server_url"))
    server_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="server_name"))
    server_script_path: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="server_script_path"))
    wiki: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wiki"))
    parsedcomment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parsedcomment"))
    notify_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="notify_url"))
    log_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="log_type"))
    log_action: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="log_action"))
    log_action_comment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="log_action_comment"))
    log_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="log_id"))
    log_params_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="log_params_json"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'RecentChange':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['RecentChange']:
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
                return RecentChange.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'RecentChange':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            event_id='ilewtimabafbogqriuas',
            event_time='kwkorghyajkdvaajcbrs',
            schema_uri='dmxnikerbllhgfiuwtlo',
            meta=None,
            id='rpahsssnmcyvlfzoxfmf',
            type='brvrdvogmwngmkdrcsju',
            namespace=int(13),
            title='jgsuvkynvwphpgrlmdrz',
            title_url='oelebaqcfrnoyjkxbepn',
            comment='nlwdbqsxwkqszhyrhutn',
            timestamp=int(16),
            user='swdpjseuilkxyurvvhyw',
            bot=True,
            minor=True,
            patrolled=True,
            length=None,
            revision=None,
            server_url='fspyrgxetoofkcvygkjw',
            server_name='grckqptpxpncafaquciu',
            server_script_path='mrjnfphdfzprinlgpgxf',
            wiki='laqoyfuhoirgtraxtbtc',
            parsedcomment='vikxshcgdldenvrqejft',
            notify_url='xaprxqzzecypvimofzjd',
            log_type='efrtmoesmnjpnzduxvxj',
            log_action='nluewtuxpvokshyjhjam',
            log_action_comment='mfmtoanfyjbgwufrhbzb',
            log_id='alyimtxxdbarwxdpfvmg',
            log_params_json='bodtdklpoaaizywniomt'
        )