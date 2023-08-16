"""The main class for the game"""

from enum import Enum
from board import BoardMaker
from constants import MARBLES_PER_PLAYER
from player import HumanPlayer, Player, RandomPlayer
from tile import Socket, SocketState, TileOwner


class PlayerNumber(Enum):
    """An enum for the players"""

    ONE = 1
    TWO = 2


# pylint: disable=too-many-instance-attributes


class Kulami:
    """The main class for the game"""

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

        self.turn = 0
        self.max_turns = 2 * MARBLES_PER_PLAYER

        self.player1_last_marble: Socket = None
        self.player2_last_marble: Socket = None

        self.possible_moves: list[Socket] = None
        
    def initialize_standard_board(self) -> None:
        """Initializes the board with the standard tiles"""
        self.board = BoardMaker.get_standard_board()
        
        self.calculate_possible_moves()
    
    def initialize_very_small_board(self) -> None:
        """Initializes the board with the very small tiles"""
        self.board = BoardMaker.get_very_small_board()
        
        self.calculate_possible_moves()

    def get_current_player(self) -> PlayerNumber:
        """Returns the current player"""
        if self.turn % 2 == 0:
            return PlayerNumber.ONE

        return PlayerNumber.TWO

    def player_turn(self) -> None:
        """Handles a player's turn"""
        print("Player " + str(self.turn % 2 + 1) + "'s turn")
        
        current_player = self.get_current_player()

        if current_player == PlayerNumber.ONE:
            marble_position = self.player1.get_next_move(
                self.board, self.possible_moves
            )
        else:
            marble_position = self.player2.get_next_move(
                self.board, self.possible_moves
            )

        if current_player == PlayerNumber.ONE:
            if self.board.set_p1_marble_at_position(marble_position):
                self.player1_last_marble = self.board.get_socket_at_position(
                    marble_position
                )
            else:
                print("Invalid move")
                return
        else:
            if self.board.set_p2_marble_at_position(marble_position):
                self.player2_last_marble = self.board.get_socket_at_position(
                    marble_position
                )
            else:
                print("Invalid move")
                return

        self.turn += 1      

        self.calculate_possible_moves()

    def play(self) -> None:
        """Starts the game to be played on the terminal"""
        self.board.draw()
        while self.turn < self.max_turns and self.possible_moves != []:
            self.player_turn()

        print("Game over!")
        player1_score, player2_score = self.get_scores()
        print("Player 1 score: " + str(player1_score))
        print("Player 2 score: " + str(player2_score))

    def calculate_possible_moves(self) -> None:
        """Gets all the possible moves for the current player"""
        all_sockets = self.board.get_all_sockets()

        if (
            self.player1_last_marble is None and self.player2_last_marble is None
        ):  # First turn
            self.possible_moves = all_sockets
            return

        possible_moves = []

        for socket in all_sockets:
            if socket.state != SocketState.EMPTY:
                continue

            if (
                socket.position.x == self.player1_last_marble.position.x
                and socket.position.y == self.player1_last_marble.position.y
            ):
                continue

            if socket.tile_id == self.player1_last_marble.tile_id:
                continue

            if self.player2_last_marble is not None:  # To handle the second turn
                if (
                    socket.position.x == self.player2_last_marble.position.x
                    and socket.position.y == self.player2_last_marble.position.y
                ):
                    continue

                if socket.tile_id == self.player2_last_marble.tile_id:
                    continue

            current_player = self.get_current_player()

            if current_player == PlayerNumber.ONE:
                last_move = self.player2_last_marble.position
            else:
                last_move = self.player1_last_marble.position

            if socket.position.x == last_move.x or socket.position.y == last_move.y:
                possible_moves.append(socket)

        self.possible_moves = possible_moves

    def get_scores(self) -> tuple[int, int]:
        """Calculates the scores of the players"""
        player1_score = 0
        player2_score = 0

        for tile in self.board.get_all_tiles():
            owner = tile.get_owner()
            if owner == TileOwner.PLAYER1:
                player1_score += tile.get_points()
            elif owner == TileOwner.PLAYER2:
                player2_score += tile.get_points()

        return (player1_score, player2_score)


if __name__ == "__main__":
    game = Kulami(HumanPlayer(), RandomPlayer())
    game.initialize_very_small_board()
    game.play()
