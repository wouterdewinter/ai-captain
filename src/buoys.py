import random


def trapezoidal(height=0.05, width=0.05):
    """generate a trapezoidal race course"""
    return [
        (0, 0),
        (0.01 * height, 0),
        (0.008 * height, 0.005 * width),
        (0.002 * height, 0.005 * width),
    ]


def random_course(height=0.0005, width=0.0005, min_buoys=2, max_buoys=6):
    """generate a random race course"""
    num_buoys = random.randint(min_buoys, max_buoys)
    buoys = [[0, 0]]
    for i in range(num_buoys):
        buoys.append([random.uniform(0, height), random.uniform(0, width)])
    return buoys


def buoys_translate(buoys, lat=52.3721693, lon=5.0750607):
    """add a latitude/longitude to the buoy positions"""
    return list(map(lambda buoy: [buoy[0] + lat, buoy[1] + lon], buoys))


def buoys_noise(buoys, amount=0.00003):
    """add random noise the buoy positions"""
    return list(map(lambda buoy: [
        buoy[0] + random.uniform(-1, 1) * amount,
        buoy[1] + random.uniform(-1, 1) * amount
    ], buoys))
