from enum import Enum

_VehicleStopStatus_members = []

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
        # pylint: disable=global-statement
        global _VehicleStopStatus_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _VehicleStopStatus_members:
            _VehicleStopStatus_members = list(cls)
        if 0 <= int(ordinal) < len(_VehicleStopStatus_members):
            return _VehicleStopStatus_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'VehicleStopStatus') -> int:
        """
        Get enum ordinal

        Args:
            member (VehicleStopStatus): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _VehicleStopStatus_members
        # pylint: enable=global-statement

        if not _VehicleStopStatus_members:
            _VehicleStopStatus_members = list(cls)
        return _VehicleStopStatus_members.index(member)

_VehicleStopStatus_members = list(VehicleStopStatus)