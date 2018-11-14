from .my_strategy import *
from boat import SimBoat
from polar_boat import PolarBoat

def get_strategy(env, polar):

    angles_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'angles.pkl')

    if os.path.isfile(angles_file):
        # use boat with predefined upwind and downwind angles, uncomment to use
        boat = PolarBoat(env, polar=polar, random_color=True, name='My Boat', angles_file=angles_file).set_waypoint(1)
    else:
        # use normal boat
        boat = SimBoat(env, polar=polar, random_color=True, name='My Boat').set_waypoint(1)

    # select strategy to use and return
    return MyStrategy(boat, env)
