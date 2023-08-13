from math import cos, radians, sin
from position import Pos


class Tile:
    mask_size = 3
    next_id = -1
    
    def __init__(self, raw_positions: list[Pos], rotated_raw_positions: list[Pos] = []) -> None:
        self.raw_positions = raw_positions
        self.rotated_raw_positions = rotated_raw_positions
        self.id = Tile.assign_id()
        self.has_rotation = False
        
        if (len(rotated_raw_positions) > 0):
            self.rotated_raw_positions = rotated_raw_positions
            self.has_rotation = True        
        
        self.positions = self.raw_positions.copy()
        self.rotated_positions = self.rotated_raw_positions.copy()
        
    def assign_id() -> int:
        Tile.next_id += 1
        return Tile.next_id
    
    @staticmethod
    def bit_mask(positions) -> int:
        mask = 0
        for pos in positions:
            # Set the bit to one at the specified position
            bit_position = pos.x * Tile.mask_size + pos.y
            mask |= 1 << bit_position
        return mask
    
    def get_bit_mask(self, rotated = False) -> int:
        if rotated and self.has_rotation:
            return self.bit_mask(self.rotated_positions)
        
        return self.bit_mask(self.positions)
    
    def move_to(self, position: Pos) -> None:
        self.positions.clear()
        for pos in self.raw_positions:
            self.positions.append(pos + position)
            
        self.rotated_positions.clear()
        for pos in self.rotated_raw_positions:
            self.rotated_positions.append(pos + position)
        
        
    

class TileMaker:
    def get1x1() -> Tile:
        tile = Tile([Pos(0,0)])
        return tile
    
    def get2x1() -> Tile:
        tile = Tile([Pos(0,0), Pos(1,0)], [Pos(0,0), Pos(0,1)])
        return tile