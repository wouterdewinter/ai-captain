from strategies.base import Base


class Binary(Base):

    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.set_target_rudder_angle(10)
        else:
            self._boat.set_target_rudder_angle(-10)
