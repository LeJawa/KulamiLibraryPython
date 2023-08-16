"""This module contains the player classes for the Kulami game."""

from random import choice
from board import BoardInterface
from position import Position
from tile import Socket

# pylint: disable=too-few-public-methods


class Player:
    """A mother class for players"""

    def get_next_move(
        self, board: BoardInterface, possible_moves: list[Socket]
    ) -> Position:
        """Gets the position the player wants to place their marble in"""
        raise NotImplementedError("get_next_move not implemented")


class RandomPlayer(Player):
    """A player that chooses a random move"""

    def get_next_move(
        self, board: BoardInterface, possible_moves: list[Socket]
    ) -> Position:
        """Gets the position the player wants to place their marble in"""

        return choice(possible_moves).position


class HumanPlayer(Player):
    """A player that asks the user for a move"""

    def get_next_move(
        self, board: BoardInterface, possible_moves: list[Socket]
    ) -> Position:
        """Gets the position the player wants to place their marble in"""

        board.draw()
        print_possible_moves(possible_moves)

        while True:
            coords = input("Choose a position to place your marble: ")

            try:
                if "," in coords:
                    coords = coords.split(",")
                    coords = [int(coord) for coord in coords]
                elif len(coords) == 2:
                    coords = [int(coords[0]), int(coords[1])]

                for socket in possible_moves:
                    if (
                        socket.position.x == coords[0]
                        and socket.position.y == coords[1]
                    ):
                        return socket.position
            except Exception:  # pylint: disable=broad-exception-caught
                pass

            print("Invalid coordinates")


def print_possible_moves(possible_moves: list[Socket]):
    """Prints the possible moves to the terminal"""
    positions = ""
    for socket in possible_moves:
        positions += "(" + str(socket.position.x) + "," + str(socket.position.y) + ") "
    print("Possible moves: " + positions)
