"""This module contains enums for the game."""

from enum import Enum


class TileOwner(Enum):
    """Represents the owner of a tile."""

    PLAYER1 = 1
    PLAYER2 = 2
    NONE = 3


class SocketState(Enum):
    """Represents the state of a socket."""

    OUT_OF_BOUNDS = 0
    EMPTY = 1
    PLAYER1 = 2
    PLAYER2 = 3
    PLAYER1_LAST = 4
    PLAYER2_LAST = 5


class PlayerNumber(Enum):
    """An enum for the players"""

    ONE = 1
    TWO = 2
