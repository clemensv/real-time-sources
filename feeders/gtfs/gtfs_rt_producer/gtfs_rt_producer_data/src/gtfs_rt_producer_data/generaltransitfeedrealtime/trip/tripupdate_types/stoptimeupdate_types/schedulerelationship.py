from enum import Enum


class ScheduleRelationship(Enum):
    """
    The relation between this StopTime and the static schedule.
    """
    SCHEDULED = 'SCHEDULED'
    SKIPPED = 'SKIPPED'
    NO_DATA = 'NO_DATA'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ScheduleRelationship':
        """
        Get enum member by ordinal

        Args:
            ordinal (int | str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        members = list(cls)
        if 0 <= int(ordinal) < len(members):
            return members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'ScheduleRelationship') -> int:
        """
        Get enum ordinal

        Args:
            member (ScheduleRelationship): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)