import cv2

from car import Car
from scene import Scene
from simulator.simulator import Simulator

# Set up the basic scene
scene = Scene(track_path="tracks/brands_hatch.json")
scene.add_car(Car())

# render scene as an image for NN - Not Carla
cv2.imshow("", scene.render_track() / 255)
cv2.waitKey(0)


# Add the scene to the carla simulator
simulator = Simulator()
simulator.set_scene(scene)