""" Site dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import json
import avro.schema
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.parse(
        "{\"type\": \"record\", \"name\": \"Site\", \"namespace\": \"USGS.Sites\", \"doc\": \"USGS site metadata.\", \"fields\": [{\"name\": \"agency_cd\", \"doc\": \"Agency code.\", \"type\": \"string\"}, {\"name\": \"site_no\", \"doc\": \"USGS site number.\", \"type\": \"string\"}, {\"name\": \"station_nm\", \"doc\": \"Station name.\", \"type\": \"string\"}, {\"name\": \"site_tp_cd\", \"doc\": \"Site type code.\", \"type\": \"string\"}, {\"name\": \"lat_va\", \"doc\": \"DMS latitude.\", \"type\": \"string\"}, {\"name\": \"long_va\", \"doc\": \"DMS longitude.\", \"type\": \"string\"}, {\"name\": \"dec_lat_va\", \"doc\": \"Decimal latitude.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"dec_long_va\", \"doc\": \"Decimal longitude.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"coord_meth_cd\", \"doc\": \"Latitude-longitude method code.\", \"type\": \"string\"}, {\"name\": \"coord_acy_cd\", \"doc\": \"Coordinate accuracy code.\", \"type\": \"string\"}, {\"name\": \"coord_datum_cd\", \"doc\": \"Latitude-longitude datum code.\", \"type\": \"string\"}, {\"name\": \"dec_coord_datum_cd\", \"doc\": \"Decimal latitude-longitude datum code.\", \"type\": \"string\"}, {\"name\": \"district_cd\", \"doc\": \"District code.\", \"type\": \"string\"}, {\"name\": \"state_cd\", \"doc\": \"State code.\", \"type\": \"string\"}, {\"name\": \"county_cd\", \"doc\": \"County code.\", \"type\": \"string\"}, {\"name\": \"country_cd\", \"doc\": \"Country code.\", \"type\": \"string\"}, {\"name\": \"land_net_ds\", \"doc\": \"Land net location description.\", \"type\": \"string\"}, {\"name\": \"map_nm\", \"doc\": \"Location map name.\", \"type\": \"string\"}, {\"name\": \"map_scale_fc\", \"doc\": \"Location map scale factor.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"alt_va\", \"doc\": \"Altitude.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"alt_meth_cd\", \"doc\": \"Method altitude determined code.\", \"type\": \"string\"}, {\"name\": \"alt_acy_va\", \"doc\": \"Altitude accuracy.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"alt_datum_cd\", \"doc\": \"Altitude datum code.\", \"type\": \"string\"}, {\"name\": \"huc_cd\", \"doc\": \"Hydrologic unit code.\", \"type\": \"string\"}, {\"name\": \"basin_cd\", \"doc\": \"Drainage basin code.\", \"type\": \"string\"}, {\"name\": \"topo_cd\", \"doc\": \"Topographic setting code.\", \"type\": \"string\"}, {\"name\": \"instruments_cd\", \"doc\": \"Flags for instruments at site.\", \"type\": \"string\"}, {\"name\": \"construction_dt\", \"doc\": \"Date of first construction.\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"inventory_dt\", \"doc\": \"Date site established or inventoried.\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"drain_area_va\", \"doc\": \"Drainage area.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"contrib_drain_area_va\", \"doc\": \"Contributing drainage area.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"tz_cd\", \"doc\": \"Time Zone abbreviation.\", \"type\": \"string\"}, {\"name\": \"local_time_fg\", \"doc\": \"Site honors Daylight Savings Time flag.\", \"type\": \"boolean\"}, {\"name\": \"reliability_cd\", \"doc\": \"Data reliability code.\", \"type\": \"string\"}, {\"name\": \"gw_file_cd\", \"doc\": \"Data-other GW files code.\", \"type\": \"string\"}, {\"name\": \"nat_aqfr_cd\", \"doc\": \"National aquifer code.\", \"type\": \"string\"}, {\"name\": \"aqfr_cd\", \"doc\": \"Local aquifer code.\", \"type\": \"string\"}, {\"name\": \"aqfr_type_cd\", \"doc\": \"Local aquifer type code.\", \"type\": \"string\"}, {\"name\": \"well_depth_va\", \"doc\": \"Well depth.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"hole_depth_va\", \"doc\": \"Hole depth.\", \"type\": [\"null\", \"float\"], \"default\": null}, {\"name\": \"depth_src_cd\", \"doc\": \"Source of depth data.\", \"type\": \"string\"}, {\"name\": \"project_no\", \"doc\": \"Project number.\", \"type\": \"string\"}]}"
    )

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
                    'avro/binary': Encodes the data to Avro binary format.
                    'application/vnd.apache.avro+avro': Encodes the data to Avro binary format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
            stream = io.BytesIO()
            writer = avro.io.DatumWriter(self.AvroType)
            encoder = avro.io.BinaryEncoder(stream)
            writer.write(self.to_serializer_dict(), encoder)
            result = stream.getvalue()
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Site']:
        """
        Converts the data to a dataclass based on the content type string.
        
        Args:
            data: The data to convert to a dataclass.
            content_type_string: The content type string to convert the data to. 
                Supported content types:
                    'avro/binary': Attempts to decode the data from Avro binary encoded format.
                    'application/vnd.apache.avro+avro': Attempts to decode the data from Avro binary encoded format.
                    'avro/json': Attempts to decode the data from Avro JSON encoded format.
                    'application/vnd.apache.avro+json': Attempts to decode the data from Avro JSON encoded format.
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
        if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro', 'avro/json', 'application/vnd.apache.avro+json']:
            if isinstance(data, (bytes, io.BytesIO)):
                stream = io.BytesIO(data) if isinstance(data, bytes) else data
            else:
                raise NotImplementedError('Data is not of a supported type for conversion to Stream')
            reader = avro.io.DatumReader(cls.AvroType)
            if base_content_type in ['avro/binary', 'application/vnd.apache.avro+avro']:
                decoder = avro.io.BinaryDecoder(stream)
            else:
                raise NotImplementedError(f'Unsupported Avro media type {content_type}')
            _record = reader.read(decoder)            
            return Site.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return Site.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')