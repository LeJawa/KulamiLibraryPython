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
from random import uniform
import random

random_multiplier = 0.001
# random.seed(0)

from drawer import BoardDrawer
from position import Pos
from tile import Tile, TileMaker

def bin(num: int) -> str:
    bin_length = board_size**2 + 2
    return format(num, f'#0{bin_length}b')

def collides(tile: int, board_mask: int) -> bool:
    # Or operation sets all bits that are set in either the tile or the board_mask
    # Minus operation removes the tile bits from the board_mask
    # If there is no collision, we should get the board_mask back
    # otherwise, there is a collision
    return (board_mask | tile) - tile != board_mask


CRED = '\033[91m'
CGREEN  = '\33[32m'
CEND = '\033[0m'

def check_collision(board: 'Board', tile: Tile, rotated: bool = False) -> bool:
    board_mask = board.get_board_bit_mask()
    tile_mask = tile.get_bit_mask(rotated)

    tile_mask_str = bin(tile_mask)
    colored_tile_mask_str = ""
    for i in range(len(tile_mask_str)):
        if (tile_mask_str[i] == "1"):
            if (tile_mask_str[i] == bin(board_mask)[i]):
                colored_tile_mask_str += CRED + tile_mask_str[i] + CEND
            else:
                colored_tile_mask_str += CGREEN + tile_mask_str[i] + CEND
        else:
            colored_tile_mask_str += tile_mask_str[i]
    
    
    print(colored_tile_mask_str)
    print(bin(board_mask))

    print("Collision" if collides(tile_mask, board_mask) else "No collision")

    print(board)
    
    return collides(tile_mask, board_mask)
    
class Board:
    def __init__(self, size: int) -> None: 
        self.size: int = size
        self.center = Pos(size//2, size//2)
        
        self.positions: list[Pos] = []       
        self.generate_positions()

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
        # uniform(-1,1)*random_multiplier is used to add a small random value to the weight
        pos_delta = Pos(uniform(-1,1)*random_multiplier, uniform(-1,1)*random_multiplier)
        position += pos_delta
        
        return position.distance_from(self.center)
    
    def fill(self) -> None:
        for pos in self.positions:
            distance = pos.distance_from(self.center)
            chance = cos(distance / ((self.size-1)/2) * 3.14/2)
            
            if (uniform(0,1) < chance):
                pos.set_tile_id(1)
            
        

board_size = 7
board = Board(board_size)
board.generate_positions()
board.fill()

tile = TileMaker.get2x1()
tile.move_to(Pos(2,2))


check_collision(board, tile, True)
