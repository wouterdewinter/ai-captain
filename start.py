import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from environment import Environment
from simulator import Simulator
from strategies import *
from my_strategy import *
from more_strategies import *

env = Environment()

# setup boat
#boat = Boat(env)
boat = RealBoat(env,ip_address='192.168.43.185')

# setup steering strategies
strategies = [
    MyStrategy(boat, env),
    Manual(boat, env),
    DoNothing(boat, env),
    Binary(boat, env),
    Smoother(boat, env),
    Proportional(boat, env),
]

# start the simulator
sim = Simulator(boat, env, strategies)
sim.run()