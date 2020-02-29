import math

import cv2
import numpy as np


def render_scene(track, scale: int = 10, padding: int = 10):
    min_x, min_y, max_x, max_y = math.inf, math.inf, -math.inf, -math.inf
    for cone in (track.blue_cones + track.yellow_cones + track.orange_cones + track.big_orange_cones):
        min_x = min(min_x, cone.point.x)
        min_y = min(min_y, cone.point.y)
        max_x = max(max_x, cone.point.x)
        max_y = max(max_y, cone.point.y)
    x_offset, y_offset = -min_x * scale + padding, -min_y * scale + padding

    image = np.zeros((
        int((max_y - min_y) * scale + 2 * padding),
        int((max_x - min_x) * scale + 2 * padding),
        3
    ))

    track_triangles = track.create_delaunay_graph()
    render_triangles(image, track_triangles, (255, 255, 255), scale, x_offset, y_offset)

    blue_lines, yellow_lines, orange_lines = track.create_boundary()
    render_lines(image, blue_lines, (255, 0, 0), scale, x_offset, y_offset)
    render_lines(image, yellow_lines, (0, 255, 255), scale, x_offset, y_offset)
    render_lines(image, orange_lines, (0, 100, 255), scale, x_offset, y_offset)

    render_points(image, track.blue_cones, (255, 0, 0), scale, 4, x_offset, y_offset)
    render_points(image, track.yellow_cones, (0, 255, 255), scale, 4, x_offset, y_offset)
    render_points(image, track.big_orange_cones, (0, 100, 255), scale, 4, x_offset, y_offset)

    return image


def render_points(image, points, colour, scale, radius, offset_x, offset_y):
    for blue_cone in points:
        image = cv2.circle(
            image,
            (int(round(blue_cone.point.x * scale + offset_x)), int(round(blue_cone.point.y * scale + offset_y))),
            radius,
            colour,
            -1
        )
    return image


def render_triangles(image, triangles, colour, scale, x_offset, y_offset):
    for triangle in triangles:
        cone_a = triangle[0]
        cone_b = triangle[1]
        cone_c = triangle[2]

        point_a_x = int(cone_a.point.x * scale + x_offset)
        point_a_y = int(cone_a.point.y * scale + y_offset)
        point_b_x = int(cone_b.point.x * scale + x_offset)
        point_b_y = int(cone_b.point.y * scale + y_offset)
        point_c_x = int(cone_c.point.x * scale + x_offset)
        point_c_y = int(cone_c.point.y * scale + y_offset)

        size = 1
        image = cv2.line(image, (point_a_x, point_a_y), (point_b_x, point_b_y), colour, size)
        image = cv2.line(image, (point_b_x, point_b_y), (point_c_x, point_c_y), colour, size)
        image = cv2.line(image, (point_c_x, point_c_y), (point_a_x, point_a_y), colour, size)
    return image


def render_lines(image, lines, colour, scale, x_offset, y_offset):
    for line in lines:
        image = cv2.line(
            image,
            (int(round(line.a.x * scale + x_offset)), int(round(line.a.y * scale + y_offset))),
            (int(round(line.b.x * scale + x_offset)), int(round(line.b.y * scale + y_offset))),
            colour,
            2
        )
    return image
