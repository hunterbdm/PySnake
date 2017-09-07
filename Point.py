class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __copy__(self):
        return Point(self.x, self.y)

    def copy(self):
        return self.__copy__()
