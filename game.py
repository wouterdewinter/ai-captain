import sys, pygame, objects

pygame.init()

size = width, height = 800, 600
speed = [2, 2]
blue = 0, 0, 255
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")
ballrect = ball.get_rect()

boat = objects.Boat()

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
    boat.boat_angle += 1

    boat.draw(screen)
    #pygame.draw.polygon(screen, black, [[50, 0], [100, 150], [75, 200], [25, 200], [0, 150]], 5)

    pygame.display.flip()