import pygame

from boat import Boat
from environment import Environment
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

    TEXT_COLOR = 255, 255, 255
    SIZE = 800, 600
    BG_COLOR = 0, 0, 255

    def __init__(self):
        self._offset = (0, 0)
        self._scale = 0

        pygame.init()
        pygame.font.init()

        self._font = pygame.font.SysFont('Arial', 30)
        self._smallfont = pygame.font.SysFont('Arial', 20)
        self._screen = pygame.display.set_mode(self.SIZE)

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

    def write_text(self, text, row):
        pos = 500, 30 + (row * 30)
        textsurface = self._font.render(text, True, self.TEXT_COLOR)
        self._screen.blit(textsurface, pos)

    def draw_stats(self, boat, env, strategy_name):
        # calculate mean of absolute course error
        if boat.history.shape[0] > 0:
            mae = boat.history.course_error.abs().mean()
        else:
            mae = 0

        self.write_text("Boat angle: %.1f°" % boat.boat_angle, 0)
        self.write_text("Target angle: %.1f°" % boat.target_angle, 1)
        self.write_text("Current deviation: %.1f°" % boat.get_course_error(), 2)
        self.write_text("Boat heel: %.1f°" % boat.boat_heel, 3)
        self.write_text("Rudder angle: %.1f°" % boat.rudder_angle, 4)
        self.write_text("Boat speed: %.1f knots" % boat.speed, 5)
        self.write_text("Angle of attack: %.1f°" % boat.get_angle_of_attack(), 6)
        self.write_text("Wind direction: %.1f°" % env.wind_direction, 8)
        self.write_text("Wind speed: %.1f knots" % env.wind_speed, 9)
        self.write_text("MAE: %.1f°" % mae, 11)
        self.write_text("Strategy: %s" % strategy_name, 12)

        textsurface = self._smallfont.render(
            "Press keys to change: 1/2 for target angle, 3/4 for wind direction, 5/6 for wind speed, s to change strategy, q to quit", True, self.TEXT_COLOR)
        self._screen.blit(textsurface, (20, 565))

    def draw(self, boat: Boat, env: Environment, strategy_name='Undefined'):
        # redraw objects
        self._screen.fill(self.BG_COLOR)
        self.draw_boat(boat)
        self.draw_env(env)
        self.draw_stats(boat, env, strategy_name)

        # display new frame
        pygame.display.flip()
