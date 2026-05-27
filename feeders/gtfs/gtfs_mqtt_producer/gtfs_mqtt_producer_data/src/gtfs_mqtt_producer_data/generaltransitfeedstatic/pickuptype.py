from enum import Enum


class PickupType(Enum):
    """
    Indicates pickup method. Symbols: REGULAR - Regularly scheduled pickup; NO_PICKUP - No pickup available; PHONE_AGENCY - Must phone agency to arrange pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange pickup.
    """
    REGULAR = 'REGULAR'
    NO_PICKUP = 'NO_PICKUP'
    PHONE_AGENCY = 'PHONE_AGENCY'
    COORDINATE_WITH_DRIVER = 'COORDINATE_WITH_DRIVER'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'PickupType':
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
    def to_ordinal(cls, member: 'PickupType') -> int:
        """
        Get enum ordinal

        Args:
            member (PickupType): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)