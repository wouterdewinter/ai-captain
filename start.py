import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from environment import Environment
from strategies import *
from simulator import Simulator

env = Environment()
boat = Boat(env)
#boat = RealBoat(ip_address='192.168.1.12')
#strategy = Manual(boat, env)
strategy = GB(boat, env)

sim = Simulator(boat, env, strategy)
sim.run()