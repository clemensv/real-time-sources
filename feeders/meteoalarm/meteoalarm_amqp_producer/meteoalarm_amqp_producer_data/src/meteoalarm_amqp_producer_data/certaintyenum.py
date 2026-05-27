from enum import Enum


class CertaintyEnum(Enum):
    """
    The CAP certainty level indicating the confidence in the forecast.
    """
    Observed = 'Observed'
    Likely = 'Likely'
    Possible = 'Possible'
    Unlikely = 'Unlikely'
    Unknown = 'Unknown'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'CertaintyEnum':
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
    def to_ordinal(cls, member: 'CertaintyEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (CertaintyEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)