""" WildfireIncident dataclass. """

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
class WildfireIncident:
    """
    Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.
    
    Attributes:
        irwin_id (str)
        incident_name (str)
        unique_fire_identifier (typing.Optional[str])
        incident_type_category (typing.Optional[str])
        incident_type_kind (typing.Optional[str])
        fire_discovery_datetime (typing.Optional[str])
        daily_acres (typing.Optional[float])
        calculated_acres (typing.Optional[float])
        discovery_acres (typing.Optional[float])
        percent_contained (typing.Optional[float])
        poo_state (typing.Optional[str])
        poo_county (typing.Optional[str])
        latitude (typing.Optional[float])
        longitude (typing.Optional[float])
        fire_cause (typing.Optional[str])
        fire_cause_general (typing.Optional[str])
        gacc (typing.Optional[str])
        total_incident_personnel (typing.Optional[int])
        incident_management_organization (typing.Optional[str])
        fire_mgmt_complexity (typing.Optional[str])
        residences_destroyed (typing.Optional[int])
        other_structures_destroyed (typing.Optional[int])
        injuries (typing.Optional[int])
        fatalities (typing.Optional[int])
        containment_datetime (typing.Optional[str])
        control_datetime (typing.Optional[str])
        fire_out_datetime (typing.Optional[str])
        final_acres (typing.Optional[float])
        modified_on_datetime (str)
        state (str)
        status (str)
    """
    
    
    irwin_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="irwin_id"))
    incident_name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="incident_name"))
    unique_fire_identifier: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="unique_fire_identifier"))
    incident_type_category: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="incident_type_category"))
    incident_type_kind: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="incident_type_kind"))
    fire_discovery_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fire_discovery_datetime"))
    daily_acres: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="daily_acres"))
    calculated_acres: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="calculated_acres"))
    discovery_acres: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="discovery_acres"))
    percent_contained: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="percent_contained"))
    poo_state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="poo_state"))
    poo_county: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="poo_county"))
    latitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    fire_cause: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fire_cause"))
    fire_cause_general: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fire_cause_general"))
    gacc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gacc"))
    total_incident_personnel: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="total_incident_personnel"))
    incident_management_organization: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="incident_management_organization"))
    fire_mgmt_complexity: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fire_mgmt_complexity"))
    residences_destroyed: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="residences_destroyed"))
    other_structures_destroyed: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="other_structures_destroyed"))
    injuries: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="injuries"))
    fatalities: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fatalities"))
    containment_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="containment_datetime"))
    control_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="control_datetime"))
    fire_out_datetime: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fire_out_datetime"))
    final_acres: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="final_acres"))
    modified_on_datetime: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="modified_on_datetime"))
    state: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    status: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="status"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WildfireIncident':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WildfireIncident']:
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
                return WildfireIncident.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'WildfireIncident':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            irwin_id='ehkcccgrnngwswgqsbrl',
            incident_name='yjfqyrmxnpzyssfwsbvw',
            unique_fire_identifier='puatcwgyflvhikpyqgtm',
            incident_type_category='dnttkgmvxlrdndwphmgh',
            incident_type_kind='tfpltlygekkkkfxagrzi',
            fire_discovery_datetime='mblklptkaomdbyumerlk',
            daily_acres=float(13.871467888060973),
            calculated_acres=float(31.254491029790778),
            discovery_acres=float(8.864156965068293),
            percent_contained=float(75.4780627869807),
            poo_state='yzcfhrxvbmxmrjrbdvnu',
            poo_county='eldtgcgkiccdmiwalcwq',
            latitude=float(45.51696501032204),
            longitude=float(98.00269549131852),
            fire_cause='iivzrbniuzfidghakvvc',
            fire_cause_general='ncdfplkzkkfevvcczcvz',
            gacc='srmhqanqnlxfarkwaien',
            total_incident_personnel=int(62),
            incident_management_organization='feqcsdsjrnsrymgntdxo',
            fire_mgmt_complexity='ueozcybdajhzvdzmzzwv',
            residences_destroyed=int(71),
            other_structures_destroyed=int(91),
            injuries=int(28),
            fatalities=int(79),
            containment_datetime='lbqhaomtduzmtfyqfykp',
            control_datetime='saqyzplrxkdaezjizjsm',
            fire_out_datetime='owoqqrkagjzjhsufylkr',
            final_acres=float(6.016815159293454),
            modified_on_datetime='cnaxjorjvbtkrmzbzlch',
            state='wzlohscgczlieardmueq',
            status='btrzcisopmtmwearuiyo'
        )