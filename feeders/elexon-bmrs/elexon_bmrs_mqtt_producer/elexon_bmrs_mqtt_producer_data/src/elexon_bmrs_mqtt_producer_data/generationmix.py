""" GenerationMix dataclass. """

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
class GenerationMix:
    """
    Half-hourly generation outturn summary for the GB electricity system from the Elexon BMRS API. Each record represents one settlement period and contains the generation output in megawatts (MW) broken down by fuel type, including domestic generation (biomass, CCGT, coal, nuclear, wind, OCGT, oil, hydro, pumped storage) and interconnector imports (France IFA, France IFA2, Netherlands BritNed, Belgium Nemo, Ireland EWIC, Norway NSL, Denmark Viking Link). Sourced from the BMRS /generation/outturn/summary endpoint.
    
    Attributes:
        settlement_period (int)
        start_time (datetime.datetime)
        biomass_mw (typing.Optional[float])
        ccgt_mw (typing.Optional[float])
        coal_mw (typing.Optional[float])
        nuclear_mw (typing.Optional[float])
        wind_mw (typing.Optional[float])
        ocgt_mw (typing.Optional[float])
        oil_mw (typing.Optional[float])
        npshyd_mw (typing.Optional[float])
        ps_mw (typing.Optional[float])
        intfr_mw (typing.Optional[float])
        intned_mw (typing.Optional[float])
        intnem_mw (typing.Optional[float])
        intelec_mw (typing.Optional[float])
        intifa2_mw (typing.Optional[float])
        intnsl_mw (typing.Optional[float])
        intvkl_mw (typing.Optional[float])
        other_mw (typing.Optional[float])
    """
    
    
    settlement_period: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="settlement_period"))
    start_time: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="start_time", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    biomass_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="biomass_mw"))
    ccgt_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ccgt_mw"))
    coal_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coal_mw"))
    nuclear_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nuclear_mw"))
    wind_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wind_mw"))
    ocgt_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ocgt_mw"))
    oil_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="oil_mw"))
    npshyd_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="npshyd_mw"))
    ps_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ps_mw"))
    intfr_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intfr_mw"))
    intned_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intned_mw"))
    intnem_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intnem_mw"))
    intelec_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intelec_mw"))
    intifa2_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intifa2_mw"))
    intnsl_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intnsl_mw"))
    intvkl_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="intvkl_mw"))
    other_mw: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="other_mw"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'GenerationMix':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['GenerationMix']:
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
                return GenerationMix.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'GenerationMix':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            settlement_period=int(29),
            start_time=datetime.datetime.now(datetime.timezone.utc),
            biomass_mw=float(39.323114349883014),
            ccgt_mw=float(73.82105934731635),
            coal_mw=float(8.379424031332562),
            nuclear_mw=float(71.64444842387762),
            wind_mw=float(20.869682566139957),
            ocgt_mw=float(80.82278293016873),
            oil_mw=float(90.45844921308355),
            npshyd_mw=float(43.87894105291284),
            ps_mw=float(69.4800742186866),
            intfr_mw=float(25.853750249316132),
            intned_mw=float(83.30232005558003),
            intnem_mw=float(73.47032538173353),
            intelec_mw=float(16.98088883755312),
            intifa2_mw=float(43.397670879235896),
            intnsl_mw=float(44.88655016782918),
            intvkl_mw=float(3.410861814598243),
            other_mw=float(42.84483942524877)
        )