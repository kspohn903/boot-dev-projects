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

    def overlaps(self, rect):
        # Check if they are separated. If any of these are true, they do NOT overlap.
        # Then we return the opposite (not).
        return not (
            self.get_left_x() > rect.get_right_x() or  # This is too far right
            self.get_right_x() < rect.get_left_x() or  # This is too far left
            self.get_bottom_y() > rect.get_top_y() or  # This is too far up
            self.get_top_y() < rect.get_bottom_y()     # This is too far down
        ) 

    # don't touch below this line
    def midpoint(self, other):
        # Bisect the distance between two points
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

    def __repr__(self):
        #                      (p1,                       p3)
        return f"Rectangle({self.__x1}, {self.__y1}, {self.__x2}, {self.__y2})"

class Unit():
    def __init__(self, name, pos_x, pos_y):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.__p = (self.pos_x, self.pos_y)

    def get_name(self):
        return self.name

    def get_pos_x(self):
        return self.pos_x

    def get_pos_y(self):
        return self.pos_y
    
    #                 p1 = (x1,y1), p2 = (x2, y2)
    def in_area(self, x1, y1, x2, y2): 
        # HAS 2 Points
        # x1, y1 = p1[0], p1[1]
        # x2, y2 = p2[0], p2[1]
        min_x = min(x1, x2)
        max_x = max(x1, x2)
        min_y = min(y1, y2)
        max_y = max(y1, y2)
        return ( 
            self.pos_x >= min_x and self.pos_x <= max_x and
            self.pos_y >= min_y and self.pos_y <= max_y
        )


    def __repr__(self):
        return f"Unit({self.__name}, {self.__pos_x}, {self.__pos_y})"

# don't touch above this line
class Dragon(Unit):
    def __init__(self, name, pos_x, pos_y, height, width, fire_range):
        super().__init__(name, pos_x, pos_y)
        self.height = height
        self.width = width
        self.fire_range = fire_range
        
        # Calculate corners based on pos_x/pos_y being the center point
        left_x = pos_x - (width / 2)
        bottom_y = pos_y - (height / 2)
        right_x = pos_x + (width / 2)
        top_y = pos_y + (height / 2)
        
        # Create the private __hit_box member
        self.__hit_box = Rectangle(left_x, bottom_y, right_x, top_y)
    
    def in_area(self, x1, y1, x2, y2):
        # Create a new rectangle for the target area
        target_area = Rectangle(x1, y1, x2, y2)
        
        # Check if the dragon's hit box overlaps with the target area
        return self.__hit_box.overlaps(target_area)
