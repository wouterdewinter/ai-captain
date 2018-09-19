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
boat = Boat(env)
#boat = RealBoat(ip_address='192.168.1.12')

# setup steering strategy
#strategy = Manual(boat, env)
strategy = MyStrategy(boat, env)

# start the simulator
sim = Simulator(boat, env, strategy)
sim.run()