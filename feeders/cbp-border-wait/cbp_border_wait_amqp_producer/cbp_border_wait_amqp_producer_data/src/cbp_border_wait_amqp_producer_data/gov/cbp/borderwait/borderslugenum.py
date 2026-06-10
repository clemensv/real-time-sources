from enum import Enum


class BorderSlugenum(Enum):
    """
    Lowercase kebab-case MQTT/UNS routing segment derived from the CBP border field. Expected values are canadian-border or mexican-border.
    """
    canadian_MINUSborder = 'canadian-border'
    mexican_MINUSborder = 'mexican-border'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'BorderSlugenum':
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
    def to_ordinal(cls, member: 'BorderSlugenum') -> int:
        """
        Get enum ordinal

        Args:
            member (BorderSlugenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)