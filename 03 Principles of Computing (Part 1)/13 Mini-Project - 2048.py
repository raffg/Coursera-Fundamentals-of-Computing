"""
Clone of 2048 game.
"""

import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    new_line = [item for item in line if item] + [0]*line.count(0)
    for _item in range(len(new_line)-1):
        if new_line[_item] == new_line[_item+1]:
            new_line[_item] *= 2
            new_line[_item+1] = 0
    new_line = [item for item in new_line if item] + [0]*new_line.count(0)
    return new_line

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._initial_tiles = {
            UP: [(0, col) for col in range(grid_width)],
            DOWN: [(grid_height - 1, col) for col in range(grid_width)],
            LEFT: [(row, 0) for row in range(grid_height)],
            RIGHT: [(row, grid_width - 1) for row in range(grid_height)]
        }
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # Create a rectangular grid using nested list comprehension 
        # Inner comprehension creates a single row
        self._grid = [[0 for _col in range(self._grid_width)] 
                        for _row in range(self._grid_height)]
        
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_string = ""
        for row in self._grid:
            grid_string += str(row) + "\n"
        return grid_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        if direction in [UP, DOWN]:
            num_steps = self._grid_height
        elif direction in [LEFT, RIGHT]:
            num_steps = self._grid_width
        
        changed = False
        
        for cell in self._initial_tiles[direction]:
            tmp_list = self.traverse_grid(cell, OFFSETS[direction], num_steps)
            merged_list = merge(tmp_list)
            if merged_list != tmp_list:
                changed = True
            self.change_grid(cell, OFFSETS[direction], merged_list)                
        if changed:
            self.new_tile()

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        value = 2 if random.random() < 0.9 else 4
        
        row = random.randrange(self._grid_height)
        col = random.randrange(self._grid_width)
        
        while self.get_tile(row, col) != 0:
            row = random.randrange(self._grid_height)
            col = random.randrange(self._grid_width)
        
        self.set_tile(row, col, value)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]
    
    def traverse_grid(self, start_cell, direction, num_steps):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        Both start_cell is a tuple(row, col) denoting the
        starting cell

        direction is a tuple that contains difference between
        consecutive cells in the traversal
        """
        
        return [self._grid[start_cell[0] + step * direction[0]][start_cell[1] + step * direction[1]] for step in range(num_steps)]

    
    def change_grid(self, start_cell, direction, new_list):
        """
        Function like traverse_grid, but modifies the original
        grid as it iterates
        """
        
        for step in range(len(new_list)):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            self._grid[row][col] = new_list[step]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))