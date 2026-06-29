from enum import Enum


class TransportModeEnum(Enum):
    """
    Transport mode of the vehicle: `bus`, `tram`, `train`, `ferry`, `metro`, `ubus` (U-line bus) or `robot` (robot bus). From the MQTT-topic `transport_mode` level.
    """
    bus = 'bus'
    tram = 'tram'
    train = 'train'
    ferry = 'ferry'
    metro = 'metro'
    ubus = 'ubus'
    robot = 'robot'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TransportModeEnum':
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
    def to_ordinal(cls, member: 'TransportModeEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (TransportModeEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)