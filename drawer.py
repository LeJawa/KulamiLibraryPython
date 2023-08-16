"""
This file contains the BoardDrawer class, which is used to draw the board.
"""

# pylint: disable=too-many-branches, too-many-statements, too-many-boolean-expressions

# from board import Board
from bash_color import Color, colorize
from tile import Socket, SocketState

symbols = ["+", "❶", "❷", "①", "②", "⁕", "O", "?"]


class BoardDrawer:
    """Represents the board drawer."""

    def __init__(self, board) -> None:
        self.board = board
        self.size = board.available_size

        self.debug = False
        self.show_axis = True

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def get_symbol(socket: Socket) -> str:
        """Get the symbol to represent the given socket."""

        symbol = "?"

        if socket is None:
            return colorize("+", Color.DARKGREY)

        state = socket.state
        if state == SocketState.PLAYER1:
            symbol = colorize("❶", Color.RED)
        elif state == SocketState.PLAYER1_LAST:
            symbol = colorize("①", Color.RED)
        elif state == SocketState.PLAYER2:
            symbol = colorize("❷", Color.BLUE)
        elif state == SocketState.PLAYER2_LAST:
            symbol = colorize("②", Color.BLUE)
        elif state == SocketState.EMPTY:
            symbol = "O"

        return symbol

    @staticmethod
    def get_debug_symbol(socket: Socket) -> str:
        """Get the debug symbol to represent the given socket."""
        if socket is None:
            return "•"

        return str(socket.tile_id)

    def __str__(self) -> str:
        str_board = ""

        if self.show_axis:
            str_board += "  "
            for x in range(self.size):
                str_board += hex(x)[2:] + " "
            str_board += "\n"

        for y in range(self.size):
            first_line_str = ""
            second_line_str = ""

            if self.show_axis:
                first_line_str = " "
                second_line_str = hex(y)[2:]

            for x in range(self.size):
                upper_left_symbol = self.get_upper_left_symbol(x, y)
                up_symbol = self.get_up_symbol(x, y)
                left_symbol = self.get_left_symbol(x, y)

                if self.debug:
                    pos_symbol = BoardDrawer.get_debug_symbol(
                        self.board.get_socket_at(x, y)
                    )
                else:
                    pos_symbol = BoardDrawer.get_symbol(self.board.get_socket_at(x, y))

                first_line_str += colorize(
                    upper_left_symbol + up_symbol, Color.DARKGREY
                )
                second_line_str += colorize(left_symbol, Color.DARKGREY) + pos_symbol

            upper_right_symbol = self.get_upper_right_symbol(x, y)
            right_symbol = self.get_right_symbol(x, y)

            first_line_str += colorize(upper_right_symbol, Color.DARKGREY) + "\n"
            second_line_str += colorize(right_symbol, Color.DARKGREY) + "\n"

            str_board += first_line_str + second_line_str

        last_line_str = ""
        if self.show_axis:
            last_line_str = " "

        for x in range(self.size):
            upper_left_symbol = self.get_upper_left_symbol(x, y + 1)
            up_symbol = self.get_up_symbol(x, y + 1)
            last_line_str += upper_left_symbol + up_symbol
        upper_right_symbol = self.get_upper_right_symbol(x, y + 1)
        last_line_str += upper_right_symbol + "\n"

        str_board += colorize(last_line_str, Color.DARKGREY)

        return str_board

    def get_right_symbol(self, x: int, y: int) -> str:
        """
        Get the symbol directly to the right of the given position.
        """
        left_id = self.board.get_tile_id_at(x, y)
        if left_id == -1:
            return " "

        return "│"

    def get_upper_right_symbol(self, x: int, y: int) -> str:
        """
        Get the symbol in the upper right corner of the given position.
        """
        upper_left_id = self.board.get_tile_id_at(x, y - 1)
        lower_left_id = self.board.get_tile_id_at(x, y)

        symbol = ""

        if upper_left_id == -1 and lower_left_id == -1:
            symbol = " "
        elif upper_left_id != -1 and lower_left_id != -1:
            if upper_left_id == lower_left_id:
                symbol = "│"
            else:
                symbol = "┤"
        elif upper_left_id == -1 and lower_left_id != -1:
            symbol = "┐"
        else:
            symbol = "┘"

        return symbol

    def get_up_symbol(self, x: int, y: int) -> str:
        """
        Get the symbol directly above the given position.
        """
        up_id = self.board.get_tile_id_at(x, y - 1)
        down_id = self.board.get_tile_id_at(x, y)

        symbol = ""

        if (up_id == -1 and down_id == -1) or (
            up_id != -1 and down_id != -1 and up_id == down_id
        ):
            symbol = " "
        else:
            symbol = "─"

        return symbol

    def get_left_symbol(self, x: int, y: int) -> str:
        """
        Get the symbol directly to the left of the given position.
        """
        left_id = self.board.get_tile_id_at(x - 1, y)
        right_id = self.board.get_tile_id_at(x, y)

        if (left_id == -1 and right_id == -1) or (
            left_id != -1 and right_id != -1 and left_id == right_id
        ):
            symbol = " "
        else:
            symbol = "│"

        return symbol

    def get_upper_left_symbol(self, x: int, y: int) -> str:
        """
        Get the symbol in the upper left corner of the given position.
        """
        upper_left_id = self.board.get_tile_id_at(x - 1, y - 1)
        upper_right_id = self.board.get_tile_id_at(x, y - 1)
        lower_left_id = self.board.get_tile_id_at(x - 1, y)
        lower_right_id = self.board.get_tile_id_at(x, y)

        symbol = ""

        # All empty
        if (
            upper_left_id == -1
            and upper_right_id == -1
            and lower_left_id == -1
            and lower_right_id == -1
        ):
            symbol = " "

        # Only one filled
        elif (
            upper_left_id == -1
            and upper_right_id == -1
            and lower_left_id == -1
            and lower_right_id != -1
        ):
            symbol = "┌"
        elif (
            upper_left_id == -1
            and upper_right_id == -1
            and lower_left_id != -1
            and lower_right_id == -1
        ):
            symbol = "┐"
        elif (
            upper_left_id == -1
            and upper_right_id != -1
            and lower_left_id == -1
            and lower_right_id == -1
        ):
            symbol = "└"
        elif (
            upper_left_id != -1
            and upper_right_id == -1
            and lower_left_id == -1
            and lower_right_id == -1
        ):
            symbol = "┘"

        # Two filled
        elif (
            upper_left_id == -1
            and upper_right_id == -1
            and lower_left_id != -1
            and lower_right_id != -1
        ):
            if lower_left_id == lower_right_id:
                symbol = "─"
            else:
                symbol = "┬"
        elif (
            upper_left_id == -1
            and upper_right_id != -1
            and lower_left_id == -1
            and lower_right_id != -1
        ):
            if upper_right_id == lower_right_id:
                symbol = "│"
            else:
                symbol = "├"
        elif (
            upper_left_id != -1
            and upper_right_id == -1
            and lower_left_id == -1
            and lower_right_id != -1
        ):
            symbol = "┼"

        elif (
            upper_left_id == -1
            and upper_right_id != -1
            and lower_left_id != -1
            and lower_right_id == -1
        ):
            symbol = "┼"
        elif (
            upper_left_id != -1
            and upper_right_id == -1
            and lower_left_id != -1
            and lower_right_id == -1
        ):
            if upper_left_id == lower_left_id:
                symbol = "│"
            else:
                symbol = "┤"

        elif (
            upper_left_id != -1
            and upper_right_id != -1
            and lower_left_id == -1
            and lower_right_id == -1
        ):
            if upper_left_id == upper_right_id:
                symbol = "─"
            else:
                symbol = "┴"

        # Three filled or three same/one different
        elif (
            upper_left_id == -1
            and upper_right_id != -1
            and lower_left_id != -1
            and lower_right_id != -1
        ) or (
            upper_left_id != upper_right_id
            and upper_left_id != lower_left_id
            and upper_left_id != lower_right_id
            and upper_right_id == lower_left_id
            and upper_right_id == lower_right_id
        ):
            if upper_right_id == lower_right_id and upper_right_id != lower_left_id:
                symbol = "┤"
            elif upper_right_id == lower_left_id and upper_right_id != lower_right_id:
                symbol = "┼"
            elif (
                upper_right_id != lower_right_id
                and upper_right_id != lower_left_id
                and lower_right_id == lower_left_id
            ):
                symbol = "┴"
            elif (
                upper_right_id != lower_right_id
                and upper_right_id != lower_left_id
                and lower_right_id != lower_left_id
            ):
                symbol = "┼"
            else:
                symbol = "┘"

        elif (
            upper_left_id != -1
            and upper_right_id == -1
            and lower_left_id != -1
            and lower_right_id != -1
        ) or (
            upper_right_id != upper_left_id
            and upper_right_id != lower_left_id
            and upper_right_id != lower_right_id
            and upper_left_id == lower_left_id
            and upper_left_id == lower_right_id
        ):
            if upper_left_id == lower_left_id and upper_left_id != lower_right_id:
                symbol = "├"
            elif upper_left_id == lower_right_id and upper_left_id != lower_left_id:
                symbol = "┼"
            elif (
                upper_left_id != lower_right_id
                and upper_left_id != lower_left_id
                and lower_right_id == lower_left_id
            ):
                symbol = "┴"
            elif (
                upper_left_id != lower_right_id
                and upper_left_id != lower_left_id
                and lower_right_id != lower_left_id
            ):
                symbol = "┼"
            else:
                symbol = "└"

        elif (
            upper_left_id != -1
            and upper_right_id != -1
            and lower_left_id == -1
            and lower_right_id != -1
        ) or (
            lower_left_id != upper_right_id
            and lower_left_id != upper_left_id
            and lower_left_id != lower_right_id
            and upper_left_id == upper_right_id
            and upper_left_id == lower_right_id
        ):
            if upper_left_id == upper_right_id and upper_left_id != lower_right_id:
                symbol = "┬"
            elif upper_left_id == lower_right_id and upper_left_id != upper_right_id:
                symbol = "┼"
            elif (
                upper_left_id != lower_right_id
                and upper_left_id != upper_right_id
                and lower_right_id == upper_right_id
            ):
                symbol = "┤"
            elif (
                upper_left_id != lower_right_id
                and upper_left_id != upper_right_id
                and lower_right_id != upper_right_id
            ):
                symbol = "┼"
            else:
                symbol = "┐"

        elif (
            upper_left_id != -1
            and upper_right_id != -1
            and lower_left_id != -1
            and lower_right_id == -1
        ) or (
            lower_right_id != upper_right_id
            and lower_right_id != lower_left_id
            and lower_right_id != upper_left_id
            and upper_left_id == upper_right_id
            and upper_left_id == lower_left_id
        ):
            if upper_left_id == upper_right_id and upper_left_id != lower_left_id:
                symbol = "┬"
            elif upper_left_id == lower_left_id and upper_left_id != upper_right_id:
                symbol = "├"
            elif (
                upper_left_id != lower_left_id
                and upper_left_id != upper_right_id
                and lower_left_id == upper_right_id
            ):
                symbol = "┼"
            elif (
                upper_left_id != lower_left_id
                and upper_left_id != upper_right_id
                and lower_left_id != upper_right_id
            ):
                symbol = "┼"
            else:
                symbol = "┌"

        # All filled
        elif (
            upper_left_id != -1
            and upper_right_id != -1
            and lower_left_id != -1
            and lower_right_id != -1
        ):
            if (
                upper_left_id == lower_left_id
                and upper_right_id == lower_right_id
                and upper_left_id != upper_right_id
            ):
                symbol = "│"
            elif (
                upper_left_id == lower_left_id
                and upper_right_id != lower_right_id
                and upper_left_id != upper_right_id
            ):
                symbol = "├"
            elif (
                upper_right_id == lower_right_id
                and upper_left_id != lower_left_id
                and upper_left_id != upper_right_id
            ):
                symbol = "┤"
            elif (
                upper_left_id == upper_right_id
                and lower_left_id == lower_right_id
                and upper_left_id != lower_left_id
            ):
                symbol = "─"
            elif (
                upper_left_id == upper_right_id
                and lower_left_id != lower_right_id
                and upper_left_id != lower_left_id
            ):
                symbol = "┬"
            elif (
                lower_left_id == lower_right_id
                and upper_left_id != upper_right_id
                and upper_left_id != lower_left_id
            ):
                symbol = "┴"
            elif (
                upper_left_id == lower_right_id and upper_left_id != upper_right_id
            ) or (upper_right_id == lower_left_id and upper_left_id != upper_right_id):
                symbol = "┼"
            elif (
                upper_left_id == upper_right_id
                and upper_left_id == lower_left_id
                and upper_left_id == lower_right_id
            ):
                symbol = " "
            elif (
                upper_left_id != upper_right_id
                and upper_left_id != lower_left_id
                and upper_left_id != lower_right_id
                and upper_right_id != lower_left_id
                and upper_right_id != lower_right_id
                and lower_left_id != lower_right_id
            ):
                symbol = "┼"

        return symbol
