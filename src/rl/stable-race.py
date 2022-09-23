import gym
import os
from stable_baselines3 import A2C, PPO
from stable_baselines3.ppo import CnnPolicy
import gym_sail

t = 1548451946

ENV_NAME = 'race-continuous-v0'

#LOAD = True

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)

#model = A2C('MlpPolicy', env, verbose=1)
model = PPO('MlpPolicy', env, verbose=3, gamma=0.95, n_steps=256, ent_coef=0.0905168, learning_rate=0.00062211, vf_coef=0.042202, max_grad_norm=0.9, gae_lambda=0.99, n_epochs=5, clip_range=0.3, batch_size=256)

#Training and saving models along the way
TIMESTEPS = 1000
for i in range(10):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=3000, tb_log_name="PPO")
    model_filename = os.path.join('data', 'models', '%s_%d_%d_weights.h5f' % (ENV_NAME, t, TIMESTEPS*i))
    model.save(model_filename)

#model.learn(total_timesteps=90000, reset_num_timesteps=3000)

obs = env.reset()
for i in range(3000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()