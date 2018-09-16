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
            self._boat.steer(+self.STEERING_FORCE)
        if pressed[pygame.K_RIGHT]:
            self._boat.steer(-self.STEERING_FORCE)

class DoNothing(Base):
    def update(self):
        return

class Binary(Base):
    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.rudder_angle = +10
        else:
            self._boat.rudder_angle = -10

class Smoother(Base):
    STEERING_FORCE = .3

    def update(self):
        if self._boat.get_course_error() > 0:
            self._boat.steer(self.STEERING_FORCE)
        else:
            self._boat.steer(-self.STEERING_FORCE)
