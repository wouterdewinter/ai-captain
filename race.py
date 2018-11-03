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
    (52.3721693, 5.0750607),
    (52.3831693, 5.0750607)
]

# create environment
env = Environment(buoys=buoys)

def create_boat(**kwargs):
    boat = SimBoat(env, polar=polar, random_color=True, **kwargs)
    boat.set_waypoint(1)
    return boat

# setup steering strategies
strategies = [
#    TurnSpeed(create_boat(), env),
#    MyStrategy(create_boat(), env),
#    DoNothing(create_boat(), env),
#    Binary(create_boat(), env),
#    Smoother(create_boat(), env),
    Proportional(create_boat(upwind_twa=35, tack_angle=60, name='35-60'), env),
    Proportional(create_boat(upwind_twa=38, tack_angle=60, name='38-60'), env),
    Proportional(create_boat(upwind_twa=40, tack_angle=60, name='40-60'), env),
    Proportional(create_boat(upwind_twa=38, tack_angle=45, name='38-45'), env),
    Proportional(create_boat(upwind_twa=38, tack_angle=60, name='38-60'), env),
    Proportional(create_boat(upwind_twa=48, tack_angle=80, name='38-80'), env),
]

# start the simulator
sim = RaceSimulator(env, strategies)
sim.run()