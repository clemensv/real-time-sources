from enum import Enum


class StateMnwMhwEnum(Enum):
    """
    Categorical classification of the current water level against the gauge's long-term mean low water (MNW) and mean high water (MHW) reference values, as computed by the upstream feed. Omitted by upstream when the gauge has no MNW/MHW reference series configured (treat absence as 'unknown').
    """
    low = 'low'
    normal = 'normal'
    high = 'high'
    unknown = 'unknown'
    commented = 'commented'
    out_dated = 'out-dated'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'StateMnwMhwEnum':
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
    def to_ordinal(cls, member: 'StateMnwMhwEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (StateMnwMhwEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)