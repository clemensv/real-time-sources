from enum import Enum
_ContinuousPickup_members = []

class ContinuousPickup(Enum):
    """
    Indicates that the rider can board the transit vehicle at any point along the vehicle’s travel path. Symbols: CONTINUOUS_STOPPING - Continuous stopping pickup; NO_CONTINUOUS_STOPPING - No continuous stopping pickup; PHONE_AGENCY - Must phone agency to arrange continuous stopping pickup; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange continuous stopping pickup.
    """
    CONTINUOUS_STOPPING = 'CONTINUOUS_STOPPING'
    NO_CONTINUOUS_STOPPING = 'NO_CONTINUOUS_STOPPING'
    PHONE_AGENCY = 'PHONE_AGENCY'
    COORDINATE_WITH_DRIVER = 'COORDINATE_WITH_DRIVER'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'ContinuousPickup':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _ContinuousPickup_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if not _ContinuousPickup_members:
            _ContinuousPickup_members = list(cls)
        if 0 <= int(ordinal) < len(_ContinuousPickup_members):
            return _ContinuousPickup_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'ContinuousPickup') -> int:
        """
        Get enum ordinal

        Args:
            member (ContinuousPickup): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _ContinuousPickup_members
        # pylint: enable=global-statement
        
        if not _ContinuousPickup_members:
            _ContinuousPickup_members = list(cls)
        return _ContinuousPickup_members.index(member)
_ContinuousPickup_members = list(ContinuousPickup)