from enum import Enum


class SpacecraftEnum(Enum):
    """
    Stable channel identifier for the source spacecraft at L1. **Synthesized by the bridge — not present in the upstream payload.** Set to `dscovr` for the operational primary, `ace` for the backup. Used as the CloudEvent `subject`, the Kafka partition key, the MQTT topic `{spacecraft}` segment, the AMQP message subject, and the AMQP `x-opt-partition-key` message annotation. SWPC does not currently disclose source spacecraft per row in the propagated-solar-wind feed; the bridge sets `dscovr` by default and exposes a configuration override for operators who know the active spacecraft has switched.
    """
    dscovr = 'dscovr'
    ace = 'ace'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'SpacecraftEnum':
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
    def to_ordinal(cls, member: 'SpacecraftEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (SpacecraftEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)