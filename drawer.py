# from board import Board
from bash_color import Color, color
from position import Pos, State

symbols = ["+", "❶", "❷", "①", "②", "⁕", "O", "?"]

class BoardDrawer:
    def __init__(self, board) -> None:
        self.board = board       
        self.size = board.available_size 
        
        self.debug = False
        self.show_axis = True
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @staticmethod
    def get_symbol(pos: Pos) -> str:
        state = pos.state
        if (state == State.EMPTY):
            return color("+", Color.DARKGREY)
        elif (state == State.PLAYER1):
            return color("❶", Color.RED)
        elif (state == State.PLAYER1_LAST):
            return color("①", Color.RED)
        elif (state == State.PLAYER2):
            return color("❷", Color.BLUE)
        elif (state == State.PLAYER2_LAST):
            return color("②", Color.BLUE)
        elif (state == State.EMPTY_TILE):
            return "O"
        else:
            return "?"
    
    @staticmethod
    def get_debug_symbol(pos: Pos) -> str:
        if (pos.state == State.EMPTY):
            return "•"
        else:
            return str(pos.tile_id)
    
    def __str__(self) -> str:
        str_board = ""
        
        if (self.show_axis):
            str_board += "  "
            for x in range(self.size):
                str_board += hex(x)[2:] + " "
            str_board += "\n"
    
        for y in range(self.size):
            first_line_str = " "
            second_line_str = hex(y)[2:]
            for x in range(self.size):
                upper_left_symbol = self.get_upper_left_symbol(x, y)
                up_symbol = self.get_up_symbol(x, y)
                left_symbol = self.get_left_symbol(x, y)
                
                if (self.debug):
                    pos_symbol = BoardDrawer.get_debug_symbol(self.board.get_pos_at(x, y))
                else:              
                    pos_symbol = BoardDrawer.get_symbol(self.board.get_pos_at(x, y))
                
                first_line_str += color(upper_left_symbol + up_symbol, Color.DARKGREY)
                second_line_str += color(left_symbol, Color.DARKGREY) + pos_symbol
            
            upper_right_symbol = self.get_upper_right_symbol(x, y)
            right_symbol = self.get_right_symbol(x, y)
            
            first_line_str += color(upper_right_symbol, Color.DARKGREY) + "\n"
            second_line_str += color(right_symbol, Color.DARKGREY) + "\n" 
                
            str_board += first_line_str + second_line_str
        
        last_line_str = " "
        for x in range(self.size):
            upper_left_symbol = self.get_upper_left_symbol(x, y+1)
            up_symbol = self.get_up_symbol(x, y+1)
            last_line_str += upper_left_symbol + up_symbol
        upper_right_symbol = self.get_upper_right_symbol(x, y+1)
        last_line_str += upper_right_symbol + "\n"
        
        str_board += color(last_line_str, Color.DARKGREY)
        
        return str_board
    
    def get_right_symbol(self, x: int, y: int) -> str:
        left_id = self.board.get_tile_id_at(x, y)
        if (left_id == -1):
            return " "
        else:
            return "│" 
    
    def get_upper_right_symbol(self, x: int, y: int) -> str:
        upper_left_id = self.board.get_tile_id_at(x, y-1)
        lower_left_id = self.board.get_tile_id_at(x, y)
        
        if (upper_left_id == -1 and lower_left_id == -1):
            return " "
        elif (upper_left_id != -1 and lower_left_id != -1):
            if (upper_left_id == lower_left_id):
                return "│"
            else:
                return "┤"
        elif (upper_left_id == -1 and lower_left_id != -1):
            return "┐"
        else:
            return "┘"
    
    def get_up_symbol(self, x: int, y: int) -> str:
        up_id = self.board.get_tile_id_at(x, y-1)
        down_id = self.board.get_tile_id_at(x, y)
        
        if (up_id == -1 and down_id == -1) or (up_id != -1 and down_id != -1 and up_id == down_id):
            return " "
        else:
            return "─"
    
    def get_left_symbol(self, x: int, y: int) -> str:
        left_id = self.board.get_tile_id_at(x-1, y)
        right_id = self.board.get_tile_id_at(x, y)
        
        if (left_id == -1 and right_id == -1) or (left_id != -1 and right_id != -1 and left_id == right_id):
            return " "
        else:
            return "│"    
        
    def get_upper_left_symbol(self, x: int, y: int) -> str:
        upper_left_id = self.board.get_tile_id_at(x-1, y-1)
        upper_right_id = self.board.get_tile_id_at(x, y-1)
        lower_left_id = self.board.get_tile_id_at(x-1, y)
        lower_right_id = self.board.get_tile_id_at(x, y)
        
        # All empty
        if (upper_left_id == -1 and upper_right_id == -1 and lower_left_id == -1 and lower_right_id == -1):
            return " "
        
        # Only one filled
        elif (upper_left_id == -1 and upper_right_id == -1 and lower_left_id == -1 and lower_right_id != -1):
            return "┌"
        elif (upper_left_id == -1 and upper_right_id == -1 and lower_left_id != -1 and lower_right_id == -1):
            return "┐"
        elif (upper_left_id == -1 and upper_right_id != -1 and lower_left_id == -1 and lower_right_id == -1):
            return "└"
        elif (upper_left_id != -1 and upper_right_id == -1 and lower_left_id == -1 and lower_right_id == -1):
            return "┘"
        
        # Two filled
        elif (upper_left_id == -1 and upper_right_id == -1 and lower_left_id != -1 and lower_right_id != -1):
            if (lower_left_id == lower_right_id):
                return "─"
            else:
                return "┬"
        elif (upper_left_id == -1 and upper_right_id != -1 and lower_left_id == -1 and lower_right_id != -1):
            if (upper_right_id == lower_right_id):
                return "│"
            else:
                return "├"
        elif (upper_left_id != -1 and upper_right_id == -1 and lower_left_id == -1 and lower_right_id != -1):
            return "┼"
        
        elif (upper_left_id == -1 and upper_right_id != -1 and lower_left_id != -1 and lower_right_id == -1):
            return "┼"
        elif (upper_left_id != -1 and upper_right_id == -1 and lower_left_id != -1 and lower_right_id == -1):
            if (upper_left_id == lower_left_id):
                return "│"
            else:
                return "┤"
            
        elif (upper_left_id != -1 and upper_right_id != -1 and lower_left_id == -1 and lower_right_id == -1):
            if (upper_left_id == upper_right_id):
                return "─"
            else:
                return "┴"        
        
        
        # Three filled or three same/one different
        elif (upper_left_id == -1 and upper_right_id != -1 and lower_left_id != -1 and lower_right_id != -1) or (upper_left_id != upper_right_id and upper_left_id != lower_left_id and upper_left_id != lower_right_id and upper_right_id == lower_left_id and upper_right_id == lower_right_id):
            if (upper_right_id == lower_right_id and upper_right_id != lower_left_id):
                return "┤"
            elif (upper_right_id == lower_left_id and upper_right_id != lower_right_id):
                return "┼"
            elif (upper_right_id != lower_right_id and upper_right_id != lower_left_id and lower_right_id == lower_left_id):
                return "┴"
            elif (upper_right_id != lower_right_id and upper_right_id != lower_left_id and lower_right_id != lower_left_id):
                return "┼"
            else:
                return "┘"
        
        elif (upper_left_id != -1 and upper_right_id == -1 and lower_left_id != -1 and lower_right_id != -1) or (upper_right_id != upper_left_id and upper_right_id != lower_left_id and upper_right_id != lower_right_id and upper_left_id == lower_left_id and upper_left_id == lower_right_id):
            if (upper_left_id == lower_left_id and upper_left_id != lower_right_id):
                return "├"
            elif (upper_left_id == lower_right_id and upper_left_id != lower_left_id):
                return "┼"
            elif (upper_left_id != lower_right_id and upper_left_id != lower_left_id and lower_right_id == lower_left_id):
                return "┴"
            elif (upper_left_id != lower_right_id and upper_left_id != lower_left_id and lower_right_id != lower_left_id):
                return "┼"
            else:
                return "└"

        elif (upper_left_id != -1 and upper_right_id != -1 and lower_left_id == -1 and lower_right_id != -1) or (lower_left_id != upper_right_id and lower_left_id != upper_left_id and lower_left_id != lower_right_id and upper_left_id == upper_right_id and upper_left_id == lower_right_id):
            if (upper_left_id == upper_right_id and upper_left_id != lower_right_id):
                return "┬"
            elif (upper_left_id == lower_right_id and upper_left_id != upper_right_id):
                return "┼"
            elif (upper_left_id != lower_right_id and upper_left_id != upper_right_id and lower_right_id == upper_right_id):
                return "┤"
            elif (upper_left_id != lower_right_id and upper_left_id != upper_right_id and lower_right_id != upper_right_id):
                return "┼"
            else:
                return "┐"
            
        elif (upper_left_id != -1 and upper_right_id != -1 and lower_left_id != -1 and lower_right_id == -1) or (lower_right_id != upper_right_id and lower_right_id != lower_left_id and lower_right_id != upper_left_id and upper_left_id == upper_right_id and upper_left_id == lower_left_id):
            if (upper_left_id == upper_right_id and upper_left_id != lower_left_id):
                return "┬"
            elif (upper_left_id == lower_left_id and upper_left_id != upper_right_id):
                return "├"
            elif (upper_left_id != lower_left_id and upper_left_id != upper_right_id and lower_left_id == upper_right_id):
                return "┼"
            elif (upper_left_id != lower_left_id and upper_left_id != upper_right_id and lower_left_id != upper_right_id):
                return "┼"
            else:
                return "┌"
        
        # All filled
        elif (upper_left_id != -1 and upper_right_id != -1 and lower_left_id != -1 and lower_right_id != -1):
            if (upper_left_id == lower_left_id and upper_right_id == lower_right_id and upper_left_id != upper_right_id):
                return "│"
            elif (upper_left_id == lower_left_id and upper_right_id != lower_right_id and upper_left_id != upper_right_id):
                return "├"
            elif (upper_right_id == lower_right_id and upper_left_id != lower_left_id and upper_left_id != upper_right_id):
                return "┤"
            elif (upper_left_id == upper_right_id and lower_left_id == lower_right_id and upper_left_id != lower_left_id):
                return "─"
            elif (upper_left_id == upper_right_id and lower_left_id != lower_right_id and upper_left_id != lower_left_id):
                return "┬"
            elif (lower_left_id == lower_right_id and upper_left_id != upper_right_id and upper_left_id != lower_left_id):
                return "┴"
            elif (upper_left_id == lower_right_id and upper_left_id != upper_right_id) or (upper_right_id == lower_left_id and upper_left_id != upper_right_id):
                return "┼"            
            elif (upper_left_id == upper_right_id and upper_left_id == lower_left_id and upper_left_id == lower_right_id):
                return " "
            elif (upper_left_id != upper_right_id and upper_left_id != lower_left_id and upper_left_id != lower_right_id and upper_right_id != lower_left_id and upper_right_id != lower_right_id and lower_left_id != lower_right_id):
                return "┼"
        
        print("Error: get_upper_left_symbol")
        print("upper_left_id: " + str(upper_left_id))
        print("upper_right_id: " + str(upper_right_id))
        print("lower_left_id: " + str(lower_left_id))
        print("lower_right_id: " + str(lower_right_id))
        return " "