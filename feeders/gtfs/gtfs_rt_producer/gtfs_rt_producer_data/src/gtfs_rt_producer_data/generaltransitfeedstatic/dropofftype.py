from enum import Enum
_DropOffType_members = []

class DropOffType(Enum):
    """
    Indicates drop off method. Symbols: REGULAR - Regularly scheduled drop off; NO_DROP_OFF - No drop off available; PHONE_AGENCY - Must phone agency to arrange drop off; COORDINATE_WITH_DRIVER - Must coordinate with driver to arrange drop off.
    """
    REGULAR = 'REGULAR'
    NO_DROP_OFF = 'NO_DROP_OFF'
    PHONE_AGENCY = 'PHONE_AGENCY'
    COORDINATE_WITH_DRIVER = 'COORDINATE_WITH_DRIVER'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'DropOffType':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _DropOffType_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if not _DropOffType_members:
            _DropOffType_members = list(cls)
        if 0 <= int(ordinal) < len(_DropOffType_members):
            return _DropOffType_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'DropOffType') -> int:
        """
        Get enum ordinal

        Args:
            member (DropOffType): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _DropOffType_members
        # pylint: enable=global-statement
        
        if not _DropOffType_members:
            _DropOffType_members = list(cls)
        return _DropOffType_members.index(member)
_DropOffType_members = list(DropOffType)