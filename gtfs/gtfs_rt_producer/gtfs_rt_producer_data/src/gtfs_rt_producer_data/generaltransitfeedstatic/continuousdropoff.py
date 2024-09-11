from enum import Enum

class ContinuousDropOff(Enum):
    """
    Indicates that the rider can alight from the transit vehicle at any point along the vehicle’s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping drop off; NO_CONTINUOUS_STOPPING - No continuous stopping drop off; PHONE_AGENCY - Must phone agency to arrange continuous stopping drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping drop off.
    """
    CONTINUOUS_STOPPING = 'CONTINUOUS_STOPPING'
    NO_CONTINUOUS_STOPPING = 'NO_CONTINUOUS_STOPPING'
    PHONE_AGENCY = 'PHONE_AGENCY'
    COORDINATE_WITH_DRIVER = 'COORDINATE_WITH_DRIVER'

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'ContinuousDropOff':
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
    def to_ordinal(cls, member: 'ContinuousDropOff') -> int:
        """
        Get enum ordinal

        Args:
            member (ContinuousDropOff): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)