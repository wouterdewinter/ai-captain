from strategies.my_strategy.strategy import *
from keras.models import load_model
import os


class MyDeepStrategy(MyStrategy):
    def __init__(self, boat, env):
        super().__init__(boat, env)
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'my-keras-model.h5')
        self._model = load_model(filename)

    def update(self):
        ### CREATE FEATURE DATAFRAME OR NUMPY ARRAY HERE ###
        x = ...
        pred = self._model.predict(x)

        # cast to float because output is numpy array
        angle = float(pred[0])

        # set the rudder angle
        self._boat.set_target_rudder_angle(angle)
