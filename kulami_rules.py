from board import BoardInterface
from enums import PlayerNumber
from game import Kulami
from tile import SocketState, TileOwner

def calculate_possible_moves(game: Kulami) -> None:
    """Gets all the possible moves for the current player"""
    all_sockets = game.board.get_all_sockets()

    if (
        game.player1_last_marble is None and game.player2_last_marble is None
    ):  # First turn
        game.possible_moves = all_sockets
        return

    possible_moves = []

    for socket in all_sockets:
        if socket.state != SocketState.EMPTY:
            continue

        if (
            socket.position.x == game.player1_last_marble.position.x
            and socket.position.y == game.player1_last_marble.position.y
        ):
            continue

        if socket.tile_id == game.player1_last_marble.tile_id:
            continue

        if game.player2_last_marble is not None:  # To handle the second turn
            if (
                socket.position.x == game.player2_last_marble.position.x
                and socket.position.y == game.player2_last_marble.position.y
            ):
                continue

            if socket.tile_id == game.player2_last_marble.tile_id:
                continue

        current_player = game.get_current_player()

        if current_player == PlayerNumber.ONE:
            last_move = game.player2_last_marble.position
        else:
            last_move = game.player1_last_marble.position

        if socket.position.x == last_move.x or socket.position.y == last_move.y:
            possible_moves.append(socket)

    game.possible_moves = possible_moves

