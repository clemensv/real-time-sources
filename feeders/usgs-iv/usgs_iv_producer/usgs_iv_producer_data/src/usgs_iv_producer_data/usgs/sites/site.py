""" Site dataclass. """

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
class Site:
    """
    USGS site metadata.
    
    Attributes:
        agency_cd (str)
        site_no (str)
        station_nm (str)
        site_tp_cd (str)
        lat_va (str)
        long_va (str)
        dec_lat_va (typing.Optional[float])
        dec_long_va (typing.Optional[float])
        coord_meth_cd (str)
        coord_acy_cd (str)
        coord_datum_cd (str)
        dec_coord_datum_cd (str)
        district_cd (str)
        state_cd (str)
        county_cd (str)
        country_cd (str)
        land_net_ds (str)
        map_nm (str)
        map_scale_fc (typing.Optional[float])
        alt_va (typing.Optional[float])
        alt_meth_cd (str)
        alt_acy_va (typing.Optional[float])
        alt_datum_cd (str)
        huc_cd (str)
        basin_cd (str)
        topo_cd (str)
        instruments_cd (str)
        construction_dt (typing.Optional[str])
        inventory_dt (typing.Optional[str])
        drain_area_va (typing.Optional[float])
        contrib_drain_area_va (typing.Optional[float])
        tz_cd (str)
        local_time_fg (bool)
        reliability_cd (str)
        gw_file_cd (str)
        nat_aqfr_cd (str)
        aqfr_cd (str)
        aqfr_type_cd (str)
        well_depth_va (typing.Optional[float])
        hole_depth_va (typing.Optional[float])
        depth_src_cd (str)
        project_no (str)
    """
    
    
    agency_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency_cd"))
    site_no: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_no"))
    station_nm: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_nm"))
    site_tp_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_tp_cd"))
    lat_va: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="lat_va"))
    long_va: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="long_va"))
    dec_lat_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dec_lat_va"))
    dec_long_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dec_long_va"))
    coord_meth_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coord_meth_cd"))
    coord_acy_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coord_acy_cd"))
    coord_datum_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coord_datum_cd"))
    dec_coord_datum_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dec_coord_datum_cd"))
    district_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="district_cd"))
    state_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_cd"))
    county_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="county_cd"))
    country_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country_cd"))
    land_net_ds: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="land_net_ds"))
    map_nm: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="map_nm"))
    map_scale_fc: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="map_scale_fc"))
    alt_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_va"))
    alt_meth_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_meth_cd"))
    alt_acy_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_acy_va"))
    alt_datum_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_datum_cd"))
    huc_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="huc_cd"))
    basin_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="basin_cd"))
    topo_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="topo_cd"))
    instruments_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="instruments_cd"))
    construction_dt: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="construction_dt"))
    inventory_dt: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="inventory_dt"))
    drain_area_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="drain_area_va"))
    contrib_drain_area_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="contrib_drain_area_va"))
    tz_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tz_cd"))
    local_time_fg: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="local_time_fg"))
    reliability_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="reliability_cd"))
    gw_file_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="gw_file_cd"))
    nat_aqfr_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="nat_aqfr_cd"))
    aqfr_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aqfr_cd"))
    aqfr_type_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="aqfr_type_cd"))
    well_depth_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="well_depth_va"))
    hole_depth_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hole_depth_va"))
    depth_src_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="depth_src_cd"))
    project_no: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="project_no"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Site':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Site']:
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
                return Site.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'Site':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            agency_cd='qrntjuwuokehlruvjpob',
            site_no='pbthxvijttppvaelpchx',
            station_nm='fhaeykcuuldtihwdgyqr',
            site_tp_cd='tmcetfyiuolswczjkado',
            lat_va='nhrhntuphtxucgarucyg',
            long_va='fkpgfavixqqkyfhhndys',
            dec_lat_va=float(46.33152986945679),
            dec_long_va=float(0.13127724922855633),
            coord_meth_cd='zvxaqlktlrpcgkificuw',
            coord_acy_cd='njpkbffiqcsrprazhexz',
            coord_datum_cd='uywjcklezayqnbhgzyqi',
            dec_coord_datum_cd='stkfuqawfgauhapqhynl',
            district_cd='ehiakwwhbijirwzttpki',
            state_cd='tjgxekowujrmluhmzvvp',
            county_cd='xhflxxzuvmaqvfvgvmaf',
            country_cd='hzxpanumjaovfxnavljb',
            land_net_ds='fydukbggneagtetwxtul',
            map_nm='digicszdzxcdwxwxgxqs',
            map_scale_fc=float(66.95002770689608),
            alt_va=float(65.92766075886071),
            alt_meth_cd='mqykchiuplcvihxfoump',
            alt_acy_va=float(32.48505890829074),
            alt_datum_cd='ucecuuptkwateejptixc',
            huc_cd='kwgxgojgsgguzfzjspdp',
            basin_cd='rqrljjlljxxycritjxvj',
            topo_cd='nxyflwgfqclkflmaxgsv',
            instruments_cd='ajotapedajmdjaevspsx',
            construction_dt='dkmsmodkkbkdnwzccsyj',
            inventory_dt='odbswxzcwgknloqcnjdq',
            drain_area_va=float(65.58511906127572),
            contrib_drain_area_va=float(58.63514250527045),
            tz_cd='xsfqhoxwvmucikbuwtri',
            local_time_fg=True,
            reliability_cd='yqtngeovekuhdwxdhzfi',
            gw_file_cd='xwudbfqlwjopxirrsoid',
            nat_aqfr_cd='slkgahxxupnxixfxgzty',
            aqfr_cd='xeynpjbnwdzvskyqevkt',
            aqfr_type_cd='mhecztzajgmgkbyusobl',
            well_depth_va=float(69.7448376406673),
            hole_depth_va=float(11.262455349539756),
            depth_src_cd='uhkneipsrwmqopbnsbwl',
            project_no='lrshhwpgvptkszjamrwo'
        )