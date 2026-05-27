from enum import Enum


class CategoryEnum(Enum):
    """
    Per-region tsunami forecast category from VTSE41 detail bulletins, normalized from JMA 大津波警報, 津波警報, 津波注意報, or 津波予報 text.
    """
    MAJOR_WARNING = 'MAJOR_WARNING'
    WARNING = 'WARNING'
    ADVISORY = 'ADVISORY'
    FORECAST = 'FORECAST'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'CategoryEnum':
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
    def to_ordinal(cls, member: 'CategoryEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (CategoryEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)