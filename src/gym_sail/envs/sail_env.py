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

        high = np.array([180, 30])
        self.observation_space = spaces.Box(low=-high, high=high, dtype=np.float32)

        self.seed()
        self.observation = None

        # start simulator
        polar = Polar(os.path.join('..', 'data', 'polars', 'first-27.csv'))
        self._env = Environment()
        self._boat = SimBoat(self._env, polar=polar)
        self._sim = Simulator(self._boat, self._env)

        self.reset()

        self._step = 0

        self._last_course_error = 0

    def render(self, mode='human', close=False):
        self._sim.render()

    def seed(self, seed=None):
        seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)

        if action == 0:
            # steer left
            self._boat.steer(-1)

        elif action == 1:
            # do nothing
            pass

        elif action == 2:
            # steer right
            self._boat.steer(1)

        # update boat and environment
        self._env.update()
        self._boat.update()

        # change in course error
        # delta = abs(self._last_course_error - self._boat.get_course_error())
        # print (delta)

        reward = -abs(self._boat.get_course_error() / 180)

        # print(reward)
        self.observation = self._boat.get_course_error(), self._boat.rudder_angle

        # save couse error
        self._last_course_error = self._boat.get_course_error()

        self._step += 1
        done = False
        if self._step > 300:
            self._step = 0
            done = True

        return self.observation, reward, done, {"debug": 123}

    def reset(self):
        print("resetting")
        self._boat.reset_rudder()
        self._env.shuffle()
        self._boat.shuffle()
        return self._boat.get_course_error(), self._boat.rudder_angle
