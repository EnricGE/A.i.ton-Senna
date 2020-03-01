from simulator.objects import Point


class Car:
    def __init__(
            self,
            pos: Point = Point(0, 0),
            orientation: float = 0,
            width: float = 1,
            length: float = 2.5,
            max_rpm: int = 10000,
            mass: float = 1000  # kg
    ):
        self.orientation = orientation
        self.pos = pos
        self.width = width  # meters
        self.length = length

        self.max_rpm = max_rpm
        self.mass = mass
