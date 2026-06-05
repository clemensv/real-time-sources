from enum import Enum


class OccupancyStatus(Enum):
    """
    The degree of passenger occupancy of the vehicle. This field is still experimental, and subject to change. It may be formally adopted in the future.
    """
    EMPTY = 'EMPTY'
    MANY_SEATS_AVAILABLE = 'MANY_SEATS_AVAILABLE'
    FEW_SEATS_AVAILABLE = 'FEW_SEATS_AVAILABLE'
    STANDING_ROOM_ONLY = 'STANDING_ROOM_ONLY'
    CRUSHED_STANDING_ROOM_ONLY = 'CRUSHED_STANDING_ROOM_ONLY'
    FULL = 'FULL'
    NOT_ACCEPTING_PASSENGERS = 'NOT_ACCEPTING_PASSENGERS'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'OccupancyStatus':
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
    def to_ordinal(cls, member: 'OccupancyStatus') -> int:
        """
        Get enum ordinal

        Args:
            member (OccupancyStatus): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)