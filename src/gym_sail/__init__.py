from gym.envs.registration import register

register(
    id='sail-v0',
    entry_point='gym_sail.envs:SailEnv',
)