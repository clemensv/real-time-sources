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
    def from_ordinal(cls, ordinal: int|str) -> 'Cause':
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
            if ordinal == 1:
                return Cause.UNKNOWN_CAUSE
            elif ordinal == 2:
                return Cause.OTHER_CAUSE
            elif ordinal == 3:
                return Cause.TECHNICAL_PROBLEM
            elif ordinal == 4:
                return Cause.STRIKE
            elif ordinal == 5:
                return Cause.DEMONSTRATION
            elif ordinal == 6:
                return Cause.ACCIDENT
            elif ordinal == 7:
                return Cause.HOLIDAY
            elif ordinal == 8:
                return Cause.WEATHER
            elif ordinal == 9:
                return Cause.MAINTENANCE
            elif ordinal == 10:
                return Cause.CONSTRUCTION
            elif ordinal == 11:
                return Cause.POLICE_ACTIVITY
            elif ordinal == 12:
                return Cause.MEDICAL_EMERGENCY
            raise ValueError("Ordinal not found in enum")
        else:
            raise ValueError("Ordinal must be an integer or a string representation of an integer")

    @classmethod
    def to_ordinal(cls, member: 'Cause') -> int:
        """
        Get enum ordinal

        Args:
            member (Cause): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        
        if member == Cause.UNKNOWN_CAUSE:
            return 1
        if member == Cause.OTHER_CAUSE:
            return 2
        if member == Cause.TECHNICAL_PROBLEM:
            return 3
        if member == Cause.STRIKE:
            return 4
        if member == Cause.DEMONSTRATION:
            return 5
        if member == Cause.ACCIDENT:
            return 6
        if member == Cause.HOLIDAY:
            return 7
        if member == Cause.WEATHER:
            return 8
        if member == Cause.MAINTENANCE:
            return 9
        if member == Cause.CONSTRUCTION:
            return 10
        if member == Cause.POLICE_ACTIVITY:
            return 11
        if member == Cause.MEDICAL_EMERGENCY:
            return 12
        raise ValueError("Member not found in enum")