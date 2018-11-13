import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from boats.polar_boat import PolarBoat
from strategies import *
from environment import Environment
from polar import Polar
from race_simulator import RaceSimulator

# load polar
polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))

# create some buoys
buoys = [
    (52.3721693, 5.0750607),
    (52.3721693 + 0.01, 5.0750607),
    (52.3721693 + 0.008, 5.0750607 + 0.005),
    (52.3721693 + 0.002, 5.0750607 + 0.005),
]

# create environment
env = Environment(buoys=buoys)

# setup steering strategies
strategies = [
    Proportional(SimBoat(env, polar=polar, random_color=True, name='normal').set_waypoint(1), env),
    Proportional(PolarBoat(env, polar=polar, random_color=True, name='polar', angles_file=os.path.join('data', 'angles.pkl')).set_waypoint(1), env),
]

# start the simulator
sim = RaceSimulator(env, strategies)
sim.run()