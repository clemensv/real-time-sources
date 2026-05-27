from enum import Enum


class AlertLevelenum(Enum):
    """
    The overall GDACS alert level for the event, indicating the expected humanitarian impact. Green = low impact, Orange = moderate impact, Red = high impact requiring international response.
    """
    Green = 'Green'
    Orange = 'Orange'
    Red = 'Red'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'AlertLevelenum':
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
    def to_ordinal(cls, member: 'AlertLevelenum') -> int:
        """
        Get enum ordinal

        Args:
            member (AlertLevelenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)