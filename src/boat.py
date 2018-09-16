import pygame
from math import sin, cos, radians
from random import random, uniform
from tools import rotate_point, add_vector, rotate_vectors
from autopilot.ai_captain_utils import PilotControl

class Boat():
    WEATHER_HELM_FORCE = 0.02
    BOAT_HEEL_FORCE = 1
    RUDDER_SPEED = 1

    COLOR = 255, 255, 255
    RUDDER_COLOR = 200, 0, 0
    SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    RUDDER_ORIGIN = [50, 180]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    ORIGIN = [50, 150]

    def __init__(self, env):
        self.rudder_angle = 0.
        self.target_rudder_angle = 0.
        self.boat_angle = 0.
        self.boat_heel = 0.
        self.target_angle = 0
        self.speed = 3.
        self.x = 250.
        self.y = 250.
        self._env = env
        self.history = []

        self.shuffle()

    def shuffle(self):
        self.set_target_angle(uniform(0, 360))

    def get_course_error(self):
        err = self.boat_angle - self.target_angle
        err = (err + 180) % 360 - 180
        return err

    def steer(self, rudder_movement):
        self.set_target_rudder_angle(self.target_rudder_angle + rudder_movement)

    def set_target_rudder_angle(self, target_rudder_angle):
        self.target_rudder_angle = target_rudder_angle

        # maximize rudder angle
        self.target_rudder_angle = min(50, self.target_rudder_angle)
        self.target_rudder_angle = max(-50, self.target_rudder_angle)

    def set_target_angle(self, target_angle):
        target_angle = target_angle + 360 if target_angle<0 else target_angle
        target_angle = target_angle - 360 if target_angle>360 else target_angle
        self.target_angle = target_angle

    def calculate_speed(self):
        delta = self._env.wind_direction - self.boat_angle
        delta = abs((delta + 180) % 360 - 180)
        speed = sin(radians(delta / 1.2)) *  self._env.wind_speed / 4
        return speed

    def move(self):
        """Simulates or fetches movement of boat"""

        # steering input
        self.boat_angle -= self.rudder_angle / 10

        # apply weather helm
        force = sin(radians(self.boat_angle - self._env.wind_direction + 180))
        self.boat_angle += force * self.WEATHER_HELM_FORCE * self._env.wind_speed

        # calculate boat heel
        self.boat_heel = abs(force) * self._env.wind_speed * self.BOAT_HEEL_FORCE

        # calculate speed
        self.speed = self.calculate_speed()

        # move rudder
        if abs(self.target_rudder_angle - self.rudder_angle) < self.RUDDER_SPEED:
            self.rudder_angle = self.target_rudder_angle
        else:
            if self.target_rudder_angle > self.rudder_angle:
                self.rudder_angle += self.RUDDER_SPEED
            else:
                self.rudder_angle -= self.RUDDER_SPEED

        # wrap boat angle
        self.boat_angle = self.boat_angle + 360 if self.boat_angle<0 else self.boat_angle
        self.boat_angle = self.boat_angle - 360 if self.boat_angle>360 else self.boat_angle

    def update(self):

        # simulate or fetch boat movements
        self.move()

        # save history
        self.history.append({
            'boat_angle': self.boat_angle,
            'boat_heel': self.boat_heel,
            'boat_speed': self.speed,
            'target_angle': self.target_angle,
            'course_error': self.get_course_error(),
            'rudder_angle': self.rudder_angle,
            'wind_direction': self._env.wind_direction,
            'wind_speed': self._env.wind_speed,
        })

        # change target angle
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_1]:
            self.set_target_angle(self.target_angle - 3)
        if pressed[pygame.K_2]:
            self.set_target_angle(self.target_angle + 3)

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
            vector = add_vector(vector, self.RUDDER_ORIGIN)

            # boat rotation
            vector = rotate_point(vector, self.boat_angle, self.ORIGIN)

            # boat position
            vectors[i] = [self.x + vector[0], self.y + vector[1]]

        pygame.draw.line(screen, self.RUDDER_COLOR, vectors[0], vectors[1], 4)

        # draw target direction
        vectors = [[250, 30], [250, 50]]
        vectors = rotate_vectors(vectors, self.target_angle, (250, 250), reverse=True)
        pygame.draw.line(screen, (0, 255, 0),  vectors[0], vectors[1], 10)

class RealBoat(Boat):
    def __init__(self, env, ip_address='127.0.0.1'):
        super().__init__(env)
        self._pilot = PilotControl(ip_address=ip_address)

    def set_target_rudder_angle(self, target_rudder_angle):
        super().set_target_rudder_angle(target_rudder_angle)
        self._pilot.set_rudder_angle(self.target_rudder_angle)

    def set_target_angle(self, target_angle):
        super().set_target_angle(target_angle)
        self._pilot.set_course(self.target_angle)

    def move(self):
        data = self._pilot.get_data_from_pilot()
        # todo: update speed, rudder angle, heel, course

