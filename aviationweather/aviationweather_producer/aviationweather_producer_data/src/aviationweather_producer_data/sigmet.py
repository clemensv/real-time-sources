""" Sigmet dataclass. """

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
class Sigmet:
    """
    SIGMET advisory from the AviationWeather.gov API.

    Attributes:
        icao_id (str)
        series_id (str)
        valid_time_from (str)
        valid_time_to (str)
        hazard (typing.Optional[str])
        qualifier (typing.Optional[str])
        sigmet_type (typing.Optional[str])
        altitude_hi (typing.Optional[int])
        altitude_low (typing.Optional[int])
        movement_dir (typing.Optional[str])
        movement_spd (typing.Optional[str])
        severity (typing.Optional[int])
        raw_sigmet (typing.Optional[str])
        coords (typing.Optional[str])
    """


    icao_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="icao_id"))
    series_id: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="series_id"))
    valid_time_from: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="valid_time_from"))
    valid_time_to: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="valid_time_to"))
    hazard: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="hazard"))
    qualifier: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="qualifier"))
    sigmet_type: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="sigmet_type"))
    altitude_hi: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude_hi"))
    altitude_low: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="altitude_low"))
    movement_dir: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="movement_dir"))
    movement_spd: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="movement_spd"))
    severity: typing.Optional[int]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="severity"))
    raw_sigmet: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="raw_sigmet"))
    coords: typing.Optional[str]=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="coords"))

    @classmethod
    def from_serializer_dict(cls, data: dict) -> 'Sigmet':
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
