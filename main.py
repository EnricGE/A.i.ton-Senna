from car import Car
from scene import Scene
from carla.simulator import Simulator

scene = Scene(track_path="tracks/brands_hatch.json")
scene.add_car(Car())

simulator = Simulator()
simulator.set_scene(scene)
