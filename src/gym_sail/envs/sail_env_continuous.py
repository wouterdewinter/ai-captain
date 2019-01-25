import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import os

from boat import *
from environment import Environment
from polar import Polar
from drawers.sim_drawer import SimDrawer


class SailEnvContinuous(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Box(low=-30, high=30, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        self.seed()
        self.observation = None

        # start simulator
        polar = Polar(os.path.join('..', 'data', 'polars', 'first-27.csv'))
        self._env = Environment()
        self._boat = SimBoat(self._env, polar=polar, keep_log=False)
        self._drawer = SimDrawer()

        self.reset()
        self._step = 0

    def render(self, mode='human', close=False):
        self._drawer.draw(self._boat, self._env)

        # should we quit?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()

    def seed(self, seed=None):
        seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        action = action * 30
        self._boat.set_target_rudder_angle(int(action))

        # update boat and environment
        self._env.update()
        self._boat.update()

        reward = -abs(self._boat.get_course_error() / 180)

        self._step += 1
        done = False
        if self._step > 300:
            self._step = 0
            done = True

        return self.get_observation(), reward, done, {"debug": 123}

    def get_observation(self):
        return (
            self._boat.get_course_error() / 180,
            self._boat.rudder_angle / 30,
            #self._boat.get_angle_of_attack()
        )

    def reset(self):
        print("resetting")
        self._boat.reset_rudder()
        self._env.shuffle()
        self._boat.shuffle()
        return self.get_observation()
