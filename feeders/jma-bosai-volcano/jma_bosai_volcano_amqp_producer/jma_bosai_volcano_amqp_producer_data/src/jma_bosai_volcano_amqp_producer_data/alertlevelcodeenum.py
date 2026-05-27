from enum import Enum


class AlertLevelCodeenum(Enum):
    """
    JMA volcanic warning code from warning.json. Enum symbols CODE_02, CODE_03, CODE_04, CODE_11, CODE_12, CODE_13, CODE_22, CODE_23, CODE_36, CODE_43, CODE_44, CODE_45, and CODE_49 correspond via altenums.json to observed live JMA wire codes 02, 03, 04, 11, 12, 13, 22, 23, 36, 43, 44, 45, and 49. JMA explains eruption alert levels as indicators combining volcanic activity state, area requiring caution, and expected disaster-prevention actions. Labels for CODE_11/CODE_12/CODE_13 are from JMA eruption alert level guidance; CODE_22/CODE_23/CODE_36 are target-volcano warning labels observed in live warning.json; CODE_02/CODE_03/CODE_04/CODE_43/CODE_44/CODE_45/CODE_49 labels are taken from live warning.json item name fields because the Bosai JSON feed publishes those public JMA labels directly.
    """
    CODE_02 = 'CODE_02'
    CODE_03 = 'CODE_03'
    CODE_04 = 'CODE_04'
    CODE_11 = 'CODE_11'
    CODE_12 = 'CODE_12'
    CODE_13 = 'CODE_13'
    CODE_22 = 'CODE_22'
    CODE_23 = 'CODE_23'
    CODE_36 = 'CODE_36'
    CODE_43 = 'CODE_43'
    CODE_44 = 'CODE_44'
    CODE_45 = 'CODE_45'
    CODE_49 = 'CODE_49'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'AlertLevelCodeenum':
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
    def to_ordinal(cls, member: 'AlertLevelCodeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (AlertLevelCodeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)