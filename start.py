import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from environment import Environment
from simulator import Simulator
from polar import Polar

# import configuration
if os.path.isfile('config.py'):
    import config
else:
    print("Please copy config_default.py to config.py to add your own strategies")
    import config_default as config

# load polar
polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))

# setup boat
real_boat = len(sys.argv) == 2 and sys.argv[1] == 'real'

if real_boat:
    print('Using real boat, happy sailing!')
    env = Environment(wind_speed_var=1, wind_direction_var=0)
    boat = RealBoat(env, ip_address='192.168.43.185')
    shuffle_interval = 0
else:
    print('Using simulator boat')
    env = Environment()
    boat = SimBoat(env, polar=polar)
    shuffle_interval = 20

# instantiate all strategies
strategies = []
for strategy in config.strategy_list:
    strategies.append(strategy(boat, env))

# start the simulator
sim = Simulator(boat, env, strategies, shuffle_interval=shuffle_interval)
sim.run()
