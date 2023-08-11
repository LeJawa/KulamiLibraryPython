from math import cos, radians, sin
from position import Pos


class Tile:
    next_id = -1
    
    def __init__(self, raw_positions: list[Pos]) -> None:
        self.raw_positions = raw_positions
        self.positions = raw_positions.copy()
        self.id = Tile.assign_id()
        
    def assign_id() -> int:
        Tile.next_id += 1
        return Tile.next_id
    
    def rotate(self, angle: int) -> list[Pos]:
        rotated_positions: list[Pos] = []
        angle_in_radians = radians(angle)
        for pos in self.raw_positions:
            new_x, new_y = round(pos.x * cos(angle_in_radians) - pos.y * sin(angle_in_radians)), round(pos.x * sin(angle_in_radians) + pos.y * cos(angle_in_radians))
            rotated_positions.append(Pos(new_x, new_y))
        
        return rotated_positions
    