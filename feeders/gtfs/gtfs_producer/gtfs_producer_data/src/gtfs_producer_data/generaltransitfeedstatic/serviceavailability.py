from enum import Enum


class ServiceAvailability(Enum):
    """
    Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.
    """
    NO_SERVICE = 'NO_SERVICE'
    SERVICE_AVAILABLE = 'SERVICE_AVAILABLE'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ServiceAvailability':
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
    def to_ordinal(cls, member: 'ServiceAvailability') -> int:
        """
        Get enum ordinal

        Args:
            member (ServiceAvailability): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)