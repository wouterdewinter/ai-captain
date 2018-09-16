import pygame
from math import sin, cos, radians
from random import random, uniform
from tools import rotate_point

class Environment():
    WIND_SPEED_VAR = 1.2
    WIND_DIRECTION_VAR = 1.2
    MAX_WIND_SPEED = 50
    MIN_WIND_SPEED = 2

    ARROW_SHAPE = [(0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)]
    ARROW_COLOR = (0, 255, 0)
    ARROW_POS = [350, 250]
    ARROW_ORIGIN = [150, 100]
    ARROW_SCALE = 0.2
    CENTER = (250, 250)

    def __init__(self):
        self.main_wind_speed = uniform(5, 25)
        self.main_wind_direction = uniform(0, 360)
        self.wind_speed = self.main_wind_speed
        self.wind_direction = self.main_wind_direction

    def update(self):
        self.wind_speed += (random() - 0.5) * 2
        max_wind_speed = self.main_wind_speed * self.WIND_SPEED_VAR
        min_wind_speed = self.main_wind_speed / self.WIND_SPEED_VAR
        self.wind_speed = min(self.wind_speed, max_wind_speed)
        self.wind_speed = max(self.wind_speed, min_wind_speed)

        self.wind_direction += (random() - 0.5) * 2
        max_wind_dir = self.main_wind_direction * self.WIND_SPEED_VAR
        min_wind_dir = self.main_wind_direction / self.WIND_SPEED_VAR
        self.wind_direction = min(self.wind_direction, max_wind_dir)
        self.wind_direction = max(self.wind_direction, min_wind_dir)

        # wrap wind dir
        self.wind_direction = self.wind_direction + 360 if self.wind_direction < 0 else self.wind_direction
        self.wind_direction = self.wind_direction - 360 if self.wind_direction > 360 else self.wind_direction

        # change target direction
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_3]:
            self.main_wind_direction -= 1
        if pressed[pygame.K_4]:
            self.main_wind_direction += 1

        # change wind speed
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_5] and self.main_wind_speed>self.MIN_WIND_SPEED:
            self.main_wind_speed -= 1
        if pressed[pygame.K_6] and self.main_wind_speed<self.MAX_WIND_SPEED:
            self.main_wind_speed += 1

    def draw(self, screen):
        vectors = self.ARROW_SHAPE.copy()
        for i, vector in enumerate(vectors):
            vector = rotate_point(vector, self.wind_direction + 90, self.ARROW_ORIGIN)
            vector = [self.ARROW_POS[0] + vector[0], self.ARROW_POS[1] + vector[1]]
            vector = [vector[0] * self.ARROW_SCALE, vector[1] * self.ARROW_SCALE]
            vectors[i] = vector

        # surface = pygame.transform.rotate(screen, self.wind_direction)
        pygame.draw.polygon(screen, self.ARROW_COLOR, vectors)

        pygame.draw.circle(screen, (100, 100, 100), self.CENTER, 200, 5)
