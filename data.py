"""Contains dataclasses for the game"""

from dataclasses import dataclass
from board import BoardInterface

from enums import PlayerNumber
from tile import Socket


@dataclass
class GameInfo:
    """Contains information about the board"""

    current_player: PlayerNumber
    possible_moves: list[Socket]
    board: BoardInterface
    turn: int
