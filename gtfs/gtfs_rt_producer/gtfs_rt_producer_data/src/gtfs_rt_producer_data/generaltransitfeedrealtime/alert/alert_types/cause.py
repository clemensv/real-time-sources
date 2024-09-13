from enum import Enum

_Cause_members = []

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
    def from_ordinal(cls, ordinal: int|str) -> 'Cause':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _Cause_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _Cause_members:
            _Cause_members = list(cls)
        if 0 <= int(ordinal) < len(_Cause_members):
            return _Cause_members[ordinal]
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
        # pylint: disable=global-statement
        global _Cause_members
        # pylint: enable=global-statement

        if not _Cause_members:
            _Cause_members = list(cls)
        return _Cause_members.index(member)

_Cause_members = list(Cause)