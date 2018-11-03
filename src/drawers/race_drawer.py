import pygame

class RaceDrawer():
    BUOY_COLOR = (253,228,46)
    RACE_CANVAS_DIM = (500, 500)

    def __init__(self, screen):
        self._screen = screen
        self._offset = (0, 0)
        self._scale = 0

    def autoscale(self, buoys):
        """ Scale race canvas to fit all buoys """
        lat, lon = zip(*buoys)

        # get bounding positions
        lat1 = min(lat)
        lon1 = min(lon)
        lat2 = max(lat)
        lon2 = max(lon)

        # get bbox dimensions
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # check aspect ratio
        if dlat > dlon:
            height = dlat
        else:
            height = dlon

        # scale to pixels
        olat = (lat1 + dlat / 2) - height / 2
        olon = (lon1 + dlon / 2) - height / 2

        self._offset = (olat, olon)
        self._scale = self.RACE_CANVAS_DIM[0] / height



    def translate_pos(self, pos):
        y = (pos[0]-self._offset[0]) * self._scale
        x = (pos[1]-self._offset[1]) * self._scale
        return (int(round(x)), int(round(y)))

    def draw_boat(self, boat):
        x, y = self.translate_pos(boat.get_position())
        pygame.draw.circle(self._screen, (0, 127, 255), (x, y), 20, 4)

    def draw_buoys(self, buoys):
        for position in buoys:
            x, y = self.translate_pos(position)
            pygame.draw.circle(self._screen, self.BUOY_COLOR, (x, y), 5, 4)


