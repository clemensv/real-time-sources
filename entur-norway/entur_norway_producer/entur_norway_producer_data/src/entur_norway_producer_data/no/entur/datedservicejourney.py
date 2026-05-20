""" DatedServiceJourney dataclass. """

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
class DatedServiceJourney:
    """
    Reference data for a dated service journey in the Norwegian public transport network.
    Attributes:
        service_journey_id (str): NeTEx ServiceJourney identifier from DatedVehicleJourneyRef. Example: RUT:ServiceJourney:1-1234.
        operating_day (str): ISO 8601 date string for the operating day from DataFrameRef. Example: 2024-01-01.
        line_ref (str): NeTEx Line reference. Example: RUT:Line:1.
        operator_ref (str): NeTEx Operator or codespace reference. Example: RUT.
        direction_ref (typing.Optional[str]): Direction reference, e.g. Outbound or Inbound.
        vehicle_mode (typing.Optional[str]): SIRI VehicleMode: bus, tram, rail, ferry, metro, water, air, coach, taxi.
        route_ref (typing.Optional[str]): NeTEx Route reference.
        published_line_name (typing.Optional[str]): Public-facing line number or name displayed to passengers.
        external_line_ref (typing.Optional[str]): External line reference.
        origin_name (typing.Optional[str]): Origin stop or place name for this journey.
        destination_name (typing.Optional[str]): Destination stop or place name for this journey.
        data_source (typing.Optional[str]): Operator codespace originating this data record."""
    
    service_journey_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="service_journey_id"))
    operating_day: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operating_day"))
    line_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="line_ref"))
    operator_ref: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="operator_ref"))
    direction_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="direction_ref"))
    vehicle_mode: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="vehicle_mode"))
    route_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="route_ref"))
    published_line_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="published_line_name"))
    external_line_ref: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="external_line_ref"))
    origin_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="origin_name"))
    destination_name: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="destination_name"))
    data_source: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="data_source"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"DatedServiceJourney\", \"namespace\": \"no.entur\", \"doc\": \"Reference data for a dated service journey in the Norwegian public transport network.\", \"fields\": [{\"name\": \"service_journey_id\", \"type\": \"string\", \"doc\": \"NeTEx ServiceJourney identifier from DatedVehicleJourneyRef. Example: RUT:ServiceJourney:1-1234.\"}, {\"name\": \"operating_day\", \"type\": \"string\", \"doc\": \"ISO 8601 date string for the operating day from DataFrameRef. Example: 2024-01-01.\"}, {\"name\": \"line_ref\", \"type\": \"string\", \"doc\": \"NeTEx Line reference. Example: RUT:Line:1.\"}, {\"name\": \"operator_ref\", \"type\": \"string\", \"doc\": \"NeTEx Operator or codespace reference. Example: RUT.\"}, {\"name\": \"direction_ref\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Direction reference, e.g. Outbound or Inbound.\"}, {\"name\": \"vehicle_mode\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"SIRI VehicleMode: bus, tram, rail, ferry, metro, water, air, coach, taxi.\"}, {\"name\": \"route_ref\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"NeTEx Route reference.\"}, {\"name\": \"published_line_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Public-facing line number or name displayed to passengers.\"}, {\"name\": \"external_line_ref\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"External line reference.\"}, {\"name\": \"origin_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Origin stop or place name for this journey.\"}, {\"name\": \"destination_name\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Destination stop or place name for this journey.\"}, {\"name\": \"data_source\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Operator codespace originating this data record.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.service_journey_id=str(self.service_journey_id)
        self.operating_day=str(self.operating_day)
        self.line_ref=str(self.line_ref)
        self.operator_ref=str(self.operator_ref)
        self.direction_ref=str(self.direction_ref) if self.direction_ref else None
        self.vehicle_mode=str(self.vehicle_mode) if self.vehicle_mode else None
        self.route_ref=str(self.route_ref) if self.route_ref else None
        self.published_line_name=str(self.published_line_name) if self.published_line_name else None
        self.external_line_ref=str(self.external_line_ref) if self.external_line_ref else None
        self.origin_name=str(self.origin_name) if self.origin_name else None
        self.destination_name=str(self.destination_name) if self.destination_name else None
        self.data_source=str(self.data_source) if self.data_source else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'DatedServiceJourney':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['DatedServiceJourney']:
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
            return DatedServiceJourney.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return DatedServiceJourney.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')