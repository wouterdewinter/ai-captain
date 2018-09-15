import sys, pygame, objects, random, math

pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Arial', 30)


size = width, height = 800, 600
speed = [2, 2]
blue = 0, 0, 255
black = 0, 0, 0
text_color = 255, 255, 255

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

boat = objects.Boat()
env = objects.Environment()

def write_text(screen, text, row):
    pos = 500, 30 + (row * 30)
    textsurface = myfont.render(text, False, text_color)
    screen.blit(textsurface, pos)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(blue)
    #screen.blit(ball, ballrect)
    #boat.boat_angle += 1

    env.update()
    boat.update(env)

    #boat.rudder_angle += (random.random() - 0.5) * 5

    boat.draw(screen)
    env.draw(screen)

    write_text(screen, "Boat angle: %.2f" % boat.boat_angle, 0)
    write_text(screen, "Target angle: %.2f" % boat.target_angle, 1)
    write_text(screen, "Current deviation: %.2f" % abs(boat.boat_angle - boat.target_angle), 2)
    write_text(screen, "Boat heel: %.2f" % boat.boat_heel, 3)
    write_text(screen, "Boat speed: %.2f" % boat.speed, 4)
    write_text(screen, "Rudder angle: %.2f" % boat.rudder_angle, 5)

    write_text(screen, "Wind speed: %.2f" % env.wind_speed, 6)
    write_text(screen, "Wind direction: %.2f" % env.wind_direction, 7)

    #pygame.draw.polygon(screen, black, [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]], 5)

    pygame.display.flip()
