class Settings:
    """Global settings"""

    # Number of steering frames per second
    UPDATE_FPS = 5

    # number of graphical frames per second
    DRAW_FPS = 20

    # scale the race area
    BUOY_SCALE = 0.05

    # definition of buoy positions
    BUOYS = [
        (52.3721693, 5.0750607),
        (52.3721693 + 0.01 * BUOY_SCALE, 5.0750607),
        (52.3721693 + 0.008 * BUOY_SCALE, 5.0750607 + 0.005 * BUOY_SCALE),
        (52.3721693 + 0.002 * BUOY_SCALE, 5.0750607 + 0.005 * BUOY_SCALE),
    ]

