class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__min_x = min(x1, x2)
        self.__max_x = max(x1, x2)
        self.__min_y = min(y1, y2)
        self.__max_y = max(y1, y2)
        
        self.__p1 = (self.__min_x, self.__min_y)
        self.__p2 = (self.__max_x, self.__min_y)
        self.__p3 = (self.__max_x, self.__max_y)
        self.__p4 = (self.__min_x, self.__max_y)

    def get_left_x(self):
        return self.__min_x

    def get_right_x(self):
        return self.__max_x

    def get_top_y(self):
        return self.__max_y

    def get_bottom_y(self):
        return self.__min_y

    # don't touch below this line

    def __repr__(self):
        return f"Rectangle({self.__x1}, {self.__y1}, {self.__x2}, {self.__y2})"

