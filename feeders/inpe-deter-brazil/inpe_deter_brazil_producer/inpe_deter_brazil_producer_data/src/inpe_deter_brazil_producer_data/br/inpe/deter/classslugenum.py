from enum import Enum


class ClassSlugenum(Enum):
    """
    Lowercase-kebab normalized DETER class used as a topic-safe MQTT routing axis, e.g. desmatamento-cr, degradacao, mineracao.
    """
    desmatamento_MINUScr = 'desmatamento-cr'
    desmatamento_MINUSveg = 'desmatamento-veg'
    degradacao = 'degradacao'
    mineracao = 'mineracao'
    cs_MINUSdesordenado = 'cs-desordenado'
    cs_MINUSgeometrico = 'cs-geometrico'
    cicatriz_MINUSde_MINUSqueimada = 'cicatriz-de-queimada'
    corte_MINUSseletivo = 'corte-seletivo'
    unknown = 'unknown'

    @classmethod
    def from_ordinal(cls, ordinal: int | str) -> 'ClassSlugenum':
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
    def to_ordinal(cls, member: 'ClassSlugenum') -> int:
        """
        Get enum ordinal

        Args:
            member (ClassSlugenum): The enum member to get the ordinal of.

        Returns:
            The ordinal of the enum member.
        """
        members = list(cls)
        return members.index(member)