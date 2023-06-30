import os
# from sklearn.externals import joblib
import pandas as pd
from .strategy import *

class MyMlStrategy(MyStrategy):

    def __init__(self, boat, env):
        super().__init__(boat, env)

        ### Uncomment these lines to start ###
        # filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'my-model.pkl')
        # self._model = joblib.load(filename)

    def update(self):
        ### Uncomment these lines to start ###

        # data = [{
        #     'angle_of_attack': self._boat.get_angle_of_attack(),
        #     'boat_heel': self._boat.boat_heel,
        #     'boat_speed': self._boat.speed,
        #     'course_error': self._boat.get_course_error(),
        #     'wind_speed': self._env.wind_speed,
        # }]
        # x = pd.DataFrame(data)
        #
        # pred = self._model.predict(x)
        # angle = pred[0]
        #
        # self._boat.set_target_rudder_angle(angle)

        pass

