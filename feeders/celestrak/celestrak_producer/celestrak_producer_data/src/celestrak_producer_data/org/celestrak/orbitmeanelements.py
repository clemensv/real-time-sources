""" OrbitMeanElements dataclass. """

# pylint: disable=too-many-lines, too-many-locals, too-many-branches, too-many-statements, too-many-arguments, line-too-long, wildcard-import
from __future__ import annotations
import io
import gzip
import enum
import typing
import dataclasses
from dataclasses import dataclass
import dataclasses_json
from dataclasses_json import Undefined, dataclass_json
from marshmallow import fields
import json
from typing import Any
import datetime


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OrbitMeanElements:
    """
    A General Perturbations (GP) orbital element set for one catalogued object, as published by CelesTrak at `NORAD/elements/gp.php`. This is a CCSDS Orbit Mean-Elements Message (OMM, CCSDS 502.0-B-3) fit by the US Space Force 18th Space Defense Squadron to Space Surveillance Network observations for use with the SGP4 propagator. The property names are the verbatim OMM keys, so the payload is a drop-in OMM JSON object for SGP4 libraries. Emitted whenever the bridge observes a new or refreshed element set for the object (GP data updates several times per day). Keyed by `NORAD_CAT_ID`.
    
    Attributes:
        OBJECT_NAME (typing.Optional[str])
        OBJECT_ID (typing.Optional[str])
        EPOCH (datetime.datetime)
        MEAN_MOTION (float)
        ECCENTRICITY (float)
        INCLINATION (float)
        RA_OF_ASC_NODE (float)
        ARG_OF_PERICENTER (float)
        MEAN_ANOMALY (float)
        EPHEMERIS_TYPE (int)
        CLASSIFICATION_TYPE (Any)
        NORAD_CAT_ID (int)
        ELEMENT_SET_NO (int)
        REV_AT_EPOCH (int)
        BSTAR (float)
        MEAN_MOTION_DOT (float)
        MEAN_MOTION_DDOT (float)
    """
    
    
    OBJECT_NAME: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OBJECT_NAME"))
    OBJECT_ID: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="OBJECT_ID"))
    EPOCH: datetime.datetime=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="EPOCH", encoder=lambda d: d.isoformat() if isinstance(d, datetime.datetime) else d if d else None, decoder=lambda d: datetime.datetime.fromisoformat(d) if isinstance(d, str) else d if d else None, mm_field=fields.DateTime(format='iso')))
    MEAN_MOTION: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="MEAN_MOTION"))
    ECCENTRICITY: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ECCENTRICITY"))
    INCLINATION: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="INCLINATION"))
    RA_OF_ASC_NODE: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="RA_OF_ASC_NODE"))
    ARG_OF_PERICENTER: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ARG_OF_PERICENTER"))
    MEAN_ANOMALY: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="MEAN_ANOMALY"))
    EPHEMERIS_TYPE: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="EPHEMERIS_TYPE"))
    CLASSIFICATION_TYPE: Any=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="CLASSIFICATION_TYPE"))
    NORAD_CAT_ID: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="NORAD_CAT_ID"))
    ELEMENT_SET_NO: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="ELEMENT_SET_NO"))
    REV_AT_EPOCH: int=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="REV_AT_EPOCH"))
    BSTAR: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="BSTAR"))
    MEAN_MOTION_DOT: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="MEAN_MOTION_DOT"))
    MEAN_MOTION_DDOT: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="MEAN_MOTION_DDOT"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'OrbitMeanElements':
        """
        Converts a dictionary to a dataclass instance.
        
        Args:
            data: The dictionary to convert to a dataclass.
        
        Returns:
            The dataclass representation of the dataclass.
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
            if isinstance(v, enum.Enum):
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            #pylint: disable=no-member
            result = self.to_json()
            #pylint: enable=no-member
            if isinstance(result, str):
                result = result.encode('utf-8')
            if isinstance(result, str):
                result = result.encode('utf-8')

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
    def from_data(cls, data: typing.Any, content_type_string: typing.Optional[str] = None) -> typing.Optional['OrbitMeanElements']:
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
        
        # Strip compression suffix for base type matching
        base_content_type = content_type.replace('+gzip', '')
        if base_content_type == 'application/json':
            if isinstance(data, (bytes, str)):
                data_str = data.decode('utf-8') if isinstance(data, bytes) else data
                _record = json.loads(data_str)
                return OrbitMeanElements.from_serializer_dict(_record)
            else:
                raise NotImplementedError('Data is not of a supported type for JSON deserialization')
        raise NotImplementedError(f'Unsupported media type {content_type}')

    @classmethod
    def create_instance(cls) -> 'OrbitMeanElements':
        """
        Creates an instance of the dataclass with test values.
        
        Returns:
            An instance of the dataclass.
        """
        return cls(
            OBJECT_NAME='qhuacctgqghgjbrjcwxf',
            OBJECT_ID='yliyuyeofhcjiyybrbhf',
            EPOCH=datetime.datetime.now(datetime.timezone.utc),
            MEAN_MOTION=float(26.96864869486564),
            ECCENTRICITY=float(2.313001381367008),
            INCLINATION=float(89.29084961293945),
            RA_OF_ASC_NODE=float(51.51351570850379),
            ARG_OF_PERICENTER=float(5.1183797858268765),
            MEAN_ANOMALY=float(39.05093008067099),
            EPHEMERIS_TYPE=int(15),
            CLASSIFICATION_TYPE=None,
            NORAD_CAT_ID=int(8),
            ELEMENT_SET_NO=int(7),
            REV_AT_EPOCH=int(76),
            BSTAR=float(36.89584112788773),
            MEAN_MOTION_DOT=float(0.17025166103343814),
            MEAN_MOTION_DDOT=float(19.29611145988509)
        )