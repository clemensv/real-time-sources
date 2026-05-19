""" Grid dataclass. """

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
class Grid:
    """
    An ICON-D2 forecast grid for one model run, one parameter, and one lead hour. Values are pre-aggregated to a regular 0.1 degree lat/lon grid by area mean over the source ICON triangular cells. The lats/lons/values arrays have the same length and are aligned by index: cell i has coordinates (lats[i], lons[i]) and value values[i].
    
    Attributes:
        run_id (str)
        run_time (str)
        parameter (str)
        unit (str)
        lead_hour (int)
        valid_time (str)
        produced_at (str)
        source_url (str)
        resolution_deg (float)
        bbox_min_lon (float)
        bbox_min_lat (float)
        bbox_max_lon (float)
        bbox_max_lat (float)
        lats (typing.List[float])
        lons (typing.List[float])
        values (typing.List[float])
    """
    
    
    run_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="run_id"))
    run_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="run_time"))
    parameter: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter"))
    unit: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unit"))
    lead_hour: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lead_hour"))
    valid_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="valid_time"))
    produced_at: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="produced_at"))
    source_url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source_url"))
    resolution_deg: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="resolution_deg"))
    bbox_min_lon: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_min_lon"))
    bbox_min_lat: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_min_lat"))
    bbox_max_lon: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_max_lon"))
    bbox_max_lat: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bbox_max_lat"))
    lats: typing.List[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lats"))
    lons: typing.List[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lons"))
    values: typing.List[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="values"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Grid':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Grid']:
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
                return Grid.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Grid':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            run_id='fbwxbhhdiylivoirxtjm',
            run_time='vpuejmrdahqhhuamdnhr',
            parameter='rrztexdawnogkvoprtqd',
            unit='ninijtcwhauzfctckolb',
            lead_hour=int(42),
            valid_time='mlekfqgyjccgxvjskcbx',
            produced_at='civrqaaikdrpgrrymnww',
            source_url='zptojjzmjooxtdrbgmhr',
            resolution_deg=float(57.489659757633014),
            bbox_min_lon=float(86.34681962440187),
            bbox_min_lat=float(99.49208569174088),
            bbox_max_lon=float(12.254348066598542),
            bbox_max_lat=float(38.58950624026703),
            lats=[float(39.92187281437259), float(43.721652771192396)],
            lons=[float(26.50590691509871)],
            values=[float(65.46033357057797)]
        )