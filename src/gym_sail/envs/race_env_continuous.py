import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import os
import random

from boat import *
from environment import Environment
from polar import Polar
from drawers.race_drawer import RaceDrawer
from settings import Settings


class RaceEnvContinuous(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(3,), dtype=np.float32)

        self.seed()
        self.observation = None

        # start simulator
        polar = Polar(os.path.join('..', 'data', 'polars', 'first-27.csv'))
        self._env = Environment(buoys=Settings.BUOYS)
        self._boat = SimBoat(self._env, polar=polar, keep_log=False).set_waypoint(1)
        self._drawer = RaceDrawer([self._boat], self._env)

        self.reset()
        self._step = 0

    def render(self, mode='human', close=False):
        self._drawer.draw()

        # should we quit?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()

    def seed(self, seed=None):
        seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        #assert self.action_space.contains(action)
        rudder_angle = float(action) * 30
        self._boat.set_target_rudder_angle(rudder_angle)

        # update boat and environment
        self._env.update()
        self._boat.update()

        mark_reward = self._boat.get_marks_passed() * 100
        reward = mark_reward - self._boat.get_distance_to_waypoint()

        # self._step += 1
        done = False
        # if self._step > 300:
        #     self._step = 0
        #     done = True
        #     print("done")q

        return self.get_observation(), reward, done, {"debug": 123}

    def get_observation(self):
        delta = self._boat.get_heading() - self._boat.get_bearing_to_waypoint()
        delta = (delta + 180) % 360 - 180
        return (
            delta / 180,
            self._boat.rudder_angle / 30,
            self._boat.get_angle_of_attack() / 180
        )

    def reset(self):
        self._boat.reset_rudder()
        self._boat.reset_boat_position()
        self._boat.set_heading(random.randint(-90, 90))
        return self.get_observation()
