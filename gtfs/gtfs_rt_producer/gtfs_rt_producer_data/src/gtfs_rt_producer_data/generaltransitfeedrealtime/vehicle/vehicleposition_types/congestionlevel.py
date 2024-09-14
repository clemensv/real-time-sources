from enum import Enum

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

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if isinstance(ordinal, int):
            if ordinal == 0:
                return CongestionLevel.UNKNOWN_CONGESTION_LEVEL
            elif ordinal == 1:
                return CongestionLevel.RUNNING_SMOOTHLY
            elif ordinal == 2:
                return CongestionLevel.STOP_AND_GO
            elif ordinal == 3:
                return CongestionLevel.CONGESTION
            elif ordinal == 4:
                return CongestionLevel.SEVERE_CONGESTION
            raise ValueError("Ordinal not found in enum")
        else:
            raise ValueError("Ordinal must be an integer or a string representation of an integer")

    @classmethod
    def to_ordinal(cls, member: 'CongestionLevel') -> int:
        """
        Get enum ordinal

        Args:
            member (CongestionLevel): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        
        if member == CongestionLevel.UNKNOWN_CONGESTION_LEVEL:
            return 0
        if member == CongestionLevel.RUNNING_SMOOTHLY:
            return 1
        if member == CongestionLevel.STOP_AND_GO:
            return 2
        if member == CongestionLevel.CONGESTION:
            return 3
        if member == CongestionLevel.SEVERE_CONGESTION:
            return 4
        raise ValueError("Member not found in enum")