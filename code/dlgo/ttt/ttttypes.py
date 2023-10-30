import enum
from collections import namedtuple

__all__ = [
    'Player',
    'Point',
]

class Player(enum):
    x = 1
    o = 2

    @property
    def other(self):
        return Player.x if self == Player.o else Player.o


class Point(namedtuple('Point', 'row col')):
    def __deepcopy__(self, memodict={}):
        # These types are immutable, so we don't actually need to make a copy in memory
        return self