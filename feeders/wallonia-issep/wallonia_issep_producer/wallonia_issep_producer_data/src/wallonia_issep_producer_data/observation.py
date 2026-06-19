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
    A current environmental measurement from Wallonia's Institut Scientifique de Service Public (ISSeP). It carries pollutant concentration measurements when the upstream feed reports a new or refreshed value.
    
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
            configuration_id='yddqvdtitosopvqsmemf',
            province='jwxulooymsqghoymyroo',
            moment='dchibusvrcgtqanlphoa',
            co=int(40),
            no=int(34),
            no2=int(12),
            o3no2=int(16),
            ppbno=float(44.734614817138116),
            ppbno_statut=int(44),
            ppbno2=float(7.232074913561581),
            ppbno2_statut=int(93),
            ppbo3=float(74.51127606616244),
            ppbo3_statut=int(21),
            ugpcmno=float(84.44686506945736),
            ugpcmno_statut=int(81),
            ugpcmno2=float(72.99132450163421),
            ugpcmno2_statut=int(42),
            ugpcmo3=float(85.32440589530457),
            ugpcmo3_statut=int(49),
            bme_t=float(0.36475030340782366),
            bme_t_statut=int(28),
            bme_pres=int(43),
            bme_pres_statut=int(41),
            bme_rh=float(30.380847360451966),
            bme_rh_statut=int(72),
            pm1=float(47.97138726130357),
            pm1_statut=int(35),
            pm25=float(17.80467110854662),
            pm25_statut=int(68),
            pm4=float(47.735387559005204),
            pm4_statut=int(18),
            pm10=float(59.854711330113794),
            pm10_statut=int(71),
            vbat=float(94.27714869301175),
            vbat_statut=int(78),
            mwh_bat=float(2.431951899230411),
            mwh_pv=float(62.67861435867768),
            co_rf=float(6.5313160107893005),
            no_rf=float(7.214222679055993),
            no2_rf=float(88.51154031804238),
            o3no2_rf=float(74.84603810215708),
            o3_rf=float(84.35992724972756),
            pm10_rf=float(26.56897316788802)
        )