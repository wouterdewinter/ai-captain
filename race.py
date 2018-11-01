import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from strategies import *
from environment import Environment
from simulator import Simulator
from polar import Polar
from race_simulator import RaceSimulator

# load polar
polar = Polar(os.path.join('data', 'polars', 'first-27.csv'))

# setup boat
real_boat = len(sys.argv) == 2 and sys.argv[1] == 'real'

# create some buoys
buoys = [
    (52.3831693, 5.0750607),
    (52.3721693, 5.0750607)
]

# create environment
env = Environment(buoys=buoys)

def create_boat():
    boat = SimBoat(env, polar=polar)
    return boat

# setup steering strategies
strategies = [
    TurnSpeed(create_boat(), env),
    MyStrategy(create_boat(), env),
    DoNothing(create_boat(), env),
    Binary(create_boat(), env),
    Smoother(create_boat(), env),
    Proportional(create_boat(), env),
]

# start the simulator
sim = RaceSimulator(env, strategies)
sim.run()