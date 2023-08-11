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

board = Board(15)
board.generate_positions()


print(board)