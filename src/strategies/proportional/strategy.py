from strategies.base import Base


class Proportional(Base):

    def update(self):
        target = self._boat.get_course_error() / 2
        self._boat.set_target_rudder_angle(target)
