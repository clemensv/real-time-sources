from enum import Enum


class ConditionEnum(Enum):
    """
    Normalized lifecycle condition derived from the Japanese JMA condition text. 発表 is mapped to ISSUED, 引上げ to RAISED, 引下げ to LOWERED, 継続 to CONTINUED, 切替 to SWITCHED, and 解除 to CANCELLED so downstream consumers can compare reports without parsing Japanese status labels.
    """
    ISSUED = 'ISSUED'
    RAISED = 'RAISED'
    LOWERED = 'LOWERED'
    CONTINUED = 'CONTINUED'
    SWITCHED = 'SWITCHED'
    CANCELLED = 'CANCELLED'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ConditionEnum':
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
    def to_ordinal(cls, member: 'ConditionEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (ConditionEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)