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

    def update(self):
        target = self._boat.get_course_error() / 2
        self._boat.set_target_rudder_angle(target)

class TurnSpeed(Base):
    def update(self):
        if self._boat.history.shape[0] < 3:
            return

        last = float(self._boat.history.iloc[-3:-2]['course_error'])

        # calculate turning speed
        current = self._boat.get_course_error()
        delta = last-current

        # calculate target turning speed based on course difference
        target_delta = self._boat.get_course_error() / 20
        target_delta = min(target_delta, 2)
        target_delta = max(target_delta, -2)

        # steer towards target turning speed
        steer = (target_delta - delta) / 2
        steer = min(steer, 0.3)
        steer = max(steer, -0.3)

        # steer the boat
        self._boat.steer(steer)

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

