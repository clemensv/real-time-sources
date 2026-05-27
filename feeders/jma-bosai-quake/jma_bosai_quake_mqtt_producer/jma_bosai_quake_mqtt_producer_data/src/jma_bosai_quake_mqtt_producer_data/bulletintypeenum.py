from enum import Enum


class BulletinTypeenum(Enum):
    """
    JMA detail bulletin product code parsed from the detail JSON filename. Supported earthquake-related JMA Bosai codes are VXSE51 (震度速報), VXSE52 (震源に関する情報), VXSE53 (震源・震度に関する情報), VXSE5k (震源・震度情報 Bosai variant), VXSE61 (長周期地震動に関する観測情報), and VYSE52 (南海トラフ地震関連解説情報). Tsunami-specific VTSE products are deliberately not modeled by this source.
    """
    VXSE51 = 'VXSE51'
    VXSE52 = 'VXSE52'
    VXSE53 = 'VXSE53'
    VXSE5k = 'VXSE5k'
    VXSE61 = 'VXSE61'
    VYSE52 = 'VYSE52'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'BulletinTypeenum':
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
    def to_ordinal(cls, member: 'BulletinTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (BulletinTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)