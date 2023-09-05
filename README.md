# Kulami Library in Python

[![Pylint](https://github.com/LeJawa/KulamiLibraryPython/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/LeJawa/KulamiLibraryPython/actions/workflows/pylint.yml)

Python playground for implementing an AI that will play Kulami.

Three types of players have been implemented:

- RandomPlayer: Selects a random move each turn.
- NaivePlayer: Plays the move that will immediately maximize the score on its favor.
- MinimaxPlayer: Implements the minimax algorithm to find the best move. Not really optimized. More than depth 5 and it gets really slow.

## NaivePlayer vs MinimaxPlayer

![NaivePlayer vs MinimaxPlayer](images/Naive_vs_Minimax3.gif)

## Documentation

To generate documentation, run the following command in the root directory:

`pdoc --html .`
