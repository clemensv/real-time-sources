""" Observation dataclass. """

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


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Observation:
    """
    A hydrometric Observation record.
    Attributes:
        code_station (str): Station code for this observation
        date_obs (str): Observation timestamp in ISO 8601
        resultat_obs (float): Observation value (mm for H, L/s for Q)
        grandeur_hydro (str): Hydrometric quantity: H (height) or Q (discharge)
        libelle_methode_obs (str): Observation method label
        libelle_qualification_obs (str): Quality qualification label
    """

    code_station: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="code_station"))
    date_obs: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="date_obs"))
    resultat_obs: float=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="resultat_obs"))
    grandeur_hydro: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="grandeur_hydro"))
    libelle_methode_obs: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_methode_obs"))
    libelle_qualification_obs: str=dataclasses.field(kw_only=True, metadata=dataclasses_json.config(field_name="libelle_qualification_obs"))

    def __post_init__(self):
        self.code_station=str(self.code_station)
        self.date_obs=str(self.date_obs)
        self.resultat_obs=float(self.resultat_obs)
        self.grandeur_hydro=str(self.grandeur_hydro)
        self.libelle_methode_obs=str(self.libelle_methode_obs)
        self.libelle_qualification_obs=str(self.libelle_qualification_obs)

    def to_byte_array(self, content_type_string: str) -> bytes:
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            return json.dumps(self.to_dict()).encode('utf-8')
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    @classmethod
    def from_data(cls, data: typing.Any, content_type_string: str = 'application/json') -> 'Observation':
        content_type = content_type_string.split(';')[0].strip()
        if content_type == 'application/json':
            if isinstance(data, str):
                data = json.loads(data)
            if isinstance(data, bytes):
                data = json.loads(data.decode('utf-8'))
            return Observation.from_dict(data)
        raise NotImplementedError(f"Unsupported content type: {content_type}")

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
