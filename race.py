import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from environment import Environment
from polar import Polar
from simulators.race_simulator import RaceSimulator
from boat import SimBoat
from settings import Settings

# import configuration
if os.path.isfile('config.py'):
    from config import strategy_list
else:
    print("Please copy config_default.py to config.py to add your own strategies")
    from config_default import strategy_list

# load polar
polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))

# create environment
env = Environment(buoys=Settings.BUOYS)

# instantiate all strategies
strategies = []
for strategy in strategy_list:
    boat = SimBoat(env, polar=polar, random_color=True, name=strategy.__name__).set_waypoint(1)
    strategies.append(strategy(boat, env))

# start the simulator
sim = RaceSimulator(env, strategies)
sim.run()