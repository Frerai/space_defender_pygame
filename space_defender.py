import pygame
import os
import time
import random
pygame.font.init()  # 6 allows us to access fonts, and start writing on the screen

WIDTH, HEIGHT = 1600, 1300  # 1
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # 1
pygame.display.set_caption("Invasion of Kynis!")  # 1c

VEL = 25

RED_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_red_small.png'))  # 2
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_blue_small.png'))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_yellow.png'))

RED_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_green.png'))
YELLOW_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_yellow.png'))

WHITE = (255, 255, 255)
RED = (255, 0, 0)

BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join(
        'material', 'background-black.png')), (
        WIDTH, HEIGHT))  # 2 rescale first argument, second argument are dimensions of our rescaling = width, height


class Ship:  # 7 we create ship class, to inherit from later
    def __init__(self, x, y, health=100):  # we need x pos, y pos, health for default value
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None  # this allows us to draw the ship and lasers
        self.laser_img = None  #
        self.lasers = []  #
        self.cool_down_counter = 0  #

    def draw(self, window):  # 8
        pygame.draw.rect(window, RED, (
            self.x, self.y, 50, 50))  # 8draw on window, color, pos of the rect(pos of ship), size of rect


def main():  # 3
    run = True  # 3
    FPS = 60  # 4
    level = 1
    lives = 6
    main_font = pygame.font.SysFont('linuxlibertinegsemibold', 50)  # 6 pass in name and size of our desired font

    ship = Ship(200, 900)  # 9 call in ship from class of Ship, at position - must then be drawn inside redraw func

    clock = pygame.time.Clock()  # 4 sets up the FPS, and checks for collisions, movement, shooting etc

    def redraw_window():  # 5 new function inside main func, to draw on screen and etc
        WIN.blit(BACKGROUND, (0, 0))  # 5 WIN.blit = draw a surface of "BACKGROUND", at pos x=0 and y=0
        lives_label = main_font.render(f'Lives: {lives}', 1, WHITE)  # 6 1=antialiasing, is always 1
        level_label = main_font.render(f'Level: {level}', 1, WHITE)

        WIN.blit(lives_label, (10, 10))  # 6 we blit(draw) lives on screen, at the pos of x=10 and y=10
        WIN.blit(level_label, (WIDTH - level_label.get_width(), 10))  # 6 use .get_width to get the width of level text

        ship.draw(WIN)  # 9 call ship, draw it, on the window (WIN)

        pygame.display.update()  # 5

    while run:  # 3
        clock.tick(FPS)  # 4 we call the "clock" object here, and pass in how often to check it: which is FPS
        redraw_window()  # 5 call it here
        for event in pygame.event.get():  # 5 allows us to quit the game, when X button is pressed
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()  # 10 allows several keys to be pressed at same time
        if keys[pygame.K_a] and ship.x - VEL > 0:
            ship.x -= VEL  # -= on x axis, since it's left movement
        if keys[pygame.K_d] and ship.x + VEL < WIDTH:
            ship.x += VEL  # += also on x axis, since we're moving right
        if keys[pygame.K_w] and ship.y - VEL > 0:  # if we are greater than 0, we can move, so until edge of HEIGHT
            ship.y -= VEL  # -= on y axis, since we're moving up
        if keys[pygame.K_s] and ship.y + VEL < HEIGHT:  # move, if ship.y position is less than height, if VEL is added
            ship.y += VEL  # += on y axis, since we're moving down, and need to + the velocity


main()
