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

from drawer import BoardDrawer
from position import Pos

def bin(num: int) -> str:
    bin_length = (board_size * 2 + 1)**2 + 2
    return format(num, f'#0{bin_length}b')

def collides(tile: int, board_mask: int) -> bool:
    # Or operation sets all bits that are set in either the tile or the board_mask
    # Minus operation removes the tile bits from the board_mask
    # If there is no collision, we should get the board_mask back
    # otherwise, there is a collision
    return (board_mask | tile) - tile != board_mask
    
class Board:
    def __init__(self, size: int) -> None: 
        self.size: int = size
        self.positions: list[Pos] = []       
        self.generate_positions()

    def generate_positions(self):
        self.positions.clear()
        for x in range(-self.size, self.size+1):
            for y in range(-self.size, self.size+1):
                self.positions.append(Pos(x, y))

    def get_sorted_positions(self) -> list[Pos]:
        sorted_positions = self.positions.copy()
        sorted_positions.sort(key=lambda pos: pos.calculate_weight())
        return sorted_positions
        
    def __str__(self) -> str:
        drawer = BoardDrawer(self)
        drawer.debug = False        
        return str(drawer)
    
   
    def get_id(self, x: int, y: int) -> int:
        if (x < -self.size or x > self.size or y < -self.size or y > self.size):
            return -1        
        
        board_size = int(self.size * 2 + 1)
        return self.positions[ (x+self.size)*board_size + (y + self.size) ].id
    
    def get_board_bit_mask(self) -> int:
        mask = 0
        for pos in self.positions:
            if (pos.is_empty()):
                continue
            # Set the bit to one at the specified position
            bit_position = (pos.x + self.size) * (self.size * 2 + 1) + (pos.y + self.size)
            mask |= 1 << bit_position
        return mask

board_size = 1
board = Board(board_size)
board.generate_positions()


tile_no_collision = 0b100100000
tile_collision = 0b110000000
board_mask = board.get_board_bit_mask()

tile = tile_no_collision


print(bin(tile))
print(bin(board_mask))

print("Collision" if collides(tile, board_mask) else "No collision")

print(board)