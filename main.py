import time
from threading import Thread

import cv2

import renderer
from car import Car
from scene import Scene
from simulator.simulator import Simulator

# Set up the basic scene
from track import Track


track = Track("tracks/brands_hatch.json")
car = Car(pos=track.car_pos)

scene = Scene()
scene.set_track(track)
scene.add_car(car)


def run_rl():
    for i in range(100):
        cv2.imshow("", renderer.render_scene(scene) / 255)
        cv2.waitKey(0)


def run_carla_simulator():
    simulator = Simulator()
    simulator.set_scene(scene)


Thread(target=run_rl).start()
Thread(target=run_carla_simulator).start()
