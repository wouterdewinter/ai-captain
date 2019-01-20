import pygame
from random import random, uniform


class Environment:
    MAX_WIND_SPEED = 50
    MIN_WIND_SPEED = 2

    def __init__(self, wind_speed_var=1.2, wind_direction_var=10, buoys=None):
        self.main_wind_speed = 20
        self.main_wind_direction = 0
        self.wind_speed = 20
        self.wind_direction = 0
        self.unwrapped_wind_direction = 0
        self._wind_speed_var = wind_speed_var
        self._wind_direction_var = wind_direction_var
        self._buoys = buoys

    def shuffle(self):
        self.main_wind_speed = uniform(5, 25)
        self.wind_speed = self.main_wind_speed
        self.main_wind_direction = uniform(0, 360)
        self.wind_direction = self.main_wind_direction
        self.unwrapped_wind_direction = self.main_wind_direction

    def update(self):
        # update wind speed
        self.wind_speed += (random() - 0.5) * 2
        max_wind_speed = self.main_wind_speed * self._wind_speed_var
        min_wind_speed = self.main_wind_speed / self._wind_speed_var
        self.wind_speed = min(self.wind_speed, max_wind_speed)
        self.wind_speed = max(self.wind_speed, min_wind_speed)

        # update wind direction
        self.unwrapped_wind_direction += (random() - 0.5) * 2
        max_wind_dir = self.main_wind_direction + self._wind_direction_var
        min_wind_dir = self.main_wind_direction - self._wind_direction_var
        self.unwrapped_wind_direction = min(self.unwrapped_wind_direction, max_wind_dir)
        self.unwrapped_wind_direction = max(self.unwrapped_wind_direction, min_wind_dir)

        # wrap wind dir
        self.wind_direction = self.unwrapped_wind_direction + 360 if self.unwrapped_wind_direction < 0 else self.unwrapped_wind_direction
        self.wind_direction = self.unwrapped_wind_direction - 360 if self.unwrapped_wind_direction > 360 else self.unwrapped_wind_direction

    def change_wind_direction(self, amount):
        self.main_wind_direction += amount
        self.main_wind_direction = self.main_wind_direction % 360

    def change_wind_speed(self, amount):
        self.main_wind_speed += amount
        self.main_wind_speed = max(self.MIN_WIND_SPEED, min(self.MAX_WIND_SPEED, self.main_wind_speed))
        print(self.main_wind_speed)

    def get_buoys(self):
        return self._buoys
