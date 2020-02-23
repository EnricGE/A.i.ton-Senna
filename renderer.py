from math import ceil

import cv2
import numpy as np

from scene import Scene


def render_scene(scene: Scene, scale: int = 12, padding: int = 10):
    max_x_span, max_y_span = 0, 0
    for cone in scene.track.all_cones:
        max_x_span = max(max_x_span, abs(cone.point.x))
        max_y_span = max(max_y_span, abs(cone.point.y))
    max_x_span = max_x_span * scale + padding
    max_y_span = max_y_span * scale + padding

    image = np.zeros((2 * ceil(max_y_span), 2 * ceil(max_x_span), 3))

    for blue_cone in scene.track.blue_cones:
        image = cv2.circle(
            image,
            (int(round(blue_cone.point.x * scale + max_x_span)), int(round(blue_cone.point.y * scale + max_y_span))),
            scale // 2 + 1,
            (255, 0, 0),
            -1
        )
    for yellow_cone in scene.track.yellow_cones:
        image = cv2.circle(
            image,
            (int(round(yellow_cone.point.x * scale + max_x_span)), int(round(yellow_cone.point.y * scale + max_y_span))),
            scale // 2 + 1,
            (0, 255, 255),
            -1
        )

    grey = (100, 100, 100)
    connected_indexes, loose_indexes, valid_triangles, invalid_triangles, potential_triangles, surrounding_triangles = scene.track.get_delaunay()
    for valid_triangle in invalid_triangles:
        cone_a = scene.track.all_cones[valid_triangle[0]]
        cone_b = scene.track.all_cones[valid_triangle[1]]
        cone_c = scene.track.all_cones[valid_triangle[2]]

        point_a_x = int(cone_a.point.x * scale + max_x_span)
        point_a_y = int(cone_a.point.y * scale + max_y_span)
        point_b_x = int(cone_b.point.x * scale + max_x_span)
        point_b_y = int(cone_b.point.y * scale + max_y_span)
        point_c_x = int(cone_c.point.x * scale + max_x_span)
        point_c_y = int(cone_c.point.y * scale + max_y_span)

        size = 1
        image = cv2.line(image, (point_a_x, point_a_y), (point_b_x, point_b_y), (50, 50, 50), size)
        image = cv2.line(image, (point_b_x, point_b_y), (point_c_x, point_c_y), (50, 50, 50), size)
        image = cv2.line(image, (point_c_x, point_c_y), (point_a_x, point_a_y), (50, 50, 50), size)

    for valid_triangle in valid_triangles:
        cone_a = scene.track.all_cones[valid_triangle[0]]
        cone_b = scene.track.all_cones[valid_triangle[1]]
        cone_c = scene.track.all_cones[valid_triangle[2]]

        point_a_x = int(cone_a.point.x * scale + max_x_span)
        point_a_y = int(cone_a.point.y * scale + max_y_span)
        point_b_x = int(cone_b.point.x * scale + max_x_span)
        point_b_y = int(cone_b.point.y * scale + max_y_span)
        point_c_x = int(cone_c.point.x * scale + max_x_span)
        point_c_y = int(cone_c.point.y * scale + max_y_span)

        size = 1
        image = cv2.line(image, (point_a_x, point_a_y), (point_b_x, point_b_y), (255, 255, 255), size)
        image = cv2.line(image, (point_b_x, point_b_y), (point_c_x, point_c_y), (255, 255, 255), size)
        image = cv2.line(image, (point_c_x, point_c_y), (point_a_x, point_a_y), (255, 255, 255), size)

    for valid_triangle in potential_triangles:
        cone_a = scene.track.all_cones[valid_triangle[0]]
        cone_b = scene.track.all_cones[valid_triangle[1]]
        cone_c = scene.track.all_cones[valid_triangle[2]]

        point_a_x = int(cone_a.point.x * scale + max_x_span)
        point_a_y = int(cone_a.point.y * scale + max_y_span)
        point_b_x = int(cone_b.point.x * scale + max_x_span)
        point_b_y = int(cone_b.point.y * scale + max_y_span)
        point_c_x = int(cone_c.point.x * scale + max_x_span)
        point_c_y = int(cone_c.point.y * scale + max_y_span)

        size = 1
        image = cv2.line(image, (point_a_x, point_a_y), (point_b_x, point_b_y), (255, 0, 255), size)
        image = cv2.line(image, (point_b_x, point_b_y), (point_c_x, point_c_y), (255, 0, 255), size)
        image = cv2.line(image, (point_c_x, point_c_y), (point_a_x, point_a_y), (255, 0, 255), size)

    for valid_triangle in surrounding_triangles:
        cone_a = scene.track.all_cones[valid_triangle[0]]
        cone_b = scene.track.all_cones[valid_triangle[1]]
        cone_c = scene.track.all_cones[valid_triangle[2]]

        point_a_x = int(cone_a.point.x * scale + max_x_span)
        point_a_y = int(cone_a.point.y * scale + max_y_span)
        point_b_x = int(cone_b.point.x * scale + max_x_span)
        point_b_y = int(cone_b.point.y * scale + max_y_span)
        point_c_x = int(cone_c.point.x * scale + max_x_span)
        point_c_y = int(cone_c.point.y * scale + max_y_span)

        size = 1
        image = cv2.line(image, (point_a_x, point_a_y), (point_b_x, point_b_y), (0, 250, 0), size)
        image = cv2.line(image, (point_b_x, point_b_y), (point_c_x, point_c_y), (0, 250, 0), size)
        image = cv2.line(image, (point_c_x, point_c_y), (point_a_x, point_a_y), (0, 250, 0), size)

    cv2.imshow("", image / 255)
    cv2.waitKey(0)
