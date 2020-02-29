from typing import List, Optional

from car import Car
from track import Track


class Scene:
    def __init__(self, track_path: str = None):
        self.track: Optional[Track] = None
        self.cars: List[Car] = []

        if track_path is not None:
            self.set_track_path(track_path)

    def set_track_path(self, track_path: str):
        self.set_track(Track(track_path))

    def set_track(self, track: Track):
        self.track = track

    def add_car(self, car: Car):
        self.cars.append(car)
