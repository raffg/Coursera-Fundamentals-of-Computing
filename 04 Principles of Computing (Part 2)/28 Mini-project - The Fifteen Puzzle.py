"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # check that zero is positioned at (i, j)
        if self.get_number(target_row, target_col) != 0:
            return False
        # check that all tiles in rows i + 1 or below are 
        # positioned at their solved location
        for row in range(target_row + 1, self.get_height()):
            for col in range(0, self.get_width()):
                if (row, col) != self.current_position(row, col):
                    return False
        # check that all tiles in row i to the right of position
        # (i,j) are positioned at their solved location
        for col in range(target_col + 1, self.get_width()):
            if (target_row, col) != self.current_position(target_row, col):
                return False
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # check lower_row_invariant
        assert self.lower_row_invariant(target_row, target_col)
        # find location of target tile
        row, col = self.current_position(target_row, target_col)
        
        path = ''
        delta_row = target_row - row
        delta_col = target_col - col
        # move zero to same row and one position to the left of target tile
        if delta_col == 0:
            path += 'u' * delta_row + 'ld'
        elif delta_col > 0:
            path += 'u' * delta_row + 'l' * delta_col
        else:
            path += 'u' * delta_row + 'r' * (-delta_col - 1)
        # move target tile right to target column
        if delta_col > 1:
            path += 'drrul' * (delta_col - 1)
        # move target tile left to target column
        if delta_col < 1:
            path += 'rulld' * (-delta_col)
        # move target tile down to target position
        if delta_row != 0:
            path += 'druld' * (delta_row - 1)
            if delta_col != 0:
                path += 'druld'
        
        print path, 'interior'
        self.update_puzzle(path)
        print self.__str__()
        assert self.lower_row_invariant(target_row, target_col - 1)
        
        return path

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        # find location of target tile
        row, col = self.current_position(target_row, 0)
        
        delta_row = target_row - row
        delta_col = 0 - col
        path = 'ur'
        # if target tile already in position, move zero to far right
        if delta_row == 1 and delta_col == 0:
            path += 'r' * (self.get_width() - 2)
        else:
            # reposition target tile to (i-1,1) and zero to (i-1, 0)
            if delta_col == 0:
                path += 'u' * (delta_row - 1) + 'l' + 'druld' * (delta_row - 1)
            elif delta_col == -1:
                if delta_row == 1:
                    path += 'l'
                else:
                    path += 'u' * (delta_row - 1) + 'ld' + 'druld' * (delta_row - 2)
            elif row == 0:
                path += 'u' * (delta_row - 1) + 'r' * (-delta_col - 2) + 'druld' * (delta_row - 1) + 'rulld' * (-delta_col - 1)
            else:
                path += 'u' * (delta_row - 1) + 'r' * (-delta_col - 2) + 'rulld' * (-delta_col - 1)
            
            # move target tile down to target position
            path += 'ruldrdlurdluurddlur'
            path += 'r' * (self.get_width() - 2)
        
        print path, 'col0'
        self.update_puzzle(path)
        print self.__str__()
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        
        return path

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check that zero is positioned at (0, j)
        if self.get_number(0, target_col) != 0:
            return False
        # check that all tiles in rows > 1 or below are 
        # positioned at their solved location
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (row, col) != self.current_position(row, col):
                    return False
        # check that all tiles in rows 0 to the right of position
        # (0,j) are positioned at their solved location
        for col in range(target_col + 1, self.get_width()):
            if (0, col) != self.current_position(0, col):
                return False
        # check that all tiles in row 1 to the right of position
        # (1,j) are positioned at their solved location
        for col in range(target_col, self.get_width()):
            if (1, col) != self.current_position(1, col):
                return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # check that zero is positioned at (1, j)
        if self.get_number(1, target_col) != 0:
            return False
        # check that all tiles in rows > 1 or below are 
        # positioned at their solved location
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (row, col) != self.current_position(row, col):
                    return False
        # check that all tiles in rows 0 and 1 to the right of position
        # (1,j) are positioned at their solved location
        for col in range(target_col + 1, self.get_width()):
            if (0, col) != self.current_position(0, col):
                return False
            if (1, col) != self.current_position(1, col):
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        
        # find location of target tile
        row, col = self.current_position(0, target_col)
        delta_row = 0 - row
        delta_col = target_col - col
        path = ''
        
        # check target tile is at position (0,j)
        if row == 0 and col == target_col - 1:
            path = 'ld'
        else:
            #reposition target tile to position (1,j-1) with zero in (1,j-2)
            if delta_row == -1 and delta_col == 1:
                path += 'lld'
            else:
                path += 'ld' + 'l' * (delta_col - 1)
                if row == 0:
                    path += 'urdl'
                if delta_col > 2:
                    path += 'urrdl' * (delta_col - 2)
            path += 'urdlurrdluldrruld'
        
        print path, 'row0'
        self.update_puzzle(path)
        print self.__str__()
        assert self.row1_invariant(target_col - 1)
        return path

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        
        # find location of target tile
        row, col = self.current_position(1, target_col)
        
        path = ''
        delta_col = target_col - col
        # move target tile to row 1 and position zero to its left
        path += 'l'  * delta_col
        if row == 0 and delta_col != 0:
            path += 'urdl'
        # move target tile to target position with zero above
        if row == 0 and delta_col == 0:
            path += 'u'
        else:
            path += 'urrdl' * (delta_col - 1) + 'ur'
        
        print path, 'row1'
        self.update_puzzle(path)
        print self.__str__()
        assert self.row0_invariant(target_col)
        return path

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        row, col = self.current_position(0, 1)
        assert self.row1_invariant(1)
        if (row, col) == (0, 0):
            path = 'ul'
        elif (row, col) == (0, 1):
            path = 'lu'
        elif (row, col) == (1, 0):
            path = 'lurdlu'
        print path, '2x2'
        self.update_puzzle(path)
        print self.__str__()
        return path

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # check if puzzle is in solved position
        zero_row, zero_col = self.current_position(0, 0)
        height = self.get_height()
        width = self.get_width()
        # check if puzzle is in solved position
        flag = 'solved'
        for col in range(width):
            for row in range(height):
                if (row, col) != self.current_position(row, col):
                    flag = 'unsolved'
                    break
        if flag == 'solved':
            return ''
        # move zero to bottom right corner
        path = 'd' * (height - zero_row - 1) + 'r' * (width - zero_col - 1)
        print path, 'bottom right'
        self.update_puzzle(path)
        # solve bottom m-2 rows from right to left and bottom to top
        for row in range(height - 1, 1, -1):
            for col in range(width - 1, 0, -1):
                path += self.solve_interior_tile(row, col)
            path += self.solve_col0_tile(row)
        print path, 'm-2'
        # solve right n-2 columns of top 2 rows bottom to top and right to left
        for col in range(width - 1, 1, -1):
            path += self.solve_row1_tile(col)
            path += self.solve_row0_tile(col)
        print path, 'n-2'
        # solve remaining 2x2 puzzle
        path += self.solve_2x2()
        
        print path, '2x2'
        print self.__str__()
        return path

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

# Testing

# lower_row_invariant(self, target_row, target_col)
#obj = Puzzle(4, 4, [[8,1,2,3],[9,6,4,7],[5,0,10,11],[12,13,14,15]])
#print obj.lower_row_invariant(2, 1)
#print ""

# solve_interior_tile(self, target_row, target_col)
#obj = Puzzle(4, 4, [[8,1,2,3],[9,6,4,7],[5,0,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_interior_tile(2, 1)
#print ""

#obj = Puzzle(4, 4, [[8,1,2,3],[7,6,4,9],[5,0,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_interior_tile(2, 1)
#print ""

# solve_col0_tile(self, target_row)
#obj = Puzzle(4, 4, [[7,1,2,3],[8,6,4,5],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

#obj = Puzzle(4, 4, [[8,1,2,3],[7,6,4,5],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

#obj = Puzzle(4, 4, [[3,1,2,8],[7,6,4,5],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

#obj = Puzzle(4, 4, [[3,1,2,5],[7,6,4,8],[0,9,10,11],[12,13,14,15]])
#print obj.__str__()
#print obj.solve_col0_tile(2)
#print ""

# row1_invariant(self, target_col)
#obj = Puzzle(4, 4, [[4,1,2,3],[5,0,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row1_invariant(1)
#print ""

# row1_invariant(self, target_col)
#obj = Puzzle(4, 4, [[4,1,2,3],[0,5,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row1_invariant(0)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(4, 4, [[2,1,0,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row0_invariant(2)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(4, 4, [[3,1,2,0],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
#print obj.row0_invariant(3)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(3, 3, [[3, 0, 2], [1, 4, 5], [6, 7, 8]])
#print obj.row0_invariant(1)
#print ""

# row0_invariant(self, target_col)
#obj = Puzzle(4, 5, [[7, 2, 0, 3, 4], [5, 6, 1, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.row0_invariant(2)
#print ""

# solve_row0_tile(self, target_col)
#obj = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_row0_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_row1_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 4], [2, 1, 0, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_row1_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_row1_tile(2)
#print ""

# solve_row1_tile(self, target_col)
#obj = Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_row1_tile(4)
#print ""

# solve_2x2(self)
#obj = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_2x2()
#print ""

# solve_puzzle(self)
#obj = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_interior_tile(self, target_row, target_col)
#obj = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#print obj.__str__()
#print obj.solve_interior_tile(2, 1)
#print ""

# solve_puzzle(self)
#obj = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_puzzle(self)
#obj = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_puzzle(self)
#obj = Puzzle(2, 4, [[0, 3, 2, 7], [4, 5, 6, 1]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""

# solve_puzzle(self)
#obj = Puzzle(3, 6, [[16, 7, 13, 17, 5, 9], [3, 0, 14, 10, 12, 6], [4, 15, 2, 11, 8, 1]])
#print obj.__str__()
#print obj.solve_puzzle()
#print ""