from boat import Boat
from tools import calc_angle

class Base():
    def __init__(self, boat:Boat, env):
        self._boat = boat
        self._env = env
        self._boat.set_strategy(self)

    def update(self):
        raise NotImplementedError()

    def get_boat(self) -> Boat:
        return self._boat

    def get_name(self):
        return type(self).__name__

    def get_downwind_twa(self):
        return 170

    def get_upwind_twa(self):
        return 30

    def need_to_tack(self) -> bool:
        """ Do we need to tack? """
        diff = calc_angle(self._boat.target_angle, self._boat._bearing)
        return abs(diff) > self.get_upwind_twa() * 1.5

    def need_to_gybe(self) -> bool:
        """ Do we need to gybe? """
        diff = calc_angle(self._boat.target_angle, self._boat._bearing)
        return abs(diff) > (180 - self.get_downwind_twa() * 1.5)
