from enum import Enum


class WheelchairBoarding(Enum):
    """
    Indicates whether wheelchair boardings are possible from the location. Symbols: NO_INFO - No accessibility information; SOME_VEHICLES - Some vehicles at this stop can be boarded by a rider in a wheelchair; NOT_POSSIBLE - Wheelchair boarding is not possible at this stop.
    """
    NO_INFO = 'NO_INFO'
    SOME_VEHICLES = 'SOME_VEHICLES'
    NOT_POSSIBLE = 'NOT_POSSIBLE'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'WheelchairBoarding':
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
    def to_ordinal(cls, member: 'WheelchairBoarding') -> int:
        """
        Get enum ordinal

        Args:
            member (WheelchairBoarding): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)