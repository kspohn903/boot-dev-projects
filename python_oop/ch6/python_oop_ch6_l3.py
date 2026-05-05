class Point():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__p = (self.__x, self.__y)
    
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_point(self):
        return self.__p

    def distance_to(self, other):
        # Euclidean Distance (L2 Norm)
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def taxicab_to(self, other):
        # Taxicab Distance (L1 Norm)
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __repr__(self):
        return f"Point: ({self.get_x()}, {self.get_y()})" 


class Line():
    def __init__(self, p1: Point, p2: Point):
        # Store the Point objects directly
        self.__p1 = p1
        self.__p2 = p2
         
    def get_p1(self):
        return self.__p1

    def get_p2(self):
        return self.__p2

    def length(self):
        # Use the Point's built-in Euclidean distance method
        return self.__p1.distance_to(self.__p2)

    def taxicab_length(self):
        # Use the Point's built-in Taxicab distance method
        return self.__p1.taxicab_to(self.__p2)

    def get_slope(self):
        # Rise over Run: (y2 - y1) / (x2 - x1)
        dx = self.__p2.get_x() - self.__p1.get_x()
        dy = self.__p2.get_y() - self.__p1.get_y()
        
        if dx == 0: 
           # Vertical line has undefined slope
           raise ValueError("ZeroDivisionError has occurred. dx = 0.") 
        
        return dy / dx

    def midpoint(self):
        # Geometric center of the line segment[cite: 11]
        mid_x = (self.__p1.get_x() + self.__p2.get_x()) / 2
        mid_y = (self.__p1.get_y() + self.__p2.get_y()) / 2
        return Point(mid_x, mid_y)

    def __repr__(self):
        return f"Line({self.__p1}, {self.__p2})"

class Rectangle():
    def __init__(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__min_x = min(x1, x2)
        self.__max_x = max(x1, x2)
        self.__min_y = min(y1, y2)
        self.__max_y = max(y1, y2)
        
        # Base Geometric Skeleton; HAS 4 Points
        self.__p1 = Point(self.__min_x, self.__min_y)
        self.__p2 = Point(self.__max_x, self.__min_y)
        self.__p3 = Point(self.__max_x, self.__max_y)
        self.__p4 = Point(self.__min_x, self.__max_y)


    def get_left_x(self):
        return self.__min_x

    def get_right_x(self):
        return self.__max_x

    def get_top_y(self):
        return self.__max_y

    def get_bottom_y(self):
        return self.__min_y

    def contains_point(self, point):
        return (self.get_left_x() <= point.get_x() <= self.get_right_x() and
                self.get_bottom_y() <= point.get_y() <= self.get_top_y())

    def overlaps(self, other_rect):
        # Check if two larger geometric objects intersect
        return not (self.get_right_x() < other_rect.get_left_x() or
                    self.get_left_x() > other_rect.get_right_x() or
                    self.get_top_y() < other_rect.get_bottom_y() or
                    self.get_bottom_y() > other_rect.get_top_y())   

    # don't touch below this line
    def midpoint(self, other):
        # Bisect the distance between two points
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

    def __repr__(self):
        #                      (p1,                       p3)
        return f"Rectangle({self.__x1}, {self.__y1}, {self.__x2}, {self.__y2})"

