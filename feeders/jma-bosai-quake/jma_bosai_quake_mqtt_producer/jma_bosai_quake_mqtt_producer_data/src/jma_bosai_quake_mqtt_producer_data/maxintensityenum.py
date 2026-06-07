from enum import Enum


class MaxIntensityenum(Enum):
    """
    Maximum observed JMA seismic intensity for the report copied from list.json maxi or detail Body.Intensity.Observation.MaxInt. Null is emitted when the bulletin has no observed intensity summary, including 震度速報, 南海トラフ関連解説情報, and 顕著な地震の震源要素更新のお知らせ bulletins.
    """
    VALUE_1 = '1'
    VALUE_2 = '2'
    VALUE_3 = '3'
    VALUE_4 = '4'
    VALUE_5_MINUS = '5-'
    VALUE_5_PLUS = '5+'
    VALUE_6_MINUS = '6-'
    VALUE_6_PLUS = '6+'
    VALUE_7 = '7'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'MaxIntensityenum':
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
    def to_ordinal(cls, member: 'MaxIntensityenum') -> int:
        """
        Get enum ordinal

        Args:
            member (MaxIntensityenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)