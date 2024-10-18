""" Routes dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from gtfs_rt_producer_data.generaltransitfeedstatic.continuousdropoff import ContinuousDropOff
from gtfs_rt_producer_data.generaltransitfeedstatic.continuouspickup import ContinuousPickup
from gtfs_rt_producer_data.generaltransitfeedstatic.routetype import RouteType


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Routes:
    """
    Identifies a route.
    Attributes:
        routeId (str): Identifies a route.
        agencyId (typing.Optional[str]): Agency for the specified route.
        routeShortName (typing.Optional[str]): Short name of a route.
        routeLongName (typing.Optional[str]): Full name of a route.
        routeDesc (typing.Optional[str]): Description of a route that provides useful, quality information.
        routeType (RouteType): Indicates the type of transportation used on a route.
        routeUrl (typing.Optional[str]): URL of a web page about the particular route.
        routeColor (typing.Optional[str]): Route color designation that matches public facing material.
        routeTextColor (typing.Optional[str]): Legible color to use for text drawn against a background of route_color.
        routeSortOrder (typing.Optional[int]): Orders the routes in a way which is ideal for presentation to customers.
        continuousPickup (ContinuousPickup): Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path.
        continuousDropOff (ContinuousDropOff): Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path.
        networkId (typing.Optional[str]): Identifies a group of routes."""
    
    routeId: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeId"))
    agencyId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agencyId"))
    routeShortName: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeShortName"))
    routeLongName: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeLongName"))
    routeDesc: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeDesc"))
    routeType: RouteType=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeType"))
    routeUrl: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeUrl"))
    routeColor: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeColor"))
    routeTextColor: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeTextColor"))
    routeSortOrder: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="routeSortOrder"))
    continuousPickup: ContinuousPickup=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="continuousPickup"))
    continuousDropOff: ContinuousDropOff=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="continuousDropOff"))
    networkId: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="networkId"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.routeId=str(self.routeId)
        self.agencyId=str(self.agencyId) if self.agencyId else None
        self.routeShortName=str(self.routeShortName) if self.routeShortName else None
        self.routeLongName=str(self.routeLongName) if self.routeLongName else None
        self.routeDesc=str(self.routeDesc) if self.routeDesc else None
        self.routeType=RouteType(self.routeType)
        self.routeUrl=str(self.routeUrl) if self.routeUrl else None
        self.routeColor=str(self.routeColor) if self.routeColor else None
        self.routeTextColor=str(self.routeTextColor) if self.routeTextColor else None
        self.routeSortOrder=int(self.routeSortOrder) if self.routeSortOrder else None
        self.continuousPickup=ContinuousPickup(self.continuousPickup)
        self.continuousDropOff=ContinuousDropOff(self.continuousDropOff)
        self.networkId=str(self.networkId) if self.networkId else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Routes':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Routes']:
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
                return Routes.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')