from enum import Enum


class DataStatusCodeEnum(Enum):
    """
    Data status code, present only when element data is unavailable: `NCE` no current elements, `NIE` no initial elements, `NEA` no elements available. Absent/null when elements are available. From the SATCAT `DATA_STATUS_CODE` field (upstream empty string is mapped to null).
    """
    NCE = 'NCE'
    NIE = 'NIE'
    NEA = 'NEA'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'DataStatusCodeEnum':
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
    def to_ordinal(cls, member: 'DataStatusCodeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (DataStatusCodeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)