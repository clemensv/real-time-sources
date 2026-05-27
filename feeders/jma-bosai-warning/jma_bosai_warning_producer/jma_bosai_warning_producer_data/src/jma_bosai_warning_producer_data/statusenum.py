from enum import Enum


class StatusEnum(Enum):
    """
    Normalized status or alert class for the JMA warning item. Values preserve the documented JMA status set using Python/Avro-safe symbols; lang:ja altenums carries the original JMA labels including 発表警報・注意報はなし.
    """
    ISSUED = 'ISSUED'
    CONTINUED = 'CONTINUED'
    CANCELLED = 'CANCELLED'
    NO_WARNINGS_OR_ADVISORIES = 'NO_WARNINGS_OR_ADVISORIES'
    WARNING = 'WARNING'
    ADVISORY = 'ADVISORY'
    EMERGENCY_WARNING = 'EMERGENCY_WARNING'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'StatusEnum':
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
    def to_ordinal(cls, member: 'StatusEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (StatusEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)