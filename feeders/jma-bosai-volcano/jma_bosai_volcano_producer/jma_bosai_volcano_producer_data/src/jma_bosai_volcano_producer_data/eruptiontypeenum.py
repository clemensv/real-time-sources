from enum import Enum


class EruptionTypeenum(Enum):
    """
    Normalized phenomenon name from JMA eruption observation bulletins. JMA documentation says the report carries the phenomenon name, with examples including eruption and continuous-eruption state changes; null means the live JSON item did not expose a recognizable phenomenon name.
    """
    ERUPTION = 'ERUPTION'
    EXPLOSION = 'EXPLOSION'
    CONTINUOUS_ERUPTION_CONTINUING = 'CONTINUOUS_ERUPTION_CONTINUING'
    CONTINUOUS_ERUPTION_STOPPED = 'CONTINUOUS_ERUPTION_STOPPED'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'EruptionTypeenum':
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
    def to_ordinal(cls, member: 'EruptionTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (EruptionTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)