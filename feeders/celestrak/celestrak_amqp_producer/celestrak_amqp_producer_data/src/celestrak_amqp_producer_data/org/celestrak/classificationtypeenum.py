from enum import Enum


class ClassificationTypeEnum(Enum):
    """
    Security classification of the element set: `U` unclassified, `C` classified, `S` secret. Public CelesTrak/Space-Track GP data is always `U`; supplemental operator data may carry `C`. From the CCSDS OMM `CLASSIFICATION_TYPE` keyword (GP `CLASSIFICATION_TYPE`).
    """
    U = 'U'
    C = 'C'
    S = 'S'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ClassificationTypeEnum':
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
    def to_ordinal(cls, member: 'ClassificationTypeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (ClassificationTypeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)