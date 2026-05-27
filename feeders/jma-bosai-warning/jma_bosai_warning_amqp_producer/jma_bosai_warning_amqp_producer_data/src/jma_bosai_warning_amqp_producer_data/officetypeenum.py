from enum import Enum


class OfficeTypeenum(Enum):
    """
    Normalized office class. PREFECTURE is used for standard prefectural offices, SUBREGION for Hokkaido/Okinawa-style regional warning offices, and OFFICE for other JMA issuing-office catalog entries.
    """
    PREFECTURE = 'PREFECTURE'
    SUBREGION = 'SUBREGION'
    OFFICE = 'OFFICE'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'OfficeTypeenum':
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
    def to_ordinal(cls, member: 'OfficeTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (OfficeTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)