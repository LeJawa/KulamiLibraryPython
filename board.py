"""
This file contains the Board class, which is used to represent the board of the game.
"""

from random import shuffle, uniform, seed
from constants import BOARD_AVAILABLE_SIZE, MAX_BOARD_SIZE

from drawer import BoardDrawer
from enums import PlayerNumber, TileOwner
from position import Position
from tile import QuantumTile, QuantumTileMaker, Socket, Tile, SocketState

RANDOM_MULTIPLIER = 0.001
seed()


class Board:
    """
    Represents the board of the game.
    """

    def __init__(self, size: int) -> None:
        self.available_size: int = size
        self.center = Position(size // 2, size // 2)
        self.max_board_size = MAX_BOARD_SIZE

        self.tiles: list[Tile] = []

        self.list_of_sockets: list[Socket] = []

    def fit_to_max_board_size(self) -> None:
        """
        Fit the board to the max board size.
        """
        min_x = self.available_size
        min_y = self.available_size

        for socket in self.list_of_sockets:
            min_x = min(min_x, socket.position.x)
            min_y = min(min_y, socket.position.y)

        for socket in self.list_of_sockets:
            socket.position.x -= min_x
        self.available_size = self.max_board_size

        for socket in self.list_of_sockets:
            socket.position.y -= min_y
        self.available_size = self.max_board_size

    def get_sorted_positions(self) -> list[Position]:
        """
        Get a list of positions sorted by their distance from the center.
        """
        sorted_positions = []
        for x in range(self.available_size):
            for y in range(self.available_size):
                sorted_positions.append(Position(x, y))
        sorted_positions.sort(key=self.calculate_weight)
        return sorted_positions

    def __str__(self) -> str:
        drawer = BoardDrawer(self)
        drawer.debug = False
        drawer.show_axis = True
        return str(drawer)

    def draw(self) -> None:
        """
        Draw the board on the terminal.
        """
        print(self)

    def get_socket_at(self, x: int, y: int) -> Socket:
        """
        Get the socket at the specified position.
        Returns None if there is no socket at the specified position.
        """
        for tile in self.tiles:
            for socket in tile.sockets:
                if socket.position.x == x and socket.position.y == y:
                    return socket

        return None

    def get_tile_id_at(self, x: int, y: int) -> int:
        """
        Get the tile id at the specified position.
        Necessary for drawing the board.
        """
        if x < 0 or x >= self.available_size or y < 0 or y >= self.available_size:
            return -1  # Out of bounds

        for tile in self.tiles:
            for socket in tile.sockets:
                if socket.position.x == x and socket.position.y == y:
                    return tile.id

        return -1  # No tile at position

    def get_board_bit_mask(self) -> int:
        """
        Get the bitmask of the board.
        """
        mask = 0

        for tile in self.tiles:
            for socket in tile.sockets:
                # Set the bit to one at the specified position
                bit_position = (
                    socket.position.x * self.available_size + socket.position.y
                )
                mask |= 1 << bit_position
        return mask

    def calculate_weight(self, position: Position) -> float:
        """
        Calculate the weight of a position.
        """
        random_pos_delta = Position(
            uniform(-1, 1) * RANDOM_MULTIPLIER, uniform(-1, 1) * RANDOM_MULTIPLIER
        )
        jittered_position = position + random_pos_delta

        return jittered_position.distance_from(self.center)

    def tile_collides_with_board(self, tile: Tile) -> bool:
        """
        Check if the tile collides with the board.
        """
        board_mask = self.get_board_bit_mask()
        tile_mask = tile.get_bit_mask(self.available_size)
        return (board_mask | tile_mask) - tile_mask != board_mask

    def placing_tile_exceeds_max_size(self, tile: Tile) -> bool:
        """
        Check if placing the tile exceeds the max board size.
        """
        min_x = self.available_size
        max_x = 0
        min_y = self.available_size
        max_y = 0

        for socket in tile.sockets:
            min_x = min(min_x, socket.position.x)
            max_x = max(max_x, socket.position.x)
            min_y = min(min_y, socket.position.y)
            max_y = max(max_y, socket.position.y)

        for _tile in self.tiles:
            for socket in _tile.sockets:
                min_x = min(min_x, socket.position.x)
                max_x = max(max_x, socket.position.x)
                min_y = min(min_y, socket.position.y)
                max_y = max(max_y, socket.position.y)

        return (
            max_x - min_x >= self.max_board_size or max_y - min_y >= self.max_board_size
        )

    def can_place_tile(self, tile: Tile) -> bool:
        """Check if the tile can be placed on the board."""
        if self.tile_collides_with_board(tile):
            return False

        if self.placing_tile_exceeds_max_size(tile):
            return False

        return True

    def place_qtile(self, qtile: QuantumTile, position: Position) -> bool:
        """
        Place a quantum tile at the specified position.
        Placing the quantum tile means collapsing it into a tile.
        """
        possible_tiles = qtile.get_possible_tiles_at(position)

        shuffle(possible_tiles)

        for tile in possible_tiles:
            if self.can_place_tile(tile):
                self.tiles.append(tile)
                return True

        return False

    def initialize_list_of_sockets(self) -> None:
        """
        Initialize the list of all sockets on the board.
        """
        self.list_of_sockets.clear()
        for tile in self.tiles:
            for socket in tile.sockets:
                self.list_of_sockets.append(socket)

    def place_all_qtiles(self, qtiles: list[QuantumTile]) -> bool:
        """
        Place all the given quantum tiles on the board.
        Returns True if all the tiles were placed successfully.
        """
        positions = self.get_sorted_positions()

        shuffle(qtiles)
        for position in positions:
            for qtile in qtiles:
                if self.place_qtile(qtile, position):
                    qtiles.remove(qtile)
                    break

            if len(qtiles) == 0:
                self.initialize_list_of_sockets()
                return True

        return False

    @staticmethod
    def get_standard_bag_of_qtiles() -> list[QuantumTile]:
        """
        Get a standard bag of quantum tiles.
        The bag contains 4 of each 2x1, 3x1, 3x2 tiles and 5 2x2 tiles.
        """
        bag_of_qtiles = []

        for _ in range(4):
            bag_of_qtiles.append(QuantumTileMaker.get2x1())
            bag_of_qtiles.append(QuantumTileMaker.get2x2())
            bag_of_qtiles.append(QuantumTileMaker.get3x1())
            bag_of_qtiles.append(QuantumTileMaker.get3x2())
        bag_of_qtiles.append(QuantumTileMaker.get2x2())

        return bag_of_qtiles

    def initialize_standard_board(self) -> None:
        """
        Initialize the board with a standard bag of quantum tiles.
        """
        bag_of_qtiles = Board.get_standard_bag_of_qtiles()

        self.place_all_qtiles(bag_of_qtiles)

        self.fit_to_max_board_size()


class BoardInterface:
    """
    Interface for the board.
    """

    def __init__(self, _board: Board) -> None:
        self.board = _board

    def get_socket_state(self, position: Position) -> SocketState:
        """
        Get the state of the socket at the specified position.
        Returns State.OUT_OF_BOUNDS if the position is out of bounds.
        """
        socket = self.board.get_socket_at(position.x, position.y)
        if socket is None:
            return SocketState.OUT_OF_BOUNDS
        return socket.state

    def get_all_sockets(self) -> list[Socket]:
        """
        Get all the sockets on the board.
        """
        return self.board.list_of_sockets

    def get_all_tiles(self) -> list[Tile]:
        """
        Get all the tiles on the board.
        """
        return self.board.tiles

    def set_socket_state(self, socket: Socket, state: SocketState) -> bool:
        """
        Set the state of the socket at the specified position.
        Returns False if the position is out of bounds or the socket is not empty.
        """
        if socket is None:
            return False
        if socket.state != SocketState.EMPTY:
            return False
        socket.state = state
        return True

    def set_p1_marble_at_socket(self, socket: Socket) -> bool:
        """
        Changes the PLAYER1_LAST marble to PLAYER1 and
        sets the state of the specified socket to PLAYER1_LAST.
        """
        for _socket in self.board.list_of_sockets:
            if _socket.state == SocketState.PLAYER1_LAST:
                _socket.state = SocketState.PLAYER1
                break

        return self.set_socket_state(socket, SocketState.PLAYER1_LAST)

    def set_p2_marble_at_socket(self, socket: Socket) -> bool:
        """
        Changes the PLAYER2_LAST marble to PLAYER2 and
        sets the state of the specified socket to PLAYER2_LAST.
        """
        for _socket in self.board.list_of_sockets:
            if _socket.state == SocketState.PLAYER2_LAST:
                _socket.state = SocketState.PLAYER2
                break

        return self.set_socket_state(socket, SocketState.PLAYER2_LAST)

    def set_p1_marble_at_position(self, position: Position) -> bool:
        """
        Changes the PLAYER1_LAST marble to PLAYER1 and
        sets the state of the specified socket to PLAYER1_LAST.
        """
        socket = self.board.get_socket_at(position.x, position.y)
        return self.set_p1_marble_at_socket(socket)

    def set_p2_marble_at_position(self, position: Position) -> bool:
        """
        Changes the PLAYER2_LAST marble to PLAYER2 and
        sets the state of the specified socket to PLAYER2_LAST.
        """
        socket = self.board.get_socket_at(position.x, position.y)
        return self.set_p2_marble_at_socket(socket)

    def draw(self) -> None:
        """
        Draw the board on the terminal.
        """
        self.board.draw()

    def get_socket_at_position(self, position: Position) -> Socket:
        """
        Get the socket at the specified position.
        Returns None if there is no socket at the specified position.
        """
        return self.board.get_socket_at(position.x, position.y)


class VirtualBoard():
    """
    Class for making moves and calculating scores without affecting the actual board.
    """
    def __init__(self, interface: BoardInterface) -> None:
        self.board = interface
        
        self.moves_made: list[Position] = []
    
    
    def place_marble_at_position(self, position: Position, player: PlayerNumber) -> bool:
        """
        Place a marble at the specified position.
        """
        if player == PlayerNumber.ONE:
            if self.board.set_p1_marble_at_position(position):
                self.moves_made.append(position)
                return True
        else:
            if self.board.set_p2_marble_at_position(position):
                self.moves_made.append(position)
                return True
        
        return False
    
    def revert_last_move(self) -> None:
        """
        Revert the last move.
        """
        if len(self.moves_made) == 0:
            return
        
        position = self.moves_made.pop()
        socket = self.board.get_socket_at_position(position)
        socket.state = SocketState.EMPTY
        
    def revert_all_moves(self) -> None:
        """
        Revert all the moves.
        """
        while len(self.moves_made) > 0:
            self.revert_last_move()
    
    def __enter__(self) -> "VirtualBoard":
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.revert_all_moves()
        
        
     

# pylint: disable=too-few-public-methods
class BoardMaker:
    """
    Class for creating boards.
    """

    @staticmethod
    def get_standard_board() -> BoardInterface:
        """
        Get a standard board.
        """
        _board = Board(BOARD_AVAILABLE_SIZE)
        _board.initialize_standard_board()

        iboard = BoardInterface(_board)
        return iboard
    
    @staticmethod
    def get_very_small_board() -> BoardInterface:
        """
        Get a very small board.
        """
        _board = Board(8)
        _board.max_board_size = 5
        
        bag_of_qtiles = [QuantumTileMaker.get2x2() for _ in range(4)]
        _board.place_all_qtiles(bag_of_qtiles)
        _board.fit_to_max_board_size()

        iboard = BoardInterface(_board)
        return iboard

def get_scores(board: BoardInterface) -> tuple[int, int]:
    """Calculates the scores of the players"""
    player1_score = 0
    player2_score = 0

    for tile in board.get_all_tiles():
        owner = tile.get_owner()
        if owner == TileOwner.PLAYER1:
            player1_score += tile.get_points()
        elif owner == TileOwner.PLAYER2:
            player2_score += tile.get_points()

    return (player1_score, player2_score)


if __name__ == "__main__":
    board = BoardMaker.get_standard_board()

    board.draw()
