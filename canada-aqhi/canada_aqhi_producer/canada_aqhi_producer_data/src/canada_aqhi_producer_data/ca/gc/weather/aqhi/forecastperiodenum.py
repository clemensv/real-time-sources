from enum import IntEnum


class ForecastPeriodenum(IntEnum):
    """
    AQHI public forecast period number: 1 Today, 2 Tonight, 3 Tomorrow, 4 Tomorrow Night.
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ForecastPeriodenum':
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
    def to_ordinal(cls, member: 'ForecastPeriodenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ForecastPeriodenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)