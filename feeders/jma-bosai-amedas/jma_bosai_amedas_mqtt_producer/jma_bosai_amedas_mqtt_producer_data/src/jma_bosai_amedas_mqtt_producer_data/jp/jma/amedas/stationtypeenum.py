from enum import Enum


class StationTypeenum(Enum):
    """
    JMA AMeDAS station capability tier as published in the live Bosai station table. The tier controls which measurements may be emitted for a station, and the current feed uses codes A through G.
    """
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'StationTypeenum':
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
    def to_ordinal(cls, member: 'StationTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (StationTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)