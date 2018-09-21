import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from environment import Environment
from simulator import Simulator
from strategies import *
from my_strategy import *
from my_deep_strategy import *
from more_strategies import *


# setup boat
real_boat = len(sys.argv) == 2 and sys.argv[1] == 'real'

if real_boat:
    print('Using real boat, happy sailing!')
    env = Environment(wind_speed_var=1, wind_direction_var=1)
    boat = RealBoat(env,ip_address='172.20.10.6')
    shuffle_interval = 0
else:
    print('Using simulator boat')
    env = Environment()
    boat = Boat(env)
    shuffle_interval = 20

# setup steering strategies
strategies = [
    #MyDeepStrategy(boat, env),
    MyStrategy(boat, env),
    Manual(boat, env),
    DoNothing(boat, env),
    Binary(boat, env),
    Smoother(boat, env),
    Proportional(boat, env),
]

# start the simulator
sim = Simulator(boat, env, strategies, shuffle_interval=shuffle_interval)
sim.run()