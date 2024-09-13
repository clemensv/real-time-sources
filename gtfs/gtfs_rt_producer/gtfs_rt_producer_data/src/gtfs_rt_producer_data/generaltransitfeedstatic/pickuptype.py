from enum import Enum

_PickupType_members = []

class PickupType(Enum):
    """
    Indicates pickup method. Symbols: REGULAR - Regularly scheduled pickup; NO_PICKUP - No pickup available; PHONE_AGENCY - Must phone agency to arrange pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange pickup.
    """
    REGULAR = 'REGULAR'
    NO_PICKUP = 'NO_PICKUP'
    PHONE_AGENCY = 'PHONE_AGENCY'
    COORDINATE_WITH_DRIVER = 'COORDINATE_WITH_DRIVER'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'PickupType':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _PickupType_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if not _PickupType_members:
            _PickupType_members = list(cls)
        if 0 <= int(ordinal) < len(_PickupType_members):
            return _PickupType_members[ordinal]
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
        # pylint: disable=global-statement
        global _PickupType_members
        # pylint: enable=global-statement

        if not _PickupType_members:
            _PickupType_members = list(cls)
        return _PickupType_members.index(member)

_PickupType_members = list(PickupType)