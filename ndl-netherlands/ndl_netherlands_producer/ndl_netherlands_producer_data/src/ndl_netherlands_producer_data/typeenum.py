from enum import Enum


class TypeEnum(Enum):
    """
    The dimension being priced. OCPI TariffDimensionType enum: ENERGY (per kWh, step_size in Wh), FLAT (one-time fee, step_size ignored), PARKING_TIME (idle time per hour, step_size in seconds), TIME (charging time per hour, step_size in seconds).
    """
    ENERGY = 'ENERGY'
    FLAT = 'FLAT'
    PARKING_TIME = 'PARKING_TIME'
    TIME = 'TIME'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TypeEnum':
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
    def to_ordinal(cls, member: 'TypeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (TypeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)