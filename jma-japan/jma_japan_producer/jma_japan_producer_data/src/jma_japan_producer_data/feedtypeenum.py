from enum import Enum


class FeedTypeenum(Enum):
    """
    Which JMA Atom feed this bulletin originated from.
    """
    regular = 'regular'
    extra = 'extra'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'FeedTypeenum':
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
    def to_ordinal(cls, member: 'FeedTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (FeedTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)