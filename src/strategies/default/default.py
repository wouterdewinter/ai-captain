from strategies.base import Base

class Default(Base):
    def update(self):
        if self._boat.history.shape[0] < 3:
            return

        last = float(self._boat.history.iloc[-3:-2]['course_error'])

        # calculate turning speed
        current = self._boat.get_course_error()
        delta = last-current

        # calculate target turning speed based on course difference
        target_delta = self._boat.get_course_error() / 10

        # maximize turn speed
        max_turn_speed = 3
        target_delta = min(target_delta, max_turn_speed)
        target_delta = max(target_delta, -max_turn_speed)

        # steer towards target turning speed
        steer = (target_delta - delta) / 2

        # maximize steering input
        max_steer = 1
        steer = min(steer, max_steer)
        steer = max(steer, -max_steer)

        # steer the boat
        self._boat.steer(steer)
