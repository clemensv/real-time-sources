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
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if isinstance(ordinal, int):
            if ordinal == 0:
                return OccupancyStatus.EMPTY
            elif ordinal == 1:
                return OccupancyStatus.MANY_SEATS_AVAILABLE
            elif ordinal == 2:
                return OccupancyStatus.FEW_SEATS_AVAILABLE
            elif ordinal == 3:
                return OccupancyStatus.STANDING_ROOM_ONLY
            elif ordinal == 4:
                return OccupancyStatus.CRUSHED_STANDING_ROOM_ONLY
            elif ordinal == 5:
                return OccupancyStatus.FULL
            elif ordinal == 6:
                return OccupancyStatus.NOT_ACCEPTING_PASSENGERS
            raise ValueError("Ordinal not found in enum")
        else:
            raise ValueError("Ordinal must be an integer or a string representation of an integer")

    @classmethod
    def to_ordinal(cls, member: 'OccupancyStatus') -> int:
        """
        Get enum ordinal

        Args:
            member (OccupancyStatus): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        
        if member == OccupancyStatus.EMPTY:
            return 0
        if member == OccupancyStatus.MANY_SEATS_AVAILABLE:
            return 1
        if member == OccupancyStatus.FEW_SEATS_AVAILABLE:
            return 2
        if member == OccupancyStatus.STANDING_ROOM_ONLY:
            return 3
        if member == OccupancyStatus.CRUSHED_STANDING_ROOM_ONLY:
            return 4
        if member == OccupancyStatus.FULL:
            return 5
        if member == OccupancyStatus.NOT_ACCEPTING_PASSENGERS:
            return 6
        raise ValueError("Member not found in enum")