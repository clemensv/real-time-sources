from enum import Enum


class StateNswHswEnum(Enum):
    """
    Categorical classification of the current water level against the highest navigable water level (HSW) reference for the reach, as computed by the upstream feed. Drives inland-shipping operational decisions (HSW = stop sign for commercial traffic). Note: upstream never emits 'low' on this series — HSW is an upper bound only. Omitted by upstream when the gauge has no HSW reference (treat absence as 'unknown').
    """
    normal = 'normal'
    high = 'high'
    unknown = 'unknown'
    commented = 'commented'
    out_dated = 'out-dated'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'StateNswHswEnum':
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
    def to_ordinal(cls, member: 'StateNswHswEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (StateNswHswEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)