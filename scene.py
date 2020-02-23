from track import Track


class Scene:
    def __init__(self, track_path):
        self.track = Track(track_path)
        self.cars = []
