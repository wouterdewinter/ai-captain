import pygame
import numpy as np
import logging

from boat import Boat
from environment import Environment
from strategies.base import Base
from settings import Settings


class Evaluate:
    # number of frames used to determine if the course is stable
    STABLE_EVALUATION_WINDOW = 10

    # maximum error after which the course is considered stable
    STABLE_MAX_ERROR = 5

    # evaluate a stable course for n frames
    STABLE_FRAMES = 100

    # number of frames after we give up on achieving a stable course
    MAX_UNSTABLE_FRAMES = 500

    def __init__(self, boat: Boat, env: Environment, stragegy: Base):
        self._boat = boat
        self._env = env
        self._strategy = stragegy
        self._clock = pygame.time.Clock()

    def run(self):

        # initial shuffle
        self._env.shuffle()
        self._boat.shuffle()

        # set both to the update fps as both get called at the same rate
        self._boat.set_draw_fps(Settings.UPDATE_FPS)
        self._strategy.set_update_fps(Settings.UPDATE_FPS)

        frame = 0
        course_errors = []
        stable = False
        stable_frame = 0
        unstable_frame = 0
        frames_to_stabilize = []
        stable_course_error = []

        while True:
            # update boat and environment
            self._env.update()
            self._boat.update()
            self._strategy.update()

            # log course error
            err = abs(self._boat.get_course_error())
            course_errors.append(err)
            if len(course_errors) > self.STABLE_EVALUATION_WINDOW:
                # pop first item of the list off
                course_errors.pop(0)

            # has course stabilized?
            max_err = max(course_errors)
            if not stable and max_err < self.STABLE_MAX_ERROR:
                stable = True
                stable_frame = frame
                frames_to_stabilize.append(frame - unstable_frame)
                logging.info("course stabilized after %d frames" % (frame - unstable_frame))

            # did stabilizing take too long?
            if not stable and frame-unstable_frame > self.MAX_UNSTABLE_FRAMES:
                logging.warning("max unstable frames reached, shuffling")
                self._env.shuffle()
                self._boat.shuffle()
                stable = False
                unstable_frame = frame

            # enough frames spent on a stable course? shuffle and get a new course
            if stable and frame - stable_frame > self.STABLE_FRAMES:
                logging.info("shuffling")
                self._env.shuffle()
                self._boat.shuffle()
                stable = False
                unstable_frame = frame

            # log course errors on stable courses
            if stable:
                stable_course_error.append(err)

            # measure fps
            self._clock.tick()

            # report stats
            frame += 1
            if frame % 100 == 0:
                fps = self._clock.get_fps()
                print('fps: %.2f, average frames needed to stabilize: %.2f, average stable course error: %.2f' % (
                    fps, np.mean(frames_to_stabilize), np.mean(stable_course_error)))
