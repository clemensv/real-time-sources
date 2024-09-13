from enum import Enum

_Effect_members = []

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
        # pylint: disable=global-statement
        global _Effect_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _Effect_members:
            _Effect_members = list(cls)
        if 0 <= int(ordinal) < len(_Effect_members):
            return _Effect_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'Effect') -> int:
        """
        Get enum ordinal

        Args:
            member (Effect): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _Effect_members
        # pylint: enable=global-statement

        if not _Effect_members:
            _Effect_members = list(cls)
        return _Effect_members.index(member)

_Effect_members = list(Effect)