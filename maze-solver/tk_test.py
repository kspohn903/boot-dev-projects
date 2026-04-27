from tkinter import Tk, Canvas

root = Tk()
root.title("Maze Solver Test")
canvas = Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Draw a test line from (50, 50) to (350, 350)
canvas.create_line(50, 50, 350, 350, fill="red", width=2)

root.mainloop()
