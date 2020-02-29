from scene import Scene
from simulator.simulator import Simulator
from track import Track

track = Track("tracks/brands_hatch.json")
scene = Scene(track)

simulator = Simulator()
simulator.set_scene(scene)
