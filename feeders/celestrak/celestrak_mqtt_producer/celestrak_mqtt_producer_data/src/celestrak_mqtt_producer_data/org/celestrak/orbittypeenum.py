from enum import Enum


class OrbitTypeEnum(Enum):
    """
    Orbit type: `ORB` orbiting, `LAN` landing, `IMP` impact, `DOC` docked to another catalogued object, `R/T` roundtrip. From the SATCAT `ORBIT_TYPE` field.
    """
    ORB = 'ORB'
    LAN = 'LAN'
    IMP = 'IMP'
    DOC = 'DOC'
    R_SLASHT = 'R/T'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'OrbitTypeEnum':
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
    def to_ordinal(cls, member: 'OrbitTypeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (OrbitTypeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)