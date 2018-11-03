import os, sys, pygame
from time import sleep
import pandas as pd
import datetime
import time
from sklearn.metrics import mean_absolute_error
from drawers.race_drawer import RaceDrawer

class RaceSimulator():
    SIZE = 800, 600
    SLEEP_TIME = 0.01
    BG_COLOR = 0, 0, 255
    TEXT_COLOR = 255, 255, 255

    def __init__(self, env, strategies):
        self._env = env
        self._strategies = strategies

        pygame.init()
        pygame.font.init()

        self._font = pygame.font.SysFont('Arial', 30)
        self._smallfont = pygame.font.SysFont('Arial', 20)
        self._screen = pygame.display.set_mode(self.SIZE)
        self._drawer = RaceDrawer(self._screen)

    def write_text(self, text, row):
        pos = 500, 30 + (row * 30)
        textsurface = self._font.render(text, True, self.TEXT_COLOR)
        self._screen.blit(textsurface, pos)

    def run(self):
        # scale the race canvas
        self._drawer.autoscale(self._env.get_buoys())

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self._screen.fill(self.BG_COLOR)
            self._env.update()

            for strategy in self._strategies:
                strategy.update()
                boat = strategy.get_boat()
                boat.update()
                self._drawer.draw_boat(boat)

            self._drawer.draw_buoys(self._env.get_buoys())

            #self._env.draw(self._screen)


            # textsurface = self._smallfont.render(
            #     "Press keys to change: 1/2 for target angle, 3/4 for wind direction, 5/6 for wind speed, s to change strategy, q to quit", True, self.TEXT_COLOR)
            # self._screen.blit(textsurface, (20, 565))

            pygame.display.flip()

            # sleep
            sleep(self.SLEEP_TIME)


            # check key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # save log and quit
                    if event.key == pygame.K_q:
                        exit()


