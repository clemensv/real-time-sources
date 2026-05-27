from enum import Enum


class MaxDangerRatingenum(Enum):
    """
    Highest EAWS danger rating across all elevation bands and time periods in this bulletin. One of: low, moderate, considerable, high, very_high, or null if no ratings are present.
    """
    low = 'low'
    moderate = 'moderate'
    considerable = 'considerable'
    high = 'high'
    very_high = 'very_high'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'MaxDangerRatingenum':
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
    def to_ordinal(cls, member: 'MaxDangerRatingenum') -> int:
        """
        Get enum ordinal

        Args:
            member (MaxDangerRatingenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)