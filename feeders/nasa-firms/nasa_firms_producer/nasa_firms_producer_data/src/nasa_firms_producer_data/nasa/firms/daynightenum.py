from enum import Enum


class DaynightEnum(Enum):
    """
    Day/Night flag for the overpass: `D` (daytime) or `N` (nighttime), based on solar elevation at the pixel. Night detections are less prone to solar false alarms. Sourced from the CSV `daynight` column.
    """
    D = 'D'
    N = 'N'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'DaynightEnum':
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
    def to_ordinal(cls, member: 'DaynightEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (DaynightEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)