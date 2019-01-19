import os

from boat import *
from environment import Environment
from simulators.evaluate import Evaluate
from polar import Polar

# import configuration
if os.path.isfile('config.py'):
    import config
else:
    print("Please copy config_default.py to config.py to add your own strategies")
    import config_default as config

# load polar
polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))

# setup boat and env
env = Environment()
boat = SimBoat(env, polar=polar)

# pick first strategy
strategy = config.strategy_list[0](boat, env)

# start the simulator
sim = Evaluate(boat, env, strategy)
sim.run()