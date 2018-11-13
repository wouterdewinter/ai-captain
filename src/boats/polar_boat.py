from boat import SimBoat

class PolarBoat(SimBoat):
    """ Uses information about boat performance """
    def __init__(self, env, polar, angles_file, **kwargs):

        pd.from_pickle()

        super().__init__(env, polar=polar, **kwargs)

    def get_downwind_twa(self):
        return self._downwind_twa

    def get_upwind_twa(self):
        return self._upwind_twa