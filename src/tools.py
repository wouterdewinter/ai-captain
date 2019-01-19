from math import sin, cos, radians


def rotate_point(point, angle, center_point=(0, 0), reverse=False):
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
    if reverse:
        new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point


def rotate_vectors(vectors, angle, center_point=(0, 0), reverse=False):
    for i, vector in enumerate(vectors):
        vectors[i] = rotate_point(vector, angle, center_point, reverse=reverse)
    return vectors


def add_vector(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def calc_angle(a1, a2):
    """ Calculate shortest angle between two angles """
    value = a1 - a2
    value = (value + 180) % 360 - 180
    return value
