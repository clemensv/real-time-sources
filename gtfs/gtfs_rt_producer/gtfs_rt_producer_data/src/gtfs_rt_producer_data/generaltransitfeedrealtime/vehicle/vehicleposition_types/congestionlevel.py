from enum import Enum

_CongestionLevel_members = []

class CongestionLevel(Enum):
    """
    Congestion level that is affecting this vehicle.
    """
    UNKNOWN_CONGESTION_LEVEL = 'UNKNOWN_CONGESTION_LEVEL'
    RUNNING_SMOOTHLY = 'RUNNING_SMOOTHLY'
    STOP_AND_GO = 'STOP_AND_GO'
    CONGESTION = 'CONGESTION'
    SEVERE_CONGESTION = 'SEVERE_CONGESTION'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'CongestionLevel':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _CongestionLevel_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _CongestionLevel_members:
            _CongestionLevel_members = list(cls)
        if 0 <= int(ordinal) < len(_CongestionLevel_members):
            return _CongestionLevel_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'CongestionLevel') -> int:
        """
        Get enum ordinal

        Args:
            member (CongestionLevel): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _CongestionLevel_members
        # pylint: enable=global-statement

        if not _CongestionLevel_members:
            _CongestionLevel_members = list(cls)
        return _CongestionLevel_members.index(member)

_CongestionLevel_members = list(CongestionLevel)