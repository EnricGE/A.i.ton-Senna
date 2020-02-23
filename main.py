from scene import Scene
import renderer

scene: Scene = Scene("tracks/circuit_de_barcelona.json")
renderer.render_scene(scene)


