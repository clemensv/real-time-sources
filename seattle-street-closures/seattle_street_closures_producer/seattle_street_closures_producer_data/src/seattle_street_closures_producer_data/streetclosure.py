""" StreetClosure dataclass. """

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
class StreetClosure:
    """
    Street closure row from the Seattle Department of Transportation street closures dataset, describing one closed street segment and its active occurrence window.
    
    Attributes:
        closure_id (str)
        permit_number (str)
        permit_type (str)
        project_name (typing.Optional[str])
        project_description (typing.Optional[str])
        start_date (str)
        end_date (str)
        sunday (typing.Optional[str])
        monday (typing.Optional[str])
        tuesday (typing.Optional[str])
        wednesday (typing.Optional[str])
        thursday (typing.Optional[str])
        friday (typing.Optional[str])
        saturday (typing.Optional[str])
        street_on (typing.Optional[str])
        street_from (typing.Optional[str])
        street_to (typing.Optional[str])
        segkey (typing.Optional[str])
        geometry_json (typing.Optional[str])
    """
    
    
    closure_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="closure_id"))
    permit_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="permit_number"))
    permit_type: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="permit_type"))
    project_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="project_name"))
    project_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="project_description"))
    start_date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_date"))
    end_date: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="end_date"))
    sunday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sunday"))
    monday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="monday"))
    tuesday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tuesday"))
    wednesday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wednesday"))
    thursday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="thursday"))
    friday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="friday"))
    saturday: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="saturday"))
    street_on: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="street_on"))
    street_from: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="street_from"))
    street_to: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="street_to"))
    segkey: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="segkey"))
    geometry_json: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry_json"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'StreetClosure':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['StreetClosure']:
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
                return StreetClosure.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'StreetClosure':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            closure_id='jhggcwbhdpczfjfquypv',
            permit_number='huhpuweydvxisfnsbste',
            permit_type='ysewyvsryidkmflmuyvy',
            project_name='nbmftbvfihczxivgquou',
            project_description='ptflckydtvjyhmyipefp',
            start_date='pgfdlzlctpaqfsyetxvh',
            end_date='ldfcwonpxabmocsagaqt',
            sunday='djfqmjykkfoeycqlrxxc',
            monday='lllgsgelihppfxvvmxcq',
            tuesday='kzshkslkukfdkbqoltjo',
            wednesday='ktaplpfngwsziyrimiuo',
            thursday='ysmfhkypwlopcoxxnanc',
            friday='bmqudyxtnpoowkepnayx',
            saturday='henyqkmupahfcirwkksl',
            street_on='oivbruswxobkbtqjpdly',
            street_from='kcfhnkslxglfmiqzsjev',
            street_to='utjlrevgwdytlaispznn',
            segkey='xjssgiqjakpnbkrknffi',
            geometry_json='eqefuueyywmqyiqxqwxh'
        )