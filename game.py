"""The main class for the game"""

from board import BoardInterface, BoardMaker, get_scores
from constants import MARBLES_PER_PLAYER
from data import GameInfo
from enums import PlayerNumber, SocketState
from player import HumanPlayer, NaivePlayer, Player, RandomPlayer
from tile import Socket

# pylint: disable=too-many-instance-attributes


class Kulami:
    """The main class for the game"""

    def __init__(self, player1: Player, player2: Player):
        self.board: BoardInterface = None

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
        current_player = self.get_current_player()

        game_info = GameInfo(
            current_player=current_player,
            possible_moves=self.possible_moves,
            board=self.board,
        )

        if current_player == PlayerNumber.ONE:
            marble_position = self.player1.get_next_move(game_info)
        else:
            marble_position = self.player2.get_next_move(game_info)

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

    def play(self) -> None:
        """Starts the game to be played on the terminal"""
        while self.turn < self.max_turns and self.possible_moves:
            self.player_turn()

        print("Game over!")
        player1_score, player2_score = get_scores(self.board)
        print("Player 1 score: " + str(player1_score))
        print("Player 2 score: " + str(player2_score))

        self.board.draw()


if __name__ == "__main__":
    human1 = HumanPlayer()
    human2 = HumanPlayer()

    naive1 = NaivePlayer()
    naive2 = NaivePlayer()

    random1 = RandomPlayer()
    random2 = RandomPlayer()

    game = Kulami(naive1, random1)
    # game.initialize_very_small_board()
    game.initialize_standard_board()
    game.play()
