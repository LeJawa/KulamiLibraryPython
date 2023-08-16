"""
This file contains the Tile class, 
which is used to represent a tile on the board. 
It also contains the QuantumTile class, 
which is used to represent a tile that is in a superposition of states. 
The QuantumTileMaker class is used to create QuantumTiles of various sizes. 
"""

from dataclasses import dataclass
from enum import Enum
from random import choice
from position import Position


class SocketState(Enum):
    """Represents the state of a socket."""

    OUT_OF_BOUNDS = 0
    EMPTY = 1
    PLAYER1 = 2
    PLAYER2 = 3
    PLAYER1_LAST = 4
    PLAYER2_LAST = 5


@dataclass
class Socket:
    """Represents a socket on the board."""

    position: Position
    tile_id: int
    state: SocketState

    def __init__(self, position: Position):
        self.position = position
        self.state: SocketState = SocketState.EMPTY
        self.tile_id = -1

    def is_empty(self) -> bool:
        """Check if the socket is empty."""
        return self.state == SocketState.EMPTY

    def set_tile_id(self, _id: int) -> None:
        """Set the tile id the socket belongs to."""
        self.tile_id = _id


class TileOwner(Enum):
    """Represents the owner of a tile."""

    PLAYER1 = 1
    PLAYER2 = 2
    NONE = 3


@dataclass
class Tile:
    """Represents a tile on the board."""

    sockets: list[Socket]
    id: int

    def get_bit_mask(self, mask_size) -> int:
        """Get the bitmask of the tile."""
        mask = 0
        for socket in self.sockets:
            # Set the bit to one at the specified position
            bit_position = socket.position.x * mask_size + socket.position.y
            mask |= 1 << bit_position
        return mask

    def __str__(self) -> str:
        return f"Tile {self.id} at {self.sockets}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def get_owner(self) -> TileOwner:
        """Get the owner of the tile."""
        score = 0
        
        for socket in self.sockets:
            if socket.state == SocketState.PLAYER1:
                score += 1
            if socket.state == SocketState.PLAYER2:
                score -= 1
        
        if score > 0:
            return TileOwner.PLAYER1
        elif score < 0:
            return TileOwner.PLAYER2
        else:
            return TileOwner.NONE
    
    def get_points(self):
        return len(self.sockets)


class QuantumTile:
    """
    Represents a tile as a superposition of all the ways
    it could be placed at a specified position.
    """

    possible_ids = [
        *"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[{]}|;:'\""
    ]
    next_id_index = -1

    def __init__(
        self,
        raw_positions: list[Position],
        rotated_raw_positions: list[Position] = None,
    ) -> None:
        self.raw_positions = raw_positions
        self.id = QuantumTile.assign_id()

        if rotated_raw_positions is not None:
            self.rotated_raw_positions = rotated_raw_positions
            self.has_rotation = True
        else:
            self.rotated_raw_positions = []
            self.has_rotation = False

        self.positions = self.raw_positions.copy()
        self.rotated_positions = self.rotated_raw_positions.copy()

    @staticmethod
    def assign_id() -> int:
        """Assign a unique id to the tile."""
        QuantumTile.next_id_index += 1
        return QuantumTile.possible_ids[QuantumTile.next_id_index]

    def move_to(self, position: Position) -> None:
        """Move the tile to a specified position."""
        self.positions.clear()
        for pos in self.raw_positions:
            self.positions.append(pos + position)

        self.rotated_positions.clear()
        for pos in self.rotated_raw_positions:
            self.rotated_positions.append(pos + position)

    @staticmethod
    def get_tiles(
        raw_positions: list[Position], positions: list[Position], _id: int
    ) -> list[Tile]:
        """
        Get all the possible tiles at a specified position,
        given the raw and the real positions.
        """
        tile_list: list[Tile] = []
        for raw_position in raw_positions:
            tile_sockets: list[Socket] = []
            out_of_bounds = False
            for pos in positions:
                possible_position = pos - raw_position
                if possible_position.is_negative():
                    out_of_bounds = True
                    continue

                possible_socket = Socket(possible_position)

                possible_socket.set_tile_id(_id)
                possible_socket.state = SocketState.EMPTY

                tile_sockets.append(possible_socket)
            if not out_of_bounds:
                tile_list.append(Tile(tile_sockets, _id))
        return tile_list

    def get_possible_tiles_at(self, position: Position) -> list[Tile]:
        """Get all the possible tiles at a specified position."""
        self.move_to(position)

        tile_list: list[Tile] = []
        tile_list += QuantumTile.get_tiles(self.raw_positions, self.positions, self.id)
        tile_list += QuantumTile.get_tiles(
            self.rotated_raw_positions, self.rotated_positions, self.id
        )

        return tile_list

    def collapse(self) -> Tile:
        """Collapse the tile to be placed at (0,0). Not used in the game"""
        return self.collapse_at(Position(0, 0))

    def collapse_at(self, position: Position) -> Tile:
        """Collapse the tile to a single position. Not used in the game"""
        return choice(self.get_possible_tiles_at(position))


class QuantumTileMaker:
    """Class to create QuantumTiles of various sizes."""

    @staticmethod
    def get1x1() -> QuantumTile:
        """Get a 1x1 tile."""
        tile = QuantumTile([Position(0, 0)])
        return tile

    @staticmethod
    def get2x1() -> QuantumTile:
        """Get a 2x1 tile."""
        tile = QuantumTile(
            [Position(0, 0), Position(1, 0)], [Position(0, 0), Position(0, 1)]
        )
        return tile

    @staticmethod
    def get3x1() -> QuantumTile:
        """Get a 3x1 tile."""
        tile = QuantumTile(
            [Position(0, 0), Position(1, 0), Position(2, 0)],
            [Position(0, 0), Position(0, 1), Position(0, 2)],
        )
        return tile

    @staticmethod
    def get2x2() -> QuantumTile:
        """Get a 2x2 tile."""
        tile = QuantumTile(
            [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]
        )
        return tile

    @staticmethod
    def get3x2() -> QuantumTile:
        """Get a 3x2 tile."""
        tile = QuantumTile(
            [
                Position(0, 0),
                Position(1, 0),
                Position(2, 0),
                Position(0, 1),
                Position(1, 1),
                Position(2, 1),
            ],
            [
                Position(0, 0),
                Position(0, 1),
                Position(0, 2),
                Position(1, 0),
                Position(1, 1),
                Position(1, 2),
            ],
        )
        return tile
