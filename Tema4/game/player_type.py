from enum import Enum, unique, auto


@unique
class PlayerTypes(Enum):
    HUMAN = auto()
    BOT = auto()
