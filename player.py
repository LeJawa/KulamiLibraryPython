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
        best_move = None
        best_score = -1000

        with VirtualBoard(game_info.board, game_info.current_player) as vboard:
            for socket in game_info.possible_moves:
                vboard.place_marble_at_position(socket.position)
                p1_score, p2_score = get_scores(vboard.board)
                vboard.revert_last_move()

                if game_info.current_player == PlayerNumber.ONE:
                    score = p1_score - p2_score
                else:
                    score = p2_score - p1_score
                    
                score = vboard.evaluate()
                
                if vboard.current_player == PlayerNumber.TWO:
                    score *= -1

                if score > best_score:
                    best_score = score
                    best_move = socket.position

        return best_move


class MinimaxPlayer(Player):
    """A player that chooses the best move using minimax"""

    def get_next_move(self, game_info: GameInfo) -> Position:
        
        if game_info.turn in (0, 1):
            return choice(game_info.possible_moves).position           
        
        best_move = None
        best_score = 1000

        with VirtualBoard(game_info.board, game_info.current_player) as vboard:
            for socket in vboard.get_possible_moves():
                vboard.place_marble_at_position(socket.position)
                score = self.minimax(vboard, 3, vboard.current_player == PlayerNumber.ONE)
                vboard.revert_last_move()

                if score < best_score:
                    best_score = score
                    best_move = socket.position
        return best_move

    def minimax(self, vboard: VirtualBoard, depth: int, maximizing: bool) -> int:
        possible_moves = vboard.get_possible_moves()
        
        if len(possible_moves) == 0:
            eval = vboard.evaluate()
            
            if eval > 0:
                return 1000
            elif eval < 0:
                return -1000
            else:
                return 0
        
        if depth == 0:
            return vboard.evaluate()

        if maximizing:
            best_value = -1000            
            
            for move in possible_moves:
                vboard.place_marble_at_position(move.position)
                best_value = max(best_value, self.minimax(vboard, depth - 1, False))
                vboard.revert_last_move()
            return best_value
        else:
            best_value = 1000
                        
            for move in possible_moves:
                vboard.place_marble_at_position(move.position)
                best_value = min(best_value, self.minimax(vboard, depth - 1, True))
                vboard.revert_last_move()
            return best_value


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
