from enum import Enum


class SeverityEnum(Enum):
    """
    Japan-native severity axis for JMA warning MQTT topics: info for office reference records, advisory for 注意報-level notices and cancellations, warning for 警報-level warnings, and emergency for 特別警報/special-warning category codes.
    """
    info = 'info'
    advisory = 'advisory'
    warning = 'warning'
    emergency = 'emergency'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'SeverityEnum':
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
    def to_ordinal(cls, member: 'SeverityEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (SeverityEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)