""" PropagatedSolarWind dataclass. """

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
from noaa_swpc_l1_amqp_producer_data.gov.noaa.swpc.l1.spacecraftenum import SpacecraftEnum
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class PropagatedSolarWind:
    """
    One minute-resolution solar-wind observation at the Sun-Earth Lagrange-1 (L1) point with forward-propagated Earth-arrival timestamp. Fuses plasma (speed/density/temperature), magnetic-field (Bx/By/Bz/Bt in GSM coordinates), and bulk velocity (Vx/Vy/Vz in GSM coordinates) into one row per `time_tag`. Sourced from `GET https://services.swpc.noaa.gov/products/geospace/propagated-solar-wind.json` — a 7-day rolling window in array-of-arrays form, with the column header at index 0 and one observation per minute thereafter. The operational primary spacecraft is NOAA's DSCOVR; NASA's ACE serves as the backup. Many sub-fields are nullable: DSCOVR's magnetometer experiences routine gaps, and DSCOVR does not measure the Vx/Vy/Vz velocity components reliably (the upstream nearly always emits null for those). Consumers must treat plasma and magnetic-field measurements as independently optional and not skip rows that have only partial values.
    
    Attributes:
        spacecraft (SpacecraftEnum)
        time_tag (datetime.datetime)
        propagated_time_tag (datetime.datetime)
        speed (typing.Optional[float])
        density (typing.Optional[float])
        temperature (typing.Optional[float])
        bx (typing.Optional[float])
        by (typing.Optional[float])
        bz (typing.Optional[float])
        bt (typing.Optional[float])
        vx (typing.Optional[float])
        vy (typing.Optional[float])
        vz (typing.Optional[float])
    """
    
    
    spacecraft: SpacecraftEnum=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="spacecraft"))
    time_tag: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_tag", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    propagated_time_tag: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="propagated_time_tag", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    speed: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="speed"))
    density: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="density"))
    temperature: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="temperature"))
    bx: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bx"))
    by: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="by"))
    bz: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bz"))
    bt: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bt"))
    vx: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vx"))
    vy: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vy"))
    vz: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vz"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PropagatedSolarWind':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PropagatedSolarWind']:
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
                return PropagatedSolarWind.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'PropagatedSolarWind':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            spacecraft=SpacecraftEnum.dscovr,
            time_tag=datetime.datetime.now(datetime.timezone.utc),
            propagated_time_tag=datetime.datetime.now(datetime.timezone.utc),
            speed=float(20.57326436625553),
            density=float(27.648281191094746),
            temperature=float(87.58644995300779),
            bx=float(69.16709557087123),
            by=float(39.299056211106844),
            bz=float(85.60474500027206),
            bt=float(75.11027625736658),
            vx=float(21.559255920280407),
            vy=float(1.9180177408143706),
            vz=float(97.1063634752036)
        )