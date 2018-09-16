import pygame
from math import sin, cos, radians
from random import random, uniform
from tools import rotate_point

class Boat():
    WEATHER_HELM_FORCE = 0.02
    BOAT_HEEL_FORCE = 2

    COLOR = 255, 255, 255
    RUDDER_COLOR = 200, 0, 0
    SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    RUDDER_ORIGIN = [50, 180]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    ORIGIN = [50, 150]

    def __init__(self, env):
        self.rudder_angle = 0.
        self.boat_angle = 0.
        self.boat_heel = 0.
        self.target_angle = uniform(0, 360)
        self.speed = 3.
        self.x = 150.
        self.y = 100.
        self._env = env

    def get_course_error(self):
        err = self.boat_angle - self.target_angle
        err = (err + 180) % 360 - 180
        return err

    def steer(self, rudder_movement):
        self.rudder_angle += rudder_movement

    def update(self):
        # steering input
        self.boat_angle -= self.rudder_angle / 10

        # weather helm
        force = sin(radians(self.boat_angle - self._env.wind_direction + 180))
        self.boat_angle += force * self.WEATHER_HELM_FORCE * self._env.wind_speed

        # calculate boat heel
        self.boat_heel = abs(force) * self._env.wind_speed * self.BOAT_HEEL_FORCE

        # maximize rudder angle
        self.rudder_angle = 50 if self.rudder_angle > 50 else self.rudder_angle
        self.rudder_angle = -50 if self.rudder_angle < -50 else self.rudder_angle

        # wrap boat angle
        self.boat_angle =  self.boat_angle + 360 if self.boat_angle<0 else self.boat_angle
        self.boat_angle =  self.boat_angle - 360 if self.boat_angle>360 else self.boat_angle

    def draw(self, screen):
        # draw boat
        vectors = self.SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, self.boat_angle, self.ORIGIN)
            vectors[i] = [self.x + new_vector[0], self.y + new_vector[1]]

        pygame.draw.polygon(screen, self.COLOR, vectors, 0)

        # draw rudder
        vectors = self.RUDDER_SHAPE.copy()
        for i, vector in enumerate(vectors):

            # rudder rotation
            vector = rotate_point(vector, self.rudder_angle, self.RUDDER_ORIGIN)

            # boat rotation
            vector = rotate_point(vector, self.boat_angle, self.ORIGIN)

            # boat position
            vectors[i] = [self.x + vector[0], self.y + vector[1]]

        pygame.draw.line(screen, self.RUDDER_COLOR, vectors[0], vectors[1], 4)