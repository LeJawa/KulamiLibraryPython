"""This module contains the player classes for the Kulami game."""

from random import choice
from board import VirtualBoard
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
        best_move = None

        best_score = -1000

        with VirtualBoard(game_info.board, game_info.current_player) as vboard:
            for socket in game_info.possible_moves:
                vboard.place_marble_at_position(socket.position)

                score = vboard.evaluate()
                vboard.revert_last_move()

                if vboard.current_player == PlayerNumber.TWO:
                    score *= -1

                if score > best_score:
                    best_score = score
                    best_move = socket.position

        return best_move


class MinimaxPlayer(Player):
    """A player that chooses the best move using minimax"""

    def __init__(self, depth: int = 3):
        self.depth = depth

    def get_next_move(self, game_info: GameInfo) -> Position:
        # If it's the first or second turn, choose a random move
        # This is to avoid slowing the minimax algorithm too much
        # when there are many possible moves
        if game_info.turn in (0, 1):
            return choice(game_info.possible_moves).position       
        
        if game_info.current_player == PlayerNumber.ONE:
            maximizing = True            
            best_score = -1000
        else:
            maximizing = False
            best_score = 1000

        best_move = None

        with VirtualBoard(game_info.board, game_info.current_player) as vboard:
            for move in game_info.possible_moves:
                vboard.place_marble_at_position(move.position)
                score = self._minimax(vboard, self.depth, maximizing)
                vboard.revert_last_move()
                
                
                if maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = move.position
                else:
                    if score < best_score:
                        best_score = score
                        best_move = move.position
                
        return best_move

    def _minimax(self, vboard: VirtualBoard, depth: int, maximizing: bool) -> int:
        """
        Returns the best score for the current player by
        recursively evaluating the board.
        """
        
        if depth == 0 or vboard.is_game_over():
            return vboard.evaluate()
        
        if maximizing:
            best_score = -1000
        else:
            best_score = 1000
        
        for move in vboard.get_possible_moves():
            vboard.place_marble_at_position(move.position)
            score = self._minimax(vboard, depth - 1, not maximizing)
            vboard.revert_last_move()
            
            if maximizing:
                if score > best_score:
                    best_score = score
            else:
                if score < best_score:
                    best_score = score
        
        return best_score
        
        


class RandomPlayer(Player):
    """A player that chooses a random move"""

    def get_next_move(self, game_info: GameInfo) -> Position:
        return choice(game_info.possible_moves).position


class HumanPlayer(Player):
    """A player that asks the user for a move"""

    def get_next_move(self, game_info: GameInfo) -> Position:
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
