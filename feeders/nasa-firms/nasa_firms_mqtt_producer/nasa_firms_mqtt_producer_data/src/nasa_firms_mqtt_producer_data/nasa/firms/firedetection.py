""" FireDetection dataclass. """

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
from nasa_firms_mqtt_producer_data.nasa.firms.confidencelevelenum import ConfidenceLevelenum
from nasa_firms_mqtt_producer_data.nasa.firms.daynightenum import DaynightEnum
from nasa_firms_mqtt_producer_data.nasa.firms.instrumentenum import InstrumentEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class FireDetection:
    """
    A single active-fire / thermal-anomaly pixel detection from a NASA FIRMS satellite product (VIIRS or MODIS), normalised across sensors. Each event is one detection in one satellite overpass; the brightness fields populated depend on `instrument`.
    
    Attributes:
        source (str)
        record_id (str)
        latitude (float)
        longitude (float)
        brightness (typing.Optional[float])
        bright_t31 (typing.Optional[float])
        bright_ti4 (typing.Optional[float])
        bright_ti5 (typing.Optional[float])
        scan (typing.Optional[float])
        track (typing.Optional[float])
        acq_date (datetime.date)
        acq_time (str)
        acq_datetime (datetime.datetime)
        satellite (str)
        instrument (InstrumentEnum)
        confidence (typing.Optional[str])
        confidence_level (ConfidenceLevelenum)
        version (typing.Optional[str])
        frp (typing.Optional[float])
        daynight (typing.Optional[DaynightEnum])
        tile (str)
    """
    
    
    source: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="source"))
    record_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="record_id"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    brightness: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="brightness"))
    bright_t31: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bright_t31"))
    bright_ti4: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bright_ti4"))
    bright_ti5: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bright_ti5"))
    scan: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="scan"))
    track: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="track"))
    acq_date: datetime.date=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="acq_date"))
    acq_time: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="acq_time"))
    acq_datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="acq_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    satellite: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="satellite"))
    instrument: InstrumentEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instrument"))
    confidence: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="confidence"))
    confidence_level: ConfidenceLevelenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="confidence_level"))
    version: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="version"))
    frp: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="frp"))
    daynight: typing.Optional[DaynightEnum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="daynight"))
    tile: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tile"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FireDetection':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['FireDetection']:
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
                return FireDetection.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'FireDetection':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            source='ydpwrzkpvlmxzfpeebqw',
            record_id='jcspszyfmxerzjfhyfdj',
            latitude=float(51.333677143489886),
            longitude=float(99.81655135739305),
            brightness=float(61.76059732044651),
            bright_t31=float(29.448012347554354),
            bright_ti4=float(16.260088756471625),
            bright_ti5=float(23.06793665576373),
            scan=float(46.805458450903856),
            track=float(12.499777989949845),
            acq_date=datetime.date.today(),
            acq_time='ascypfjbkfsodynjihng',
            acq_datetime=datetime.datetime.now(datetime.timezone.utc),
            satellite='zyoimqjavhdftyfswfnt',
            instrument=InstrumentEnum.VIIRS,
            confidence='bxudnahkxlblnwgqpxss',
            confidence_level=ConfidenceLevelenum.low,
            version='jlclpkyrtiqcskvcwjnu',
            frp=float(42.75952889516442),
            daynight=DaynightEnum.D,
            tile='fhjusggbtyzozltcbvps'
        )