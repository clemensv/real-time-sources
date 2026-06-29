from enum import IntEnum


class WheelchairBoardingenum(IntEnum):
    """
    Wheelchair accessibility of boarding at the stop. `0` (or empty) = no information, `1` = some accessible boarding, `2` = no accessible boarding. Sourced from the `wheelchair_boarding` field of `stops.txt`.
    """
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'WheelchairBoardingenum':
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
    def to_ordinal(cls, member: 'WheelchairBoardingenum') -> int:
        """
        Get enum ordinal

        Args:
            member (WheelchairBoardingenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)