"""
This file contains the Board class, which is used to represent the board of the game.
"""

from random import shuffle, uniform, seed
from constants import BOARD_AVAILABLE_SIZE, MAX_BOARD_SIZE

from drawer import BoardDrawer
from position import Position
from tile import QuantumTile, QuantumTileMaker, Socket, Tile, State

RANDOM_MULTIPLIER = 0.001
seed()


class Board:
    """Represents the board of the game."""

    def __init__(self, size: int) -> None:
        self.available_size: int = size
        self.center = Position(size // 2, size // 2)
        self.max_board_size = MAX_BOARD_SIZE

        self.tiles: list[Tile] = []

        self.list_of_sockets: list[Socket] = []

    def get_sorted_positions(self) -> list[Position]:
        """Get a list of positions sorted by their distance from the center."""
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
        """Draw the board on the terminal."""
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
        """Get the bitmask of the board."""
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
        """Calculate the weight of a position."""
        random_pos_delta = Position(
            uniform(-1, 1) * RANDOM_MULTIPLIER, uniform(-1, 1) * RANDOM_MULTIPLIER
        )
        jittered_position = position + random_pos_delta

        return jittered_position.distance_from(self.center)

    def tile_collides_with_board(self, tile: Tile) -> bool:
        """Check if the tile collides with the board."""
        board_mask = self.get_board_bit_mask()
        tile_mask = tile.get_bit_mask(self.available_size)
        return (board_mask | tile_mask) - tile_mask != board_mask

    def placing_tile_exceeds_max_size(self, tile: Tile) -> bool:
        """Check if placing the tile exceeds the max board size."""
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


if __name__ == "__main__":
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
