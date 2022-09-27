import gym
import os
from stable_baselines3 import A2C, PPO, DDPG, SAC
from stable_baselines3.common.callbacks import EvalCallback, CallbackList, CheckpointCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_util import make_vec_env
import gym_sail

ENV_NAME = 'race-continuous-v0'
RUN_NAME = 'ppo-7-video'
TIMESTEPS = 100000000
LOAD_FILE = 0
TRAIN = 1

tensorboard_log = os.path.join('data', 'logs', 'progress_tensorboard')

eval_env = gym.make(ENV_NAME, recording_path=os.path.join('data', 'models', RUN_NAME))
env = make_vec_env(ENV_NAME, n_envs=8)

#model = A2C('MlpPolicy', env, verbose=1, tensorboard_log=tensorboard_log)
model = PPO('MlpPolicy', env, verbose=0, tensorboard_log=tensorboard_log)
# model = PPO('MlpPolicy',
#             env,
#             verbose=0,
#             tensorboard_log=tensorboard_log,
#             # n_envs=16,
#             # n_timesteps=1e6,
#             n_steps=1024,
#             batch_size=64,
#             gae_lambda=0.98,
#             gamma=0.999,
#             n_epochs=4,
#             ent_coef=0.01)
#model = DDPG('MlpPolicy', env, verbose=1)
#model = SAC('MlpPolicy', env, verbose=3)
#model = PPO('MlpPolicy', env, tensorboard_log=tensorboard_log, verbose=1, gamma=0.95, n_steps=256, ent_coef=0.0905168, learning_rate=0.00062211, vf_coef=0.042202, max_grad_norm=0.9, gae_lambda=0.99, n_epochs=5, clip_range=0.3, batch_size=256)

if LOAD_FILE:
    print("loading from file")
    #model_filename = os.path.join('data', 'models', 'ppo-6', 'best_model')
    model_filename = os.path.join('data', 'models', 'ppo-5-random-course', 'best_model')
    model = model.load(model_filename, env, tensorboard_log=tensorboard_log)

if TRAIN:
    save_path = os.path.join('data', 'models', RUN_NAME)
    eval_callback = EvalCallback(eval_env=eval_env, render=True, n_eval_episodes=1, eval_freq=20000, best_model_save_path=save_path)
    checkpoint_callback = CheckpointCallback(save_freq=50000, save_path=save_path)
    callback = CallbackList([checkpoint_callback, eval_callback])

    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=RUN_NAME, callback=callback)

evaluate_policy(model, eval_env, render=True, n_eval_episodes=3)

