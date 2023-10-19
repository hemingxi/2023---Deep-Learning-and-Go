# [?] not sure what these tags do
# tag::enumimport[] 
import enum
# end::enumimport[]

class Player(enum.Enum):
    black = 1
    white = 2

    @property # allows you to access this attribute without parenthesis
    def other(self):
        return Player.black if self == Player.white else Player.white
    

from collections import namedtuple

class Point(namedtuple('Point', 'row col')):
    # create a namedtuple for better readability - so you can refer to points by point.row and point.column
    # the class "Point" inherits from the namedtuple class, defined with the name of "Point", and the two items named as "row" and "col"
    def neighbors(self):
        return [
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col), 
            Point(self.row, self.col - 1),
            Point(self.row, self.col + 1)
        ]
    
