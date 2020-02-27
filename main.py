import os

from scene import Scene
import renderer

paths = os.listdir("tracks/")
for path in paths:
    scene: Scene = Scene("tracks/" + path)

    # renderer.render_scene(scene, my_method=False)
    renderer.render_scene(scene)
