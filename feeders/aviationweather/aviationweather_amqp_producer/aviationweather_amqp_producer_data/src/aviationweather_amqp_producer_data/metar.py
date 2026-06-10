""" Metar dataclass. """

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
from marshmallow import fields
import json
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Metar:
    """
    METAR aviation weather observation from the AviationWeather.gov API. Reports surface conditions including temperature, dewpoint, wind, visibility, pressure, clouds, and flight category for an ICAO reporting station.
    
    Attributes:
        icao_id (str)
        obs_time (datetime.datetime)
        report_time (typing.Optional[datetime.datetime])
        temp (typing.Optional[float])
        dewp (typing.Optional[float])
        wdir (typing.Optional[int])
        wspd (typing.Optional[int])
        wgst (typing.Optional[int])
        visib (typing.Optional[str])
        altim (typing.Optional[float])
        slp (typing.Optional[float])
        qc_field (typing.Optional[int])
        wx_string (typing.Optional[str])
        metar_type (typing.Optional[str])
        raw_ob (str)
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        elevation (typing.Optional[float])
        flt_cat (typing.Optional[str])
        clouds (typing.Optional[str])
        name (typing.Optional[str])
    """
    
    
    icao_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icao_id"))
    obs_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="obs_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    report_time: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    temp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temp"))
    dewp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dewp"))
    wdir: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wdir"))
    wspd: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wspd"))
    wgst: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wgst"))
    visib: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="visib"))
    altim: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altim"))
    slp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="slp"))
    qc_field: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="qc_field"))
    wx_string: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wx_string"))
    metar_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="metar_type"))
    raw_ob: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="raw_ob"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    elevation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="elevation"))
    flt_cat: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="flt_cat"))
    clouds: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="clouds"))
    name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Metar':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Metar']:
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
                return Metar.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Metar':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            icao_id='qmqjforijdeuvextxphm',
            obs_time=datetime.datetime.now(datetime.timezone.utc),
            report_time=datetime.datetime.now(datetime.timezone.utc),
            temp=float(80.21572581974111),
            dewp=float(63.403277380691236),
            wdir=int(95),
            wspd=int(79),
            wgst=int(27),
            visib='fjflrjxyznvtpytkyerd',
            altim=float(20.514876563276818),
            slp=float(99.97022693673782),
            qc_field=int(57),
            wx_string='cfvhllknsuswgomtjrhy',
            metar_type='sfbvfaaftjgzdtzuqxxy',
            raw_ob='ikqvqkohwwjgfowltbfh',
            latitude=float(79.62035167736377),
            longitude=float(14.884894523411207),
            elevation=float(56.53002081043822),
            flt_cat='kycptrackfwvegwthidc',
            clouds='zqgkgphvpzdmvpdonukp',
            name='bsbperftpckfytemtmsy'
        )