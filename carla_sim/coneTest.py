import sys

from simulator.scene import Scene

try:
    sys.path.append('carla_sim\\dist\\carla.egg')
except IndexError:
    pass
import carla


class ConeTest:
    def __init__(self):
        self.__simulator = carla.Client("127.0.0.1", 2000)
        self.__simulator.set_timeout(5.0)
        self.scene = None

    def set_scene(self, scene: Scene):
        self.scene = scene

        # init scene
        import logging
        import random
        number_of_vehicles = 200
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        actor_list = []

        try:
            world = self.__simulator.get_world()
            spawn_points = world.get_map().get_spawn_points()
            number_of_spawn_points = len(spawn_points)
            if number_of_vehicles < number_of_spawn_points:
                random.shuffle(spawn_points)
            elif number_of_vehicles > number_of_spawn_points:
                msg = 'requested %d vehicles, but could only find %d spawn points'
                logging.warning(msg, number_of_vehicles, number_of_spawn_points)
                number_of_vehicles = number_of_spawn_points
            # @todo cannot import these directly.
            SpawnActor = carla.command.SpawnActor
            batch = []

            blueprints = world.get_blueprint_library().filter('static.prop.trafficcone02')
            blueprint = random.choice(blueprints)
            for cone in self.scene.track.blue_cones:
                batch.append(SpawnActor(blueprint, carla.Transform(carla.Location(x=cone.point.x, y=cone.point.y))))

            blueprints = world.get_blueprint_library().filter('static.prop.trafficcone01')
            blueprint = random.choice(blueprints)
            for cone in self.scene.track.yellow_cones:
                batch.append(SpawnActor(blueprint, carla.Transform(carla.Location(x=cone.point.x, y=cone.point.y))))

            for response in self.__simulator.apply_batch_sync(batch):
                if response.error:
                    logging.error(response.error)
                else:
                    actor_list.append(response.actor_id)
            print('spawned %d cones, press Ctrl+C to exit.' % len(actor_list))
            while True:
                world.wait_for_tick()
        finally:
            print('\ndestroying %d actors' % len(actor_list))
            self.__simulator.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
