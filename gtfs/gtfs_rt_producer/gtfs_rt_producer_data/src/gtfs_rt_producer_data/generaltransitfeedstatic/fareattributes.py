""" FareAttributes dataclass. """

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
class FareAttributes:
    """
    Defines fare attributes.
    Attributes:
        fareId (str): Identifies a fare class.
        price (float): Fare price, in the unit specified by currency_type.
        currencyType (str): Currency type used to pay the fare.
        paymentMethod (int): When 0, fare must be paid on board. When 1, fare must be paid before boarding.
        transfers (typing.Optional[int]): Specifies the number of transfers permitted on this fare.
        agencyId (typing.Optional[str]): Identifies the agency for the specified fare.
        transferDuration (typing.Optional[int]): Length of time in seconds before a transfer expires."""
    
    fareId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="fareId"))
    price: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="price"))
    currencyType: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="currencyType"))
    paymentMethod: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="paymentMethod"))
    transfers: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="transfers"))
    agencyId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyId"))
    transferDuration: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="transferDuration"))
    
    AvroType: typing.ClassVar[avro.schema.Schema] = avro.schema.make_avsc_object(
        json.loads("{\"type\": \"record\", \"name\": \"FareAttributes\", \"namespace\": \"GeneralTransitFeedStatic\", \"doc\": \"Defines fare attributes.\", \"fields\": [{\"name\": \"fareId\", \"type\": \"string\", \"doc\": \"Identifies a fare class.\"}, {\"name\": \"price\", \"type\": \"double\", \"doc\": \"Fare price, in the unit specified by currency_type.\"}, {\"name\": \"currencyType\", \"type\": \"string\", \"doc\": \"Currency type used to pay the fare.\"}, {\"name\": \"paymentMethod\", \"type\": \"int\", \"doc\": \"When 0, fare must be paid on board. When 1, fare must be paid before boarding.\"}, {\"name\": \"transfers\", \"type\": [\"null\", \"int\"], \"default\": null, \"doc\": \"Specifies the number of transfers permitted on this fare.\"}, {\"name\": \"agencyId\", \"type\": [\"null\", \"string\"], \"default\": null, \"doc\": \"Identifies the agency for the specified fare.\"}, {\"name\": \"transferDuration\", \"type\": [\"null\", \"long\"], \"default\": null, \"doc\": \"Length of time in seconds before a transfer expires.\"}]}"), avro.name.Names()
    )

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.fareId=str(self.fareId)
        self.price=float(self.price)
        self.currencyType=str(self.currencyType)
        self.paymentMethod=int(self.paymentMethod)
        self.transfers=int(self.transfers) if self.transfers else None
        self.agencyId=str(self.agencyId) if self.agencyId else None
        self.transferDuration=int(self.transferDuration) if self.transferDuration else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FareAttributes':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['FareAttributes']:
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
            return FareAttributes.from_serializer_dict(_record)
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return FareAttributes.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')