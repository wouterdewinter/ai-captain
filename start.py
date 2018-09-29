import os, sys

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import *
from environment import Environment
from simulator import Simulator
from polar import Polar

# from strategies import *
# from my_strategy import *
# from my_deep_strategy import *
# from more_strategies import *
#
# from deep_danny import *
# from roderick_deep_strategy import *
# from roderick_strategy import *
# from jeroen_strategy import *
# from tad_strategies import *
# from andre_deep_strategy import *
# from andre_strategy import *

# import importlib
#
# # import all strategy files
# path = os.path.join('src', 'strategies')
# for module in os.listdir(path):
#     if module[-3:] == '.py':
#         print(module[:-3])
#         importlib.import_module('*', 'strategies.'+module[:-3])

from strategies import *

# load polar
polar = Polar(os.path.join('data', 'polars', 'ff95-skip-intro.csv'))

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
    boat = SimBoat(env, polar=polar)
    shuffle_interval = 200

# setup steering strategies
strategies = [
    # AndreStrategy(boat, env),
    # AndreDeepStrategy(boat, env),
    # RoderickGB(boat, env),
    # RoderickDeepStrategy(boat, env),
    # DeepDanny(boat, env),
    # JeroenStrategy(boat, env),
    # TadDeepStrategy(boat, env),
    # TadRegressionStrategy(boat, env),
    # TadHeuristicStrategy(boat, env),
    # MyStrategy(boat, env),
    strategies.Manual(boat, env),
    # DoNothing(boat, env),
    # Binary(boat, env),
    # Smoother(boat, env),
    more_strategies.Proportional(boat, env),
]

# start the simulator
sim = Simulator(boat, env, strategies, shuffle_interval=shuffle_interval)
sim.run()