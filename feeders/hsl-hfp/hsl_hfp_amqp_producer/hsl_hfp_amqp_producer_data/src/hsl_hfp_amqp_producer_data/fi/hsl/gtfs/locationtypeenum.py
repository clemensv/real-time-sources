from enum import IntEnum


class LocationTypeenum(IntEnum):
    """
    Type of the location. `0` (or empty) = stop / platform, `1` = station, `2` = station entrance / exit, `3` = generic node, `4` = boarding area. Sourced from the `location_type` field of `stops.txt`.
    """
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'LocationTypeenum':
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
    def to_ordinal(cls, member: 'LocationTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (LocationTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)