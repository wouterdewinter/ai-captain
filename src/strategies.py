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

class Manual(Base):
    STEERING_FORCE = .3

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

class Smoother(Base):
    STEERING_FORCE = .3

    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.steer(self.STEERING_FORCE)
        else:
            self._boat.steer(-self.STEERING_FORCE)

class Proportional(Base):
    MAX_RUDDER = 20

    def update(self):
        err = self._boat.get_course_error()
        err = max(min(err, self.MAX_RUDDER), -self.MAX_RUDDER)
        self._boat.set_target_rudder_angle(err)

class GB(Base):

    def __init__(self, boat, env):
        super().__init__(boat, env)
        self._model = joblib.load(os.path.join('data', 'model.pkl'))

    def update(self):
        data = [{
            'boat_heel': self._boat.boat_heel,
            'boat_speed': self._boat.speed,
            'course_error': self._boat.get_course_error(),
            'wind_speed': self._env.wind_speed,
        }]
        x = pd.DataFrame(data)

        pred = self._model.predict(x)
        angle = pred[0]

        self._boat.set_target_rudder_angle(angle)

