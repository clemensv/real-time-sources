from enum import Enum


class ParameterNameenum(Enum):
    """
    OpenAQ machine-readable parameter name, for example pm25, pm10, o3, no2, so2, co, bc, temperature, relativehumidity, pressure, or windspeed. Used as a routing segment; not localized. Source: OpenAQ API v3 docs (https://api.openaq.org/openapi.json, https://docs.openaq.org/).
    """
    pm25 = 'pm25'
    pm10 = 'pm10'
    o3 = 'o3'
    no2 = 'no2'
    so2 = 'so2'
    co = 'co'
    bc = 'bc'
    no = 'no'
    nox = 'nox'
    pm1 = 'pm1'
    co2 = 'co2'
    temperature = 'temperature'
    relativehumidity = 'relativehumidity'
    pressure = 'pressure'
    windspeed = 'windspeed'
    winddirection = 'winddirection'
    um003 = 'um003'
    um005 = 'um005'
    um010 = 'um010'
    um025 = 'um025'
    um050 = 'um050'
    um100 = 'um100'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ParameterNameenum':
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
    def to_ordinal(cls, member: 'ParameterNameenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ParameterNameenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)