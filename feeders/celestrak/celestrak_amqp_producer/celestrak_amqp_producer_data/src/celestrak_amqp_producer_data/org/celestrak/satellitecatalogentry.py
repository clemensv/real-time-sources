""" SatelliteCatalogEntry dataclass. """

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
from typing import Any
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SatelliteCatalogEntry:
    """
    Reference record for one object in the US Space Force satellite catalog (SATCAT), as published by CelesTrak at `satcat/records.php`. Carries the object's identity (name, international designator, NORAD number), classification (type, owner, operational status) and coarse orbital parameters (period, inclination, apogee, perigee). Emitted as reference data at bridge start-up and periodically refreshed, so consumers can resolve the `NORAD_CAT_ID` on every OrbitMeanElements event to a named, described object without an out-of-band lookup. Shares the `NORAD_CAT_ID` key model and Kafka topic with the element-set events for temporal consistency.
    
    Attributes:
        OBJECT_NAME (typing.Optional[str])
        OBJECT_ID (typing.Optional[str])
        NORAD_CAT_ID (int)
        OBJECT_TYPE (typing.Optional[Any])
        OPS_STATUS_CODE (typing.Optional[str])
        OWNER (typing.Optional[str])
        LAUNCH_DATE (typing.Optional[datetime.date])
        LAUNCH_SITE (typing.Optional[str])
        DECAY_DATE (typing.Optional[datetime.date])
        PERIOD (typing.Optional[float])
        INCLINATION (typing.Optional[float])
        APOGEE (typing.Optional[int])
        PERIGEE (typing.Optional[int])
        RCS (typing.Optional[float])
        DATA_STATUS_CODE (typing.Optional[Any])
        ORBIT_CENTER (typing.Optional[str])
        ORBIT_TYPE (typing.Optional[Any])
    """
    
    
    OBJECT_NAME: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OBJECT_NAME"))
    OBJECT_ID: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OBJECT_ID"))
    NORAD_CAT_ID: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="NORAD_CAT_ID"))
    OBJECT_TYPE: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OBJECT_TYPE"))
    OPS_STATUS_CODE: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OPS_STATUS_CODE"))
    OWNER: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OWNER"))
    LAUNCH_DATE: typing.Optional[datetime.date]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="LAUNCH_DATE"))
    LAUNCH_SITE: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="LAUNCH_SITE"))
    DECAY_DATE: typing.Optional[datetime.date]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="DECAY_DATE"))
    PERIOD: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="PERIOD"))
    INCLINATION: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="INCLINATION"))
    APOGEE: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="APOGEE"))
    PERIGEE: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="PERIGEE"))
    RCS: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="RCS"))
    DATA_STATUS_CODE: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="DATA_STATUS_CODE"))
    ORBIT_CENTER: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ORBIT_CENTER"))
    ORBIT_TYPE: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ORBIT_TYPE"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'SatelliteCatalogEntry':
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
            if isinstance(result, str):
                result = result.encode('utf-8')
            if isinstance(result, str):
                result = result.encode('utf-8')

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['SatelliteCatalogEntry']:
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
                return SatelliteCatalogEntry.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'SatelliteCatalogEntry':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            OBJECT_NAME='xbmelcvmpfzjreqklfaf',
            OBJECT_ID='hnpiiroxmsbjkqdllxrz',
            NORAD_CAT_ID=int(29),
            OBJECT_TYPE=None,
            OPS_STATUS_CODE='ipckelfhpycniehedwsu',
            OWNER='dnwmbmeexsmhqdeswcqv',
            LAUNCH_DATE=datetime.date.today(),
            LAUNCH_SITE='bnezeugcqatsccpadbdj',
            DECAY_DATE=datetime.date.today(),
            PERIOD=float(25.841049801001148),
            INCLINATION=float(73.23927555792302),
            APOGEE=int(7),
            PERIGEE=int(59),
            RCS=float(82.44953208547575),
            DATA_STATUS_CODE=None,
            ORBIT_CENTER='edmztuavqbdqwnurrpfp',
            ORBIT_TYPE=None
        )