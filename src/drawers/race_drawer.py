import pygame
from tools import rotate_point

class RaceDrawer():
    BUOY_COLOR = (253,228,46)
    RACE_CANVAS_DIM = (700, 700)
    RACE_CANVAS_POS = (10, 10)
    RACE_CANVAS_COLOR = (33, 66, 99)

    ARROW_SHAPE = [(0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)]
    ARROW_COLOR = (0, 255, 0)
    ARROW_POS = [350, 250]
    ARROW_ORIGIN = [150, 100]
    ARROW_SCALE = 0.2

    BOAT_SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    BOAT_ORIGIN = [50, 150]
    BOAT_COLOR = (255, 255, 255)
    BOAT_SCALE = 0.1

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

        # apply some padding
        height = height * 1.5

        # scale to pixels
        olat = (lat1 + dlat / 2) - height / 2
        olon = (lon1 + dlon / 2) - height / 2

        self._offset = (olat, olon)
        self._scale = self.RACE_CANVAS_DIM[0] / height

    def translate_pos(self, pos):
        y = self.RACE_CANVAS_DIM[1] - (pos[0]-self._offset[0]) * self._scale + self.RACE_CANVAS_POS[1]
        x = (pos[1]-self._offset[1]) * self._scale + self.RACE_CANVAS_POS[0]
        return (int(round(x)), int(round(y)))

    def draw_env(self, env):
        pos = (
            self.RACE_CANVAS_POS[0],
            self.RACE_CANVAS_POS[1],
            self.RACE_CANVAS_POS[0] + self.RACE_CANVAS_DIM[0],
            self.RACE_CANVAS_POS[1] + self.RACE_CANVAS_DIM[1]
        )

        pygame.draw.rect(self._screen, self.RACE_CANVAS_COLOR, pos)

        self.draw_wind(env.wind_direction)

    def draw_wind(self, wind_direction):
        vectors = self.ARROW_SHAPE.copy()
        for i, vector in enumerate(vectors):
            vector = rotate_point(vector, wind_direction + 90, self.ARROW_ORIGIN)
            vector = [self.ARROW_POS[0] + vector[0], self.ARROW_POS[1] + vector[1]]
            vector = [vector[0] * self.ARROW_SCALE, vector[1] * self.ARROW_SCALE]
            vectors[i] = vector

        pygame.draw.polygon(self._screen, self.ARROW_COLOR, vectors)


    def draw_boat(self, boat):
        x, y = self.translate_pos(boat.get_position())

        # draw boat
        vectors = self.BOAT_SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, boat.boat_angle, self.BOAT_ORIGIN)
            vectors[i] = [x + new_vector[0] * self.BOAT_SCALE, y + new_vector[1] * self.BOAT_SCALE]

        pygame.draw.polygon(self._screen, boat.get_boat_color(), vectors, 0)
        pygame.draw.polygon(self._screen, self.BOAT_COLOR, vectors, 1)
        #pygame.draw.aalines(self._screen, self.BOAT_COLOR, 0, vectors, 2)
        #pygame.draw.circle(self._screen, (0, 127, 255), (x, y), 20, 4)



    def draw_buoys(self, buoys):
        for position in buoys:
            x, y = self.translate_pos(position)
            pygame.draw.circle(self._screen, self.BUOY_COLOR, (x, y), 5)


