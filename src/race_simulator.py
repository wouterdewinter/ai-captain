import pygame
import pandas as pd
import threading
import tensorflow as tf

from drawers.race_drawer import RaceDrawer
from settings import Settings


class RaceUpdateThread (threading.Thread):
    """Thread for updating the steering strategy"""

    def __init__(self, strategies, graph):
        threading.Thread.__init__(self)
        self._strategies = strategies
        self._clock = pygame.time.Clock()
        self._graph = graph

    def run(self):
        while 1:
            for strategy in self._strategies:

                # update steering strategy
                # need to set default graph to enable keras models to run in a different thread
                with self._graph.as_default():
                    strategy.update()

                # update strategy with current fps
                fps = self._clock.get_fps()
                if fps > 0:
                    strategy.set_update_fps(fps)

            # sleep remainder of frame
            self._clock.tick(Settings.UPDATE_FPS)


class RaceSimulator:
    SIZE = 1024, 768
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
        self._clock = pygame.time.Clock()

    def write_text(self, text, row, color=(255, 255, 255)):
        pos = 740, 30 + (row * 30)
        textsurface = self._font.render(text, True, color)
        self._screen.blit(textsurface, pos)

    def run(self):
        # scale the race canvas
        self._drawer.autoscale(self._env.get_buoys())

        # start thread for steering strategy
        thread = RaceUpdateThread(self._strategies, tf.get_default_graph())
        thread.daemon = True
        thread.start()

        while 1:
            self._screen.fill(self.BG_COLOR)
            self._env.update()

            self._drawer.draw_env(self._env)
            self._drawer.draw_buoys(self._env.get_buoys())

            # update all boats
            scoreboard = []
            for i, strategy in enumerate(self._strategies):

                # update boat and draw
                boat = strategy.get_boat()
                boat.update()
                self._drawer.draw_boat(boat)

                # update scoreboard
                scoreboard.append({
                    'name': strategy.get_name(),
                    'color': boat.get_boat_color(),
                    'marks_passed': boat.get_marks_passed(),
                    'dtw': boat.get_distance_to_waypoint()
                })

                # update boat with current fps
                fps = self._clock.get_fps()
                if fps > 0:
                    boat.set_draw_fps(fps)

            # show scoreboard
            scoreboard = pd.DataFrame(scoreboard).sort_values(by=['marks_passed', 'dtw'], ascending=[False, True])
            i = 0
            for _, row in scoreboard.iterrows():
                text = "%s (DTW: %dm)" % (row['name'], row.dtw)
                self.write_text(text, i, row.color)
                i += 1

            # display new frame
            pygame.display.flip()

            # check key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # save log and quit
                    if event.key == pygame.K_q:
                        exit()

            # sleep for the remainder of this frame
            self._clock.tick(Settings.DRAW_FPS)
