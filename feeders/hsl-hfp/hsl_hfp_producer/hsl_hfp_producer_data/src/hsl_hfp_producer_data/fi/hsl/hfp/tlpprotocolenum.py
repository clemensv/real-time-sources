from enum import Enum


class TlpProtocolEnum(Enum):
    """
    Protocol used for the traffic-light priority request: `MQTT` or `KAR-MQTT`. Populated on `tlr`. From the HFP payload `tlp-protocol` field. The `-` in `KAR-MQTT` is sanitized to the Avro symbol `KAR_MQTT` while the JSON wire value `KAR-MQTT` is preserved verbatim.
    """
    MQTT = 'MQTT'
    KAR_MINUSMQTT = 'KAR-MQTT'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'TlpProtocolEnum':
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
    def to_ordinal(cls, member: 'TlpProtocolEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (TlpProtocolEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)