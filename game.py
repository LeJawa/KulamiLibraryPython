"""The main class for the game"""

from board import BoardInterface, BoardMaker, get_scores
from constants import MARBLES_PER_PLAYER
from data import GameInfo
from enums import PlayerNumber
from player import HumanPlayer, MinimaxPlayer, NaivePlayer, Player, RandomPlayer
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

        self.possible_moves = self.board.get_possible_moves(PlayerNumber.ONE)

    def initialize_very_small_board(self) -> None:
        """Initializes the board with the very small tiles"""
        self.board = BoardMaker.get_very_small_board()

        self.possible_moves = self.board.get_possible_moves(PlayerNumber.ONE)

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
            turn=self.turn,
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

        self.possible_moves = self.board.get_possible_moves(
            PlayerNumber.ONE if current_player == PlayerNumber.TWO else PlayerNumber.TWO
        )

    def play(self) -> None:
        """Starts the game to be played on the terminal"""
        while self.turn < self.max_turns and self.possible_moves:
            print("Turn " + str(self.turn + 1))
            self.board.draw()
            self.player_turn()
            # input("Press enter to continue...")

        self.board.draw()
        print("Game over!")
        player1_score, player2_score = get_scores(self.board)
        print("Player 1 score: " + str(player1_score))
        print("Player 2 score: " + str(player2_score))


if __name__ == "__main__":
    human1 = HumanPlayer()
    human2 = HumanPlayer()

    naive1 = NaivePlayer()
    naive2 = NaivePlayer()

    random1 = RandomPlayer()
    random2 = RandomPlayer()

    game = Kulami(MinimaxPlayer(3), random1)
    # game.initialize_very_small_board()
    game.initialize_standard_board()
    game.play()
