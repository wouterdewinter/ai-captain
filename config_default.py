from boats import default, my_boat


def get_strategies(env, polar):
    """ setup steering strategies """
    return [
        my_boat.get_strategy(env, polar),
        default.get_strategy(env, polar)
    ]
