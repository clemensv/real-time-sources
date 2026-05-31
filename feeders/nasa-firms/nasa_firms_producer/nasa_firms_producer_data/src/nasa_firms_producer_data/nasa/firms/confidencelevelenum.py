from enum import Enum


class ConfidenceLevelenum(Enum):
    """
    Sensor-normalised detection confidence as a routing-safe class: `low`, `nominal`, or `high`. Derived by the bridge: VIIRS `l`/`n`/`h` map directly; MODIS integer maps <30 → `low`, 30–80 → `nominal`, >80 → `high`. Used as an MQTT topic level so consumers can subscribe by confidence.
    """
    low = 'low'
    nominal = 'nominal'
    high = 'high'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ConfidenceLevelenum':
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
    def to_ordinal(cls, member: 'ConfidenceLevelenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ConfidenceLevelenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)