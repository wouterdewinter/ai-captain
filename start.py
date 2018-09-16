import os, sys, pygame, random, math

# update import path
sys.path.insert(1, os.path.join(sys.path[0], 'src'))

# import project code
from boat import Boat
from environment import Environment
from strategies import *

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Arial', 30)
smallfont = pygame.font.SysFont('Arial', 25)

size = width, height = 800, 600
speed = [2, 2]
blue = 0, 0, 255
black = 0, 0, 0
text_color = 255, 255, 255

screen = pygame.display.set_mode(size)

env = Environment()
boat = Boat(env)
strategy = Proportional(boat, env)

def write_text(screen, text, row):
    pos = 500, 30 + (row * 30)
    textsurface = myfont.render(text, True, text_color)
    screen.blit(textsurface, pos)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(blue)

    env.update()
    boat.update()
    strategy.update()

    boat.draw(screen)
    env.draw(screen)

    write_text(screen, "Boat angle: %.1f°" % boat.boat_angle, 0)
    write_text(screen, "Target angle: %.1f°" % boat.target_angle, 1)
    write_text(screen, "Current deviation: %.1f°" % boat.get_course_error(), 2)
    write_text(screen, "Boat heel: %.1f°" % boat.boat_heel, 3)
    write_text(screen, "Rudder angle: %.1f°" % boat.rudder_angle, 4)
    write_text(screen, "Boat speed: %.1f knots" % boat.speed, 5)

    write_text(screen, "Wind direction: %.1f°" % env.wind_direction, 7)
    write_text(screen, "Wind speed: %.1f knots" % env.wind_speed, 8)

    textsurface = smallfont.render("Press keys to change: 1/2 for target angle, 3/4 for wind direction, 5/6 for wind speed", True, text_color)
    screen.blit(textsurface, (20, 550))

    pygame.display.flip()
