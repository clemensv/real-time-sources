from enum import Enum


class StatusEnum(Enum):
    """
    Current status of the EVSE. OCPI Status enum: AVAILABLE (ready for new session), BLOCKED (physical barrier e.g. parked car), CHARGING (in use), INOPERATIVE (temporarily unavailable but not broken), OUTOFORDER (broken/defect), PLANNED (not yet active), REMOVED (discontinued), RESERVED (reserved for a specific driver), UNKNOWN (no status info available or offline).
    """
    AVAILABLE = 'AVAILABLE'
    BLOCKED = 'BLOCKED'
    CHARGING = 'CHARGING'
    INOPERATIVE = 'INOPERATIVE'
    OUTOFORDER = 'OUTOFORDER'
    PLANNED = 'PLANNED'
    REMOVED = 'REMOVED'
    RESERVED = 'RESERVED'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'StatusEnum':
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
    def to_ordinal(cls, member: 'StatusEnum') -> int:
        """
        Get enum ordinal

        Args:
            member (StatusEnum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)