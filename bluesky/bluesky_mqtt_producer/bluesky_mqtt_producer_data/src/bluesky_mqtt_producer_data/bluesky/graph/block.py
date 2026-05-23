""" Block dataclass. """

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
class Block:
    """
    A block relationship between users
    
    Attributes:
        uri (str)
        cid (str)
        did (str)
        handle (typing.Optional[str])
        subject (str)
        subject_handle (typing.Optional[str])
        created_at (str)
        indexed_at (str)
        seq (int)
        collection (str)
        lang (str)
    """
    
    
    uri: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uri"))
    cid: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="cid"))
    did: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="did"))
    handle: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="handle"))
    subject: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subject"))
    subject_handle: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="subject_handle"))
    created_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="created_at"))
    indexed_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="indexed_at"))
    seq: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="seq"))
    collection: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="collection"))
    lang: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lang"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Block':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Block']:
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
                return Block.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Block':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            uri='snwprlpxngokrxbkbbdo',
            cid='rtcgxalmrmvecwernxcu',
            did='nkivybpxtndjinzehfqh',
            handle='pesknacusxrrxlxidfvw',
            subject='ikeeqydvyuwwymuxydgu',
            subject_handle='uhvbmrjhbcakfhhxtrgb',
            created_at='ekjctgruhyujyltmofnf',
            indexed_at='faaxincisedpkpyxmvez',
            seq=int(30),
            collection='wijrqqmyljxcftmorycg',
            lang='bqdwmiobnbweeckfhiva'
        )