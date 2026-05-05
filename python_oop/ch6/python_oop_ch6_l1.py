class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.p1 = (x1, y1)
        self.x2 = x2
        self.y2 = y2
        self.p2 = (x2, y2)
     
    def get_p1(self):
        return self.p1

    def get_p2(self):
        return self.p2

