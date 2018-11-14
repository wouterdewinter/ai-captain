from strategies.base import Base

class TurnSpeed(Base):
    def update(self):
        if self._boat.history.shape[0] < 3:
            return

        last = float(self._boat.history.iloc[-3:-2]['course_error'])

        # calculate turning speed
        current = self._boat.get_course_error()
        delta = last-current

        # calculate target turning speed based on course difference
        target_delta = self._boat.get_course_error() / 10
        target_delta = min(target_delta, 2)
        target_delta = max(target_delta, -2)

        # steer towards target turning speed
        steer = (target_delta - delta) / 2
        steer = min(steer, 0.5)
        steer = max(steer, -0.5)

        # steer the boat
        self._boat.steer(steer)
