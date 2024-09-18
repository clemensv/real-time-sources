""" Station dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
import io
import gzip
import enum
import typing
import dataclasses
import dataclasses_json
import json
from pegelonline_producer_data.de.wsv.pegelonline.water import Water


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Station:
    """
    Schema representing a PEGELONLINE station with location and water body information.
    Attributes:
        uuid (str): Unique immutable identifier of the station.
        number (str): Station number representing the unique code of the station.
        shortname (str): Short name of the station (maximum 40 characters).
        longname (str): Full name of the station (maximum 255 characters).
        km (float): River kilometer marking of the station location.
        agency (str): Waterways and Shipping Office responsible for the station.
        longitude (float): Longitude coordinate of the station in WGS84 decimal notation.
        latitude (float): Latitude coordinate of the station in WGS84 decimal notation.
        water (Water): """
    
    uuid: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="uuid"))
    number: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="number"))
    shortname: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="shortname"))
    longname: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longname"))
    km: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="km"))
    agency: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    water: Water=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="water"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.uuid=str(self.uuid)
        self.number=str(self.number)
        self.shortname=str(self.shortname)
        self.longname=str(self.longname)
        self.km=float(self.km)
        self.agency=str(self.agency)
        self.longitude=float(self.longitude)
        self.latitude=float(self.latitude)
        value_water = self.water
        self.water = value_water if isinstance(value_water, Water) else Water.from_serializer_dict(value_water) if value_water else None

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['Station']:
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
                return Station.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')