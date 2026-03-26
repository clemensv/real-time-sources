from enum import Enum
_QualityLevel_members = []

class QualityLevel(Enum):
    """
    Quality Assurance/Quality Control level
    """
    Preliminary = 'Preliminary'
    Verified = 'Verified'

    @classmethod
    def from_ordinal(cls, ordinal: int|str) -> 'QualityLevel':
        """
        Get enum member by ordinal

        Args:
            ordinal (int| str): The ordinal of the enum member. This can be an integer or a string representation of an integer.

        Returns:
            The enum member corresponding to the ordinal.
        """
        # pylint: disable=global-statement
        global _QualityLevel_members
        # pylint: enable=global-statement

        if ordinal is None:
            raise ValueError("ordinal must not be None")
        if isinstance(ordinal, str) and ordinal.isdigit():
            ordinal = int(ordinal)
        if not _QualityLevel_members:
            _QualityLevel_members = list(cls)
        if 0 <= int(ordinal) < len(_QualityLevel_members):
            return _QualityLevel_members[ordinal]
        else:
            raise IndexError("Ordinal out of range for enum")

    @classmethod
    def to_ordinal(cls, member: 'QualityLevel') -> int:
        """
        Get enum ordinal

        Args:
            member (QualityLevel): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        # pylint: disable=global-statement
        global _QualityLevel_members
        # pylint: enable=global-statement
        
        if not _QualityLevel_members:
            _QualityLevel_members = list(cls)
        return _QualityLevel_members.index(member)
_QualityLevel_members = list(QualityLevel)