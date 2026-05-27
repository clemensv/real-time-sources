from enum import Enum


class DirectionId(Enum):
    """
    Indicates the direction of travel for a trip. Symbols: OUTBOUND - Travel in one direction; INBOUND - Travel in the opposite direction.
    """
    OUTBOUND = 'OUTBOUND'
    INBOUND = 'INBOUND'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'DirectionId':
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
    def to_ordinal(cls, member: 'DirectionId') -> int:
        """
        Get enum ordinal

        Args:
            member (DirectionId): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)