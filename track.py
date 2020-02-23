import json
from scipy.spatial import Delaunay, Voronoi
import numpy as np

from objects import Point, Cone


class Track:
    def __init__(self, track_path):
        with open(track_path, "r") as track_file:
            track = json.loads(track_file.read())

            self.blue_cones = [Cone(Point(cone["x"], cone["y"]), 0) for cone in track["blue_cones"]]
            self.yellow_cones = [Cone(Point(cone["x"], cone["y"]), 1) for cone in track["yellow_cones"]]
            self.big_orange_cones = [Cone(Point(cone["x"], cone["y"]), 2) for cone in track["big_orange_cones"]]
            self.orange_cones = [Cone(Point(cone["x"], cone["y"]), 3) for cone in track["orange_cones"]]

            self.all_cones = self.blue_cones + self.yellow_cones
            self.delaunay = Delaunay(
                np.asarray([[cone.point.x, cone.point.y] for cone in self.all_cones])
            )

    def get_delaunay(self):
        valid_triangles = []
        invalid_triangles = []

        connected_indexes = set()
        loose_indexes = set([i for i in range(len(self.all_cones))])

        for triangle in self.delaunay.simplices:
            cone_a = self.all_cones[triangle[0]]
            cone_b = self.all_cones[triangle[1]]
            cone_c = self.all_cones[triangle[2]]

            if not (cone_a.color == cone_b.color and cone_b.color == cone_c.color):
                valid_triangles.append(triangle)
                for index in triangle:
                    if index in loose_indexes:
                        loose_indexes.remove(index)
                    connected_indexes.add(index)
            else:
                invalid_triangles.append(triangle)

        purple_triangles = []
        surrounding_triangles = []

        for i in range(1):
            for index in loose_indexes:
                print("------- Index: {}, Color: {} ------".format(index, self.all_cones[index].color))
                # search for potential triangles by searching through invalid triangles
                for potential_triangle in [triangle for triangle in invalid_triangles if index in triangle]:
                    print("    Current triangle: {}".format(potential_triangle))
                    for connected_triangle in valid_triangles:
                        if have_shared_edge(connected_triangle, potential_triangle):
                            purple_triangles.append(connected_triangle)

        return connected_indexes, loose_indexes, valid_triangles, invalid_triangles, purple_triangles, surrounding_triangles


def have_shared_edge(triangle_a, triangle_b):
    connected_vertices = 0
    if triangle_a[0] in triangle_b: connected_vertices += 1
    if triangle_a[1] in triangle_b: connected_vertices += 1
    if triangle_a[2] in triangle_b: connected_vertices += 1
    return connected_vertices == 2

