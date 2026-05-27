from enum import Enum


class ArrivalStatusenum(Enum):
    """
    Normalized observation lifecycle for station wave entries: ESTIMATED for expected or pending arrivals, FIRST_WAVE_OBSERVED when the first wave has arrived, and MAX_WAVE_OBSERVED when a maximum wave height is reported.
    """
    ESTIMATED = 'ESTIMATED'
    FIRST_WAVE_OBSERVED = 'FIRST_WAVE_OBSERVED'
    MAX_WAVE_OBSERVED = 'MAX_WAVE_OBSERVED'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ArrivalStatusenum':
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
    def to_ordinal(cls, member: 'ArrivalStatusenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ArrivalStatusenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)