import os

from scene import Scene
import renderer

paths = os.listdir("tracks/")
for path in [
    1, 2, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 23, 24, 27, 28, 29, 30, 32, 33, 34, 35,
    38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53
]:
    print(path)
    scene: Scene = Scene("tracks/" + paths[path])

    # renderer.render_scene(scene, my_method=False)
    renderer.render_scene(scene)
