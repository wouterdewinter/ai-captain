from boat import Boat

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