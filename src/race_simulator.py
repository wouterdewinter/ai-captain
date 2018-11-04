import os, sys, pygame
from time import sleep
import pandas as pd
import datetime
import time
from sklearn.metrics import mean_absolute_error
from drawers.race_drawer import RaceDrawer

class RaceSimulator():
    SIZE = 1024, 768
    SLEEP_TIME = 0.001
    BG_COLOR = 0, 0, 0
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

    def write_text(self, text, row, color=(255, 255, 255)):
        pos = 740, 30 + (row * 30)
        textsurface = self._font.render(text, True, color)
        self._screen.blit(textsurface, pos)

    def run(self):
        # scale the race canvas
        self._drawer.autoscale(self._env.get_buoys())

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            self._screen.fill(self.BG_COLOR)
            self._env.update()

            self._drawer.draw_env(self._env)
            self._drawer.draw_buoys(self._env.get_buoys())

            # update all boats
            scoreboard = []
            for i, strategy in enumerate(self._strategies):
                strategy.update()
                boat = strategy.get_boat()
                boat.update()
                self._drawer.draw_boat(boat)
                scoreboard.append({
                    'name': boat.get_name(),
                    'color': boat.get_boat_color(),
                    'marks_passed': boat.get_marks_passed(),
                    'dtw': boat.get_distance_to_waypoint()
                })

            # show scoreboard
            scoreboard = pd.DataFrame(scoreboard).sort_values(by=['marks_passed', 'dtw'], ascending=[False, True])
            i = 0
            for _, row in scoreboard.iterrows():
                text = "%s (DTW: %dm)" % (row['name'], row.dtw)
                self.write_text(text, i, row.color)
                i += 1

            pygame.display.flip()

            # sleep
            sleep(self.SLEEP_TIME)

            # check key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # save log and quit
                    if event.key == pygame.K_q:
                        exit()


