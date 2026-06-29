from enum import Enum


class DirEnum(Enum):
    """
    Route direction of the trip as a string, either `1` or `2`. Relative to GTFS it is offset by one (HFP `1` = GTFS `0`, HFP `2` = GTFS `1`).
    """
    VALUE_1 = '1'
    VALUE_2 = '2'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'DirEnum':
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
    def to_ordinal(cls, member: 'DirEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (DirEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)