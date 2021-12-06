from enum import Enum



class BlockType(Enum):
    EMPTY = ' '
    WALL = '#'
    CHEST = '$'
    GOAL = '.'
    PLAYER = '@'
    CHEST_ON_GOAL = 'V'
    PLAYER_ON_GOAL = 'O'


