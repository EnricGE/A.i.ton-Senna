import json
import math
from typing import List

from scipy.spatial import Delaunay
import numpy as np

from objects import *


class Track:
    def __init__(self, track_path):
        with open(track_path, "r") as track_file:
            track = json.loads(track_file.read())

            # self.cone_type = Cone[]
            self.blue_cones = [Cone(Point(cone["x"], cone["y"]), CONE_COLOR_BLUE) for cone in track["blue_cones"]]
            self.yellow_cones = [Cone(Point(cone["x"], cone["y"]), CONE_COLOR_YELLOW) for cone in track["yellow_cones"]]
            self.orange_cones = [Cone(Point(cone["x"], cone["y"]), CONE_COLOR_ORANGE) for cone in track["orange_cones"]]
            self.big_orange_cones = merge_big_orange_cones(
                [Cone(Point(cone["x"], cone["y"]), CONE_COLOR_BIG_ORANGE) for cone in track["big_orange_cones"]]
            )

    def __get_delauny_map(self):
        all_cones = self.blue_cones + self.yellow_cones + self.big_orange_cones

        delaunay = Delaunay(np.asarray([[cone.point.x, cone.point.y] for cone in all_cones]))
        # convert triangles from list of indexes to list of cones
        delaunay = [[all_cones[tri[0]], all_cones[tri[1]], all_cones[tri[2]]] for tri in delaunay.simplices]

        return all_cones, delaunay

    def create_delaunay_graph(self):
        triangles, invalid = [], []

        all_cones, delaunay = self.__get_delauny_map()
        missed_cones = set(all_cones)

        for triangle in delaunay:
            cone_a, cone_b, cone_c = triangle[0], triangle[1], triangle[2]
            triangle_colours = [cone_a.color, cone_b.color, cone_c.color]

            # bool statements to check if a triangle is part of the track
            orange_pair = triangle_colours.count(CONE_COLOR_BIG_ORANGE) == 2
            all_mixed = CONE_COLOR_BIG_ORANGE in triangle_colours and CONE_COLOR_BLUE in triangle_colours and CONE_COLOR_YELLOW in triangle_colours
            two_blue = triangle_colours.count(CONE_COLOR_BLUE) == 2 and CONE_COLOR_YELLOW in triangle_colours
            two_yellow = triangle_colours.count(CONE_COLOR_YELLOW) == 2 and CONE_COLOR_BLUE in triangle_colours

            # if triangle meets criteria then add add to valid triangles
            if (orange_pair or all_mixed or two_blue or two_yellow):
                triangles.append(triangle)
                if cone_a in missed_cones: missed_cones.remove(cone_a)
                if cone_b in missed_cones: missed_cones.remove(cone_b)
                if cone_c in missed_cones: missed_cones.remove(cone_c)
            else:
                invalid.append(triangle)

        potential_triangles = []

        # # add missing cones to the graph
        # for cone in list(missed_cones):
        #     plausable_triangles = []
        #     for triangle in delaunay:
        #         if cone in triangle and get_min_angle_in_triangle(triangle) > 20:
        #             other_vertecies = list(triangle)
        #             other_vertecies.remove(cone)
        #             if other_vertecies[0] not in missed_cones and other_vertecies[1] not in missed_cones:
        #                 for valid in triangles:
        #                     has_both = other_vertecies[0] in valid and other_vertecies[1] in valid
        #                     if has_both: plausable_triangles.append(triangle)
        #             else:
        #                 plausable_triangles.append(triangle)
        #
        #     triangle = get_best_triangle(cone, missed_cones, plausable_triangles)
        #     if triangle is not None:
        #         potential_triangles.append(triangle)

        return triangles, invalid, potential_triangles


def get_best_triangle(cone: Cone, missed_cones, potential_triangles: List[List[Cone]]):
    heuristic_to_triangle = []
    count = 0
    for triangle in potential_triangles:

        count += 1
        triangle_vertices = [vertex for vertex in triangle if cone.color == vertex.color and vertex is not cone]
        if len(triangle_vertices) >= 2:
            for i in range(len(triangle_vertices) - 1):
                triangle = [cone, triangle_vertices[i], triangle_vertices[i + 1]]

                angle = abs(100 - math.degrees(
                    find_angle(triangle_vertices[i], cone, triangle_vertices[i + 1])
                ))
                size = distance(cone.point, triangle_vertices[i].point) ** 1.6 + \
                       distance(cone.point, triangle_vertices[i + 1].point) ** 1.6
                heuristic = angle + 1.5 * size

                if triangle_vertices[i] not in missed_cones or triangle_vertices[i+1] not in missed_cones:
                    heuristic -= 10

                heuristic_to_triangle.append({
                    "heuristic": heuristic,
                    "triangle": triangle
                })

    lowest_heuristic, triangle = math.inf, None
    for heuristic in heuristic_to_triangle:
        if heuristic["heuristic"] != -1 and heuristic["heuristic"] < lowest_heuristic:
            lowest_heuristic = heuristic["heuristic"]
            triangle = heuristic["triangle"]
    return triangle


def distance(a: Point, b: Point):
    return math.hypot(a.x - b.x, a.y - b.y)


def find_angle(a: Cone, b: Cone, c: Cone):
    angle = (math.atan2(c.point.y - b.point.y, c.point.x - b.point.x) - math.atan2(a.point.y - b.point.y, a.point.x - b.point.x))
    while angle > (2 * math.pi): angle -= (2 * math.pi)
    while angle < 0: angle += (2 * math.pi)
    if angle > math.pi: angle = 2 * math.pi - angle
    return angle


def get_min_angle_in_triangle(triangle: List[Cone]):
    """
    Returns the minimum angle of a vertex in the provided triangle in degrees
    :param triangle: The triangle -> [cone, cone, cone]
    :return: min angle of each vertex in degrees -> not radius
    """
    min_angle = 180
    min_angle = min(min_angle, find_angle(triangle[0], triangle[1], triangle[2]))
    min_angle = min(min_angle, find_angle(triangle[1], triangle[2], triangle[0]))
    min_angle = min(min_angle, find_angle(triangle[2], triangle[0], triangle[1]))
    return math.degrees(min_angle)


def merge_big_orange_cones(orange_cones):
    merged_orange_cones: List[Cone] = []
    for cone in orange_cones:
        too_close = False
        for merged_cone in merged_orange_cones:
            too_close = too_close or distance(cone.point, merged_cone.point) < 2.75
        if not too_close:
            merged_orange_cones.append(cone)
    return merged_orange_cones
