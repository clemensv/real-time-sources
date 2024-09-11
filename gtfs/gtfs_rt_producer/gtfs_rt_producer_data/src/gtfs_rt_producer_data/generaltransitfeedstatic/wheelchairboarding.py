from enum import Enum

class WheelchairBoarding(Enum):
    """
    Indicates whether wheelchair boardings are possible from the location. Symbols: NO_INFO - No accessibility information; SOME_VEHICLES - Some vehicles at this stop can be boarded by a rider in a wheelchair; NOT_POSSIBLE - Wheelchair boarding is not possible at this stop.
    """
    NO_INFO = 'NO_INFO'
    SOME_VEHICLES = 'SOME_VEHICLES'
    NOT_POSSIBLE = 'NOT_POSSIBLE'

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'WheelchairBoarding':
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
    def to_ordinal(cls, member: 'WheelchairBoarding') -> int:
        """
        Get enum ordinal

        Args:
            member (WheelchairBoarding): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)