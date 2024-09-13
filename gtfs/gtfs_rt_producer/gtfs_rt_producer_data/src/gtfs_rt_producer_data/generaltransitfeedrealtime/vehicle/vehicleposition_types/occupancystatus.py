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

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'OccupancyStatus':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not cls.__member_list:
            cls.__member_list = list(cls)
        if 0 <= int(ordinal) < len(cls.__member_list):
            return cls.__member_list[int(ordinal)]
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
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)