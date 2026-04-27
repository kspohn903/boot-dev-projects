import unittest
from maze import Maze
import sys

# Set the limit here so the test environment can handle the 50x50 grid
sys.setrecursionlimit(5000)

class Tests(unittest.TestCase):
    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        # Manually "visit" some cells
        m1._cells[0][0].visited = True
        m1._cells[5][5].visited = True
    
        m1._reset_cells_visited()
    
        self.assertEqual(m1._cells[0][0].visited, False)
        self.assertEqual(m1._cells[5][5].visited, False)

    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        # Using single underscore since that's what we used in the snippets
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_create_cells_large(self):
        num_cols = 50
        num_rows = 50
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        self.assertEqual(m1._cells[0][0].has_top_wall, False)
        self.assertEqual(m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall, False)

if __name__ == "__main__":
    unittest.main()
