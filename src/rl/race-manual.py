import pygame
import gym
import gym_sail
from stable_baselines3.common.env_checker import check_env

env = gym.make('race-continuous-v0', recording_path=".")

check_env(env, skip_render_check=False)

joy = None
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(f"Found joystick {joy.get_name()} with {joy.get_numaxes()} axis")

for i_episode in range(1):
    env.reset()

    for t in range(10000):
        env.render()

        # default no action
        action = 0

        # get input from joystick
        if joy:
            action = -joy.get_axis(0)

        # get input from keyboard
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            action = 1
        elif pressed[pygame.K_RIGHT]:
            action = -1
        # allow quitting episode after a few time steps to prevent race condition
        elif pressed[pygame.K_e] and t > 10:
            print("Episode terminated manually")
            break

        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps, {}".format(t+1, info))
            break
