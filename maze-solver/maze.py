import time
from graphics import Cell
import random

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
           random.seed(seed) # Set the seed if provided
            
        self._create_cells()
        self._break_entrance_and_exit() # Added this to automate it
        self._break_walls_r(0, 0)        # Added this to generate the maze
        self._reset_cells_visited()      # Fix the typo here

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self, is_base_step = False, backtrack_factor = 8):
        if self._win is None:
            return
        self._win.redraw()
        # Pull the speed directly from the UI slider
        delay = float(self._win.speed_slider.get())
        delay = delay if(is_base_step) else (delay * backtrack_factor)
        time.sleep(delay)
    
    # Conceptual snippet for your new method
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
    
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # Determine which neighbors to visit
            
            # Left
            if i > 0 and not self._cells[i-1][j].visited:
               i_next = i-1
               next_index_list.append((i_next, j))
            # Right
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
               i_next = i+1
               next_index_list.append((i_next, j))
            # Up
            if j > 0 and not self._cells[i][j - 1].visited:
               j_next = j-1
               next_index_list.append((i, j_next))
            # Down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
               j_next = j+1
               next_index_list.append((i, j_next))

            # If there is nowhere to go, break out
            if len(next_index_list) == 0 or not next_index_list:
               self._draw_cell(i, j)
               return

            # Pick a random direction
            direction_index = random.randrange(len(next_index_list))
            next_i, next_j = next_index_list[direction_index]

            # Knock down walls between current and next cell
            # Right
            if next_i == i + 1:
               self._cells[i][j].has_right_wall = False
               self._cells[next_i][j].has_left_wall = False
            # Left
            if next_i == i - 1:
               self._cells[i][j].has_left_wall = False
               self._cells[next_i][j].has_right_wall = False
            # Down
            if next_j == j + 1:
               self._cells[i][j].has_bottom_wall = False
               self._cells[i][next_j].has_top_wall = False
            # Up
            if next_j == j - 1:
               self._cells[i][j].has_top_wall = False
               self._cells[i][next_j].has_bottom_wall = False

            # Recursively visit the next cell
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False  

    # maze.py

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate(is_base_step = True)
        self._cells[i][j].visited = True

        # If we are at the goal, we are done!
        if i == self._num_cols - 1 and j == self._num_rows - 1:
           return True

        # Directions: Left, Right, Up, Down
        # For each direction, check:
        # 1. Is there a neighbor?
        # 2. Is there NO wall in between?
        # 3. Has the neighbor NOT been visited?

        # Right
        if (i < self._num_cols - 1 and 
            not self._cells[i][j].has_right_wall and 
            not self._cells[i + 1][j].visited):
           
           next_i = i+1 
           self._cells[i][j].draw_move(self._cells[next_i][j])
           if self._solve_r(next_i, j):
              return True
           else:
              self._cells[i][j].draw_move(self._cells[next_i][j], undo=True)
              self._animate(is_base_step=False)

        # Left
        if (i > 0 and 
            not self._cells[i][j].has_left_wall and 
            not self._cells[i - 1][j].visited):
           
           next_i = i-1 
           self._cells[i][j].draw_move(self._cells[next_i][j])
           if self._solve_r(next_i, j):
              return True
           else:
              self._cells[i][j].draw_move(self._cells[next_i][j], undo=True)
              self._animate(is_base_step=False)

        # Down
        if (j < self._num_rows - 1 and 
            not self._cells[i][j].has_bottom_wall and 
            not self._cells[i][j + 1].visited):
            
           next_j = j+1
           self._cells[i][j].draw_move(self._cells[i][next_j])
           if self._solve_r(i, next_j):
              return True
           else:
              self._cells[i][j].draw_move(self._cells[i][next_j], undo=True)
              self._animate(is_base_step=False)

        # Up
        if (j > 0 and 
            not self._cells[i][j].has_top_wall and 
            not self._cells[i][j - 1].visited):

           next_j = j-1 
           self._cells[i][j].draw_move(self._cells[i][next_j])
           if self._solve_r(i, next_j):
              return True
           else:
              self._cells[i][j].draw_move(self._cells[i][next_j], undo=True)
              self._animate(is_base_step=False)

        # No path found from this cell
        return False

