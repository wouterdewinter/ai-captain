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
    COLOR = 0, 0, 0
    RUDDER_COLOR = 200, 0, 0
    SHAPE = [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]]
    RUDDER_SHAPE = [[50, 180], [50, 240]]
    ORIGIN = [50, 150]

    def __init__(self):
        self.rudder_angle = 10
        self.boat_angle = 0
        self.target_angle = 0
        self.speed = 3
        self.x = 200
        self.y = 100

    def draw(self, screen):
        # draw boat
        vectors = self.SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, self.boat_angle, self.ORIGIN)
            vectors[i] = [self.x + new_vector[0], self.y + new_vector[1]]

        pygame.draw.polygon(screen, self.COLOR, vectors, 2)

        # draw rudder
        vectors = self.RUDDER_SHAPE.copy()
        for i, vector in enumerate(vectors):
            new_vector = rotate_point(vector, self.boat_angle, self.ORIGIN)
            vectors[i] = [self.x + new_vector[0], self.y + new_vector[1]]

        pygame.draw.line(screen, self.RUDDER_COLOR, vectors[0], vectors[1], 4)


class Environment():
    def __init__(self):
        self.wind_speed = 15
        self.wind_direction = 90
        self.boat_angle = 0
