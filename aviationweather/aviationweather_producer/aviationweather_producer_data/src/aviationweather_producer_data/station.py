""" Station dataclass. """

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
import json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Station:
    """
    Reference record for an aviation weather reporting station.

    Attributes:
        icao_id (str)
        iata_id (typing.Optional[str])
        faa_id (typing.Optional[str])
        wmo_id (typing.Optional[str])
        name (str)
        latitude (float)
        longitude (float)
        elevation (typing.Optional[float])
        state (typing.Optional[str])
        country (typing.Optional[str])
        site_type (typing.Optional[str])
    """


    icao_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icao_id"))
    iata_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="iata_id"))
    faa_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="faa_id"))
    wmo_id: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="wmo_id"))
    name: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="name"))
    latitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="latitude"))
    longitude: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="longitude"))
    elevation: typing.Optional[float]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="elevation"))
    state: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="state"))
    country: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="country"))
    site_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="site_type"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Station':
        """Converts a dictionary to a dataclass instance."""
        return cls(**data)

    def to_serializer_dict(self) -> dict:
        """Converts the dataclass to a dictionary."""
        return self.to_dict()

    def to_byte_array(self, content_type: str = "application/json") -> bytes:
        """Converts the dataclass to a byte array."""
        if content_type == "application/json":
            return json.dumps(self.to_serializer_dict()).encode("utf-8")
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        """Converts the dataclass to a JSON string."""
        return json.dumps(self.to_serializer_dict())
