""" Attributions dataclass. """

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
class Attributions:
    """
    Provides information about the attributions.
    Attributes:
        attributionId (typing.Optional[str]): Identifies an attribution for the dataset.
        agencyId (typing.Optional[str]): Identifies the agency associated with the attribution.
        routeId (typing.Optional[str]): Identifies the route associated with the attribution.
        tripId (typing.Optional[str]): Identifies the trip associated with the attribution.
        organizationName (str): Name of the organization associated with the attribution.
        isProducer (typing.Optional[int]): Indicates if the organization is a producer.
        isOperator (typing.Optional[int]): Indicates if the organization is an operator.
        isAuthority (typing.Optional[int]): Indicates if the organization is an authority.
        attributionUrl (typing.Optional[str]): URL of a web page about the attribution.
        attributionEmail (typing.Optional[str]): Email address associated with the attribution.
        attributionPhone (typing.Optional[str]): Phone number associated with the attribution."""
    
    attributionId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attributionId"))
    agencyId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyId"))
    routeId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeId"))
    tripId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="tripId"))
    organizationName: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="organizationName"))
    isProducer: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="isProducer"))
    isOperator: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="isOperator"))
    isAuthority: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="isAuthority"))
    attributionUrl: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attributionUrl"))
    attributionEmail: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attributionEmail"))
    attributionPhone: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="attributionPhone"))    
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.attributionId=str(self.attributionId) if self.attributionId else None
        self.agencyId=str(self.agencyId) if self.agencyId else None
        self.routeId=str(self.routeId) if self.routeId else None
        self.tripId=str(self.tripId) if self.tripId else None
        self.organizationName=str(self.organizationName)
        self.isProducer=int(self.isProducer) if self.isProducer else None
        self.isOperator=int(self.isOperator) if self.isOperator else None
        self.isAuthority=int(self.isAuthority) if self.isAuthority else None
        self.attributionUrl=str(self.attributionUrl) if self.attributionUrl else None
        self.attributionEmail=str(self.attributionEmail) if self.attributionEmail else None
        self.attributionPhone=str(self.attributionPhone) if self.attributionPhone else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Attributions':
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
            result = self.to_json()

        if result is not None and content_type.endswith('+gzip'):
            with io.BytesIO() as stream:
                with gzip.GzipFile(fileobj=stream, mode='wb') as gzip_file:
                    gzip_file.write(result)
                result = stream.getvalue()

        if result is None:
            raise NotImplementedError(f"Unsupported media type {content_type}")

        return result

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Attributions']:
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
                return Attributions.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')