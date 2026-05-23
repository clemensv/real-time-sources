""" Observation dataclass. """

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
class Observation:
    """
    Air quality observation from one ISSeP Wallonia sensor at a specific moment in time. Includes raw electrochemical gas readings, calibrated ppb and µg/m³ values, particulate matter concentrations, environmental parameters, reference station comparisons, and quality status flags. Negative raw values (e.g. no2=-4) are valid sensor readings and must not be filtered.
    
    Attributes:
        configuration_id (str)
        province (str)
        moment (str)
        co (typing.Optional[int])
        no (typing.Optional[int])
        no2 (typing.Optional[int])
        o3no2 (typing.Optional[int])
        ppbno (typing.Optional[float])
        ppbno_statut (typing.Optional[int])
        ppbno2 (typing.Optional[float])
        ppbno2_statut (typing.Optional[int])
        ppbo3 (typing.Optional[float])
        ppbo3_statut (typing.Optional[int])
        ugpcmno (typing.Optional[float])
        ugpcmno_statut (typing.Optional[int])
        ugpcmno2 (typing.Optional[float])
        ugpcmno2_statut (typing.Optional[int])
        ugpcmo3 (typing.Optional[float])
        ugpcmo3_statut (typing.Optional[int])
        bme_t (typing.Optional[float])
        bme_t_statut (typing.Optional[int])
        bme_pres (typing.Optional[int])
        bme_pres_statut (typing.Optional[int])
        bme_rh (typing.Optional[float])
        bme_rh_statut (typing.Optional[int])
        pm1 (typing.Optional[float])
        pm1_statut (typing.Optional[int])
        pm25 (typing.Optional[float])
        pm25_statut (typing.Optional[int])
        pm4 (typing.Optional[float])
        pm4_statut (typing.Optional[int])
        pm10 (typing.Optional[float])
        pm10_statut (typing.Optional[int])
        vbat (typing.Optional[float])
        vbat_statut (typing.Optional[int])
        mwh_bat (typing.Optional[float])
        mwh_pv (typing.Optional[float])
        co_rf (typing.Optional[float])
        no_rf (typing.Optional[float])
        no2_rf (typing.Optional[float])
        o3no2_rf (typing.Optional[float])
        o3_rf (typing.Optional[float])
        pm10_rf (typing.Optional[float])
    """
    
    
    configuration_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="configuration_id"))
    province: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="province"))
    moment: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="moment"))
    co: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="co"))
    no: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no"))
    no2: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2"))
    o3no2: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3no2"))
    ppbno: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ppbno"))
    ppbno_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ppbno_statut"))
    ppbno2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ppbno2"))
    ppbno2_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ppbno2_statut"))
    ppbo3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ppbo3"))
    ppbo3_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ppbo3_statut"))
    ugpcmno: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugpcmno"))
    ugpcmno_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugpcmno_statut"))
    ugpcmno2: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugpcmno2"))
    ugpcmno2_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugpcmno2_statut"))
    ugpcmo3: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugpcmo3"))
    ugpcmo3_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ugpcmo3_statut"))
    bme_t: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bme_t"))
    bme_t_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bme_t_statut"))
    bme_pres: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bme_pres"))
    bme_pres_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bme_pres_statut"))
    bme_rh: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bme_rh"))
    bme_rh_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bme_rh_statut"))
    pm1: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm1"))
    pm1_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm1_statut"))
    pm25: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm25"))
    pm25_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm25_statut"))
    pm4: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm4"))
    pm4_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm4_statut"))
    pm10: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10"))
    pm10_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_statut"))
    vbat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vbat"))
    vbat_statut: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vbat_statut"))
    mwh_bat: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mwh_bat"))
    mwh_pv: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="mwh_pv"))
    co_rf: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="co_rf"))
    no_rf: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no_rf"))
    no2_rf: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="no2_rf"))
    o3no2_rf: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3no2_rf"))
    o3_rf: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="o3_rf"))
    pm10_rf: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="pm10_rf"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Observation':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Observation']:
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
                return Observation.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Observation':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            configuration_id='gfulknwbzpfsgwfdytqa',
            province='dmhbsjhpbitfuvekrvpl',
            moment='vldnqtcsfjigoedxjlsm',
            co=int(83),
            no=int(31),
            no2=int(88),
            o3no2=int(60),
            ppbno=float(38.88104499599242),
            ppbno_statut=int(93),
            ppbno2=float(61.155561549765125),
            ppbno2_statut=int(22),
            ppbo3=float(47.29630332223245),
            ppbo3_statut=int(23),
            ugpcmno=float(76.39859427920483),
            ugpcmno_statut=int(63),
            ugpcmno2=float(55.45350484640309),
            ugpcmno2_statut=int(41),
            ugpcmo3=float(74.16400076119484),
            ugpcmo3_statut=int(37),
            bme_t=float(85.53752025452533),
            bme_t_statut=int(7),
            bme_pres=int(28),
            bme_pres_statut=int(61),
            bme_rh=float(77.03445825672055),
            bme_rh_statut=int(57),
            pm1=float(16.129236434611492),
            pm1_statut=int(8),
            pm25=float(43.62485923221633),
            pm25_statut=int(94),
            pm4=float(69.19844505740777),
            pm4_statut=int(84),
            pm10=float(82.15620356870048),
            pm10_statut=int(12),
            vbat=float(66.23211266578703),
            vbat_statut=int(91),
            mwh_bat=float(40.04066080529497),
            mwh_pv=float(95.24381597031412),
            co_rf=float(95.68347655258395),
            no_rf=float(62.38572091990584),
            no2_rf=float(76.05566735261662),
            o3no2_rf=float(69.69889161695323),
            o3_rf=float(78.62969919594475),
            pm10_rf=float(6.339080591731705)
        )