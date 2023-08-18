"""
This module contains the MatchMaker class
It is used to play a given number of matches between two players and save the results.
"""

import datetime
from enums import PlayerNumber
from game import Kulami

# pylint: disable=unused-import
from player import Player, RandomPlayer, MinimaxPlayer, NaivePlayer

# pylint: enable=unused-import


class MatchMaker:
    """Plays a given number of matches between two players and saves the results"""

    def __init__(
        self, player1: Player, player2: Player, number_of_matches: int
    ) -> None:
        self.player1 = player1
        self.player2 = player2
        self.number_of_matches = number_of_matches

        self.player1_wins = 0
        self.player2_wins = 0

    def play_matches(self) -> None:
        """Plays the given number of matches"""
        print("Playing matches between", self.player1, "and", self.player2)

        for _ in range(self.number_of_matches):
            game = Kulami(self.player1, self.player2)
            game.initialize_standard_board()
            winner = game.play()

            if winner == PlayerNumber.ONE:
                self.player1_wins += 1
            elif winner == PlayerNumber.TWO:
                self.player2_wins += 1

        self.save_results()

    def save_results(self) -> None:
        """Saves the results of the matches"""
        with open(
            f"results/{self.player1}_vs_{self.player2}_{self.number_of_matches}.txt",
            "w",
            encoding="utf-8",
        ) as file:
            file.write(f"{self.player1} wins: {self.player1_wins}\n")
            file.write(f"{self.player2} wins: {self.player2_wins}\n")
            file.write(f"Total matches: {self.number_of_matches}\n")


if __name__ == "__main__":
    N = 100

    matches = [
        (RandomPlayer(), RandomPlayer()),
        (RandomPlayer(), NaivePlayer()),
        (RandomPlayer(), MinimaxPlayer(0)),
        (RandomPlayer(), MinimaxPlayer(1)),
        (RandomPlayer(), MinimaxPlayer(2)),
        (RandomPlayer(), MinimaxPlayer(3)),
        (NaivePlayer(), RandomPlayer()),
        (NaivePlayer(), NaivePlayer()),
        (NaivePlayer(), MinimaxPlayer(0)),
        (NaivePlayer(), MinimaxPlayer(1)),
        (NaivePlayer(), MinimaxPlayer(2)),
        (NaivePlayer(), MinimaxPlayer(3)),
        (MinimaxPlayer(0), RandomPlayer()),
        (MinimaxPlayer(0), NaivePlayer()),
        (MinimaxPlayer(0), MinimaxPlayer(0)),
        (MinimaxPlayer(0), MinimaxPlayer(1)),
        (MinimaxPlayer(0), MinimaxPlayer(2)),
        (MinimaxPlayer(0), MinimaxPlayer(3)),
        (MinimaxPlayer(1), RandomPlayer()),
        (MinimaxPlayer(1), NaivePlayer()),
        (MinimaxPlayer(1), MinimaxPlayer(0)),
        (MinimaxPlayer(1), MinimaxPlayer(1)),
        (MinimaxPlayer(1), MinimaxPlayer(2)),
        (MinimaxPlayer(1), MinimaxPlayer(3)),
        (MinimaxPlayer(2), RandomPlayer()),
        (MinimaxPlayer(2), NaivePlayer()),
        (MinimaxPlayer(2), MinimaxPlayer(0)),
        (MinimaxPlayer(2), MinimaxPlayer(1)),
        (MinimaxPlayer(2), MinimaxPlayer(2)),
        (MinimaxPlayer(2), MinimaxPlayer(3)),
        (MinimaxPlayer(3), RandomPlayer()),
        (MinimaxPlayer(3), NaivePlayer()),
        (MinimaxPlayer(3), MinimaxPlayer(0)),
        (MinimaxPlayer(3), MinimaxPlayer(1)),
        (MinimaxPlayer(3), MinimaxPlayer(2)),
        (MinimaxPlayer(3), MinimaxPlayer(3)),
    ]

    total_start_time = datetime.datetime.now()

    for match in matches:
        match_start_time = datetime.datetime.now()

        match_maker = MatchMaker(match[0], match[1], N)
        match_maker.play_matches()
        match_time = datetime.datetime.now() - match_start_time
        total_time = datetime.datetime.now() - total_start_time

        match_time = datetime.datetime.utcfromtimestamp(
            match_time.total_seconds()
        ).strftime("%H:%M:%S.%f")
        total_time = datetime.datetime.utcfromtimestamp(
            total_time.total_seconds()
        ).strftime("%H:%M:%S.%f")
        print(f"Time elapsed: {match_time} / {total_time}")
