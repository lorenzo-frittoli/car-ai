import pygame

# from neural_network.neuralnetwork import NeuralNetwork
from map_handler.map_handler import MapHandler
from helpers import clamp, line_intersection
from globals import DISPLAY_SIZE


class Car:
    def __init__(self, net_shape: tuple | list, pos: pygame.Vector2) -> None:
        # super().__init__(net_shape)
        self.pos = pos
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

        self.pos_bounds = ((0, DISPLAY_SIZE[0]), (0, DISPLAY_SIZE[1]))
        self.velocity_bounds = ((-20, +20), (-20, +20))
        self.acceleration_bounds = ((-5, +5), (-5, +5))

        self.raycast_angles = (-90, -60, -30, 0, 30, 60, 90)

    def display(self, display) -> None:
        pygame.draw.circle(display, "black", self.pos, 5)
        pygame.draw.line(display, "black", self.pos, self.pos+self.velocity)

    def update(self, delta_time: float) -> None:
        self.velocity += self.acceleration * delta_time
        self.pos += self.velocity * delta_time

        self.pos = clamp(self.pos, self.pos_bounds)
        self.velocity = clamp(self.velocity, self.velocity_bounds)

    def raycast(self, map_handler: MapHandler, display) -> list[float]:
        """
        Raycast over self.raycast_angles and return distances.
        """
        if not map_handler.map.chains:
            return

        for chain in map_handler.map.chains:
            if not chain.points:
                return

            points = chain.get_points()
            if chain.closed:
                points.append(points[0])

            # pygame.draw.circle(display, "red", p, 5)
            point_ = points[0]
            for point in points[1:]:
                inter = line_intersection(self.pos, (0, 0), point, point_)
            if not inter:
