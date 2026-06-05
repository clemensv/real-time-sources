from enum import Enum


class CountryEnum(Enum):
    """
    ISO 3166-1 alpha-3 country code (typically 'DNK').
    """
    DNK = 'DNK'
    GRL = 'GRL'
    FRO = 'FRO'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'CountryEnum':
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
    def to_ordinal(cls, member: 'CountryEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (CountryEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)