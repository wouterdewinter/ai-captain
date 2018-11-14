import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from environment import Environment
from polar import Polar
from race_simulator import RaceSimulator
from boat import SimBoat

# import configuration
try:
    from config import strategy_list
except ImportError:
    from config_default import strategy_list

# load polar
polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))

# create some buoys
scale = 0.05
buoys = [
    (52.3721693, 5.0750607),
    (52.3721693 + 0.01 * scale, 5.0750607),
    (52.3721693 + 0.008 * scale, 5.0750607 + 0.005 * scale),
    (52.3721693 + 0.002 * scale, 5.0750607 + 0.005 * scale),
]

# create environment
env = Environment(buoys=buoys)

# instantiate all strategies
strategies = []
for strategy in strategy_list:
    boat = SimBoat(env, polar=polar, random_color=True).set_waypoint(1)
    strategies.append(strategy(boat, env))

# start the simulator
sim = RaceSimulator(env, strategies)
sim.run()