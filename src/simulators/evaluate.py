import pygame
import numpy as np

from boat import Boat
from environment import Environment
from strategies.base import Base


class Evaluate:
    def __init__(self, boat: Boat, env: Environment, stragegy: Base):
        self._boat = boat
        self._env = env
        self._strategy = stragegy
        self._clock = pygame.time.Clock()

    def run(self):

        # initial shuffle
        self._env.shuffle()
        self._boat.shuffle()

        # set to same framerate as they are called in the same thread
        self._boat.set_draw_fps(5)
        self._strategy.set_update_fps(5)

        i = 0
        course_errors = np.array([])

        while True:
            # update boat and environment
            self._env.update()
            self._boat.update()
            self._strategy.update()

            # log course error
            err = abs(self._boat.get_course_error())
            course_errors = np.append(course_errors, err)

            # measure fps
            self._clock.tick()

            i += 1
            if i % 100 == 0:
                print('running at %f fps' % self._clock.get_fps())
                print(course_errors.mean(), self._boat.get_course_error())

