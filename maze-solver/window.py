from tkinter import Tk, BOTH, Canvas, Frame, Label, Entry, Button, StringVar

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        
        # Control Panel Frame
        self.controls = Frame(self.__root, width=250, bg="#f0f0f0")
        self.controls.pack(side="left", fill="y")
        
        # UI Elements for Maze Parameters
        Label(self.controls, text="Maze Settings", font=("Arial", 12, "bold")).pack(pady=10)

        self.seed = StringVar(value="None")
        Label(self.controls, text="Seed:").pack()
        Entry(self.controls, textvariable=self.seed_var).pack(pady=5)
        
        self.num_rows = StringVar(value="20")
        Label(self.controls, text="Rows:").pack()
        Entry(self.controls, textvariable=self.num_rows).pack(pady=5)
        
        self.num_cols = StringVar(value="30")
        Label(self.controls, text="Cols:").pack()
        Entry(self.controls, textvariable=self.num_cols).pack(pady=5)

        # Action Button
        Button(self.controls, text="Generate & Solve", command=on_generate).pack(pady=20)
        
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.canvas.pack(side="right", fill=BOTH, expand=True)
        
        # State management for the main loop
        self.__running = False
        
        # Connect the window 'X' button to our close method
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """Forces the window to update and render any changes."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """Starts the loop that keeps the window alive."""
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window closed...")

    def close(self):
        """Stops the redraw loop and allows the program to exit."""
        self.__running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self.canvas, fill_color)
