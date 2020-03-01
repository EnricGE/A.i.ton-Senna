from typing import List, Optional

from simulator.car import Car
from simulator.pedestrian import Pedestrian
from simulator.track import Track


class Scene:
    def __init__(self, track_path: str = None):
        self.track: Optional[Track] = None
        self.cars: List[Car] = []
        self.pedestrians: List[Pedestrian] = []

        if track_path is not None:
            self.set_track_path(track_path)

    def update(self, interval: float):
        for pedestrian in self.pedestrians:
            pedestrian.update(interval)

    def gen_pedestrians(self, count: int):
        for i in range(count):
            print(i)

    def set_track_path(self, track_path: str):
        self.set_track(Track(track_path))

    def set_track(self, track: Track):
        self.track = track

    def add_car(self, car: Car):
        self.cars.append(car)
