from strategies import *
from keras.models import load_model

class MyDeepStrategy(Base):
    def __init__(self, boat, env):
        super().__init__(boat, env)
        self._model = load_model(os.path.join('data', 'my-keras-model.h5'))

    def update(self):
        ### CREATE FEATURE DATAFRAME OR NUMPY ARRAY ###
        x = ...
        pred = self._model.predict(x)

        # cast to float because output is numpy array
        angle = float(pred[0])

        self._boat.set_target_rudder_angle(angle)