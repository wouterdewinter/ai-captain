import gym
import os
from stable_baselines3 import A2C, PPO, DDPG, SAC
from stable_baselines3.common.callbacks import EvalCallback
import gym_sail

ENV_NAME = 'race-continuous-v0'
RUN_NAME = 'ppo-justin-1'
TIMESTEPS = 100000000
#LOAD_FILE = "ppo-1_1380000_weights.zip"  # 270000
LOAD_FILE = "ppo-justin-1"
TRAIN = 0

env = gym.make(ENV_NAME)

#model = A2C('MlpPolicy', env, verbose=1)
#model = PPO('MlpPolicy', env, verbose=3)
#model = DDPG('MlpPolicy', env, verbose=1)
#model = SAC('MlpPolicy', env, verbose=3)
model = PPO('MlpPolicy', env, verbose=1, gamma=0.95, n_steps=256, ent_coef=0.0905168, learning_rate=0.00062211, vf_coef=0.042202, max_grad_norm=0.9, gae_lambda=0.99, n_epochs=5, clip_range=0.3, batch_size=256)

if LOAD_FILE:
    print("loading "+LOAD_FILE)
    model_filename = os.path.join('data', 'models', LOAD_FILE, 'best_model.zip')
    model.load(model_filename, env)

if TRAIN:
    save_path = os.path.join('data', 'models', RUN_NAME)
    cb = EvalCallback(eval_env=env, render=False, n_eval_episodes=3, eval_freq=100000, best_model_save_path=save_path, log_path=save_path)
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO", callback=cb)
    # for i in range(100):
    #     model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO", callback=cb)
    #     model_filename = os.path.join('data', 'models', '%s_%d_weights' % (RUN_NAME, TIMESTEPS * (i + 1)))
    #     model.save(model_filename)

obs = env.reset()
for i in range(30000):
    action, _state = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()