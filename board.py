from random import shuffle, uniform, seed
from constants import BOARD_AVAILABLE_SIZE, MAX_BOARD_SIZE

random_multiplier = 0.001
seed()

from drawer import BoardDrawer
from position import Position
from tile import QuantumTile, QuantumTileMaker, Socket, Tile, State
    
class Board:
    def __init__(self, size: int) -> None: 
        self.available_size: int = size
        self.center = Position(size//2, size//2)
        self.max_board_size = MAX_BOARD_SIZE
        
        self.tiles: list[Tile] = []
        
        self.list_of_sockets: list[Socket] = []

    def get_sorted_positions(self) -> list[Position]:
        sorted_positions = []
        for x in range(self.available_size):
            for y in range(self.available_size):
                sorted_positions.append(Position(x, y))
        sorted_positions.sort(key=lambda position: self.calculate_weight(position))
        return sorted_positions
        
    def __str__(self) -> str:
        drawer = BoardDrawer(self)
        drawer.debug = False    
        drawer.show_axis = True
        return str(drawer)
    
    def draw(self) -> None:
        print(self)
        
    def get_socket_at(self, x: int, y: int) -> Socket:
        for tile in self.tiles:
            for socket in tile.sockets:
                if (socket.position.x == x and socket.position.y == y):
                    return socket
        
        return None
    
   
    def get_tile_id_at(self, x: int, y: int) -> int:
        if (x < 0 or x >= self.available_size or y < 0 or y >= self.available_size):
            return -1 # Out of bounds    
        
        for tile in self.tiles:
            for socket in tile.sockets:
                if (socket.position.x == x and socket.position.y == y):
                    return tile.id
        
        return -1 # No tile at position
    
    def get_board_bit_mask(self) -> int:
        mask = 0
        
        for tile in self.tiles:
            for socket in tile.sockets:
                # Set the bit to one at the specified position
                bit_position = socket.position.x * self.available_size + socket.position.y
                mask |= 1 << bit_position
        return mask
    
    def calculate_weight(self, position: Position) -> float:
        random_pos_delta = Position(uniform(-1,1)*random_multiplier, uniform(-1,1)*random_multiplier)
        jittered_position = position + random_pos_delta
        
        return jittered_position.distance_from(self.center)
    
    def tile_collides_with_board(self, tile: Tile) -> bool:
        board_mask = self.get_board_bit_mask()
        tile_mask = tile.get_bit_mask(self.available_size)
        return (board_mask | tile_mask) - tile_mask != board_mask
    
    def placing_tile_exceeds_max_size(self, tile: Tile) -> bool:
        min_x = self.available_size
        max_x = 0
        min_y = self.available_size
        max_y = 0
        
        for socket in tile.sockets:
            min_x = min(min_x, socket.position.x)
            max_x = max(max_x, socket.position.x)
            min_y = min(min_y, socket.position.y)
            max_y = max(max_y, socket.position.y)
        
        for tile in self.tiles:
            for socket in tile.sockets:
                min_x = min(min_x, socket.position.x)
                max_x = max(max_x, socket.position.x)
                min_y = min(min_y, socket.position.y)
                max_y = max(max_y, socket.position.y)
        
        if (max_x - min_x >= self.max_board_size or max_y - min_y >= self.max_board_size):
            return True
        else:
            return False
        
    
    def can_place_tile(self, tile: Tile) -> bool:
        if (self.tile_collides_with_board(tile)):
            return False
        
        if (self.placing_tile_exceeds_max_size(tile)):
            return False    

        return True
    
    def place_qtile(self, qtile: QuantumTile, position: Position) -> bool:
        possible_tiles = qtile.get_possible_tiles_at(position)
        
        shuffle(possible_tiles)
        
        for tile in possible_tiles:
            if (self.can_place_tile(tile)):
                self.tiles.append(tile)
                return True
            
        return False
    
    def initialize_occupied_positions(self) -> None:
        self.list_of_sockets.clear()
        for tile in self.tiles:
            for pos in tile.sockets:
                self.list_of_sockets.append(pos)
    
    def place_all_qtiles(self, bag_of_qtiles: list[QuantumTile]) -> bool:
        positions = self.get_sorted_positions()
        
        shuffle(bag_of_qtiles)
        for position in positions:
            for qtile in bag_of_qtiles:
                if (self.place_qtile(qtile, position)):
                    bag_of_qtiles.remove(qtile)
                    break
            
            if (len(bag_of_qtiles) == 0):
                self.initialize_occupied_positions()
                return True
        
        return False        

board = Board(BOARD_AVAILABLE_SIZE)

bag_of_qtiles = []

for _ in range(4):
    bag_of_qtiles.append(QuantumTileMaker.get2x1())
    bag_of_qtiles.append(QuantumTileMaker.get2x2())
    bag_of_qtiles.append(QuantumTileMaker.get3x1())
    bag_of_qtiles.append(QuantumTileMaker.get3x2())
bag_of_qtiles.append(QuantumTileMaker.get2x2())

board.place_all_qtiles(bag_of_qtiles)

board.list_of_sockets[4].state = State.PLAYER1
board.list_of_sockets[10].state = State.PLAYER2

board.draw()
