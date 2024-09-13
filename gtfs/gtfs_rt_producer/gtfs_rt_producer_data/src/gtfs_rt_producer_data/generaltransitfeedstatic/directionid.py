from enum import Enum

_DirectionId_members = []

class DirectionId(Enum):
    """
    Indicates the direction of travel for a trip. Symbols: OUTBOUND - Travel in one direction; INBOUND - Travel in the opposite direction.
    """
    OUTBOUND = 'OUTBOUND'
    INBOUND = 'INBOUND'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'DirectionId':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _DirectionId_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _DirectionId_members:
            _DirectionId_members = list(cls)
        if 0 <= int(ordinal) < len(_DirectionId_members):
            return _DirectionId_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'DirectionId') -> int:
        """
        Get enum ordinal

        Args:
            member (DirectionId): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _DirectionId_members
        # pylint: enable=global-statement

        if not _DirectionId_members:
            _DirectionId_members = list(cls)
        return _DirectionId_members.index(member)

_DirectionId_members = list(DirectionId)