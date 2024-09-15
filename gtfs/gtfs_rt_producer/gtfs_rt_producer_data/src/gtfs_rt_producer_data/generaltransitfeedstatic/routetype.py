from enum import Enum
_RouteType_members = []

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

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'RouteType':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _RouteType_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if not _RouteType_members:
            _RouteType_members = list(cls)
        if 0 <= int(ordinal) < len(_RouteType_members):
            return _RouteType_members[ordinal]
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
        # pylint: disable=global-statement
        global _RouteType_members
        # pylint: enable=global-statement
        
        if not _RouteType_members:
            _RouteType_members = list(cls)
        return _RouteType_members.index(member)
_RouteType_members = list(RouteType)