from enum import Enum

_OccupancyStatus_members = []

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
        # pylint: disable=global-statement
        global _OccupancyStatus_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _OccupancyStatus_members:
            _OccupancyStatus_members = list(cls)
        if 0 <= int(ordinal) < len(_OccupancyStatus_members):
            return _OccupancyStatus_members[ordinal]
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
        # pylint: disable=global-statement
        global _OccupancyStatus_members
        # pylint: enable=global-statement

        if not _OccupancyStatus_members:
            _OccupancyStatus_members = list(cls)
        return _OccupancyStatus_members.index(member)

_OccupancyStatus_members = list(OccupancyStatus)