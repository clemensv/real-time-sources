from enum import Enum

class ServiceAvailability(Enum):
    """
    Indicates whether the service operates on all Mondays in the date range specified. Symbols: NO_SERVICE - Service is not available; SERVICE_AVAILABLE - Service is available.
    """
    NO_SERVICE = 'NO_SERVICE'
    SERVICE_AVAILABLE = 'SERVICE_AVAILABLE'

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'ServiceAvailability':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not cls.__member_list:
            cls.__member_list = list(cls)
        if 0 <= int(ordinal) < len(cls.__member_list):
            return cls.__member_list[int(ordinal)]
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
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)