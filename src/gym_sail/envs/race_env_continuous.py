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
        polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))
        self._env = Environment(buoys=Settings.BUOYS)
        self._boat = SimBoat(self._env, polar=polar, keep_log=False).set_waypoint(1)
        self._drawer = RaceDrawer([self._boat], self._env)

        self.reset()
        self._step = 0
        self._last_distance = 0
        self._last_reward = 0
        self._last_marks_passed = 0

    def render(self, mode='human', close=False):
        obs = self.get_observation()
        self._drawer.draw(str(round(obs[0], 3)) + " / " + str(round(obs[1], 3)) + " / " + str(round(obs[2], 3)) + "R: " + str(round(self._last_reward, 2)))

        # should we quit?
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()

    def seed(self, seed=None):
        seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        self._last_distance = self._boat.get_distance_to_waypoint()

        #assert self.action_space.contains(action)
        rudder_angle = float(action) * 30
        self._boat.set_target_rudder_angle(rudder_angle)

        # update boat and environment
        self._env.update()
        self._boat.update()

        #mark_reward = self._boat.get_marks_passed() * 100
        #reward = mark_reward - self._boat.get_distance_to_waypoint()
        reward = self._last_distance - self._boat.get_distance_to_waypoint()

        # make a negative reward count heavier to prevent going in circles
        if reward < 0:
            reward *= 3

        self._step += 1

        # limit number of steps
        done = False
        if self._step > 15000:
            self._step = 0
            done = True
            print("done due to max steps")

        # out of bounds
        if self._boat.get_distance_to_waypoint() > 80:
            self._step = 0
            done = True
            reward = -100
            print("done due to max distance")

        if self._boat.get_marks_passed() > self._last_marks_passed:
            self._last_marks_passed = self._boat.get_marks_passed()
            print("we rounded a mark!")
            reward = 1000

        # penalty if we are going too slow
        if self._boat.speed < 1:
            reward -= 1

        self._last_reward = reward

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
        self._boat.set_waypoint(1)
        return self.get_observation()
