""" ChargingLocation dataclass. """

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
from open_charge_map_mqtt_producer_data.io.openchargemap.connection import Connection
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ChargingLocation:
    """
    One electric-vehicle charging location (point of interest) from the Open Charge Map v3 POI API `https://api.openchargemap.io/v3/poi/`. Open Charge Map is the largest global open registry of EV charging equipment, with 300,000+ locations worldwide contributed and verified by operators, national databases, and the public under open licences. This event carries the stable identity, the parsed and flattened address with WGS 84 coordinates, denormalized operator/usage/status labels, editorial and freshness timestamps, and the itemized charging connections. The feeder emits it at startup for the configured scope and thereafter on the `DateLastStatusUpdate` delta, so consumers can maintain a temporally consistent view of each charging location keyed by `poi_id`.
    
    Attributes:
        poi_id (int)
        uuid (str)
        data_provider_id (typing.Optional[int])
        operator_id (typing.Optional[int])
        operator_title (typing.Optional[str])
        usage_type_id (typing.Optional[int])
        usage_type_title (typing.Optional[str])
        usage_cost (typing.Optional[str])
        status_type_id (typing.Optional[int])
        status_title (typing.Optional[str])
        is_operational (typing.Optional[bool])
        submission_status_type_id (typing.Optional[int])
        submission_status_title (typing.Optional[str])
        data_quality_level (typing.Optional[int])
        number_of_points (typing.Optional[int])
        general_comments (typing.Optional[str])
        is_recently_verified (typing.Optional[bool])
        date_created (typing.Optional[datetime.datetime])
        date_last_status_update (typing.Optional[datetime.datetime])
        date_last_verified (typing.Optional[datetime.datetime])
        date_last_confirmed (typing.Optional[datetime.datetime])
        date_planned (typing.Optional[datetime.datetime])
        address_id (typing.Optional[int])
        address_title (typing.Optional[str])
        address_line1 (typing.Optional[str])
        address_line2 (typing.Optional[str])
        town (typing.Optional[str])
        state_or_province (typing.Optional[str])
        postcode (typing.Optional[str])
        country_id (typing.Optional[int])
        country_iso_code (typing.Optional[str])
        country_title (typing.Optional[str])
        latitude (float)
        longitude (float)
        contact_telephone1 (typing.Optional[str])
        contact_telephone2 (typing.Optional[str])
        contact_email (typing.Optional[str])
        access_comments (typing.Optional[str])
        related_url (typing.Optional[str])
        connections (typing.List[Connection])
    """
    
    
    poi_id: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="poi_id"))
    uuid: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uuid"))
    data_provider_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_provider_id"))
    operator_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_id"))
    operator_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_title"))
    usage_type_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="usage_type_id"))
    usage_type_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="usage_type_title"))
    usage_cost: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="usage_cost"))
    status_type_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status_type_id"))
    status_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status_title"))
    is_operational: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_operational"))
    submission_status_type_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="submission_status_type_id"))
    submission_status_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="submission_status_title"))
    data_quality_level: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_quality_level"))
    number_of_points: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="number_of_points"))
    general_comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="general_comments"))
    is_recently_verified: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_recently_verified"))
    date_created: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_created", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    date_last_status_update: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_last_status_update", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    date_last_verified: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_last_verified", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    date_last_confirmed: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_last_confirmed", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    date_planned: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_planned", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    address_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_id"))
    address_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_title"))
    address_line1: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_line1"))
    address_line2: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address_line2"))
    town: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="town"))
    state_or_province: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_or_province"))
    postcode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="postcode"))
    country_id: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_id"))
    country_iso_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_iso_code"))
    country_title: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_title"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    contact_telephone1: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact_telephone1"))
    contact_telephone2: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact_telephone2"))
    contact_email: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contact_email"))
    access_comments: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="access_comments"))
    related_url: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="related_url"))
    connections: typing.List[Connection]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connections"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'ChargingLocation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['ChargingLocation']:
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
                return ChargingLocation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'ChargingLocation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            poi_id=int(22),
            uuid='bacvaieggxehvmzjqfci',
            data_provider_id=int(14),
            operator_id=int(40),
            operator_title='zhzllmvzhfkstpleqgji',
            usage_type_id=int(9),
            usage_type_title='afxxaunrhlibzvemzfwg',
            usage_cost='wolcviaifpvzbgcgmzpf',
            status_type_id=int(87),
            status_title='lfzmopuhjlzhwxukmeob',
            is_operational=True,
            submission_status_type_id=int(21),
            submission_status_title='kuiyqquvdbbfzqaazwvb',
            data_quality_level=int(39),
            number_of_points=int(23),
            general_comments='nzufwkbtvjhpjwyovzls',
            is_recently_verified=False,
            date_created=datetime.datetime.now(datetime.timezone.utc),
            date_last_status_update=datetime.datetime.now(datetime.timezone.utc),
            date_last_verified=datetime.datetime.now(datetime.timezone.utc),
            date_last_confirmed=datetime.datetime.now(datetime.timezone.utc),
            date_planned=datetime.datetime.now(datetime.timezone.utc),
            address_id=int(83),
            address_title='rypkkkqlsdmmykmrnnss',
            address_line1='kskbxsbqwrsialvvdzwi',
            address_line2='bioravatonlxrdfkvtcm',
            town='mycsgcikhoubbvbcgwtx',
            state_or_province='djmspowkyisjwwuwrbrd',
            postcode='snfdcmibjazbosgljlum',
            country_id=int(28),
            country_iso_code='dhpclvovatseuwjtjtsm',
            country_title='kylihdvmkbnkepzktyed',
            latitude=float(96.27547340431354),
            longitude=float(0.8295924492855877),
            contact_telephone1='naihgqceoxxjjtxzamwy',
            contact_telephone2='tcmtflbglbarwokhlckm',
            contact_email='zuwsbwrkfefrcqzyfkga',
            access_comments='nrmffzmbbrnonnlxrtqe',
            related_url='ysheygdejxvjhlojofly',
            connections=[None, None, None, None, None]
        )