from cmath import sqrt
from dataclasses import dataclass

class State:
    EMPTY = 0
    EMPTY_TILE = 1
    PLAYER1 = 2
    PLAYER2 = 3
    PLAYER1_LAST = 4
    PLAYER2_LAST = 5


@dataclass
class Pos:
    x: int
    y: int
    tile_id: int
    state: State    
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.state: State = State.EMPTY
        self.tile_id = -1
    
    def is_empty(self) -> bool:
        return self.state == State.EMPTY_TILE or self.state == State.EMPTY
    
    def set_tile_id(self, id: int) -> None:
        self.tile_id = id
        
    def __add__(self, other: 'Pos'):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Pos'):
        return Pos(self.x - other.x, self.y - other.y)
    
    def distance_from(self, other: 'Pos') -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2).real
    
    def is_negative(self) -> bool:
        return self.x < 0 or self.y < 0
                   