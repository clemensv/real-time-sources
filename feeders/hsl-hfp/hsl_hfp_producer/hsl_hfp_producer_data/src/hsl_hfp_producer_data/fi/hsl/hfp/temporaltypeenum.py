from enum import Enum


class TemporalTypeEnum(Enum):
    """
    Journey temporal type: `ongoing` (journey currently in progress) or `upcoming` (journey about to start, within ~30 minutes). From the MQTT-topic `temporal_type` level.
    """
    ongoing = 'ongoing'
    upcoming = 'upcoming'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TemporalTypeEnum':
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
    def to_ordinal(cls, member: 'TemporalTypeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (TemporalTypeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)