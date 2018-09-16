import os, sys, pygame
from time import sleep

class Simulator():
    SIZE = 800, 600
    SLEEP_TIME = 0.01
    BG_COLOR = 0, 0, 255
    TEXT_COLOR = 255, 255, 255

    def __init__(self, boat, env, strategy):
        self._boat = boat
        self._env = env
        self._strategy = strategy

        pygame.init()
        pygame.font.init()

        self._font = pygame.font.SysFont('Arial', 30)
        self._smallfont = pygame.font.SysFont('Arial', 25)
        self._screen = pygame.display.set_mode(self.SIZE)

    def write_text(self, text, row):
        pos = 500, 30 + (row * 30)
        textsurface = self._font.render(text, True, self.TEXT_COLOR)
        self._screen.blit(textsurface, pos)

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self._screen.fill(self.BG_COLOR)

            self._env.update()
            self._boat.update()
            self._strategy.update()

            self._boat.draw(self._screen)
            self._env.draw(self._screen)

            self.write_text("Boat angle: %.1f°" % self._boat.boat_angle, 0)
            self.write_text("Target angle: %.1f°" % self._boat.target_angle, 1)
            self.write_text("Current deviation: %.1f°" % self._boat.get_course_error(), 2)
            self.write_text("Boat heel: %.1f°" % self._boat.boat_heel, 3)
            self.write_text("Rudder angle: %.1f°" % self._boat.rudder_angle, 4)
            self.write_text("Boat speed: %.1f knots" % self._boat.speed, 5)

            self.write_text("Wind direction: %.1f°" % self._env.wind_direction, 7)
            self.write_text("Wind speed: %.1f knots" % self._env.wind_speed, 8)

            textsurface = self._smallfont.render(
                "Press keys to change: 1/2 for target angle, 3/4 for wind direction, 5/6 for wind speed", True, self.TEXT_COLOR)
            self._screen.blit(textsurface, (20, 550))

            pygame.display.flip()
            sleep(self.SLEEP_TIME)