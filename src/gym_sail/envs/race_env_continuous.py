import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import os
import random

from boat import *
from buoys import trapezoidal, buoys_noise, buoys_translate
from environment import Environment
from polar import Polar
from drawers.race_drawer import RaceDrawer
from settings import Settings


class RaceEnvContinuous(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = spaces.Box(low=-1, high=1, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(7,), dtype=np.float32)

        self.seed()
        self.observation = None

        # start simulator
        polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))
        self._env = Environment(buoys=Settings.BUOYS)
        self._boat = SimBoat(self._env, polar=polar, keep_log=False).set_waypoint(1)
        self._drawer = RaceDrawer([self._boat], self._env)

        self._step = 0
        self._last_distance = 0
        self._last_reward = 0
        self._total_reward = 0
        self._last_marks_passed = 0
        self._last_action = 0

        self.reset()

    def render(self, mode='human', close=False):
        obs = self.get_observation()
        debug = [
            # 'Delta: ' + str(round(obs[0], 3)),
            # 'Rudder angle: ' + str(round(obs[1], 3)),
            # 'Angle of attack: ' + str(round(obs[2], 3)),
            # 'Speed: ' + str(round(obs[3], 3)),
            # 'DTW: ' + str(round(obs[4], 3)),
            'Delta x: ' + str(round(obs[0], 3)),
            'Delta y: ' + str(round(obs[1], 3)),
            'Angle of attack x: ' + str(round(obs[2], 3)),
            'Angle of attack y: ' + str(round(obs[3], 3)),
            'Rudder angle: ' + str(round(obs[4], 3)),
            'Speed: ' + str(round(obs[5], 3)),
            'DTW: ' + str(round(obs[6], 3)),
            'Reward: ' + str(round(self._last_reward, 2)),
            'Total reward: ' + str(round(self._total_reward, 2)),
            'Last action: %.2f ' % self._last_action,
            'Step: ' + str(self._step)
        ]
        self._drawer.draw(debug)

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
        self._last_action = action
        self._step += 1

        #assert self.action_space.contains(action)
        rudder_angle = float(action) * 30
        self._boat.set_target_rudder_angle(rudder_angle)

        # update boat and environment
        self._env.update()
        self._boat.update()

        #mark_reward = self._boat.get_marks_passed() * 100
        #reward = mark_reward - self._boat.get_distance_to_waypoint()
        reward = self._last_distance - self._boat.get_distance_to_waypoint()

        # after a reset of the last distance, prevent giving a negative reward
        if self._last_distance == 0:
            reward = 0

        # make a negative reward count heavier to prevent going in circles
        if reward < 0:
            reward *= 3

        # limit number of steps
        done = False
        if self._step > 5000:
            done = True
            print("done due to max steps")

        # out of bounds
        if self._boat.get_distance_to_waypoint() > 80:
            done = True
            reward = -100
            print("done due to max distance")

        # big reward for passing a mark
        if self._boat.get_marks_passed() > self._last_marks_passed:
            self._last_marks_passed = self._boat.get_marks_passed()
            print("we rounded a mark!")
            reward = 1000

        # give a small award for speed
        reward += self._boat.speed / 100

        # penalty if we are going too slow
        if self._boat.speed < 2:
            reward -= 1

        self._last_reward = reward
        self._total_reward += reward

        return self.get_observation(), reward, done, {"total_reward": self._total_reward}

    def get_observation(self):
        delta = self._boat.get_heading() - self._boat.get_bearing_to_waypoint()
        #delta = (delta + 180) % 360 - 180
        return np.array(
            list(to_vector(delta)) + list(to_vector(self._boat.get_angle_of_attack())) + [
            self._boat.rudder_angle / 30,
            self._boat.speed / 10,
            self._boat.get_distance_to_waypoint() / 100
        ])

    # def get_observation(self):
    #     delta = self._boat.get_heading() - self._boat.get_bearing_to_waypoint()
    #     delta = (delta + 180) % 360 - 180
    #     return np.array([
    #         delta / 180,
    #         self._boat.rudder_angle / 30,
    #         self._boat.get_angle_of_attack() / 180,
    #         self._boat.speed / 10,
    #         self._boat.get_distance_to_waypoint() / 100
    #     ])
    def reset(self):
        self._boat.reset_rudder()
        self._boat.reset_boat_position()
        self._boat.set_heading(random.randint(-90, 90))
        self._boat.set_waypoint(1)

        self._step = 0
        self._last_distance = 0
        self._last_reward = 0
        self._total_reward = 0
        self._last_marks_passed = 0
        self._last_action = 0

        # generate new course
        buoys = buoys_translate(buoys_noise(trapezoidal(width=random.uniform(0.04, 0.06))))
        self._env.set_buoys(buoys)

        return self.get_observation()


def to_vector(deg):
    rad = radians(deg)
    return [cos(rad), sin(rad)]
