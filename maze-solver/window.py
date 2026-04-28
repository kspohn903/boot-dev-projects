from tkinter import Tk, BOTH, Canvas, Frame, Label, Spinbox, Scale, HORIZONTAL, StringVar, Entry, Button
class Window:
    def __init__(self, width, height, on_generate):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.on_generate = on_generate # Store the callback
        
        # Control Panel Frame
        self.controls = Frame(self.__root, width=250, bg="#f0f0f0")
        self.controls.pack(side="left", fill="y")
        
        # UI Elements for Maze Parameters
        Label(self.controls, text="Maze Settings", font=("Arial", 12, "bold")).pack(pady=10)

        self.seed = StringVar(value="None")
        Label(self.controls, text="Seed:").pack()
        Entry(self.controls, textvariable=self.seed).pack(pady=5)
       
        # Spinbox for Rows (1 to 50)
        Label(self.controls, text="Rows:").pack()
        self.num_rows = Spinbox(self.controls, from_=1, to=50, width=5)
        self.num_rows.delete(0, "end")
        self.num_rows.insert(0, "20")
        self.num_rows.pack(pady=5)

        # Spinbox for Cols (1 to 50)
        Label(self.controls, text="Cols:").pack()
        self.num_cols = Spinbox(self.controls, from_=1, to=50, width=5)
        self.num_cols.delete(0, "end")
        self.num_cols.insert(0, "30")
        self.num_cols.pack(pady=5)

        # Speed Slider (0.0s to 0.1s)
        Label(self.controls, text="Animation Delay (sec):").pack(pady=(10, 0))
        self.speed_slider = Scale(self.controls, from_=0.0, to=0.1, resolution=0.01, orient=HORIZONTAL)
        self.speed_slider.set(0.05)
        self.speed_slider.pack(pady=5)

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
