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
        dec_lat_va (typing.Optional[float]): Decimal latitude.
        dec_long_va (typing.Optional[float]): Decimal longitude.
        coord_acy_cd (str): Coordinate accuracy code.
        dec_coord_datum_cd (str): Decimal coordinate datum code.
        alt_va (typing.Optional[float]): Altitude.
        alt_acy_va (typing.Optional[float]): Altitude accuracy.
        alt_datum_cd (str): Altitude datum code."""
    
    agency_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="agency_cd"))
    site_no: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_no"))
    station_nm: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="station_nm"))
    site_tp_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_tp_cd"))
    dec_lat_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dec_lat_va"))
    dec_long_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dec_long_va"))
    coord_acy_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coord_acy_cd"))
    dec_coord_datum_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="dec_coord_datum_cd"))
    alt_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_va"))
    alt_acy_va: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_acy_va"))
    alt_datum_cd: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="alt_datum_cd"))
    

    def __post_init__(self):
        """ Initializes the dataclass with the provided keyword arguments."""
        self.agency_cd=str(self.agency_cd)
        self.site_no=str(self.site_no)
        self.station_nm=str(self.station_nm)
        self.site_tp_cd=str(self.site_tp_cd)
        self.dec_lat_va=float(self.dec_lat_va) if self.dec_lat_va else None
        self.dec_long_va=float(self.dec_long_va) if self.dec_long_va else None
        self.coord_acy_cd=str(self.coord_acy_cd)
        self.dec_coord_datum_cd=str(self.dec_coord_datum_cd)
        self.alt_va=float(self.alt_va) if self.alt_va else None
        self.alt_acy_va=float(self.alt_acy_va) if self.alt_acy_va else None
        self.alt_datum_cd=str(self.alt_datum_cd)

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