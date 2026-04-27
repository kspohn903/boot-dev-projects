import sys
from window import Window
from maze import Maze
# from graphics import Cell
# from graphics import Line, Point

sys.setrecursionlimit(5000)

def main(screen_x = 800, screen_y = 600, margin = 50):
    win = None

    def handle_generate():
        # Clear existing canvas if needed (Tkinter: canvas.delete("all"))
        nonlocal win, margin
        
        win.canvas.delete("all")

        # Parse dynamic inputs
        seed_getter = win.seed.get()
        num_rows_getter = win.num_rows.get()
        num_cols_getter = win.num_cols.get()
        
        seed_val = int(seed_getter) if raw_seed.isdigit() else None
        
        try:
            num_rows = int(num_rows_getter)
            num_cols = int(num_cols_getter)
        except ValueError as ve:
            ve.print_exc()
            return 

        cell_size_x = (screen_x - 2 * margin) / num_cols
        cell_size_y = (screen_y - 2 * margin) / num_rows

        # Re-calculate size and initialize
        maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=seed_val)
        maze.solve()

    win = Window(screen_x, screen_y, on_generate=handle_generate)
    win.wait_for_close()


if __name__ == "__main__":
    main()
