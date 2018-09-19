import os, sys, pygame
from time import sleep
import pandas as pd
import datetime
import time
from sklearn.metrics import mean_absolute_error

class Simulator():
    SIZE = 800, 600
    SLEEP_TIME = 0.01
    BG_COLOR = 0, 0, 255
    TEXT_COLOR = 255, 255, 255
    SHUFFLE_INTERVAL = 10

    def __init__(self, boat, env, strategies):
        self._boat = boat
        self._env = env
        self._strategies = strategies

        # pick first strategy as default
        self._strategy_id = 0
        self._strategy = strategies[self._strategy_id]

        pygame.init()
        pygame.font.init()

        self._font = pygame.font.SysFont('Arial', 30)
        self._smallfont = pygame.font.SysFont('Arial', 20)
        self._screen = pygame.display.set_mode(self.SIZE)

    def write_text(self, text, row):
        pos = 500, 30 + (row * 30)
        textsurface = self._font.render(text, True, self.TEXT_COLOR)
        self._screen.blit(textsurface, pos)

    def run(self):
        shuffle_time = time.time() + self.SHUFFLE_INTERVAL

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self._screen.fill(self.BG_COLOR)

            self._env.update()
            self._boat.update()
            self._strategy.update()

            self._boat.draw(self._screen)
            self._env.draw(self._screen)

            mae = mean_absolute_error(self._boat.history.target_angle, self._boat.history.boat_angle)

            self.write_text("Boat angle: %.1f°" % self._boat.boat_angle, 0)
            self.write_text("Target angle: %.1f°" % self._boat.target_angle, 1)
            self.write_text("Current deviation: %.1f°" % self._boat.get_course_error(), 2)
            self.write_text("Boat heel: %.1f°" % self._boat.boat_heel, 3)
            self.write_text("Rudder angle: %.1f°" % self._boat.rudder_angle, 4)
            self.write_text("Boat speed: %.1f knots" % self._boat.speed, 5)

            self.write_text("Angle of attack: %.1f°" % self._boat.get_angle_of_attack(), 6)
            self.write_text("Wind direction: %.1f°" % self._env.wind_direction, 8)
            self.write_text("Wind speed: %.1f knots" % self._env.wind_speed, 9)
            self.write_text("MAE: %.1f°" % mae, 11)

            self.write_text("Strategy: %s" % type(self._strategy).__name__, 13)

            textsurface = self._smallfont.render(
                "Press keys to change: 1/2 for target angle, 3/4 for wind direction, 5/6 for wind speed, s to change strategy, q to quit", True, self.TEXT_COLOR)
            self._screen.blit(textsurface, (20, 565))

            pygame.display.flip()

            # sleep
            sleep(self.SLEEP_TIME)

            # shuffle once in a while
            if time.time() > shuffle_time:
                self._env.shuffle()
                self._boat.shuffle()
                shuffle_time += self.SHUFFLE_INTERVAL

            # check key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # switch strategy
                    if event.key == pygame.K_s:
                        self._strategy_id = self._strategy_id + 1 if self._strategy_id < len(self._strategies) - 1 else 0
                        self._strategy = self._strategies[self._strategy_id]

                    # save log and quit
                    if event.key == pygame.K_q:
                        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M')
                        filename = os.path.join('data', 'logs', 'history_%s.csv' % date)
                        self._boat.history.to_csv(filename)
                        print("Wrote datalog to %s" % filename)
                        exit()


