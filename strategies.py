import pygame

class Base():
    def __init__(self, boat, env):
        self._boat = boat
        self._env = env

    def update(self):
        raise NotImplementedError()

class Manual(Base):
    STEERING_FORCE = .3

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self._boat.steer(self.STEERING_FORCE)
        if pressed[pygame.K_RIGHT]:
            self._boat.steer(-self.STEERING_FORCE)

class DoNothing(Base):
    def update(self):
        return

class Binary(Base):
    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.set_target_rudder_angle(10)
        else:
            self._boat.set_target_rudder_angle(-10)

class Smoother(Base):
    STEERING_FORCE = .3

    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.steer(self.STEERING_FORCE)
        else:
            self._boat.steer(-self.STEERING_FORCE)

class Proportional(Base):
    MAX_RUDDER = 20

    def update(self):
        err = self._boat.get_course_error()
        err = max(min(err, self.MAX_RUDDER), -self.MAX_RUDDER)
        self._boat.set_target_rudder_angle(err)