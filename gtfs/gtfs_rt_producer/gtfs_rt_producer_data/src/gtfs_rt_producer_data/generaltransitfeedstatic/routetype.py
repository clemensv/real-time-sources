from enum import Enum

class RouteType(Enum):
    """
    Indicates the type of transportation used on a route. Symbols: TRAM - Tram, streetcar, light rail; SUBWAY - Subway, metro; RAIL - Intercity or long-distance travel; BUS - Short- and long-distance bus routes; FERRY - Boat service; CABLE_TRAM - Street-level rail cars with a cable running beneath the vehicle; AERIAL_LIFT - Cable transport with suspended cabins or chairs; FUNICULAR - Rail system designed for steep inclines; TROLLEYBUS - Electric buses with overhead wires; MONORAIL - Railway with a single rail or beam.
    """
    TRAM = 'TRAM'
    SUBWAY = 'SUBWAY'
    RAIL = 'RAIL'
    BUS = 'BUS'
    FERRY = 'FERRY'
    CABLE_TRAM = 'CABLE_TRAM'
    AERIAL_LIFT = 'AERIAL_LIFT'
    FUNICULAR = 'FUNICULAR'
    RESERVED_1 = 'RESERVED_1'
    RESERVED_2 = 'RESERVED_2'
    RESERVED_3 = 'RESERVED_3'
    TROLLEYBUS = 'TROLLEYBUS'
    MONORAIL = 'MONORAIL'
    OTHER = 'OTHER'

    __member_list = []

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'RouteType':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not cls.__member_list:
            cls.__member_list = list(cls)
        if 0 <= int(ordinal) < len(cls.__member_list):
            return cls.__member_list[int(ordinal)]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'RouteType') -> int:
        """
        Get enum ordinal

        Args:
            member (RouteType): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        if not cls.__member_list:
            cls.__member_list = list(cls)
        return cls.__member_list.index(member)