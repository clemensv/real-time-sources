""" PowerSystemSnapshot dataclass. """

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
class PowerSystemSnapshot:
    """
    Minute-by-minute snapshot of the Danish power system from Energi Data Service (Energinet). Published by the PowerSystemRightNow dataset at approximately 1-minute intervals.
    
    Attributes:
        minutes1_utc (str)
        minutes1_dk (str)
        price_area (str)
        co2_emission (typing.Optional[float])
        production_ge_100mw (typing.Optional[float])
        production_lt_100mw (typing.Optional[float])
        solar_power (typing.Optional[float])
        offshore_wind_power (typing.Optional[float])
        onshore_wind_power (typing.Optional[float])
        exchange_sum (typing.Optional[float])
        exchange_dk1_de (typing.Optional[float])
        exchange_dk1_nl (typing.Optional[float])
        exchange_dk1_gb (typing.Optional[float])
        exchange_dk1_no (typing.Optional[float])
        exchange_dk1_se (typing.Optional[float])
        exchange_dk1_dk2 (typing.Optional[float])
        exchange_dk2_de (typing.Optional[float])
        exchange_dk2_se (typing.Optional[float])
        exchange_bornholm_se (typing.Optional[float])
        afrr_activated_dk1 (typing.Optional[float])
        afrr_activated_dk2 (typing.Optional[float])
        mfrr_activated_dk1 (typing.Optional[float])
        mfrr_activated_dk2 (typing.Optional[float])
        imbalance_dk1 (typing.Optional[float])
        imbalance_dk2 (typing.Optional[float])
    """
    
    
    minutes1_utc: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minutes1_utc"))
    minutes1_dk: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minutes1_dk"))
    price_area: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price_area"))
    co2_emission: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="co2_emission"))
    production_ge_100mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="production_ge_100mw"))
    production_lt_100mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="production_lt_100mw"))
    solar_power: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="solar_power"))
    offshore_wind_power: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="offshore_wind_power"))
    onshore_wind_power: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="onshore_wind_power"))
    exchange_sum: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_sum"))
    exchange_dk1_de: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_de"))
    exchange_dk1_nl: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_nl"))
    exchange_dk1_gb: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_gb"))
    exchange_dk1_no: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_no"))
    exchange_dk1_se: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_se"))
    exchange_dk1_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk1_dk2"))
    exchange_dk2_de: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk2_de"))
    exchange_dk2_se: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_dk2_se"))
    exchange_bornholm_se: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exchange_bornholm_se"))
    afrr_activated_dk1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="afrr_activated_dk1"))
    afrr_activated_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="afrr_activated_dk2"))
    mfrr_activated_dk1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mfrr_activated_dk1"))
    mfrr_activated_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mfrr_activated_dk2"))
    imbalance_dk1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imbalance_dk1"))
    imbalance_dk2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="imbalance_dk2"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'PowerSystemSnapshot':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['PowerSystemSnapshot']:
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
                return PowerSystemSnapshot.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'PowerSystemSnapshot':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            minutes1_utc='bpxiuowbrlrcuxjocfzm',
            minutes1_dk='xnpmttendvylxokvzzgy',
            price_area='rbwthmrsmjgdcqwjjisn',
            co2_emission=float(62.96444384519493),
            production_ge_100mw=float(27.482452791616907),
            production_lt_100mw=float(2.266522255847636),
            solar_power=float(8.40200205592735),
            offshore_wind_power=float(78.33569713820914),
            onshore_wind_power=float(19.72640995072904),
            exchange_sum=float(10.649610701120448),
            exchange_dk1_de=float(57.74585996879813),
            exchange_dk1_nl=float(64.86126603815438),
            exchange_dk1_gb=float(43.74928833043077),
            exchange_dk1_no=float(41.094335512383886),
            exchange_dk1_se=float(59.31998283039768),
            exchange_dk1_dk2=float(6.976521734783036),
            exchange_dk2_de=float(64.7357436212105),
            exchange_dk2_se=float(3.7757852788593893),
            exchange_bornholm_se=float(39.86076993290081),
            afrr_activated_dk1=float(34.847326861887865),
            afrr_activated_dk2=float(23.81896403943722),
            mfrr_activated_dk1=float(35.06633366373014),
            mfrr_activated_dk2=float(85.9858486451197),
            imbalance_dk1=float(58.570552214357186),
            imbalance_dk2=float(43.40503041488244)
        )