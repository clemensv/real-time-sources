""" MonitoringLocationMetadata dataclass. """

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
from usgs_waterdata_amqp_producer_data.usgs.waterdata.point import Point
import datetime




@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class MonitoringLocationMetadata:
    """
    Complete selected USGS monitoring-locations resource properties and geometry.
    
    Attributes:
        id (typing.Optional[str])
        agency_code (typing.Optional[str])
        agency_name (typing.Optional[str])
        monitoring_location_number (typing.Optional[str])
        monitoring_location_name (typing.Optional[str])
        district_code (typing.Optional[str])
        country_code (typing.Optional[str])
        country_name (typing.Optional[str])
        state_code (typing.Optional[str])
        state_name (typing.Optional[str])
        county_code (typing.Optional[str])
        county_name (typing.Optional[str])
        minor_civil_division_code (typing.Optional[str])
        site_type_code (typing.Optional[str])
        site_type (typing.Optional[str])
        hydrologic_unit_code (typing.Optional[str])
        basin_code (typing.Optional[str])
        altitude (typing.Optional[float])
        altitude_accuracy (typing.Optional[float])
        altitude_method_code (typing.Optional[str])
        altitude_method_name (typing.Optional[str])
        vertical_datum (typing.Optional[str])
        vertical_datum_name (typing.Optional[str])
        horizontal_positional_accuracy_code (typing.Optional[str])
        horizontal_positional_accuracy (typing.Optional[str])
        horizontal_position_method_code (typing.Optional[str])
        horizontal_position_method_name (typing.Optional[str])
        original_horizontal_datum (typing.Optional[str])
        original_horizontal_datum_name (typing.Optional[str])
        drainage_area (typing.Optional[float])
        contributing_drainage_area (typing.Optional[float])
        time_zone_abbreviation (typing.Optional[str])
        uses_daylight_savings (typing.Optional[str])
        construction_date (typing.Optional[str])
        aquifer_code (typing.Optional[str])
        national_aquifer_code (typing.Optional[str])
        aquifer_type_code (typing.Optional[str])
        well_constructed_depth (typing.Optional[float])
        hole_constructed_depth (typing.Optional[float])
        depth_source_code (typing.Optional[str])
        revision_note (typing.Optional[str])
        revision_created (typing.Optional[datetime.datetime])
        revision_modified (typing.Optional[datetime.datetime])
        geometry (typing.Optional[Point])
    """
    
    
    
    id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="id"))
    agency_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency_code"))
    agency_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency_name"))
    monitoring_location_number: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="monitoring_location_number"))
    monitoring_location_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="monitoring_location_name"))
    district_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="district_code"))
    country_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_code"))
    country_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_name"))
    state_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_code"))
    state_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_name"))
    county_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="county_code"))
    county_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="county_name"))
    minor_civil_division_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="minor_civil_division_code"))
    site_type_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_type_code"))
    site_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_type"))
    hydrologic_unit_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hydrologic_unit_code"))
    basin_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin_code"))
    altitude: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude"))
    altitude_accuracy: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude_accuracy"))
    altitude_method_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude_method_code"))
    altitude_method_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude_method_name"))
    vertical_datum: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vertical_datum"))
    vertical_datum_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vertical_datum_name"))
    horizontal_positional_accuracy_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="horizontal_positional_accuracy_code"))
    horizontal_positional_accuracy: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="horizontal_positional_accuracy"))
    horizontal_position_method_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="horizontal_position_method_code"))
    horizontal_position_method_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="horizontal_position_method_name"))
    original_horizontal_datum: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="original_horizontal_datum"))
    original_horizontal_datum_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="original_horizontal_datum_name"))
    drainage_area: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drainage_area"))
    contributing_drainage_area: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contributing_drainage_area"))
    time_zone_abbreviation: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="time_zone_abbreviation"))
    uses_daylight_savings: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uses_daylight_savings"))
    construction_date: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="construction_date"))
    aquifer_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aquifer_code"))
    national_aquifer_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="national_aquifer_code"))
    aquifer_type_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aquifer_type_code"))
    well_constructed_depth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="well_constructed_depth"))
    hole_constructed_depth: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hole_constructed_depth"))
    depth_source_code: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="depth_source_code"))
    revision_note: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="revision_note"))
    revision_created: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="revision_created", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    revision_modified: typing.Optional[datetime.datetime]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="revision_modified", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    geometry: typing.Optional[Point]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="geometry"))


    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'MonitoringLocationMetadata':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['MonitoringLocationMetadata']:
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
                return MonitoringLocationMetadata.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'MonitoringLocationMetadata':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            id='pczzypqxdxztebmfbfra',
            agency_code='czrhfnsnsfpkdcsoxgfj',
            agency_name='nlnanjfbwespqbwqhery',
            monitoring_location_number='bmlajdqgyaidbarcymis',
            monitoring_location_name='spntnldgivwivsfwhgnv',
            district_code='jrdkwrnlxdhsbawmalps',
            country_code='mtuwaotgnfcnzfkxeiep',
            country_name='qyrhgqdaebvuotiuqict',
            state_code='kgwpuriwfcscyksoduzq',
            state_name='wljwgmznahgfabgnhdio',
            county_code='omriiphxueypctjlddbr',
            county_name='jutukbcfzwxcrogrtlhq',
            minor_civil_division_code='fmnrzdzdqyehywvjmljt',
            site_type_code='pcnlraybzthjcwrtjlka',
            site_type='rxryxmpoaiecxyvneyms',
            hydrologic_unit_code='xdlbzadtifwmqlovmmls',
            basin_code='fjlqmaopwdgjybpymxqv',
            altitude=float(16.382390532164347),
            altitude_accuracy=float(95.56736827954099),
            altitude_method_code='bezmkydqrnjnwwmbpikd',
            altitude_method_name='zcomwsltafwbqtygjrcv',
            vertical_datum='sifbipmhticridfalgfx',
            vertical_datum_name='ndbsyoxxbomyjjkotulm',
            horizontal_positional_accuracy_code='ztlycfjitcqlzhjfulgw',
            horizontal_positional_accuracy='kyxzdwgfheonzgnqsasd',
            horizontal_position_method_code='zeafalwqtfcfhvuryuyz',
            horizontal_position_method_name='bubijnpqhzmqagtuxims',
            original_horizontal_datum='tnzmsrktxfldytyemnzs',
            original_horizontal_datum_name='axzkeadycvrenhtqelmc',
            drainage_area=float(30.23788897685882),
            contributing_drainage_area=float(2.3514408695612277),
            time_zone_abbreviation='pjxtnlvpgwgdpenyzcxu',
            uses_daylight_savings='ulpdkoidtsrmcwuczmdo',
            construction_date='xpewrkhdsmrvsftcbdgi',
            aquifer_code='hfymbnsxmpujnbklgocr',
            national_aquifer_code='awijwtelwzeytjsknikt',
            aquifer_type_code='xxeruotchtkamolylnlt',
            well_constructed_depth=float(48.47380229431765),
            hole_constructed_depth=float(2.3808367563236232),
            depth_source_code='aotfmaxwhxkketrgdupx',
            revision_note='tzictiuzhnejkmktlcby',
            revision_created=datetime.datetime.now(datetime.timezone.utc),
            revision_modified=datetime.datetime.now(datetime.timezone.utc),
            geometry=None
        )