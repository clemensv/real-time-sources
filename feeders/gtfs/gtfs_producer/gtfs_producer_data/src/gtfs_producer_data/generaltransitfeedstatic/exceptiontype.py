from enum import Enum


class ExceptionType(Enum):
    """
    Indicates whether service is available on the date specified. Symbols: SERVICE_ADDED - Service has been added for the specified date; SERVICE_REMOVED - Service has been removed for the specified date.
    """
    SERVICE_ADDED = 'SERVICE_ADDED'
    SERVICE_REMOVED = 'SERVICE_REMOVED'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ExceptionType':
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
    def to_ordinal(cls, member: 'ExceptionType') -> int:
        """
        Get enum ordinal

        Args:
            member (ExceptionType): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)