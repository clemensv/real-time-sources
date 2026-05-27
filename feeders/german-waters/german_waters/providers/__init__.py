"""Base provider interface for German water data sources."""

import abc
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class StationData:
    """Internal station representation across all providers."""
    station_id: str
    station_name: str
    water_body: str
    provider: str
    state: str = ""
    region: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    river_km: float = 0.0
    altitude: float = 0.0
    station_type: str = ""
    warn_level_cm: float = 0.0
    alarm_level_cm: float = 0.0
    warn_level_m3s: float = 0.0
    alarm_level_m3s: float = 0.0


@dataclass
class ObservationData:
    """Internal observation representation across all providers."""
    station_id: str
    provider: str
    water_level: float = 0.0
    water_level_unit: str = "cm"
    water_level_timestamp: str = ""
    discharge: float = 0.0
    discharge_unit: str = "m3/s"
    discharge_timestamp: str = ""
    trend: int = 0
    situation: int = 0


class BaseProvider(abc.ABC):
    """Abstract base class for German water data providers."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Short provider identifier used for CLI filtering."""
        ...

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """Human-readable description."""
        ...

    @abc.abstractmethod
    def get_stations(self) -> List[StationData]:
        """Fetch all stations from this provider."""
        ...

    @abc.abstractmethod
    def get_observations(self) -> List[ObservationData]:
        """Fetch current observations from this provider."""
        ...
