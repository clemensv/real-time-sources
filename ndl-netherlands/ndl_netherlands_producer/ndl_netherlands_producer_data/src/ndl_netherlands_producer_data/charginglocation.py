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
from typing import Any
from ndl_netherlands_producer_data.parkingtypeenum import ParkingTypeenum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ChargingLocation:
    """
    Reference data for an EV charging location from the NDL. Contains the static properties of an OCPI v2.2 Location object including address, coordinates, operator details, and aggregate counts of EVSEs and connectors.
    
    Attributes:
        location_id (str)
        country_code (str)
        party_id (str)
        publish (bool)
        name (typing.Optional[str])
        address (str)
        city (str)
        postal_code (typing.Optional[str])
        state (typing.Optional[str])
        country (str)
        latitude (float)
        longitude (float)
        parking_type (typing.Optional[ParkingTypeenum])
        operator_name (typing.Optional[str])
        operator_website (typing.Optional[str])
        suboperator_name (typing.Optional[str])
        owner_name (typing.Optional[str])
        facilities (typing.Optional[Any])
        time_zone (str)
        opening_times_twentyfourseven (typing.Optional[bool])
        charging_when_closed (typing.Optional[bool])
        energy_mix_is_green_energy (typing.Optional[bool])
        energy_mix_supplier_name (typing.Optional[str])
        evse_count (int)
        connector_count (int)
        last_updated (datetime.datetime)
    """
    
    
    location_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_id"))
    country_code: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_code"))
    party_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="party_id"))
    publish: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="publish"))
    name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    address: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="address"))
    city: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="city"))
    postal_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="postal_code"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    country: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    parking_type: typing.Optional[ParkingTypeenum]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parking_type"))
    operator_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_name"))
    operator_website: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_website"))
    suboperator_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="suboperator_name"))
    owner_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="owner_name"))
    facilities: typing.Optional[Any]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="facilities"))
    time_zone: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_zone"))
    opening_times_twentyfourseven: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="opening_times_twentyfourseven"))
    charging_when_closed: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="charging_when_closed"))
    energy_mix_is_green_energy: typing.Optional[bool]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="energy_mix_is_green_energy"))
    energy_mix_supplier_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="energy_mix_supplier_name"))
    evse_count: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="evse_count"))
    connector_count: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="connector_count"))
    last_updated: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="last_updated", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))

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
            location_id='blbguhrbkzhkmqvdlcft',
            country_code='mgwtuklmnsuopbsbiswq',
            party_id='tejpzrgqvkbuvxbvfhgr',
            publish=True,
            name='gpirjksyswdqjecoxrde',
            address='kofutgvnfkloolgblexi',
            city='xgzdyxvwlqcleaeozdfb',
            postal_code='yeetlfwbfzftoejrgeum',
            state='yyrdnzahjxallsrrilpw',
            country='ibkveeeromyootirbavv',
            latitude=float(87.46895938054465),
            longitude=float(78.8595677660295),
            parking_type=ParkingTypeenum.ALONG_MOTORWAY,
            operator_name='wyotintzunvqxvqjzvep',
            operator_website='vsdsmmhxcgruptzhtnda',
            suboperator_name='aspgrlmsmwsqiqdadzso',
            owner_name='ixtbfvcogxzcvhyqbmee',
            facilities=None,
            time_zone='airzflrzgdefuqpufako',
            opening_times_twentyfourseven=False,
            charging_when_closed=True,
            energy_mix_is_green_energy=True,
            energy_mix_supplier_name='iyriupwmwabobeykglsf',
            evse_count=int(30),
            connector_count=int(20),
            last_updated=datetime.datetime.now(datetime.timezone.utc)
        )