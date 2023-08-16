"""This module contains the player classes for the Kulami game."""

from random import choice
from board import VirtualBoard, get_scores
from data import GameInfo
from enums import PlayerNumber
from position import Position
from tile import Socket

# pylint: disable=too-few-public-methods


class Player:
    """A mother class for players"""

    def get_next_move(self, game_info: GameInfo) -> Position:
        """Gets the position the player wants to place their marble in"""
        raise NotImplementedError("get_next_move not implemented")


class NaivePlayer(Player):
    """A player that chooses the move with the highest immediate score"""

    def get_next_move(self, game_info: GameInfo) -> Position:
        """Gets the position the player wants to place their marble in"""

        best_move = None
        best_score = -1

        with VirtualBoard(game_info.board) as virtual_board:
            for socket in game_info.possible_moves:
                virtual_board.place_marble_at_position(
                    socket.position, game_info.current_player
                )
                p1_score, p2_score = get_scores(virtual_board.board)
                virtual_board.revert_last_move()

                if game_info.current_player == PlayerNumber.ONE:
                    score = p1_score - p2_score
                else:
                    score = p2_score - p1_score

                if score > best_score:
                    best_score = score
                    best_move = socket.position

        return best_move


class RandomPlayer(Player):
    """A player that chooses a random move"""

    def get_next_move(self, game_info: GameInfo) -> Position:
        """Gets the position the player wants to place their marble in"""

        return choice(game_info.possible_moves).position


class HumanPlayer(Player):
    """A player that asks the user for a move"""

    def get_next_move(self, game_info: GameInfo) -> Position:
        """Gets the position the player wants to place their marble in"""

        game_info.board.draw()
        print("Player " + str(game_info.current_player) + "'s turn")
        print_possible_moves(game_info.possible_moves)

        while True:
            coords = input("Choose a position to place your marble: ")

            try:
                if "," in coords:
                    coords = coords.split(",")
                    coords = [int(coord) for coord in coords]
                elif len(coords) == 2:
                    coords = [int(coords[0]), int(coords[1])]

                for socket in game_info.possible_moves:
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
