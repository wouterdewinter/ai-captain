import gym
import time

# # Will be supported in future releases
# from gym.envs import mujoco
#
# mujoco.AntEnv

import gym_sail

env = gym.make('sail-v0')

for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print(observation, reward, action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

        #time.sleep(1)
