from enum import Enum


class TariffTypeenum(Enum):
    """
    Type of tariff for distinguishing charging preferences. When omitted, valid for all sessions. OCPI TariffType enum: AD_HOC_PAYMENT (card terminal), PROFILE_CHEAP, PROFILE_FAST, PROFILE_GREEN, REGULAR (RFID or default).
    """
    AD_HOC_PAYMENT = 'AD_HOC_PAYMENT'
    PROFILE_CHEAP = 'PROFILE_CHEAP'
    PROFILE_FAST = 'PROFILE_FAST'
    PROFILE_GREEN = 'PROFILE_GREEN'
    REGULAR = 'REGULAR'
    None = 'None'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TariffTypeenum':
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
    def to_ordinal(cls, member: 'TariffTypeenum') -> int:
        """
        Get enum ordinal

        Args:
            member (TariffTypeenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)