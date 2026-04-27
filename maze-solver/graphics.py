class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x, self.p1.y, 
            self.p2.x, self.p2.y, 
            fill=fill_color, 
            width=2
        )

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        # Left wall
        line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        if self.has_left_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")

        # Top wall
        line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        if self.has_top_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")

        # Right wall
        line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        if self.has_right_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")

        # Bottom wall
        line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        if self.has_bottom_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
           return
    
        # Calculate centers of the current cell
        x_mid = (self._x1 + self._x2) / 2
        y_mid = (self._y1 + self._y2) / 2

        # Calculate centers of the destination cell
        to_x_mid = (to_cell._x1 + to_cell._x2) / 2
        to_y_mid = (to_cell._y1 + to_cell._y2) / 2

        fill_color = "red"
        if undo:
            fill_color = "gray"

        # Draw the line between the two centers
        line = Line(Point(x_mid, y_mid), Point(to_x_mid, to_y_mid))
        self._win.draw_line(line, fill_color) 
    
