from enum import Enum


class PowerTypeenum(Enum):
    """
    Power type delivered by this connector. OCPI PowerType enum: AC_1_PHASE, AC_2_PHASE, AC_2_PHASE_SPLIT, AC_3_PHASE, DC.
    """
    AC_1_PHASE = 'AC_1_PHASE'
    AC_2_PHASE = 'AC_2_PHASE'
    AC_2_PHASE_SPLIT = 'AC_2_PHASE_SPLIT'
    AC_3_PHASE = 'AC_3_PHASE'
    DC = 'DC'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'PowerTypeenum':
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
    def to_ordinal(cls, member: 'PowerTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (PowerTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)