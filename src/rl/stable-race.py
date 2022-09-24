import gym
import os
from stable_baselines3 import A2C, PPO, DDPG, SAC
from stable_baselines3.common.callbacks import EvalCallback, CallbackList, CheckpointCallback
from stable_baselines3.common.evaluation import evaluate_policy
import gym_sail

ENV_NAME = 'race-continuous-v0'
RUN_NAME = 'justin-ppo-7'
TIMESTEPS = 100000000
LOAD_FILE = 0
TRAIN = 1

tensorboard_log = os.path.join('data', 'logs', 'progress_tensorboard')

env = gym.make(ENV_NAME)

#model = A2C('MlpPolicy', env, verbose=1)
#model = PPO('MlpPolicy', env, verbose=3, tensorboard_log=tensorboard_log)
#model = DDPG('MlpPolicy', env, verbose=1)
#model = SAC('MlpPolicy', env, verbose=3)
model = PPO('MlpPolicy', env, verbose=1, gamma=0.95, n_steps=256, ent_coef=0.0905168, learning_rate=0.00062211, vf_coef=0.042202, max_grad_norm=0.9, gae_lambda=0.99, n_epochs=5, clip_range=0.3, batch_size=256)

if LOAD_FILE:
    print("loading from file")
    #model_filename = os.path.join('data', 'models', 'ppo-6', 'best_model')
    model_filename = os.path.join('data', 'models', 'ppo-justin-5', 'best_model')
    model = model.load(model_filename, env)

if TRAIN:
    save_path = os.path.join('data', 'models', RUN_NAME)
    eval_callback = EvalCallback(eval_env=env, render=True, n_eval_episodes=1, eval_freq=100000, best_model_save_path=save_path)
    checkpoint_callback = CheckpointCallback(save_freq=50000, save_path=save_path)
    callback = CallbackList([checkpoint_callback, eval_callback])

    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=ENV_NAME, callback=callback)
    # for i in range(100):
    #     model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO", callback=cb)
    #     model_filename = os.path.join('data', 'models', '%s_%d_weights' % (RUN_NAME, TIMESTEPS * (i + 1)))
    #     model.save(model_filename)

evaluate_policy(model, env, render=True, n_eval_episodes=3, deterministic=True)

# obs = env.reset()
# for i in range(30000):
#     action, _state = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action*100)
#     env.render()
#     if done:
#       obs = env.reset()