import pygame
from math import sin, cos, radians
from random import randint, random, uniform

#water
#barricade
#sail

def rotate_point(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

class Boat():
    WEATHER_HELM_FORCE = 0.02
    BOAT_HEEL_FORCE = 2

    COLOR = 255, 255, 255
    RUDDER_COLOR = 200, 0, 0
    SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    RUDDER_ORIGIN = [50, 180]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    ORIGIN = [50, 150]

    def __init__(self):
        self.rudder_angle = 0.
        self.boat_angle = 0.
        self.boat_heel = 0.
        self.target_angle = 0.
        self.speed = 3.
        self.x = 150.
        self.y = 100.

    def update(self, env):
        # steering input
        self.boat_angle -= self.rudder_angle / 10

        # weather helm
        force = sin(radians(self.boat_angle - env.wind_direction + 180))
        self.boat_angle += force * self.WEATHER_HELM_FORCE * env.wind_speed

        # calculate boat heel
        self.boat_heel = abs(force) * env.wind_speed * self.BOAT_HEEL_FORCE

        # maximize rudder angle
        self.rudder_angle = 50 if self.rudder_angle > 50 else self.rudder_angle
        self.rudder_angle = -50 if self.rudder_angle < -50 else self.rudder_angle

        # wrap boat angle
        self.boat_angle =  self.boat_angle + 360 if self.boat_angle<0 else self.boat_angle
        self.boat_angle =  self.boat_angle - 360 if self.boat_angle>360 else self.boat_angle

    def draw(self, screen):
        # draw boat
        vectors = self.SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, self.boat_angle, self.ORIGIN)
            vectors[i] = [self.x + new_vector[0], self.y + new_vector[1]]

        pygame.draw.polygon(screen, self.COLOR, vectors, 0)

        # draw rudder
        vectors = self.RUDDER_SHAPE.copy()
        for i, vector in enumerate(vectors):

            # rudder rotation
            vector = rotate_point(vector, self.rudder_angle, self.RUDDER_ORIGIN)

            # boat rotation
            vector = rotate_point(vector, self.boat_angle, self.ORIGIN)

            # boat position
            vectors[i] = [self.x + vector[0], self.y + vector[1]]

        pygame.draw.line(screen, self.RUDDER_COLOR, vectors[0], vectors[1], 4)


class Environment():
    
    WIND_SPEED_VAR = 1.2
    WIND_DIRECTION_VAR = 1.2

    ARROW_SHAPE = [(0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)]
    ARROW_COLOR = (0, 255, 0)
    ARROW_POS = [350, 250]
    ARROW_ORIGIN = [0, 100]
    ARROW_SCALE = 0.2

    def __init__(self):
        self.main_wind_speed = uniform(5, 25)
        self.main_wind_direction = uniform(0, 360)
        self.wind_speed = self.main_wind_speed
        self.wind_direction = self.main_wind_direction

    def update(self):
        
        self.wind_speed += (random() - 0.5) * 2
        max_wind_speed = self.main_wind_speed * self.WIND_SPEED_VAR
        min_wind_speed = self.main_wind_speed / self.WIND_SPEED_VAR
        self.wind_speed = self.wind_speed if self.wind_speed < max_wind_speed else max_wind_speed
        self.wind_speed = self.wind_speed if self.wind_speed > min_wind_speed else min_wind_speed
        
        self.wind_direction += (random() - 0.5) * 2
        max_wind_dir = self.main_wind_direction * self.WIND_SPEED_VAR
        min_wind_dir = self.main_wind_direction / self.WIND_SPEED_VAR
        self.wind_direction = self.wind_direction if self.wind_direction < max_wind_dir else max_wind_dir
        self.wind_direction = self.wind_direction if self.wind_direction > min_wind_dir else min_wind_dir
        
        # wrap wind dir
        self.wind_direction =  self.wind_direction + 360 if self.wind_direction<0 else self.wind_direction
        self.wind_direction =  self.wind_direction - 360 if self.wind_direction>360 else self.wind_direction

    def draw(self, screen):
        vectors = self.ARROW_SHAPE.copy()
        for i, vector in enumerate(vectors):
            vector = rotate_point(vector, self.wind_direction + 90, self.ARROW_ORIGIN)
            vector = [self.ARROW_POS[0] + vector[0], self.ARROW_POS[1] + vector[1]]
            vector = [vector[0] * self.ARROW_SCALE, vector[1] * self.ARROW_SCALE]
            vectors[i] = vector

        #surface = pygame.transform.rotate(screen, self.wind_direction)
        pygame.draw.polygon(screen, self.ARROW_COLOR, vectors)
