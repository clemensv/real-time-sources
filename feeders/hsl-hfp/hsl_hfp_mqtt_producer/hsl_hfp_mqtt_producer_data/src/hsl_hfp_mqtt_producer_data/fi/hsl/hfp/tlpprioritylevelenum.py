from enum import Enum


class TlpPriorityLevelEnum(Enum):
    """
    Priority level of the traffic-light priority request: `normal`, `high` or `norequest` (no request sent). From the HFP payload `tlp-prioritylevel` field.
    """
    normal = 'normal'
    high = 'high'
    norequest = 'norequest'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TlpPriorityLevelEnum':
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
    def to_ordinal(cls, member: 'TlpPriorityLevelEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (TlpPriorityLevelEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)