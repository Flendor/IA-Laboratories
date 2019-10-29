from enum import Enum, unique


@unique
class Directions(Enum):
    HUMAN = ((-1, 1), (-1, -1))
    BOT = ((1, 1), (1, -1))
    ALL = ((-1, 1), (-1, -1), (1, 1), (1, -1))
