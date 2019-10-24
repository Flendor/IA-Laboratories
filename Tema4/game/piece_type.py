from enum import Enum, unique, auto


@unique
class PiecesTypes(Enum):
    NORMAL = auto()
    KING = auto()
