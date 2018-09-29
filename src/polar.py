import pandas as pd
import numpy as np


class Polar():
    def __init__(self, filename):
        # load polar csv
        data = pd.read_csv(filename, delimiter=';')
        data = data.rename(columns={'twa/tws': 'twa'})
        data = data.set_index('twa')
        data.columns = data.columns.astype('int')

        # interpolate for every wind angle
        idx = np.arange(0, 181, 1)
        data = data.reindex(idx)
        # todo: assumption, set downwind speed to 80% of speed ar 150 degrees as we don't have the real numbers
        data.iloc[180] = data.iloc[150] * 0.8
        data.interpolate(method='polynomial', order=2, inplace=True)

        self._data = data

    def get_speed(self, twa, tws):
        twa = int(round(abs(twa)))
        tws = int(round(tws))

        # must be within range
        tws = min(tws, 25)
        tws = max(tws, 0)

        series = self._data.iloc[twa]
        # todo: assumption, extend to 0 knots TWS by setting to 0
        series[0] = 0
        # todo: assumption, extend to 25 knots by adding fixed percentage
        series[25] = series[20] * 1.005
        idx = np.arange(0, 26, 1)
        series = series.reindex(idx).interpolate(method='polynomial', order=2)

        # return speed
        return series[tws]