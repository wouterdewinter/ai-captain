import pygame
import os
from sklearn.externals import joblib
import pandas as pd

class Base():
    def __init__(self, boat, env):
        self._boat = boat
        self._env = env

    def update(self):
        raise NotImplementedError()

    def get_boat(self):
        return self._boat

    def get_name(self):
        return type(self).__name__

class Manual(Base):
    STEERING_FORCE = 1

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self._boat.steer(self.STEERING_FORCE)
        if pressed[pygame.K_RIGHT]:
            self._boat.steer(-self.STEERING_FORCE)

class DoNothing(Base):
    def update(self):
        return

class Binary(Base):
    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.set_target_rudder_angle(10)
        else:
            self._boat.set_target_rudder_angle(-10)