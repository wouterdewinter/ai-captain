import pygame
from strategies.base import Base

class Manual(Base):
    STEERING_FORCE = 1

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self._boat.steer(self.STEERING_FORCE)
        if pressed[pygame.K_RIGHT]:
            self._boat.steer(-self.STEERING_FORCE)
