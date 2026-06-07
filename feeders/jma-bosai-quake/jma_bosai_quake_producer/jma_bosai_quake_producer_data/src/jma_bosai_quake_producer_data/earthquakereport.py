""" EarthquakeReport dataclass. """

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
from jma_bosai_quake_producer_data.affectedprefecture import AffectedPrefecture
from jma_bosai_quake_producer_data.maxintensityenum import MaxIntensityenum
from jma_bosai_quake_producer_data.affectedcity import AffectedCity
from jma_bosai_quake_producer_data.infotypeenum import InfoTypeenum
from jma_bosai_quake_producer_data.bulletintypeenum import BulletinTypeenum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class EarthquakeReport:
    """
    JMA Bosai earthquake and seismic intensity report header enriched with parsed hypocenter coordinates, prefecture and city intensity summaries, and tsunami-related comment interpretation from the detail bulletin when available.
    
    Attributes:
        prefecture (str)
        magnitude_bucket (str)
        event_id (str)
        serial (int)
        report_id (str)
        info_type (InfoTypeenum)
        report_datetime (datetime.datetime)
        report_datetime_local (datetime.datetime)
        control_datetime (datetime.datetime)
        control_datetime_local (datetime.datetime)
        origin_datetime (datetime.datetime)
        origin_datetime_local (datetime.datetime)
        title_jp (str)
        title_en (typing.Optional[str])
        epicenter_area_code (typing.Optional[str])
        epicenter_area_jp (typing.Optional[str])
        epicenter_area_en (typing.Optional[str])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        depth_km (typing.Optional[float])
        magnitude (typing.Optional[float])
        max_intensity (typing.Optional[MaxIntensityenum])
        bulletin_type (BulletinTypeenum)
        detail_url (str)
        affected_prefectures (typing.List[AffectedPrefecture])
        affected_cities (typing.List[AffectedCity])
        tsunami_possible (typing.Optional[bool])
    """
    
    
    prefecture: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="prefecture"))
    magnitude_bucket: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="magnitude_bucket"))
    event_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="event_id"))
    serial: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="serial"))
    report_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_id"))
    info_type: InfoTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="info_type"))
    report_datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    report_datetime_local: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="report_datetime_local", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    control_datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="control_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    control_datetime_local: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="control_datetime_local", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    origin_datetime: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_datetime", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    origin_datetime_local: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_datetime_local", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    title_jp: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title_jp"))
    title_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="title_en"))
    epicenter_area_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="epicenter_area_code"))
    epicenter_area_jp: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="epicenter_area_jp"))
    epicenter_area_en: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="epicenter_area_en"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    depth_km: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="depth_km"))
    magnitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="magnitude"))
    max_intensity: typing.Optional[MaxIntensityenum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="max_intensity"))
    bulletin_type: BulletinTypeenum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bulletin_type"))
    detail_url: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="detail_url"))
    affected_prefectures: typing.List[AffectedPrefecture]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="affected_prefectures"))
    affected_cities: typing.List[AffectedCity]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="affected_cities"))
    tsunami_possible: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tsunami_possible"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'EarthquakeReport':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['EarthquakeReport']:
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
                return EarthquakeReport.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'EarthquakeReport':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            prefecture='wfphjtdzotowsorwnukz',
            magnitude_bucket='vlfirfgffdrabahwkopj',
            event_id='kvupqzxkmlkekyhskgee',
            serial=int(23),
            report_id='fwebykfrxcmwycfanomh',
            info_type=InfoTypeenum.ISSUED,
            report_datetime=datetime.datetime.now(datetime.timezone.utc),
            report_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            control_datetime=datetime.datetime.now(datetime.timezone.utc),
            control_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            origin_datetime=datetime.datetime.now(datetime.timezone.utc),
            origin_datetime_local=datetime.datetime.now(datetime.timezone.utc),
            title_jp='zhxelhuclarerrtwwhhr',
            title_en='nmtlsincastfgduduxzg',
            epicenter_area_code='pebcbsqerahpmdmgmazd',
            epicenter_area_jp='ywltajaplmzcqvanwxpo',
            epicenter_area_en='zhvcaqwhkzjbmdasbtrr',
            latitude=float(60.126398733280226),
            longitude=float(43.10696309804229),
            depth_km=float(74.35338581856773),
            magnitude=float(66.94679135547042),
            max_intensity=MaxIntensityenum.INTENSITY_1,
            bulletin_type=BulletinTypeenum.VXSE51,
            detail_url='ogcslpncauzpwsrfutfo',
            affected_prefectures=[None],
            affected_cities=[None, None, None, None, None],
            tsunami_possible=True
        )
