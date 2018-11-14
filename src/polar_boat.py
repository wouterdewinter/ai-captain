import pandas as pd
from boat import SimBoat
import logging

class PolarBoat(SimBoat):
    """ Uses information about boat performance """

    def __init__(self, env, polar, angles_file, **kwargs):
        # load up and downwind angles from file
        self._angles = pd.read_pickle(angles_file)

        super().__init__(env, polar=polar, **kwargs)

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
