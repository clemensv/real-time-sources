from enum import Enum


class SeverityEnum(Enum):
    """
    Normalized severity derived from the JMA status text and special-warning codes. NONE represents 発表警報・注意報はなし, ADVISORY represents 注意報-level notices, WARNING represents 警報/発表/継続 items, and EMERGENCY_WARNING represents 特別警報 or special-warning category codes 32-38.
    """
    NONE = 'NONE'
    ADVISORY = 'ADVISORY'
    WARNING = 'WARNING'
    EMERGENCY_WARNING = 'EMERGENCY_WARNING'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'SeverityEnum':
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
    def to_ordinal(cls, member: 'SeverityEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (SeverityEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)