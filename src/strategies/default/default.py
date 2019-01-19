from strategies.base import Base
import logging


class Default(Base):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_course_error = None

    def update(self):
        course_error = self._boat.get_course_error()

        # we need a last course error to determine an initial turning rate
        if self._last_course_error is not None:
            # calculate turning rate in degrees per second
            delta = (self._last_course_error - course_error) * self._update_fps

            # calculate target turning speed based on course difference
            target_delta = course_error / 2

            # maximize turn speed
            max_target_delta = 30
            target_delta = min(target_delta, max_target_delta)
            target_delta = max(target_delta, -max_target_delta)

            # steer towards target turning speed
            steer = (target_delta - delta) / self._update_fps

            # maximize steering input
            max_steer = 20 / self._update_fps
            steer = min(steer, max_steer)
            steer = max(steer, -max_steer)

            # steer the boat
            self._boat.steer(steer)

            # print debugging info
            logging.debug('delta: %.2f, target delta: %.2f, steer: %.2f, max_steer:  %.2f' % (
                delta, target_delta, steer, max_steer))

        # save last course error
        self._last_course_error = course_error
