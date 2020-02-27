import math
from typing import List

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

    def rotate_around(self, position, car_angle):
        nx = math.cos(car_angle) * (self.x - position.x) - math.sin(car_angle) * (self.y - position.y) + position.x
        ny = math.sin(car_angle) * (self.x - position.x) + math.cos(car_angle) * (self.y - position.y) + position.y

        self.x = nx
        self.y = ny

    def add(self, point):
        self.x += point.x
        self.y += point.y

    def sub(self, point):
        self.x -= point.x
        self.y -= point.y

    def distance(self, point):
        return math.hypot(self.x - point.x, self.y - point.y)


class Line:
    def __init__(self, a: Point, b: Point):
        self.a = a
        self.b = b


class Cone:
    def __init__(self, point: Point, color: int):
        self.point: Point = point
        self.color = color

    def copy(self):
        return Cone(Point(self.point.x, self.point.y), self.color)

    def __str__(self):
        return "Point: ({}), Color: {}".format(self.point, self.color)


class Cluster:
    def __init__(self, initial_point: Cone):
        self.position: Point = initial_point.point
        self.points: List[Cone] = [initial_point]
        self.color: int = CONE_COLOR_BLUE

    def recalculate(self):
        """
        Recalculate the colour and mean of this cluster
        :return: how much the mean has moved
        """
        error = 0
        if len(self.points) != 0:
            average_point = Point(0, 0)

            # loop through each point in the current cluster
            blue_count, yellow_count, orange_count, big_orange_count = 0, 0, 0, 0
            for cone in self.points:
                average_point.add(cone.point)

                # increment the count of each colour depending on the colour of the cone
                blue_count += cone.color == CONE_COLOR_BLUE
                yellow_count += cone.color == CONE_COLOR_YELLOW
                orange_count += cone.color == CONE_COLOR_ORANGE
                big_orange_count += cone.color == CONE_COLOR_BIG_ORANGE

            # get the average off
            average_point.x /= len(self.points)
            average_point.y /= len(self.points)

            # update the error and position
            error = self.position.distance(average_point)
            self.position = average_point

            # set the colour of this cluster based upon the amount of colours in this cluster
            if CONE_COLOR_BIG_ORANGE > yellow_count and CONE_COLOR_BIG_ORANGE > blue_count:
                self.color = CONE_COLOR_BIG_ORANGE
            elif CONE_COLOR_ORANGE > yellow_count and CONE_COLOR_ORANGE > blue_count:
                self.color = CONE_COLOR_ORANGE
            elif yellow_count > blue_count:
                self.color = CONE_COLOR_YELLOW
            else:
                self.color = CONE_COLOR_BLUE

        return error
