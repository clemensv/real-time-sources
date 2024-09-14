from enum import Enum

class ScheduleRelationship(Enum):
    """
    The relation between this trip and the static schedule. If a trip is done in accordance with temporary schedule, not reflected in GTFS, then it shouldn't be marked as SCHEDULED, but likely as ADDED.
    """
    SCHEDULED = 'SCHEDULED'
    ADDED = 'ADDED'
    UNSCHEDULED = 'UNSCHEDULED'
    CANCELED = 'CANCELED'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'ScheduleRelationship':
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
                return ScheduleRelationship.SCHEDULED
            elif ordinal == 1:
                return ScheduleRelationship.ADDED
            elif ordinal == 2:
                return ScheduleRelationship.UNSCHEDULED
            elif ordinal == 3:
                return ScheduleRelationship.CANCELED
            raise ValueError("Ordinal not found in enum")
        else:
            raise ValueError("Ordinal must be an integer or a string representation of an integer")

    @classmethod
    def to_ordinal(cls, member: 'ScheduleRelationship') -> int:
        """
        Get enum ordinal

        Args:
            member (ScheduleRelationship): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        
        if member == ScheduleRelationship.SCHEDULED:
            return 0
        if member == ScheduleRelationship.ADDED:
            return 1
        if member == ScheduleRelationship.UNSCHEDULED:
            return 2
        if member == ScheduleRelationship.CANCELED:
            return 3
        raise ValueError("Member not found in enum")