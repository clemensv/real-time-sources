""" FDOM dataclass. """

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
class FDOM:
    """
    USGS dissolved organic matter fluorescence data (fDOM). Parameter codes 32295 and 32322.
    Attributes:
        site_no (str): {"description": "USGS site number."}
        datetime (str): {"description": "Date and time of the measurement in ISO-8601 format."}
        value (typing.Optional[float]): {"description": "Dissolved organic matter fluorescence value."}
        exception (typing.Optional[str]): {"description": "Exception code when the value is unavailable."}
        qualifiers (typing.List[str]): {"description": "Qualifiers for the measurement."}
        parameter_cd (str): {"description": "Parameter code."}
        timeseries_cd (str): {"description": "Timeseries code."}"""
    
    site_no: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_no"))
    datetime: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="datetime"))
    value: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="value"))
    exception: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="exception"))
    qualifiers: typing.List[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="qualifiers"))
    parameter_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="parameter_cd"))
    timeseries_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="timeseries_cd"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.site_no=str(self.site_no)
        self.datetime=str(self.datetime)
        self.value=float(self.value) if self.value else None
        self.exception=str(self.exception) if self.exception else None
        self.qualifiers=self.qualifiers if isinstance(self.qualifiers, list) else [str(v) for v in self.qualifiers] if self.qualifiers else None
        self.parameter_cd=str(self.parameter_cd)
        self.timeseries_cd=str(self.timeseries_cd)

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'FDOM':
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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['FDOM']:
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
                return FDOM.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')

        raise NotImplementedError(f'Unsupported media type {content_type}')