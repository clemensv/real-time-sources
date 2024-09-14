from enum import Enum

class VehicleStopStatus(Enum):
    """
    A VehicleStopStatus enum.
    """
    INCOMING_AT = 'INCOMING_AT'
    STOPPED_AT = 'STOPPED_AT'
    IN_TRANSIT_TO = 'IN_TRANSIT_TO'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'VehicleStopStatus':
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
                return VehicleStopStatus.INCOMING_AT
            elif ordinal == 1:
                return VehicleStopStatus.STOPPED_AT
            elif ordinal == 2:
                return VehicleStopStatus.IN_TRANSIT_TO
            raise ValueError("Ordinal not found in enum")
        else:
            raise ValueError("Ordinal must be an integer or a string representation of an integer")

    @classmethod
    def to_ordinal(cls, member: 'VehicleStopStatus') -> int:
        """
        Get enum ordinal

        Args:
            member (VehicleStopStatus): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        
        if member == VehicleStopStatus.INCOMING_AT:
            return 0
        if member == VehicleStopStatus.STOPPED_AT:
            return 1
        if member == VehicleStopStatus.IN_TRANSIT_TO:
            return 2
        raise ValueError("Member not found in enum")