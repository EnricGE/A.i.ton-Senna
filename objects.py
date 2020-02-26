CONE_COLOR_BLUE = 0
CONE_COLOR_YELLOW = 1
CONE_COLOR_BIG_ORANGE = 2
CONE_COLOR_ORANGE = 3


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return "x: {}, y: {}".format(self.x, self.y)


class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b


class Cone:
    def __init__(self, point: Point, color: int):
        self.point: Point = point
        self.color = color

    def __str__(self):
        return "Point: ({}), Color: {}".format(self.point, self.color)
