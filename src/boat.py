import random
from threading import Thread
import pygame
import numpy as np
from math import sin, cos, radians
from random import uniform, randint
from datetime import datetime as dt
import pandas as pd
from pygeodesy import formy as geo
import logging

from tools import rotate_point, add_vector, rotate_vectors, calc_angle
from autopilot.ai_captain_utils import PilotControl
from settings import Settings


class Boat:
    """Base class for simulated and real boats"""

    # with a straight rudder a sailboat will eventually head straight into the wind
    # disabled for RL training: WEATHER_HELM_FORCE = 0.02
    WEATHER_HELM_FORCE = 0

    # amount of boat heel caused by the wind
    BOAT_HEEL_FORCE = 1

    # degrees rudder angle can change per second
    RUDDER_SPEED = 20

    # maximum angle rudder can be in
    MAX_RUDDER_ANGLE = 30

    # distance in meters from waypoint to skip to next waypoint
    DIST_NEXT_WAYPOINT = 2

    def __init__(self, env, random_color=False, name='no-name', keep_log=True):
        self._keep_log = keep_log
        self._name = name
        self.rudder_angle = 0.
        self.target_rudder_angle = 0.
        self.boat_angle = 0.
        self.boat_heel = 0.
        self.target_angle = 0
        self.speed = 3.
        self.x = 250.
        self.y = 250.
        self._env = env
        self.history = pd.DataFrame()
        self.windspeed_shuffle = True
        self._waypoint = None
        self._marks_passed = 0

        # set a boat color
        if random_color:
            self._boat_color = randint(30, 255), randint(30, 255), randint(30, 255)
        else:
            self._boat_color = 255, 255, 255

        # frames per second, used to calibrate behaviour across (simulated) boats
        self._draw_fps = Settings.DRAW_FPS

        self._strategy = None
        self._position = None

        # set initial position of boat
        self.reset_boat_position()

    def reset_boat_position(self):
        # add some noise to the longitude to simulate a start line
        self._position = (52.3721693, 5.0750607 + random.uniform(-0.0002, 0.0002))

    def set_heading(self, heading):
        self.boat_angle = heading

    def get_heading(self):
        return self.boat_angle

    def set_strategy(self, strategy):
        self._strategy = strategy

    def shuffle(self):
        self.set_target_angle(uniform(0, 360))

    def get_course_error(self):
        err = self.boat_angle - self.target_angle
        err = (err + 180) % 360 - 180
        return err

    def get_angle_of_attack(self):
        value = self._env.wind_direction - self.boat_angle
        value = (value + 180) % 360 - 180
        return value

    def steer(self, rudder_movement):
        self.set_target_rudder_angle(self.target_rudder_angle + rudder_movement)

    def set_target_rudder_angle(self, target_rudder_angle):
        self.target_rudder_angle = target_rudder_angle

        # maximize rudder angle
        self.target_rudder_angle = min(self.MAX_RUDDER_ANGLE, self.target_rudder_angle)
        self.target_rudder_angle = max(-self.MAX_RUDDER_ANGLE, self.target_rudder_angle)

    def set_target_angle(self, target_angle):
        target_angle = target_angle % 360
        self.target_angle = target_angle

    def calculate_speed(self):
        aoa = abs(self.get_angle_of_attack())
        speed = sin(radians(aoa / 1.2)) * self._env.wind_speed / 4

        # add bonus speed, don't want the boat to stop
        # todo: implement some momentum algorithm
        speed += 1
        return speed

    def reset_rudder(self):
        self.target_rudder_angle = 0
        self.rudder_angle = 0

    def move(self):
        """Simulates or fetches movement of boat"""

        # steering input (speed dependant)
        # not taking the absolute speed makes the steering reverse when going backwards
        self.boat_angle -= self.rudder_angle / 10 * self.speed / 5

        # apply weather helm
        force = sin(radians(self.boat_angle - self._env.wind_direction + 180))
        self.boat_angle += force * self.WEATHER_HELM_FORCE * self._env.wind_speed

        # calculate boat heel
        self.boat_heel = abs(force) * self._env.wind_speed * self.BOAT_HEEL_FORCE

        # calculate speed
        self.speed = self.calculate_speed()

        # move rudder with speed corrected for fps
        corr_rudder_speed = self.RUDDER_SPEED / self._draw_fps
        if abs(self.target_rudder_angle - self.rudder_angle) < corr_rudder_speed:
            self.rudder_angle = self.target_rudder_angle
        else:
            if self.target_rudder_angle > self.rudder_angle:
                self.rudder_angle += corr_rudder_speed
            else:
                self.rudder_angle -= corr_rudder_speed

        # wrap boat angle
        self.boat_angle = self.boat_angle + 360 if self.boat_angle < 0 else self.boat_angle
        self.boat_angle = self.boat_angle - 360 if self.boat_angle > 360 else self.boat_angle

        # update position
        lat, lon = self._position
        lat += cos(radians(self.boat_angle)) * self.speed / self._draw_fps / 3600 / 60
        lon += sin(radians(self.boat_angle)) * self.speed / self._draw_fps / 3600 / 60
        self._position = (lat, lon)

    def update(self):

        # simulate or fetch boat movements
        self.move()

        # run navigation when steering strategy is active
        if self._strategy is not None:
            self.nav()

        # skip to next waypoint if we're there
        if self._waypoint is not None:
            if self.get_distance_to_waypoint() < self.DIST_NEXT_WAYPOINT:
                logging.info("hit waypoint")
                self._marks_passed += 1
                self._waypoint = self._waypoint + 1 if self._waypoint < len(self._env.get_buoys()) - 1 else 0

        # save history
        if self._keep_log:
            self.history = self.history.append([{
                'datetime': dt.now(),
                'boat_angle': self.boat_angle + np.random.normal(0, 1),
                'boat_heel': self.boat_heel if np.random.uniform(0, 1) < 0.99 else np.nan,
                'boat_speed': self.speed + np.random.normal(0, 0.25),
                'target_angle': self.target_angle if np.random.uniform(0, 1) < 0.99 else np.nan,
                'course_error': self.get_course_error(),
                'rudder_angle': self.rudder_angle,
                'wind_direction': self._env.wind_direction,
                'wind_speed': self._env.wind_speed if np.random.uniform(0, 1) < 0.99 else np.random.randint(100, 150),
                'angle_of_attack': self.get_angle_of_attack()
            }])

    def nav(self):
        """ Update navigation variables and determine new course """
        if self._waypoint is None:
            return

        # determine bearing to waypoint
        bearing = self.get_bearing_to_waypoint()

        # calculate new true wind angle to steer
        new_twa = calc_angle(self._env.wind_direction, bearing)

        # get angles for optimal vmg
        upwind_twa = self._strategy.get_upwind_twa()
        downwind_twa = self._strategy.get_downwind_twa()

        # do need to steer an upwind course?
        if abs(new_twa) < upwind_twa:
            self.set_twa(upwind_twa, tack=self._strategy.need_to_tack())

        # do need to steer an downwind course?
        elif abs(new_twa) > downwind_twa:
            self.set_twa(downwind_twa, tack=self._strategy.need_to_gybe())

        # otherwise, steer directly to waypoint
        else:
            self.set_target_angle(bearing)

    def set_twa(self, twa, tack=False):
        """ steer a true wind angle on the current (target) tack """
        assert twa >= 0, "twa must be a positive number"

        # set target on the other tack
        if tack:
            twa = -twa

        # check true wind angle of target course
        target_twa = calc_angle(self.target_angle, self._env.wind_direction)

        # check if we're on port or starboard and determine new course
        if target_twa > 0:
            heading = self._env.wind_direction + twa
        else:
            heading = self._env.wind_direction - twa

        # set new course
        self.set_target_angle(heading)

    def get_position(self):
        return self._position

    def set_waypoint(self, waypoint):
        """set new waypoint, also resets number of marks passed"""

        self._waypoint = waypoint
        self._marks_passed = 0
        return self

    def get_boat_color(self):
        return self._boat_color

    def get_marks_passed(self):
        return self._marks_passed

    def get_distance_to_waypoint(self):
        buoys = self._env.get_buoys()
        target_pos = buoys[self._waypoint]
        return geo.haversine(self._position[0], self._position[1], target_pos[0], target_pos[1])

    def get_bearing_to_waypoint(self):
        buoys = self._env.get_buoys()
        target_pos = buoys[self._waypoint]
        return geo.bearing(self._position[0], self._position[1], target_pos[0], target_pos[1])

    def get_name(self):
        return self._name

    def set_draw_fps(self, fps):
        self._draw_fps = fps

    def get_distance_to_boat(self, boat: "Boat"):
        return geo.haversine(self._position[0], self._position[1], boat._position[0], boat._position[1])


class SimBoat(Boat):

    # ratio of speed change per second so boat keeps some momentum
    SPEED_CHANGE_RATE = 0.3

    def __init__(self, env, polar, random_color=False, **kwargs):
        super().__init__(env, random_color=random_color, **kwargs)
        self._polar = polar
        self._speed = 5

    def calculate_speed(self):
        target_speed = self._polar.get_speed(twa=self.get_angle_of_attack(), tws=self._env.wind_speed)

        # add some rudder drag
        target_speed *= 1-abs(self.rudder_angle)/100

        delta = target_speed - self._speed

        self._speed += delta * (self.SPEED_CHANGE_RATE / self._draw_fps)

        return self._speed


#  todo remove!
rudder_center = 418
rudder_multiply = 3


# making threads to keep interface from lagging
def poll_data(result,pilot):
    while True:
        try:
            data = pilot.get_data_from_pilot()
        except Exception as e:
            print(e)
            return
        data = str(data).replace("'","")
        data = str(data).split(',')

        result['boat_angle'] = float(data[-2])
        result['rudder_angle'] = -1. * ((int(data[8])-rudder_center)/rudder_multiply)
        result['boat_heel'] = abs(float(data[1]))
        result['speed'] = float(data[-1]) / 1.852

        logging.info("observed rudder angle (raw: %d, real: %d)" % (int(data[8]), result['rudder_angle']))


def set_rudder_angle(angle, pilot, rudder_center):
    translated_target_rudder_angle = int((-angle * rudder_multiply) + rudder_center)
    logging.info("setting target rudder angle (raw: %d, real: %d)" % (translated_target_rudder_angle, angle))
    pilot.set_rudder_angle(translated_target_rudder_angle)
    return


class RealBoat(Boat):
    RUDDER_CENTER = 418

    def __init__(self, env, ip_address='192.168.43.185'):
        self._pilot = PilotControl(ip_address=ip_address)
        super().__init__(env)
        self.windspeed_shuffle = False
        self.result = {}
        self.result['boat_angle'] = 0
        self.result['rudder_angle'] = 0
        self.result['boat_heel'] = 0
        self.result['speed'] = 0
        self.last_rudder_angle = 0
        polling_thread = Thread(target=poll_data, args=(self.result, self._pilot),daemon=True)
        polling_thread.start()
        self.set_rudder_thread = None

    def set_target_rudder_angle(self, target_rudder_angle):
        super().set_target_rudder_angle(target_rudder_angle)

        #print('setting target rudder angle to: ', target_rudder_angle)

        if self.last_rudder_angle != target_rudder_angle:
            if self.set_rudder_thread is None or not self.set_rudder_thread.is_alive():
                print('starting thread')
                self.set_rudder_thread = Thread(target=set_rudder_angle, args=(target_rudder_angle, self._pilot, self.RUDDER_CENTER),
                                                daemon=True)
                self.set_rudder_thread.start()

        self.last_rudder_angle = target_rudder_angle

    def set_target_angle(self, target_angle):
        super().set_target_angle(target_angle)

    def move(self):
        self.boat_angle = self.result['boat_angle']
        self.rudder_angle = self.result['rudder_angle']
        self.boat_heel = self.result['boat_heel']
        self.speed = self.result['speed']
