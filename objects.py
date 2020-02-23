

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Cone:
    def __init__(self, point: Point, color: int):
        self.point: Point = point
        self.color = color
