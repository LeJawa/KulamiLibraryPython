from dataclasses import dataclass
from random import choice
from position import Pos

@dataclass
class Tile:
    positions: list[Pos]
    id: int     
    
    def get_bit_mask(self, mask_size) -> int:
        mask = 0
        for pos in self.positions:
            # Set the bit to one at the specified position
            bit_position = pos.x * mask_size + pos.y
            mask |= 1 << bit_position
        return mask
    
    def __str__(self) -> str:
        return f"Tile {self.id} at {self.positions}"
    
    def __repr__(self) -> str:
        return self.__str__()

class QuantumTile:
    next_id = -1
    
    def __init__(self, raw_positions: list[Pos], rotated_raw_positions: list[Pos] = []) -> None:
        self.raw_positions = raw_positions
        self.rotated_raw_positions = rotated_raw_positions
        self.id = QuantumTile.assign_id()
        self.has_rotation = False
        
        if (len(rotated_raw_positions) > 0):
            self.rotated_raw_positions = rotated_raw_positions
            self.has_rotation = True        
        
        self.positions = self.raw_positions.copy()
        self.rotated_positions = self.rotated_raw_positions.copy()
        
    def assign_id() -> int:
        QuantumTile.next_id += 1
        return QuantumTile.next_id
    
    def move_to(self, position: Pos) -> None:
        self.positions.clear()
        for pos in self.raw_positions:
            self.positions.append(pos + position)
            
        self.rotated_positions.clear()
        for pos in self.rotated_raw_positions:
            self.rotated_positions.append(pos + position)
            
    def get_possible_tiles_at(self, position: Pos) -> list[Tile]:
        self.move_to(position)
        
        tile_list: list[Tile] = []
        for raw_position in self.raw_positions:
            tile_positions = []
            out_of_bounds = False
            for pos in self.positions:
                possible_position = pos - raw_position
                if possible_position.is_negative():
                    out_of_bounds = True
                    continue
                
                tile_positions.append(possible_position)
            if not out_of_bounds:
                tile_list.append(Tile(tile_positions, self.id))
        
        if self.has_rotation:
            for rotated_raw_position in self.rotated_raw_positions:
                tile_positions = []
                out_of_bounds = False
                for pos in self.rotated_positions:
                    possible_position = pos - rotated_raw_position
                    if possible_position.is_negative():
                        out_of_bounds = True
                        continue
                    
                    tile_positions.append(possible_position)
                if not out_of_bounds:
                    tile_list.append(Tile(tile_positions, self.id))
            
        return tile_list
    
    def collapse(self) -> Tile:
        return self.collapse_at(Pos(0,0))
    
    def collapse_at(self, position: Pos) -> Tile:
        return choice(self.get_possible_tiles_at(position))

    

class QuantumTileMaker:
    def get1x1() -> QuantumTile:
        tile = QuantumTile([Pos(0,0)])
        return tile
    
    def get2x1() -> QuantumTile:
        tile = QuantumTile([Pos(0,0), Pos(1,0)], [Pos(0,0), Pos(0,1)])
        return tile
    
    def get3x1() -> QuantumTile:
        tile = QuantumTile([Pos(0,0), Pos(1,0), Pos(2,0)], [Pos(0,0), Pos(0,1), Pos(0,2)])
        return tile
    
    def get2x2() -> QuantumTile:
        tile = QuantumTile([Pos(0,0), Pos(1,0), Pos(0,1), Pos(1,1)])
        return tile
    
    def get3x2() -> QuantumTile:
        tile = QuantumTile([Pos(0,0), Pos(1,0), Pos(2,0), Pos(0,1), Pos(1,1), Pos(2,1)], [Pos(0,0), Pos(0,1), Pos(0,2), Pos(1,0), Pos(1,1), Pos(1,2)])
        return tile