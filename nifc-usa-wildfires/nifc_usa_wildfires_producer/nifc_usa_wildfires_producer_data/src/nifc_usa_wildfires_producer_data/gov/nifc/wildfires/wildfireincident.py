""" WildfireIncident dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import json
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
import avro.schema
import avro.name
import avro.io


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class WildfireIncident:
    """
    Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.
    Attributes:
        irwin_id (str): IRWIN incident identifier, a globally unique GUID assigned by the Integrated Reporting of Wildland-Fire Information (IRWIN) system.
        incident_name (str): The name assigned to the wildfire incident.
        unique_fire_identifier (typing.Optional[str]): Unique fire identifier string assigned by the dispatching agency.
        incident_type_category (typing.Optional[str]): Category of the incident type: WF (Wildfire), RX (Prescribed Fire), etc.
        incident_type_kind (typing.Optional[str]): Kind of incident from NWCG classification.
        fire_discovery_datetime (typing.Optional[str]): Date and time when the fire was first discovered, in ISO 8601 format.
        daily_acres (typing.Optional[float]): Most recently reported fire size in acres from the daily situation report.
        calculated_acres (typing.Optional[float]): GIS-calculated fire area in acres.
        discovery_acres (typing.Optional[float]): Size of the fire in acres at the time of initial discovery.
        percent_contained (typing.Optional[float]): Percentage of the fire perimeter that is contained (0-100).
        poo_state (typing.Optional[str]): US state where the point of origin is located.
        poo_county (typing.Optional[str]): County where the point of origin of the fire is located.
        latitude (typing.Optional[float]): Latitude of the fire incident point of origin in decimal degrees (WGS 84).
        longitude (typing.Optional[float]): Longitude of the fire incident point of origin in decimal degrees (WGS 84).
        fire_cause (typing.Optional[str]): General cause of the fire.
        fire_cause_general (typing.Optional[str]): Specific fire cause category when known.
        gacc (typing.Optional[str]): Geographic Area Coordination Center responsible for the incident.
        total_incident_personnel (typing.Optional[int]): Total number of personnel assigned to the incident.
        incident_management_organization (typing.Optional[str]): Name or type of the incident management organization.
        fire_mgmt_complexity (typing.Optional[str]): Complexity level of the fire management effort.
        residences_destroyed (typing.Optional[int]): Number of residential structures destroyed by the fire.
        other_structures_destroyed (typing.Optional[int]): Number of non-residential structures destroyed by the fire.
        injuries (typing.Optional[int]): Number of injuries reported in connection with the incident.
        fatalities (typing.Optional[int]): Number of fatalities reported in connection with the incident.
        containment_datetime (typing.Optional[str]): Date and time the fire was fully contained, in ISO 8601 format.
        control_datetime (typing.Optional[str]): Date and time the fire was declared under control, in ISO 8601 format.
        fire_out_datetime (typing.Optional[str]): Date and time the fire was declared out, in ISO 8601 format.
        final_acres (typing.Optional[float]): Final fire size in acres after the fire is declared out.
        modified_on_datetime (str): Date and time when the incident record was last modified in the IRWIN system, in ISO 8601 format."""
    
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
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"WildfireIncident\", \"namespace\": \"Gov.NIFC.Wildfires\", \"doc\": \"Active wildfire incident data from the National Interagency Fire Center (NIFC) IRWIN system, published via ArcGIS Feature Service.\", \"fields\": [{\"name\": \"irwin_id\", \"type\": \"string\", \"doc\": \"IRWIN incident identifier, a globally unique GUID assigned by the Integrated Reporting of Wildland-Fire Information (IRWIN) system.\"}, {\"name\": \"incident_name\", \"type\": \"string\", \"doc\": \"The name assigned to the wildfire incident.\"}, {\"name\": \"unique_fire_identifier\", \"type\": [\"string\", \"null\"], \"doc\": \"Unique fire identifier string assigned by the dispatching agency.\"}, {\"name\": \"incident_type_category\", \"type\": [\"string\", \"null\"], \"doc\": \"Category of the incident type: WF (Wildfire), RX (Prescribed Fire), etc.\"}, {\"name\": \"incident_type_kind\", \"type\": [\"string\", \"null\"], \"doc\": \"Kind of incident from NWCG classification.\"}, {\"name\": \"fire_discovery_datetime\", \"type\": [\"string\", \"null\"], \"doc\": \"Date and time when the fire was first discovered, in ISO 8601 format.\"}, {\"name\": \"daily_acres\", \"type\": [\"double\", \"null\"], \"doc\": \"Most recently reported fire size in acres from the daily situation report.\"}, {\"name\": \"calculated_acres\", \"type\": [\"double\", \"null\"], \"doc\": \"GIS-calculated fire area in acres.\"}, {\"name\": \"discovery_acres\", \"type\": [\"double\", \"null\"], \"doc\": \"Size of the fire in acres at the time of initial discovery.\"}, {\"name\": \"percent_contained\", \"type\": [\"double\", \"null\"], \"doc\": \"Percentage of the fire perimeter that is contained (0-100).\"}, {\"name\": \"poo_state\", \"type\": [\"string\", \"null\"], \"doc\": \"US state where the point of origin is located.\"}, {\"name\": \"poo_county\", \"type\": [\"string\", \"null\"], \"doc\": \"County where the point of origin of the fire is located.\"}, {\"name\": \"latitude\", \"type\": [\"double\", \"null\"], \"doc\": \"Latitude of the fire incident point of origin in decimal degrees (WGS 84).\"}, {\"name\": \"longitude\", \"type\": [\"double\", \"null\"], \"doc\": \"Longitude of the fire incident point of origin in decimal degrees (WGS 84).\"}, {\"name\": \"fire_cause\", \"type\": [\"string\", \"null\"], \"doc\": \"General cause of the fire.\"}, {\"name\": \"fire_cause_general\", \"type\": [\"string\", \"null\"], \"doc\": \"Specific fire cause category when known.\"}, {\"name\": \"gacc\", \"type\": [\"string\", \"null\"], \"doc\": \"Geographic Area Coordination Center responsible for the incident.\"}, {\"name\": \"total_incident_personnel\", \"type\": [\"int\", \"null\"], \"doc\": \"Total number of personnel assigned to the incident.\"}, {\"name\": \"incident_management_organization\", \"type\": [\"string\", \"null\"], \"doc\": \"Name or type of the incident management organization.\"}, {\"name\": \"fire_mgmt_complexity\", \"type\": [\"string\", \"null\"], \"doc\": \"Complexity level of the fire management effort.\"}, {\"name\": \"residences_destroyed\", \"type\": [\"int\", \"null\"], \"doc\": \"Number of residential structures destroyed by the fire.\"}, {\"name\": \"other_structures_destroyed\", \"type\": [\"int\", \"null\"], \"doc\": \"Number of non-residential structures destroyed by the fire.\"}, {\"name\": \"injuries\", \"type\": [\"int\", \"null\"], \"doc\": \"Number of injuries reported in connection with the incident.\"}, {\"name\": \"fatalities\", \"type\": [\"int\", \"null\"], \"doc\": \"Number of fatalities reported in connection with the incident.\"}, {\"name\": \"containment_datetime\", \"type\": [\"string\", \"null\"], \"doc\": \"Date and time the fire was fully contained, in ISO 8601 format.\"}, {\"name\": \"control_datetime\", \"type\": [\"string\", \"null\"], \"doc\": \"Date and time the fire was declared under control, in ISO 8601 format.\"}, {\"name\": \"fire_out_datetime\", \"type\": [\"string\", \"null\"], \"doc\": \"Date and time the fire was declared out, in ISO 8601 format.\"}, {\"name\": \"final_acres\", \"type\": [\"double\", \"null\"], \"doc\": \"Final fire size in acres after the fire is declared out.\"}, {\"name\": \"modified_on_datetime\", \"type\": \"string\", \"doc\": \"Date and time when the incident record was last modified in the IRWIN system, in ISO 8601 format.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.irwin_id=str(self.irwin_id)
        self.incident_name=str(self.incident_name)
        self.unique_fire_identifier=str(self.unique_fire_identifier) if self.unique_fire_identifier else None
        self.incident_type_category=str(self.incident_type_category) if self.incident_type_category else None
        self.incident_type_kind=str(self.incident_type_kind) if self.incident_type_kind else None
        self.fire_discovery_datetime=str(self.fire_discovery_datetime) if self.fire_discovery_datetime else None
        self.daily_acres=float(self.daily_acres) if self.daily_acres else None
        self.calculated_acres=float(self.calculated_acres) if self.calculated_acres else None
        self.discovery_acres=float(self.discovery_acres) if self.discovery_acres else None
        self.percent_contained=float(self.percent_contained) if self.percent_contained else None
        self.poo_state=str(self.poo_state) if self.poo_state else None
        self.poo_county=str(self.poo_county) if self.poo_county else None
        self.latitude=float(self.latitude) if self.latitude else None
        self.longitude=float(self.longitude) if self.longitude else None
        self.fire_cause=str(self.fire_cause) if self.fire_cause else None
        self.fire_cause_general=str(self.fire_cause_general) if self.fire_cause_general else None
        self.gacc=str(self.gacc) if self.gacc else None
        self.total_incident_personnel=int(self.total_incident_personnel) if self.total_incident_personnel else None
        self.incident_management_organization=str(self.incident_management_organization) if self.incident_management_organization else None
        self.fire_mgmt_complexity=str(self.fire_mgmt_complexity) if self.fire_mgmt_complexity else None
        self.residences_destroyed=int(self.residences_destroyed) if self.residences_destroyed else None
        self.other_structures_destroyed=int(self.other_structures_destroyed) if self.other_structures_destroyed else None
        self.injuries=int(self.injuries) if self.injuries else None
        self.fatalities=int(self.fatalities) if self.fatalities else None
        self.containment_datetime=str(self.containment_datetime) if self.containment_datetime else None
        self.control_datetime=str(self.control_datetime) if self.control_datetime else None
        self.fire_out_datetime=str(self.fire_out_datetime) if self.fire_out_datetime else None
        self.final_acres=float(self.final_acres) if self.final_acres else None
        self.modified_on_datetime=str(self.modified_on_datetime)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'WildfireIncident':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['WildfireIncident']:
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
            return WildfireIncident.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return WildfireIncident.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')