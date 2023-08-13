from cmath import sqrt
from dataclasses import dataclass

@dataclass
class Pos:
    x: int
    y: int
    
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.id: int = -1
    
    def is_empty(self) -> bool:
        return self.id == -1
    
    def set_tile_id(self, id: int) -> None:
        self.id = id
        
    def get_symbol(id: int) -> str:
        if (id == -1):
            return " "
        else:
            return "o"
        
    def get_debug_symbol(id: int) -> str:
        if (id == -1):
            return "•"
        else:
            return str(id)
        
    def __add__(self, other: 'Pos'):
        return Pos(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Pos'):
        return Pos(self.x - other.x, self.y - other.y)
    
    def distance_from(self, other: 'Pos') -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2).real
    
    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)
    
    def __lt__(self, other: 'Pos') -> bool:
        return self.magnitude() < other.magnitude()
    
    def __gt__(self, other: 'Pos') -> bool:
        return self.magnitude() > other.magnitude()
    
    def is_negative(self) -> bool:
        return self.x < 0 or self.y < 0
                   