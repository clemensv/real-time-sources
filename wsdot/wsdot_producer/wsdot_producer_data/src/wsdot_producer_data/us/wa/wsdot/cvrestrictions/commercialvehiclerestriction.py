""" CommercialVehicleRestriction dataclass. """

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
class CommercialVehicleRestriction:
    """
    Commercial vehicle restriction.
    Attributes:
        state_route_id (str): 
        bridge_number (str): 
        bridge_name (typing.Optional[str]): 
        location_name (typing.Optional[str]): 
        location_description (typing.Optional[str]): 
        latitude (float): 
        longitude (float): 
        state (typing.Optional[str]): 
        restriction_type (typing.Optional[str]): 
        vehicle_type (typing.Optional[str]): 
        restriction_weight_in_pounds (typing.Optional[int]): 
        maximum_gross_vehicle_weight_in_pounds (typing.Optional[int]): 
        restriction_height_in_inches (typing.Optional[int]): 
        restriction_width_in_inches (typing.Optional[int]): 
        restriction_length_in_inches (typing.Optional[int]): 
        is_permanent_restriction (bool): 
        is_warning (bool): 
        is_detour_available (bool): 
        is_exceptions_allowed (bool): 
        restriction_comment (typing.Optional[str]): 
        date_posted (typing.Optional[str]): 
        date_effective (typing.Optional[str]): 
        date_expires (typing.Optional[str]): """
    
    state_route_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state_route_id"))
    bridge_number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bridge_number"))
    bridge_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="bridge_name"))
    location_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_name"))
    location_description: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="location_description"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    restriction_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_type"))
    vehicle_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_type"))
    restriction_weight_in_pounds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_weight_in_pounds"))
    maximum_gross_vehicle_weight_in_pounds: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="maximum_gross_vehicle_weight_in_pounds"))
    restriction_height_in_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_height_in_inches"))
    restriction_width_in_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_width_in_inches"))
    restriction_length_in_inches: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_length_in_inches"))
    is_permanent_restriction: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_permanent_restriction"))
    is_warning: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_warning"))
    is_detour_available: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_detour_available"))
    is_exceptions_allowed: bool=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="is_exceptions_allowed"))
    restriction_comment: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="restriction_comment"))
    date_posted: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_posted"))
    date_effective: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_effective"))
    date_expires: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_expires"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"CommercialVehicleRestriction\", \"namespace\": \"us.wa.wsdot.cvrestrictions\", \"doc\": \"Commercial vehicle restriction.\", \"fields\": [{\"name\": \"state_route_id\", \"type\": \"string\"}, {\"name\": \"bridge_number\", \"type\": \"string\"}, {\"name\": \"bridge_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"location_name\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"location_description\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"latitude\", \"type\": \"double\"}, {\"name\": \"longitude\", \"type\": \"double\"}, {\"name\": \"state\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"restriction_type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"vehicle_type\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"restriction_weight_in_pounds\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"maximum_gross_vehicle_weight_in_pounds\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"restriction_height_in_inches\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"restriction_width_in_inches\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"restriction_length_in_inches\", \"type\": [\"null\", \"int\"], \"default\": null}, {\"name\": \"is_permanent_restriction\", \"type\": \"boolean\"}, {\"name\": \"is_warning\", \"type\": \"boolean\"}, {\"name\": \"is_detour_available\", \"type\": \"boolean\"}, {\"name\": \"is_exceptions_allowed\", \"type\": \"boolean\"}, {\"name\": \"restriction_comment\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"date_posted\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"date_effective\", \"type\": [\"null\", \"string\"], \"default\": null}, {\"name\": \"date_expires\", \"type\": [\"null\", \"string\"], \"default\": null}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.state_route_id=str(self.state_route_id)
        self.bridge_number=str(self.bridge_number)
        self.bridge_name=str(self.bridge_name) if self.bridge_name else None
        self.location_name=str(self.location_name) if self.location_name else None
        self.location_description=str(self.location_description) if self.location_description else None
        self.latitude=float(self.latitude)
        self.longitude=float(self.longitude)
        self.state=str(self.state) if self.state else None
        self.restriction_type=str(self.restriction_type) if self.restriction_type else None
        self.vehicle_type=str(self.vehicle_type) if self.vehicle_type else None
        self.restriction_weight_in_pounds=int(self.restriction_weight_in_pounds) if self.restriction_weight_in_pounds else None
        self.maximum_gross_vehicle_weight_in_pounds=int(self.maximum_gross_vehicle_weight_in_pounds) if self.maximum_gross_vehicle_weight_in_pounds else None
        self.restriction_height_in_inches=int(self.restriction_height_in_inches) if self.restriction_height_in_inches else None
        self.restriction_width_in_inches=int(self.restriction_width_in_inches) if self.restriction_width_in_inches else None
        self.restriction_length_in_inches=int(self.restriction_length_in_inches) if self.restriction_length_in_inches else None
        self.is_permanent_restriction=bool(self.is_permanent_restriction)
        self.is_warning=bool(self.is_warning)
        self.is_detour_available=bool(self.is_detour_available)
        self.is_exceptions_allowed=bool(self.is_exceptions_allowed)
        self.restriction_comment=str(self.restriction_comment) if self.restriction_comment else None
        self.date_posted=str(self.date_posted) if self.date_posted else None
        self.date_effective=str(self.date_effective) if self.date_effective else None
        self.date_expires=str(self.date_expires) if self.date_expires else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'CommercialVehicleRestriction':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['CommercialVehicleRestriction']:
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
            return CommercialVehicleRestriction.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return CommercialVehicleRestriction.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')