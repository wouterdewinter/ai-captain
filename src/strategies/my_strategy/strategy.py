from strategies.turnspeed.strategy import TurnSpeed
import os
import pandas as pd
import logging

class MyStrategy(TurnSpeed):
    def __init__(self, boat, env):
        super().__init__(boat, env)
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'angles.pkl')
        if (os.path.isfile(filename)):
            self._angles = pd.read_pickle(filename)
        else:
            # empty dataframe
            logging.warning("could not lead angles file")
            self._angles = pd.DataFrame()

    def get_downwind_twa(self):
        wind_speed = int(round(self._env.wind_speed))
        if wind_speed in self._angles.index:
            return self._angles.iloc[wind_speed]['downwind_twa']
        else:
            logging.warning("wind speed out of bounds")
            return super().get_downwind_twa()

    def get_upwind_twa(self):
        wind_speed = int(round(self._env.wind_speed))
        if wind_speed in self._angles.index:
            return self._angles.iloc[wind_speed]['upwind_twa']
        else:
            logging.warning("wind speed out of bounds")
            return super().get_upwind_twa()
