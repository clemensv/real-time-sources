from enum import Enum


class ZoneTypeenum(Enum):
    """
    NWS zone category from the upstream properties.type field. Forecast-zone responses use 'public' for land forecast zones and marine-oriented values such as 'coastal', 'offshore', or 'marine' for waters forecasts.
    """
    public = 'public'
    coastal = 'coastal'
    offshore = 'offshore'
    marine = 'marine'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ZoneTypeenum':
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
    def to_ordinal(cls, member: 'ZoneTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ZoneTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)