from enum import Enum

_LocationType_members = []

class LocationType(Enum):
    """
    Location type. Symbols: STOP - Stop or platform; STATION - Physical structure or area that contains one or more platforms; ENTRANCE_EXIT - Location where passengers can enter or exit a station; GENERIC_NODE - Location within a station used to link pathways; BOARDING_AREA - Specific location on a platform where passengers can board and/or alight vehicles.
    """
    STOP = 'STOP'
    STATION = 'STATION'
    ENTRANCE_EXIT = 'ENTRANCE_EXIT'
    GENERIC_NODE = 'GENERIC_NODE'
    BOARDING_AREA = 'BOARDING_AREA'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'LocationType':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _LocationType_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _LocationType_members:
            _LocationType_members = list(cls)
        if 0 <= int(ordinal) < len(_LocationType_members):
            return _LocationType_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'LocationType') -> int:
        """
        Get enum ordinal

        Args:
            member (LocationType): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _LocationType_members
        # pylint: enable=global-statement

        if not _LocationType_members:
            _LocationType_members = list(cls)
        return _LocationType_members.index(member)

_LocationType_members = list(LocationType)