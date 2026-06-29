from enum import Enum


class LocEnum(Enum):
    """
    Source of the reported vehicle location: `GPS` satellite fix; `ODO` computed from the odometer; `MAN` manually set; `DR` dead reckoning (used in tunnels and other GPS-denied locations); `N/A` location unavailable. From the HFP payload `loc` field.
    """
    GPS = 'GPS'
    ODO = 'ODO'
    MAN = 'MAN'
    DR = 'DR'
    N_SLASHA = 'N/A'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'LocEnum':
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
    def to_ordinal(cls, member: 'LocEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (LocEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)