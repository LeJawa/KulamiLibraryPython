### Board generation steps
# Iterate over all position from -n to n in both x and y
# For each position, calculate the weight of the position
#  - The weight is the distance from (0,0)
# Order the positions by weight in ascending order
# Shuffle the tiles
# While not all tiles are placed and there are still positions left
#  - Try to place the next tile in the position with the lowest weight
#    - Check all possible rotations and translations
#  - If a tile can be placed, place it and remove the position from the list
#  - If a tile cannot be placed, try the next tile

from position import Pos
    
class Board:
    def __init__(self, size: int) -> None: 
        self.size: int = size
        self.positions: list[Pos] = []       
        self.generate_positions()

    def generate_positions(self):
        self.positions.clear()
        for x in range(-self.size, self.size+1):
            for y in range(-self.size, self.size+1):
                self.positions.append(Pos(x, y))

    def get_sorted_positions(self) -> list[Pos]:
        sorted_positions = self.positions.copy()
        sorted_positions.sort(key=lambda pos: pos.calculate_weight())
        return sorted_positions
        
    def __str__(self) -> str:
        board_size = int(self.size * 2 + 1)
        str_size = board_size * 2 + 1
        str_board = ""   
    
        for y in range(-self.size, self.size+1):
            first_line_str = ""
            second_line_str = ""
            for x in range(-self.size, self.size+1):
                upper_left_symbol = self.get_upper_left_symbol(x, y)
                up_symbol = self.get_up_symbol(x, y)
                left_symbol = self.get_left_symbol(x, y)                
                pos_symbol = Pos.get_symbol(self.get_id(x, y))
                
                first_line_str += upper_left_symbol + up_symbol
                second_line_str += left_symbol + pos_symbol
            
            upper_right_symbol = self.get_upper_right_symbol(x, y)
            right_symbol = self.get_right_symbol(x, y)
            
            first_line_str += upper_right_symbol + "\n"
            second_line_str += right_symbol + "\n"
                
            str_board += first_line_str + second_line_str
        
        last_line_str = ""
        for x in range(-self.size, self.size+1):
            upper_left_symbol = self.get_upper_left_symbol(x, y+1)
            up_symbol = self.get_up_symbol(x, y+1)
            last_line_str += upper_left_symbol + up_symbol
        upper_right_symbol = self.get_upper_right_symbol(x, y+1)
        last_line_str += upper_right_symbol + "\n"
        
        str_board += last_line_str
        
        return str_board
    
    def get_right_symbol(self, x: int, y: int) -> str:
        left_id = self.get_id(x, y)
        if (left_id == -1):
            return " "
        else:
            return "│" 
    
    def get_upper_right_symbol(self, x: int, y: int) -> str:
        upper_left_id = self.get_id(x, y-1)
        lower_left_id = self.get_id(x, y)
        
        if (upper_left_id == -1 and lower_left_id == -1):
            return " "
        elif (upper_left_id != -1 and lower_left_id != -1):
            return "│"
        elif (upper_left_id == -1 and lower_left_id != -1):
            return "┐"
        else:
            return "┘"
    
    def get_up_symbol(self, x: int, y: int) -> str:
        up_id = self.get_id(x, y-1)
        down_id = self.get_id(x, y)
        
        if (up_id == -1 and down_id == -1) or (up_id != -1 and down_id != -1 and up_id == down_id):
            return " "
        else:
            return "─"
    
    def get_left_symbol(self, x: int, y: int) -> str:
        left_id = self.get_id(x-1, y)
        right_id = self.get_id(x, y)
        
        if (left_id == -1 and right_id == -1) or (left_id != -1 and right_id != -1 and left_id == right_id):
            return " "
        else:
            return "│"    
        
    def get_upper_left_symbol(self, x: int, y: int) -> str:
        upper_left_id = self.get_id(x-1, y-1)
        upper_right_id = self.get_id(x, y-1)
        lower_left_id = self.get_id(x-1, y)
        lower_right_id = self.get_id(x, y)
        
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
        
        print("Error: get_upper_left_symbol")
        print("upper_left_id: " + str(upper_left_id))
        print("upper_right_id: " + str(upper_right_id))
        print("lower_left_id: " + str(lower_left_id))
        print("lower_right_id: " + str(lower_right_id))
        return " "
   
    def get_id(self, x: int, y: int) -> int:
        if (x < -self.size or x > self.size or y < -self.size or y > self.size):
            return -1        
        
        board_size = int(self.size * 2 + 1)
        return self.positions[ (x+self.size)*board_size + (y + self.size) ].id

board = Board(15)
board.generate_positions()


print(board)