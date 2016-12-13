"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # initialization
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        max_distance = grid_height * grid_width
        visited = poc_grid.Grid(grid_height, grid_width)
        distance_field = [[max_distance for _ in range(grid_width)] 
                                       for _ in range(grid_height)]
        
        boundary = poc_queue.Queue()
        if entity_type is ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        elif entity_type is HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        
        # Breadth-First Search
        while boundary:
            current = boundary.dequeue()
            distance = distance_field[current[0]][current[1]]
            for neighbor in visited.four_neighbors(current[0], current[1]):
                if visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance + 1
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for idx, human in enumerate(self.humans()):
            candidate = human
            dist = zombie_distance_field[human[0]][human[1]]
            neighbors = self.eight_neighbors(human[0], human[1])
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    new_dist = zombie_distance_field[neighbor[0]][neighbor[1]]
                    if new_dist > dist:
                        candidate = neighbor
                        dist = new_dist
            self._human_list[idx] = candidate
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for idx, zombie in enumerate(self.zombies()):
            candidate = zombie
            dist = human_distance_field[zombie[0]][zombie[1]]
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            random.shuffle(neighbors)
            for neighbor in neighbors:
                if self.is_empty(neighbor[0], neighbor[1]):
                    new_dist = human_distance_field[neighbor[0]][neighbor[1]]
                    if new_dist < dist:
                        candidate = neighbor
                        dist = new_dist
            self._zombie_list[idx] = candidate

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
