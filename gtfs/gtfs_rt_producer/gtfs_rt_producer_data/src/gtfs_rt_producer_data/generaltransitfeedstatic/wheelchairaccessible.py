from enum import Enum
_WheelchairAccessible_members = []

class WheelchairAccessible(Enum):
    """
    Indicates wheelchair accessibility. Symbols: NO_INFO - No accessibility information for the trip; WHEELCHAIR_ACCESSIBLE - Vehicle can accommodate at least one rider in a wheelchair; NOT_WHEELCHAIR_ACCESSIBLE - No riders in wheelchairs can be accommodated on this trip.
    """
    NO_INFO = 'NO_INFO'
    WHEELCHAIR_ACCESSIBLE = 'WHEELCHAIR_ACCESSIBLE'
    NOT_WHEELCHAIR_ACCESSIBLE = 'NOT_WHEELCHAIR_ACCESSIBLE'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'WheelchairAccessible':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _WheelchairAccessible_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if not _WheelchairAccessible_members:
            _WheelchairAccessible_members = list(cls)
        if 0 <= int(ordinal) < len(_WheelchairAccessible_members):
            return _WheelchairAccessible_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'WheelchairAccessible') -> int:
        """
        Get enum ordinal

        Args:
            member (WheelchairAccessible): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _WheelchairAccessible_members
        # pylint: enable=global-statement
        
        if not _WheelchairAccessible_members:
            _WheelchairAccessible_members = list(cls)
        return _WheelchairAccessible_members.index(member)
_WheelchairAccessible_members = list(WheelchairAccessible)