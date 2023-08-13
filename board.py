### Board generation steps
# Iterate over all position from -n to n in both x and y
# For each position, calculate the weight of the position
#  - The weight is the distance from (0,0)
# Order the positions by weight in ascending order
# Shuffle the tiles
# While not all tiles are placed and there are still positions left
#  - Try to place the next tile in the position with the lowest weight
#    - Check all possible rotations and translations
#  - If a tile can be placed, place it and remove the position from the list
#  - If a tile cannot be placed, try the next tile

from math import cos
from random import shuffle, uniform, choice
import random
from bitmasking import check_collision
from constants import BOARD_SIZE

random_multiplier = 0.001
random.seed(6)

from drawer import BoardDrawer
from position import Pos
from tile import QuantumTile, QuantumTileMaker, Tile


    
class Board:
    def __init__(self, size: int) -> None: 
        self.size: int = size
        self.center = Pos(size//2, size//2)
        
        self.positions: list[Pos] = []       
        self.generate_positions()
        
        self.tiles: list[Tile] = []

    def generate_positions(self):
        self.positions.clear()
        for x in range(self.size):
            for y in range(self.size):
                self.positions.append(Pos(x, y))

    def get_sorted_positions(self) -> list[Pos]:
        sorted_positions = self.positions.copy()
        sorted_positions.sort(key=lambda position: self.calculate_weight(position))
        return sorted_positions
        
    def __str__(self) -> str:
        drawer = BoardDrawer(self)
        drawer.debug = True        
        return str(drawer)
    
    def draw(self) -> None:
        print(self)
    
   
    def get_id(self, x: int, y: int) -> int:
        if (x < 0 or x >= self.size or y < 0 or y >= self.size):
            return -1        
        
        board_size = self.size
        return self.positions[ x*board_size + y ].id
    
    def get_board_bit_mask(self) -> int:
        mask = 0
        for pos in self.positions:
            if (pos.is_empty()):
                continue
            # Set the bit to one at the specified position
            bit_position = pos.x * self.size + pos.y
            mask |= 1 << bit_position
        return mask
    
    def calculate_weight(self, position: Pos) -> float:
        random_pos_delta = Pos(uniform(-1,1)*random_multiplier, uniform(-1,1)*random_multiplier)
        jittered_position = position + random_pos_delta
        
        return jittered_position.distance_from(self.center)
    
    def fill(self) -> None:
        for pos in self.positions:
            distance = pos.distance_from(self.center)
            chance = cos(distance / ((self.size-1)/2) * 3.14/2)
            
            if (uniform(0,1) < chance):
                pos.set_tile_id(choice([1,1,2]))
    
    def can_place_tile(self, tile: Tile) -> bool:
        board_mask = self.get_board_bit_mask()
        tile_mask = tile.get_bit_mask(BOARD_SIZE)
        return (board_mask | tile_mask) - tile_mask == board_mask
    
    def place_qtile(self, qtile: QuantumTile, position: Pos) -> bool:
        possible_tiles = qtile.get_possible_tiles_at(position)
        
        shuffle(possible_tiles)
        
        for tile in possible_tiles:
            if (self.can_place_tile(tile)):
                self.tiles.append(tile)
                return True
            
        return False
        
        
            
        

board = Board(BOARD_SIZE)
board.generate_positions()
board.fill()

qtile = QuantumTileMaker.get2x1()
qtile2 = QuantumTileMaker.get2x2()

tile = qtile.collapse_at(Pos(0,1))

print(board.place_qtile(qtile, Pos(0,1)))
print(board.place_qtile(qtile2, Pos(3,3)))


check_collision(tile.get_bit_mask(BOARD_SIZE), board.get_board_bit_mask(), BOARD_SIZE**2)

print(board.tiles)

print(board)
