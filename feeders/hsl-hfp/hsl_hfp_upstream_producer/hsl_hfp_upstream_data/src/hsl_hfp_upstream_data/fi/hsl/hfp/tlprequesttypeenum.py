from enum import Enum


class TlpRequestTypeEnum(Enum):
    """
    Type of the traffic-light priority request: `NORMAL`, `DOOR_CLOSE`, `DOOR_OPEN` or `ADVANCE`. From the HFP payload `tlp-requesttype` field.
    """
    NORMAL = 'NORMAL'
    DOOR_CLOSE = 'DOOR_CLOSE'
    DOOR_OPEN = 'DOOR_OPEN'
    ADVANCE = 'ADVANCE'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TlpRequestTypeEnum':
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
    def to_ordinal(cls, member: 'TlpRequestTypeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (TlpRequestTypeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)