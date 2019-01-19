import pygame
from tools import rotate_point, add_vector, rotate_vectors


class SimDrawer:

    BOAT_ORIGIN = [50, 150]
    BOAT_SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]

    RUDDER_ORIGIN = [50, 180]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    RUDDER_COLOR = 200, 0, 0

    ARROW_SHAPE = [(0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)]
    ARROW_COLOR = (0, 255, 0)
    ARROW_POS = [350, 250]
    ARROW_ORIGIN = [150, 100]
    ARROW_SCALE = 0.2

    CENTER = (250, 250)

    def __init__(self, screen):
        self._screen = screen
        self._offset = (0, 0)
        self._scale = 0

    def draw_boat(self, boat):
        # draw boat
        vectors = self.BOAT_SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, boat.boat_angle, self.BOAT_ORIGIN)
            vectors[i] = [boat.x + new_vector[0], boat.y + new_vector[1]]

        pygame.draw.polygon(self._screen, boat.get_boat_color(), vectors, 0)

        # draw rudder
        vectors = self.RUDDER_SHAPE.copy()
        for i, vector in enumerate(vectors):

            # rudder rotation
            vector = rotate_point(vector, boat.rudder_angle, self.RUDDER_ORIGIN)
            vector = add_vector(vector, self.RUDDER_ORIGIN)

            # boat rotation
            vector = rotate_point(vector, boat.boat_angle, self.BOAT_ORIGIN)

            # boat position
            vectors[i] = [boat.x + vector[0], boat.y + vector[1]]

        pygame.draw.line(self._screen, self.RUDDER_COLOR, vectors[0], vectors[1], 4)

        # draw target direction
        vectors = [[250, 30], [250, 50]]
        vectors = rotate_vectors(vectors, boat.target_angle, (250, 250), reverse=True)
        pygame.draw.line(self._screen, (0, 255, 0),  vectors[0], vectors[1], 10)

    def draw_env(self, env):
        vectors = self.ARROW_SHAPE.copy()
        for i, vector in enumerate(vectors):
            vector = rotate_point(vector, env.wind_direction + 90, self.ARROW_ORIGIN)
            vector = [self.ARROW_POS[0] + vector[0], self.ARROW_POS[1] + vector[1]]
            vector = [vector[0] * self.ARROW_SCALE, vector[1] * self.ARROW_SCALE]
            vectors[i] = vector

        pygame.draw.polygon(self._screen, self.ARROW_COLOR, vectors)
        pygame.draw.circle(self._screen, (100, 100, 100), self.CENTER, 200, 5)
