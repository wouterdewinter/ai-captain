from strategies.base import Base
from .strategy import *


class MyRuleStrategy(MyStrategy):

    def update(self):
        ### create your rule based strategy here ###

        # set a target rudder angle
        #self._boat.set_target_rudder_angle(123)

        return
