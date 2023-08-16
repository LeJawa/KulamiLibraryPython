"""The main class for the game"""

from enum import Enum
from board import BoardMaker
from constants import MARBLES_PER_PLAYER
from tile import Socket


class Player(Enum):
    """An enum for the players"""

    ONE = 1
    TWO = 2


class Kulami:
    """The main class for the game"""

    def __init__(self):
        self.board = BoardMaker.get_standard_board()

        self.turn = 0
        self.max_turns = 2 * MARBLES_PER_PLAYER

        self.player1_last_marble: Socket = None
        self.player2_last_marble: Socket = None

        self.possibles_moves: list[Socket] = None
        self.calculate_possible_moves()

    def get_socket(self) -> Socket:
        """Gets the socket the player wants to place their marble in"""
        while True:
            coords = input("Choose a socket to place your marble: ")

            try:
                if "," in coords:
                    coords = coords.split(",")
                    coords = [int(coord) for coord in coords]
                elif len(coords) == 2:
                    coords = [int(coords[0]), int(coords[1])]

                for socket in self.possibles_moves:
                    if (
                        socket.position.x == coords[0]
                        and socket.position.y == coords[1]
                    ):
                        return socket
            except Exception:  # pylint: disable=broad-exception-caught
                pass

            print("Invalid coordinates")

    def get_current_player(self) -> Player:
        """Returns the current player"""
        if self.turn % 2 == 0:
            return Player.ONE

        return Player.TWO

    def player_turn(self) -> None:
        """Handles a player's turn"""
        print("Player " + str(self.turn % 2 + 1) + "'s turn")

        self.calculate_possible_moves()

        marble_socket = self.get_socket()

        if self.turn % 2 == 0:
            if self.board.set_p1_marble(marble_socket):
                self.player1_last_marble = marble_socket
            else:
                print("Invalid move")
                return
        else:
            if self.board.set_p2_marble(marble_socket):
                self.player2_last_marble = marble_socket
            else:
                print("Invalid move")
                return

        self.board.draw()

        self.turn += 1

    def play(self) -> None:
        """Starts the game"""
        self.board.draw()
        while self.turn < self.max_turns:
            self.player_turn()

        print("Game over!")

    def calculate_possible_moves(self) -> None:
        """Gets all the possible moves for the current player"""
        all_sockets = self.board.get_all_sockets()

        if (
            self.player1_last_marble is None and self.player2_last_marble is None
        ):  # First turn
            self.possibles_moves = all_sockets
            return

        possible_moves = []

        for socket in all_sockets:
            if (
                socket.position.x == self.player1_last_marble.position.x
                and socket.position.y == self.player1_last_marble.position.y
            ):
                continue

            if self.player2_last_marble is not None:  # To handle the second turn
                if (
                    socket.position.x == self.player2_last_marble.position.x
                    and socket.position.y == self.player2_last_marble.position.y
                ):
                    continue

            if socket.tile_id == self.player1_last_marble.tile_id:
                continue

            if self.player2_last_marble is not None:  # To handle the second turn
                if socket.tile_id == self.player2_last_marble.tile_id:
                    continue

            current_player = self.get_current_player()

            if current_player == Player.ONE:
                last_move = self.player2_last_marble.position
            else:
                last_move = self.player1_last_marble.position

            if socket.position.x == last_move.x or socket.position.y == last_move.y:
                possible_moves.append(socket)

        self.possibles_moves = possible_moves

        positions = ""
        for socket in self.possibles_moves:
            positions += (
                "(" + str(socket.position.x) + "," + str(socket.position.y) + ") "
            )
        print("Possible moves: " + positions)


if __name__ == "__main__":
    game = Kulami()
    game.play()
