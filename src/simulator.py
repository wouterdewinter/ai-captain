import os, pygame
import datetime
import time
import threading
import tensorflow as tf

from boat import Boat
from environment import Environment
from strategies.base import Base
from settings import Settings
from drawers.sim_drawer import SimDrawer


class UpdateThread (threading.Thread):
    """Thread for updating the steering strategy"""

    def __init__(self, boat: Boat, env: Environment, strategy: Base, graph):
        threading.Thread.__init__(self)
        self._boat = boat
        self._env = env
        self._strategy = strategy
        self._clock = pygame.time.Clock()
        self._graph = graph

    def set_strategy(self, strategy: Base):
        self._strategy = strategy

    def run(self):
        while 1:
            # update steering strategy
            # need to set default graph to enable keras models to run in a different thread
            with self._graph.as_default():
                self._strategy.update()

            # sleep remainder of frame
            self._clock.tick(Settings.UPDATE_FPS)
            fps = self._clock.get_fps()

            # update strategy with current fps
            if fps > 0:
                self._strategy.set_update_fps(fps)


class Simulator:
    """Single boat simulator"""

    def __init__(self, boat: Boat, env: Environment, strategies: list, shuffle_interval=10):
        self._boat = boat
        self._env = env
        self._strategies = strategies
        self._shuffle_interval = shuffle_interval

        # pick first strategy as default
        self._strategy_id = 0
        self._strategy = strategies[self._strategy_id]

        self._drawer = SimDrawer()
        self._clock = pygame.time.Clock()

    def run(self):
        shuffle_time = time.time() + self._shuffle_interval

        # initial shuffle
        self._env.shuffle()
        self._boat.shuffle()

        # start thread for steering strategy
        thread = UpdateThread(self._boat, self._env, self._strategy, tf.get_default_graph())
        thread.daemon = True
        thread.start()

        while 1:
            # update boat and environment
            self._env.update()
            self._boat.update()

            # redraw objects
            self._drawer.draw(self._boat, self._env, self._strategy.get_name())

            # shuffle once in a while
            if self._shuffle_interval and time.time() > shuffle_time:
                self._env.shuffle()
                self._boat.shuffle()
                shuffle_time += self._shuffle_interval

            # check key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:

                    # switch strategy
                    if event.key == pygame.K_s:
                        self._strategy_id = self._strategy_id + 1 if self._strategy_id < len(self._strategies) - 1 else 0
                        self._strategy = self._strategies[self._strategy_id]
                        thread.set_strategy(self._strategy)

                    # save log and quit
                    if event.key == pygame.K_q:
                        date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d_%H%M')
                        filename = os.path.join('data', 'logs', 'history_%s.csv' % date)
                        self._boat.history.to_csv(filename)
                        print("Wrote datalog to %s" % filename)
                        exit()

            # check for pressed keys (not the same as key events)
            pressed = pygame.key.get_pressed()

            # change wind direction
            if pressed[pygame.K_3]:
                self._env.change_wind_direction(-1)
            if pressed[pygame.K_4]:
                self._env.change_wind_direction(1)

            # change wind direction
            if pressed[pygame.K_5]:
                self._env.change_wind_speed(-1)
            if pressed[pygame.K_6]:
                self._env.change_wind_speed(1)

            # change target angle
            if pressed[pygame.K_1]:
                self._boat.set_target_angle(self._boat.target_angle - 3)
            if pressed[pygame.K_2]:
                self._boat.set_target_angle(self._boat.target_angle + 3)

            # sleep for the remainder of this frame
            self._clock.tick(Settings.DRAW_FPS)
            fps = self._clock.get_fps()

            # update boat with current fps
            if fps > 0:
                self._boat.set_draw_fps(fps)
