from typing import List

from objects import Point, Cone, CONE_COLOR_BLUE, CONE_COLOR_BIG_ORANGE, CONE_COLOR_ORANGE, CONE_COLOR_YELLOW
from track import distance


class Cluster:
    def __init__(self, point: Point):
        self.point = point
        self.points: List[Cone] = []
        self.color = CONE_COLOR_BLUE

    def recalculate(self):
        error = 0
        if len(self.points) != 0:
            average_point = Point(0, 0)

            blue_count, yellow_count, orange_count, big_orange_count = 0, 0, 0, 0
            for cone in self.points:
                average_point.add(cone.point)

                blue_count += cone.color == CONE_COLOR_BLUE
                yellow_count += cone.color == CONE_COLOR_YELLOW
                orange_count += cone.color == CONE_COLOR_ORANGE
                big_orange_count += cone.color == CONE_COLOR_BIG_ORANGE

            average_point.x /= len(self.points)
            average_point.y /= len(self.points)

            error = distance(self.point, average_point)
            self.point = average_point

            if CONE_COLOR_BIG_ORANGE > yellow_count and CONE_COLOR_BIG_ORANGE > blue_count:
                self.color = CONE_COLOR_BIG_ORANGE
            elif CONE_COLOR_ORANGE > yellow_count and CONE_COLOR_ORANGE > blue_count:
                self.color = CONE_COLOR_ORANGE
            elif yellow_count > blue_count:
                self.color = CONE_COLOR_YELLOW
            else:
                self.color = CONE_COLOR_BLUE

        return error




class Mapping:
    def __init__(self):
        self.clusters: List[Cluster]  = []
        self.locked_clusters: List[Cone]  = []

    def map(self, position: Point, angle: float, visual_cones: List[Cone]):
        if len(self.clusters) == 0:
            for c in visual_cones:
                c.point.rotate_around(angle, 0, 0)
                c.point.add(position)

                self.clusters.append(Cluster(c.point))

    def recluster_loop(self):
        error: float = 1
        count: int = 0
        while error > 0.01 and count < self.MAX_EPOCHS:
            error = self.recluster()
            count += 1

    def miosis(self) -> bool:
        new_clusters: List[Cluster] = []
        for cluster in self.clusters:
            if len(cluster.points) != 0:
                avg_distance = 0
                furthest_point = Cone(Point(0, 0), CONE_COLOR_BLUE)
                furthest_distance = -1

                for cone in cluster.points:
                    distance_to_cluster = distance(cone.point, cluster.position)
                    avg_distance += distance_to_cluster

                    if distance > furthest_distance:
                        furthest_distance = distance
                        furthest_point = c

                avg_distance /= len(cluster.points)

                if avg_distance > MIN_DISTANCE / 2:
                    new_clusters.append(Cluster(furthest_point.point))

        self.clusters = self.clusters + new_clusters
        return len(new_clusters) != 0

    def recluster(self):
        for ia in range(len(clusters)):
            moved_cones = List[int] = []
            for cone in self.clusters[ia].points:
                distance_to_current_cluster = distance(cone.point, self.clusters[ia].point)
                closest_cluster = ia

                for ib in range(len(self.clusters)):
                    distance_to_new_cluster = distance(cone.point, self.clusters[ib].point)
                    if distance_to_new_cluster < distance_to_current_cluster:
                        closest_cluster = ib
                        distance_to_current_cluster = distance_to_new_cluster

                if closest_cluster != ia:
                    moved_cones.append(cone)
                    self.clusters[closest_cluster].points.append(cone)

            for moved_cone in moved_cones:
                self.clusters[ia].points.remove(moved_cone)

        # re-calculate cluster centers
        total_error = 0
        for cluster in self.clusters:
            total_error += cluster.recalculate()

        return  total_error

    def get_nearest_cluster_point(self, p: Point) -> Cluster:
        nearest_cluster = self.clusters[0]

        cluster_distance = distance(nearest_cluster.point, p)
        for cluster in self.clusters:
            current_distance = distance(p, cluster.point)
            if current_distance < cluster_distance:
                nearest_cluster = cluster
                cluster_distance = current_distance

        return nearest_cluster

    def get_clusters_global(self):
        data_points: List[Cone] = list(self.locked_clusters)

        if len(self.clusters) + len(self.locked_clusters) > 2:
            for cluster in self.clusters:
                if len(cluster.points) > MINIMUM_CLUSTER_SIZE:
                    data_points.append(Cone(cluster.point, cluster.color))
        else:
            for cluster in self.clusters:
                data_points.append(Cone(cluster.point, cluster.color))

   