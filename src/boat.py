from threading import Thread

import pygame
from math import sin, cos, radians
from random import random, uniform, randint
from tools import rotate_point, add_vector, rotate_vectors, calc_angle
from autopilot.ai_captain_utils import PilotControl
from datetime import datetime as dt
import pandas as pd
from pygeodesy import formy as geo

class Boat():
    WEATHER_HELM_FORCE = 0.02
    BOAT_HEEL_FORCE = 1
    RUDDER_SPEED = 1

    COLOR = 255, 255, 255
    RUDDER_COLOR = 200, 0, 0
    SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    RUDDER_ORIGIN = [50, 180]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    ORIGIN = [50, 150]
    MAX_RUDDER_ANGLE = 30

    # distance in meters from waypoint to skip to next waypoint
    DIST_NEXT_WAYPOINT = 30

    def __init__(self, env, random_color=False, upwind_twa=30, tack_angle=50, downwind_twa=170, gybe_angle=160, name='no-name'):
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

        # increase speed of the boat to speedup simulation
        self._speedup = 10

        self._upwind_twa = upwind_twa
        self._downwind_twa = downwind_twa
        self._tack_angle = tack_angle
        self._gybe_angle = gybe_angle

        self._name = name

        self._position = (52.3721693, 5.0750607)
        self._waypoint = None
        self._bearing = 0.
        self._distance = 0.
        self._marks_passed = 0

        # set a boat color
        if random_color:
            self._boat_color = randint(30, 255), randint(30, 255), randint(30, 255)
        else:
            self._boat_color = 255, 255, 255

        # frames per second, used to calibrate behaviour across (simulated) boats
        self._fps = 20

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
        target_angle = target_angle + 360 if target_angle<0 else target_angle
        target_angle = target_angle - 360 if target_angle>360 else target_angle
        self.target_angle = target_angle

    def calculate_speed(self):
        aoa = abs(self.get_angle_of_attack())
        speed = sin(radians(aoa / 1.2)) * self._env.wind_speed / 4

        # add bonus speed, don't want the boat to stop
        # todo: implement some momentum algorithm
        speed += 1
        return speed

    def move(self):
        """Simulates or fetches movement of boat"""

        # steering input (speed dependant)
        self.boat_angle -= self.rudder_angle / 10 * self.speed / 5

        # apply weather helm
        force = sin(radians(self.boat_angle - self._env.wind_direction + 180))
        self.boat_angle += force * self.WEATHER_HELM_FORCE * self._env.wind_speed

        # calculate boat heel
        self.boat_heel = abs(force) * self._env.wind_speed * self.BOAT_HEEL_FORCE

        # calculate speed
        self.speed = self.calculate_speed()

        # move rudder
        if abs(self.target_rudder_angle - self.rudder_angle) < self.RUDDER_SPEED:
            self.rudder_angle = self.target_rudder_angle
        else:
            if self.target_rudder_angle > self.rudder_angle:
                self.rudder_angle += self.RUDDER_SPEED
            else:
                self.rudder_angle -= self.RUDDER_SPEED

        # wrap boat angle
        self.boat_angle = self.boat_angle + 360 if self.boat_angle<0 else self.boat_angle
        self.boat_angle = self.boat_angle - 360 if self.boat_angle>360 else self.boat_angle

        # update position
        lat, lon = self._position
        lat += cos(radians(self.boat_angle)) * self.speed / self._fps / 3600 / 60 * self._speedup
        lon += sin(radians(self.boat_angle)) * self.speed / self._fps / 3600 / 60 * self._speedup
        self._position = (lat, lon)

    def update(self):

        # simulate or fetch boat movements
        self.move()

        # run navigation
        self.nav()

        # save history
        self.history = self.history.append([{
            'datetime': dt.now(),
            'boat_angle': self.boat_angle,
            'boat_heel': self.boat_heel,
            'boat_speed': self.speed,
            'target_angle': self.target_angle,
            'course_error': self.get_course_error(),
            'rudder_angle': self.rudder_angle,
            'wind_direction': self._env.wind_direction,
            'wind_speed': self._env.wind_speed,
            'angle_of_attack': self.get_angle_of_attack()
        }])

        # change target angle
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_1]:
            self.set_target_angle(self.target_angle - 3)
        if pressed[pygame.K_2]:
            self.set_target_angle(self.target_angle + 3)

    def nav(self):
        """ Update navigation variables and determine new course """

        if self._waypoint is None:
            return

        buoys = self._env.get_buoys()

        # get target position from waypoint
        target_pos = buoys[self._waypoint]

        # determine bearing to waypoint
        self._bearing = geo.bearing(self._position[0], self._position[1], target_pos[0], target_pos[1])

        # distance to waypoint
        self._distance = geo.haversine(self._position[0], self._position[1], target_pos[0], target_pos[1])

        # calculate new true wind angle to steer
        new_twa = calc_angle(self._env.wind_direction, self._bearing)

        # get angles for optimal vmg
        upwind_twa = self.get_upwind_twa()
        downwind_twa = self.get_downwind_twa()

        # do need to steer an upwind course?
        if abs(new_twa) < upwind_twa:
            self.set_twa(upwind_twa, tack=self.need_to_tack())

        # do need to steer an downwind course?
        elif abs(new_twa) > downwind_twa:
            self.set_twa(downwind_twa, tack=self.need_to_tack())

        # otherwise, steer directly to waypoint
        else:
            self.set_target_angle(self._bearing)

        # skip to next waypoint if we're there
        if self._distance < self.DIST_NEXT_WAYPOINT:
            self._marks_passed += 1
            self._waypoint = self._waypoint + 1 if self._waypoint < len(buoys)-1 else 0

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

    def draw(self, screen):
        # draw boat
        vectors = self.SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, self.boat_angle, self.ORIGIN)
            vectors[i] = [self.x + new_vector[0], self.y + new_vector[1]]

        pygame.draw.polygon(screen, self.get_boat_color(), vectors, 0)

        # draw rudder
        vectors = self.RUDDER_SHAPE.copy()
        for i, vector in enumerate(vectors):

            # rudder rotation
            vector = rotate_point(vector, self.rudder_angle, self.RUDDER_ORIGIN)
            vector = add_vector(vector, self.RUDDER_ORIGIN)

            # boat rotation
            vector = rotate_point(vector, self.boat_angle, self.ORIGIN)

            # boat position
            vectors[i] = [self.x + vector[0], self.y + vector[1]]

        pygame.draw.line(screen, self.RUDDER_COLOR, vectors[0], vectors[1], 4)

        # draw target direction
        vectors = [[250, 30], [250, 50]]
        vectors = rotate_vectors(vectors, self.target_angle, (250, 250), reverse=True)
        pygame.draw.line(screen, (0, 255, 0),  vectors[0], vectors[1], 10)

    def get_position(self):
        return self._position

    def set_waypoint(self, waypoint):
        self._waypoint = waypoint
        return self

    def get_boat_color(self):
        return self._boat_color

    def get_marks_passed(self):
        return self._marks_passed

    def get_distance_to_waypoint(self):
        return self._distance

    def get_name(self):
        return self._name

    def get_downwind_twa(self):
        return self._downwind_twa

    def get_upwind_twa(self):
        return self._upwind_twa

    def need_to_tack(self):
        diff = calc_angle(self.target_angle, self._bearing)
        return abs(diff) > self._tack_angle

    def need_to_gybe(self):
        diff = calc_angle(self.target_angle, self._bearing)
        return abs(diff) > self._gybe_angle


class SimBoat(Boat):

    # ratio of speed change per second
    SPEED_CHANGE_RATE = 0.5

    def __init__(self, env, polar, random_color=False, **kwargs):
        super().__init__(env, random_color=random_color, **kwargs)
        self._polar = polar
        self._speed = 5

    def calculate_speed(self):
        target_speed = self._polar.get_speed(twa=self.get_angle_of_attack(), tws=self._env.wind_speed)
        delta = target_speed - self._speed

        self._speed += delta * (self.SPEED_CHANGE_RATE / self._fps)

        return self._speed

#  todo remove!
rudder_center = 360
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
        print("raw rudder angle", data[8])

def set_rudder_angle(angle, pilot, rudder_center):
    translated_target_rudder_angle = int((-angle * rudder_multiply) + rudder_center)
    pilot.set_rudder_angle(translated_target_rudder_angle)
    return

class RealBoat(Boat):
    RUDDER_CENTER = 360

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