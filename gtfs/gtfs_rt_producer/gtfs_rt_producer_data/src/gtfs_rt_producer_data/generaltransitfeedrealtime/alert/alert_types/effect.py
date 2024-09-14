from enum import Enum

class Effect(Enum):
    """
    What is the effect of this problem on the affected entity.
    """
    NO_SERVICE = 'NO_SERVICE'
    REDUCED_SERVICE = 'REDUCED_SERVICE'
    SIGNIFICANT_DELAYS = 'SIGNIFICANT_DELAYS'
    DETOUR = 'DETOUR'
    ADDITIONAL_SERVICE = 'ADDITIONAL_SERVICE'
    MODIFIED_SERVICE = 'MODIFIED_SERVICE'
    OTHER_EFFECT = 'OTHER_EFFECT'
    UNKNOWN_EFFECT = 'UNKNOWN_EFFECT'
    STOP_MOVED = 'STOP_MOVED'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'Effect':
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
                return Effect.NO_SERVICE
            elif ordinal == 2:
                return Effect.REDUCED_SERVICE
            elif ordinal == 3:
                return Effect.SIGNIFICANT_DELAYS
            elif ordinal == 4:
                return Effect.DETOUR
            elif ordinal == 5:
                return Effect.ADDITIONAL_SERVICE
            elif ordinal == 6:
                return Effect.MODIFIED_SERVICE
            elif ordinal == 7:
                return Effect.OTHER_EFFECT
            elif ordinal == 8:
                return Effect.UNKNOWN_EFFECT
            elif ordinal == 9:
                return Effect.STOP_MOVED
            raise ValueError("Ordinal not found in enum")
        else:
            raise ValueError("Ordinal must be an integer or a string representation of an integer")

    @classmethod
    def to_ordinal(cls, member: 'Effect') -> int:
        """
        Get enum ordinal

        Args:
            member (Effect): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        
        if member == Effect.NO_SERVICE:
            return 1
        if member == Effect.REDUCED_SERVICE:
            return 2
        if member == Effect.SIGNIFICANT_DELAYS:
            return 3
        if member == Effect.DETOUR:
            return 4
        if member == Effect.ADDITIONAL_SERVICE:
            return 5
        if member == Effect.MODIFIED_SERVICE:
            return 6
        if member == Effect.OTHER_EFFECT:
            return 7
        if member == Effect.UNKNOWN_EFFECT:
            return 8
        if member == Effect.STOP_MOVED:
            return 9
        raise ValueError("Member not found in enum")