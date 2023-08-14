from dataclasses import dataclass
from random import choice
from position import Position


class State:
    EMPTY = 1
    PLAYER1 = 2
    PLAYER2 = 3
    PLAYER1_LAST = 4
    PLAYER2_LAST = 5


@dataclass
class Socket:
    position: Position
    tile_id: int
    state: State

    def __init__(self, position: Position):
        self.position = position
        self.state: State = State.EMPTY
        self.tile_id = -1

    def is_empty(self) -> bool:
        return self.state == State.EMPTY or self.state == State.EMPTY

    def set_tile_id(self, id: int) -> None:
        self.tile_id = id


@dataclass
class Tile:
    sockets: list[Socket]
    id: int

    def get_bit_mask(self, mask_size) -> int:
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


class QuantumTile:
    possible_ids = [
        *"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~!@#$%^&*()-_=+[{]}|;:'\",<.>/?"
    ]
    next_id_index = -1

    def __init__(
        self, raw_positions: list[Position], rotated_raw_positions: list[Position] = []
    ) -> None:
        self.raw_positions = raw_positions
        self.rotated_raw_positions = rotated_raw_positions
        self.id = QuantumTile.assign_id()
        self.has_rotation = False

        if len(rotated_raw_positions) > 0:
            self.rotated_raw_positions = rotated_raw_positions
            self.has_rotation = True

        self.positions = self.raw_positions.copy()
        self.rotated_positions = self.rotated_raw_positions.copy()

    def assign_id() -> int:
        QuantumTile.next_id_index += 1
        return QuantumTile.possible_ids[QuantumTile.next_id_index]

    def move_to(self, position: Position) -> None:
        self.positions.clear()
        for pos in self.raw_positions:
            self.positions.append(pos + position)

        self.rotated_positions.clear()
        for pos in self.rotated_raw_positions:
            self.rotated_positions.append(pos + position)

    @staticmethod
    def getTiles(
        raw_positions: list[Position], positions: list[Position], id: int
    ) -> list[Tile]:
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

                possible_socket.set_tile_id(id)
                possible_socket.state = State.EMPTY

                tile_sockets.append(possible_socket)
            if not out_of_bounds:
                tile_list.append(Tile(tile_sockets, id))
        return tile_list

    def get_possible_tiles_at(self, position: Position) -> list[Tile]:
        self.move_to(position)

        tile_list: list[Tile] = []
        tile_list += QuantumTile.getTiles(self.raw_positions, self.positions, self.id)
        tile_list += QuantumTile.getTiles(
            self.rotated_raw_positions, self.rotated_positions, self.id
        )

        return tile_list

    def collapse(self) -> Tile:
        return self.collapse_at(Position(0, 0))

    def collapse_at(self, position: Position) -> Tile:
        return choice(self.get_possible_tiles_at(position))


class QuantumTileMaker:
    @staticmethod
    def get1x1() -> QuantumTile:
        tile = QuantumTile([Position(0, 0)])
        return tile

    @staticmethod
    def get2x1() -> QuantumTile:
        tile = QuantumTile(
            [Position(0, 0), Position(1, 0)], [Position(0, 0), Position(0, 1)]
        )
        return tile

    @staticmethod
    def get3x1() -> QuantumTile:
        tile = QuantumTile(
            [Position(0, 0), Position(1, 0), Position(2, 0)],
            [Position(0, 0), Position(0, 1), Position(0, 2)],
        )
        return tile

    @staticmethod
    def get2x2() -> QuantumTile:
        tile = QuantumTile(
            [Position(0, 0), Position(1, 0), Position(0, 1), Position(1, 1)]
        )
        return tile

    @staticmethod
    def get3x2() -> QuantumTile:
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
