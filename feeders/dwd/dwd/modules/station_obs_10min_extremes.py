"""Extreme 10-minute station observation module (wind and temperature extremes)."""

from typing import Optional, Set

from dwd.modules.station_obs_10min import StationObs10MinModule
from dwd.util.http_client import DWDHttpClient


class StationObs10MinExtremesModule(StationObs10MinModule):
    """Polls only the DWD extreme 10-minute categories."""

    def __init__(self, http_client: DWDHttpClient, station_filter: Optional[Set[str]] = None):
        super().__init__(
            http_client,
            categories=["extreme_wind", "extreme_temperature"],
            station_filter=station_filter,
        )

    @property
    def name(self) -> str:
        return "station_obs_10min_extremes"

    @property
    def default_enabled(self) -> bool:
        return False
