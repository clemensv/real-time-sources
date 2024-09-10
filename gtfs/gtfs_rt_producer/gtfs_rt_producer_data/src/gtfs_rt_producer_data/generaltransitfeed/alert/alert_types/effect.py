from enum import Enum

class Effect(Enum):
    """
    What is the effect of this problem on the affected entity.
    """
    NO_SERVICE = 'NO_SERVICE'
    REDUCED_SERVICE = 'REDUCED_SERVICE'
    SIGNIFICANT_DELAYS = 'SIGNIFICANT_DELAYS'
    DETOUR = 'DETOUR'
    ADDITIONAL_SERVICE = 'ADDITIONAL_SERVICE'
    MODIFIED_SERVICE = 'MODIFIED_SERVICE'
    OTHER_EFFECT = 'OTHER_EFFECT'
    UNKNOWN_EFFECT = 'UNKNOWN_EFFECT'
    STOP_MOVED = 'STOP_MOVED'

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'Effect':
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
    def to_ordinal(cls, member: 'Effect') -> int:
        """
        Get enum ordinal

        Args:
            member (Effect): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)