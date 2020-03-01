import sys

from simulator.scene import Scene

try:
    sys.path.append('simulator\\dist\\carla.egg')
except IndexError:
    pass
import carla


class Simulator:
    def __init__(self):
        self.__simulator = carla.Client("127.0.0.1", 2000)
        self.__simulator.set_timeout(2.0)
        self.scene = None

    def set_scene(self, scene: Scene):
        self.scene = scene

        # init scene
        import argparse
        import logging
        import random
        argparser = argparse.ArgumentParser(
            description=__doc__)
        argparser.add_argument(
            '-n', '--number-of-vehicles',
            metavar='N',
            default=200,
            type=int,
            help='number of vehicles (default: 10)')
        argparser.add_argument(
            '-d', '--delay',
            metavar='D',
            default=2.0,
            type=float,
            help='delay in seconds between spawns (default: 2.0)')
        argparser.add_argument(
            '--safe',
            action='store_true',
            help='avoid spawning vehicles prone to accidents')
        args = argparser.parse_args()
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        actor_list = []

        try:
            world = self.__simulator.get_world()
            blueprints = world.get_blueprint_library().filter('vehicle.*')
            if args.safe:
                blueprints = [x for x in blueprints if int(x.get_attribute('number_of_wheels')) == 3]
                blueprints = [x for x in blueprints if not x.id.endswith('isetta')]
                blueprints = [x for x in blueprints if not x.id.endswith('carlacola')]
            spawn_points = world.get_map().get_spawn_points()
            number_of_spawn_points = len(spawn_points)
            if args.number_of_vehicles < number_of_spawn_points:
                random.shuffle(spawn_points)
            elif args.number_of_vehicles > number_of_spawn_points:
                msg = 'requested %d vehicles, but could only find %d spawn points'
                logging.warning(msg, args.number_of_vehicles, number_of_spawn_points)
                args.number_of_vehicles = number_of_spawn_points
            # @todo cannot import these directly.
            SpawnActor = carla.command.SpawnActor
            SetAutopilot = carla.command.SetAutopilot
            FutureActor = carla.command.FutureActor
            batch = []
            for n, transform in enumerate(spawn_points):
                if n >= args.number_of_vehicles:
                    break
                blueprint = random.choice(blueprints)
                if blueprint.has_attribute('color'):
                    color = random.choice(blueprint.get_attribute('color').recommended_values)
                    blueprint.set_attribute('color', color)
                blueprint.set_attribute('role_name', 'autopilot')
                batch.append(SpawnActor(blueprint, transform).then(SetAutopilot(FutureActor, True)))
            for response in self.__simulator.apply_batch_sync(batch):
                if response.error:
                    logging.error(response.error)
                else:
                    actor_list.append(response.actor_id)
            print('spawned %d vehicles, press Ctrl+C to exit.' % len(actor_list))
            while True:
                world.wait_for_tick()
        finally:
            print('\ndestroying %d actors' % len(actor_list))
            self.__simulator.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
