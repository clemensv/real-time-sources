from enum import Enum


class ParameterIdenum(Enum):
    """
    DMI parameter identifier (e.g. 'temp_dry', 'wind_speed', 'humidity', 'pressure_at_sea').
    """
    temp_dry = 'temp_dry'
    temp_dew = 'temp_dew'
    temp_grass = 'temp_grass'
    temp_soil_10cm = 'temp_soil_10cm'
    temp_mean_past1h = 'temp_mean_past1h'
    temp_max_past1h = 'temp_max_past1h'
    temp_min_past1h = 'temp_min_past1h'
    humidity = 'humidity'
    humidity_past1h = 'humidity_past1h'
    pressure = 'pressure'
    pressure_at_sea = 'pressure_at_sea'
    wind_dir = 'wind_dir'
    wind_dir_past1h = 'wind_dir_past1h'
    wind_speed = 'wind_speed'
    wind_speed_past1h = 'wind_speed_past1h'
    wind_max = 'wind_max'
    wind_min = 'wind_min'
    wind_max_per10min_past1h = 'wind_max_per10min_past1h'
    wind_min_past1h = 'wind_min_past1h'
    gust_always_past1h = 'gust_always_past1h'
    precip_past1h = 'precip_past1h'
    precip_past10min = 'precip_past10min'
    precip_past24h = 'precip_past24h'
    snow_depth_man = 'snow_depth_man'
    snow_cover_man = 'snow_cover_man'
    visibility = 'visibility'
    visib_mean_last10min = 'visib_mean_last10min'
    cloud_cover = 'cloud_cover'
    cloud_height = 'cloud_height'
    weather = 'weather'
    leav_hum_dur_past10min = 'leav_hum_dur_past10min'
    radia_glob = 'radia_glob'
    radia_glob_past1h = 'radia_glob_past1h'
    sun_last10min_glob = 'sun_last10min_glob'
    sun_last1h_glob = 'sun_last1h_glob'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ParameterIdenum':
        """
        Get enum member by ordinal

        Args:
            ordinal (int | str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        members = list(cls)
        if 0 <= int(ordinal) < len(members):
            return members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'ParameterIdenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ParameterIdenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)