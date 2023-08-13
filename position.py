from dataclasses import dataclass
from math import sqrt
from random import uniform, choice
import random

random_multiplier = 0.001
random.seed(0)

@dataclass
class Pos:
    x: int
    y: int
    
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.id: int = -1
        
        self.id = choice([-1,1,2,-1,-1,1,2,3,1,-1])
        

    def calculate_weight(self) -> float:
        return sqrt((self.x + uniform(-1,1)*random_multiplier)**2 + (self.y + uniform(-1,1)*random_multiplier)**2)
    
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
                   