from enum import Enum

class BikesAllowed(Enum):
    """
    Indicates whether bikes are allowed. Symbols: NO_INFO - No bike information for the trip; BICYCLE_ALLOWED - Vehicle can accommodate at least one bicycle; BICYCLE_NOT_ALLOWED - No bicycles are allowed on this trip.
    """
    NO_INFO = 'NO_INFO'
    BICYCLE_ALLOWED = 'BICYCLE_ALLOWED'
    BICYCLE_NOT_ALLOWED = 'BICYCLE_NOT_ALLOWED'

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'BikesAllowed':
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
    def to_ordinal(cls, member: 'BikesAllowed') -> int:
        """
        Get enum ordinal

        Args:
            member (BikesAllowed): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)