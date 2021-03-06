from threading import Thread

import cv2

from simulator import renderer
from simulator.car import Car
from simulator.scene import Scene
from carla_sim.coneTest import ConeTest

# Set up the basic scene
from simulator.track import Track


track = Track("tracks/brands_hatch.json")
car = Car(pos=track.car_pos)

scene = Scene()
scene.set_track(track)
scene.add_car(car)
scene.gen_pedestrians(200)


def run_rl():
    cv2.imshow("", renderer.render_scene(scene) / 255)
    cv2.waitKey(0)


def run_carla_simulator():
    simulator = ConeTest()
    simulator.set_scene(scene)


Thread(target=run_rl).start()
Thread(target=run_carla_simulator).start()