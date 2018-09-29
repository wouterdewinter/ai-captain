import pygame
from .strategies import *
import os
from sklearn.externals import joblib
import pandas as pd

class Smoother(Base):
    STEERING_FORCE = .3

    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.steer(self.STEERING_FORCE)
        else:
            self._boat.steer(-self.STEERING_FORCE)

class Proportional(Base):
    MAX_RUDDER = 30

    def update(self):
        err = self._boat.get_course_error() / 2
        err = max(min(err, self.MAX_RUDDER), -self.MAX_RUDDER)
        self._boat.set_target_rudder_angle(err)

class GB(Base):

    def __init__(self, boat, env):
        super().__init__(boat, env)
        self._model = joblib.load(os.path.join('data', 'model.pkl'))

    def update(self):
        data = [{
            'angle_of_attack': self._boat.get_angle_of_attack(),
            'boat_heel': self._boat.boat_heel,
            'boat_speed': self._boat.speed,
            'course_error': self._boat.get_course_error(),
            'wind_speed': self._env.wind_speed,
        }]
        x = pd.DataFrame(data)

        pred = self._model.predict(x)
        angle = pred[0]

        self._boat.set_target_rudder_angle(angle)

