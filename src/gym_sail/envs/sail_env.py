import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import os

from simulators.rl import Simulator
from boat import *
from environment import Environment
from polar import Polar


class SailEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Discrete(3)

        self.observation_space = spaces.Box(low=-180, high=180, shape=(1,))

        self.seed()
        self.observation = None

        # start simulator
        polar = Polar(os.path.join('..', 'data', 'polars', 'first-27.csv'))
        self._env = Environment()
        self._boat = SimBoat(self._env, polar=polar)
        self._sim = Simulator(self._boat, self._env)

        self.reset()

        self._step = 0

    def render(self, mode='human', close=False):
        self._sim.render()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        print("action " + str(action))
        if action == 0:
            # do nothing
            pass

        elif action == 1:
            # steer left
            self._boat.steer(-1)

        elif action == 2:
            # steer right
            self._boat.steer(1)

        reward = 180 - abs(self._boat.get_course_error())

        self.observation = self._boat.get_course_error()

        self._step += 1
        done = False
        if self._step > 100:
            self._step = 0
            done = True

        print(self._step)

        return self.observation, reward, done, {"debug": 123}

    def reset(self):
        # self.observation = 0
        # return self.observation
        print("resetting")
        self._boat.reset_rudder()
        return self._boat.get_course_error()
