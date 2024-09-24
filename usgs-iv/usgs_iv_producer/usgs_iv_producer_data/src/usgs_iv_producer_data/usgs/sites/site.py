""" Site dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Site:
    """
    USGS site metadata.
    Attributes:
        agency_cd (str): Agency code.
        site_no (str): USGS site number.
        station_nm (str): Station name.
        site_tp_cd (str): Site type code.
        lat_va (str): DMS latitude.
        long_va (str): DMS longitude.
        dec_lat_va (typing.Optional[float]): Decimal latitude.
        dec_long_va (typing.Optional[float]): Decimal longitude.
        coord_meth_cd (str): Latitude-longitude method code.
        coord_acy_cd (str): Coordinate accuracy code.
        coord_datum_cd (str): Latitude-longitude datum code.
        dec_coord_datum_cd (str): Decimal latitude-longitude datum code.
        district_cd (str): District code.
        state_cd (str): State code.
        county_cd (str): County code.
        country_cd (str): Country code.
        land_net_ds (str): Land net location description.
        map_nm (str): Location map name.
        map_scale_fc (typing.Optional[float]): Location map scale factor.
        alt_va (typing.Optional[float]): Altitude.
        alt_meth_cd (str): Method altitude determined code.
        alt_acy_va (typing.Optional[float]): Altitude accuracy.
        alt_datum_cd (str): Altitude datum code.
        huc_cd (str): Hydrologic unit code.
        basin_cd (str): Drainage basin code.
        topo_cd (str): Topographic setting code.
        instruments_cd (str): Flags for instruments at site.
        construction_dt (typing.Optional[str]): Date of first construction.
        inventory_dt (typing.Optional[str]): Date site established or inventoried.
        drain_area_va (typing.Optional[float]): Drainage area.
        contrib_drain_area_va (typing.Optional[float]): Contributing drainage area.
        tz_cd (str): Time Zone abbreviation.
        local_time_fg (bool): Site honors Daylight Savings Time flag.
        reliability_cd (str): Data reliability code.
        gw_file_cd (str): Data-other GW files code.
        nat_aqfr_cd (str): National aquifer code.
        aqfr_cd (str): Local aquifer code.
        aqfr_type_cd (str): Local aquifer type code.
        well_depth_va (typing.Optional[float]): Well depth.
        hole_depth_va (typing.Optional[float]): Hole depth.
        depth_src_cd (str): Source of depth data.
        project_no (str): Project number."""
    
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
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.agency_cd=str(self.agency_cd)
        self.site_no=str(self.site_no)
        self.station_nm=str(self.station_nm)
        self.site_tp_cd=str(self.site_tp_cd)
        self.lat_va=str(self.lat_va)
        self.long_va=str(self.long_va)
        self.dec_lat_va=float(self.dec_lat_va) if self.dec_lat_va else None
        self.dec_long_va=float(self.dec_long_va) if self.dec_long_va else None
        self.coord_meth_cd=str(self.coord_meth_cd)
        self.coord_acy_cd=str(self.coord_acy_cd)
        self.coord_datum_cd=str(self.coord_datum_cd)
        self.dec_coord_datum_cd=str(self.dec_coord_datum_cd)
        self.district_cd=str(self.district_cd)
        self.state_cd=str(self.state_cd)
        self.county_cd=str(self.county_cd)
        self.country_cd=str(self.country_cd)
        self.land_net_ds=str(self.land_net_ds)
        self.map_nm=str(self.map_nm)
        self.map_scale_fc=float(self.map_scale_fc) if self.map_scale_fc else None
        self.alt_va=float(self.alt_va) if self.alt_va else None
        self.alt_meth_cd=str(self.alt_meth_cd)
        self.alt_acy_va=float(self.alt_acy_va) if self.alt_acy_va else None
        self.alt_datum_cd=str(self.alt_datum_cd)
        self.huc_cd=str(self.huc_cd)
        self.basin_cd=str(self.basin_cd)
        self.topo_cd=str(self.topo_cd)
        self.instruments_cd=str(self.instruments_cd)
        self.construction_dt=str(self.construction_dt) if self.construction_dt else None
        self.inventory_dt=str(self.inventory_dt) if self.inventory_dt else None
        self.drain_area_va=float(self.drain_area_va) if self.drain_area_va else None
        self.contrib_drain_area_va=float(self.contrib_drain_area_va) if self.contrib_drain_area_va else None
        self.tz_cd=str(self.tz_cd)
        self.local_time_fg=bool(self.local_time_fg)
        self.reliability_cd=str(self.reliability_cd)
        self.gw_file_cd=str(self.gw_file_cd)
        self.nat_aqfr_cd=str(self.nat_aqfr_cd)
        self.aqfr_cd=str(self.aqfr_cd)
        self.aqfr_type_cd=str(self.aqfr_type_cd)
        self.well_depth_va=float(self.well_depth_va) if self.well_depth_va else None
        self.hole_depth_va=float(self.hole_depth_va) if self.hole_depth_va else None
        self.depth_src_cd=str(self.depth_src_cd)
        self.project_no=str(self.project_no)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Site':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dictionary.
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
            if isinstance(v,enum.Enum):
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
        if content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member

        if result is not None and content_type.endswith('+gzip'):
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
        if content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Site.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')