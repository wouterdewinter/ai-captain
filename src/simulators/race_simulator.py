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

    def __init__(self, env, strategies):
        self._env = env
        self._strategies = strategies

        boats = [strategy.get_boat() for strategy in strategies]

        self._drawer = RaceDrawer(boats, env)
        self._clock = pygame.time.Clock()

    def run(self):

        # start thread for steering strategy
        thread = RaceUpdateThread(self._strategies, tf.compat.v1.get_default_graph())
        thread.daemon = True
        thread.start()

        while 1:
            self._env.update()

            # update all boats
            for strategy in self._strategies:
                boat = strategy.get_boat()
                boat.update()

                # update boat with current fps
                fps = self._clock.get_fps()
                if fps > 0:
                    boat.set_draw_fps(fps)

            # draw objects
            self._drawer.draw()

            # check key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # save log and quit
                    if event.key == pygame.K_q:
                        exit()

            # sleep for the remainder of this frame
            self._clock.tick(Settings.DRAW_FPS)
