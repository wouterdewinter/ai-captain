from boat import SimBoat
from strategies import *

def get_strategy(env, polar):

    # use normal boat
    boat = SimBoat(env, polar=polar, random_color=True, name='Default').set_waypoint(1)

    # select strategy to use and return
    return TurnSpeed(boat, env)
