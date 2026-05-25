from enum import Enum


class Cause(Enum):
    """
    Cause of this alert.
    """
    UNKNOWN_CAUSE = 'UNKNOWN_CAUSE'
    OTHER_CAUSE = 'OTHER_CAUSE'
    TECHNICAL_PROBLEM = 'TECHNICAL_PROBLEM'
    STRIKE = 'STRIKE'
    DEMONSTRATION = 'DEMONSTRATION'
    ACCIDENT = 'ACCIDENT'
    HOLIDAY = 'HOLIDAY'
    WEATHER = 'WEATHER'
    MAINTENANCE = 'MAINTENANCE'
    CONSTRUCTION = 'CONSTRUCTION'
    POLICE_ACTIVITY = 'POLICE_ACTIVITY'
    MEDICAL_EMERGENCY = 'MEDICAL_EMERGENCY'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'Cause':
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
    def to_ordinal(cls, member: 'Cause') -> int:
        """
        Get enum ordinal

        Args:
            member (Cause): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)