import pygame
from math import sin, cos, radians

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
    COLOR = 255, 255, 255
    RUDDER_COLOR = 200, 0, 0
    SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    RUDDER_ORIGIN = [50, 180]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    ORIGIN = [50, 150]

    def __init__(self):
        self.rudder_angle = 0.
        self.boat_angle = 0.
        self.target_angle = 0.
        self.speed = 3.
        self.x = 150.
        self.y = 100.

    def update(self):
        self.boat_angle -= self.rudder_angle / 10

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
    def __init__(self):
        self.wind_speed = 15
        self.wind_direction = 90
        self.boat_angle = 0
