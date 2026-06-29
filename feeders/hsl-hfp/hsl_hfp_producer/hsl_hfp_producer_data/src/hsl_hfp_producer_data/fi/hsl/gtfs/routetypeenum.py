from enum import IntEnum


class RouteTypeenum(IntEnum):
    """
    GTFS route type describing the transit mode used on the route. `0` = tram / light rail, `1` = subway / metro, `2` = rail, `3` = bus, `4` = ferry, `5` = cable tram, `6` = aerial lift, `7` = funicular, `11` = trolleybus, `12` = monorail. Sourced from the `route_type` field of `routes.txt`.
    """
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7
    VALUE_11 = 11
    VALUE_12 = 12

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'RouteTypeenum':
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
    def to_ordinal(cls, member: 'RouteTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (RouteTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)