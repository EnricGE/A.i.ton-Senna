import math
import random

from simulator.objects import Point


MAX_TARGET_POINT_DISTANCE = 20
MIN_TARGET_POINT_DISTANCE = 6

MAX_COOL_DOWN = 10  # seconds
MIN_COOL_DOWN = 4


class Pedestrian:
    def __init__(self, pos: Point, has_ai=False):
        self.has_ai = has_ai
        self.pos = pos

        self.__target_pos = pos
        self.__target_point_cooldown = 0

    def update(self, interval_time):
        if self.has_ai:
            self.__target_point_cooldown -= interval_time
            if self.__target_point_cooldown <= 0:
                self.__target_point_cooldown = random.random() * (MAX_COOL_DOWN - MIN_COOL_DOWN) + MIN_COOL_DOWN
                self.__target_pos = self.new_target_point()

    def new_target_point(self) -> Point:
        angle = random.random()
        radius = random.random() * (MAX_TARGET_POINT_DISTANCE - MIN_TARGET_POINT_DISTANCE) + MIN_TARGET_POINT_DISTANCE
        return Point(0, 0)