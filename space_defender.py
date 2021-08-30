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
PINK = (204, 102, 255)

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
        window.blit(self.ship_img, (self.x, self.y))  # 8draw on window, pos of the rect(pos of ship)

    def get_width(self):  # 14 getting accurate dimensions of ship for pixel perfect collisions
        return self.ship_img.get_width()  # 14 will return width

    def get_height(self):  # 14c getting accurate height
        return self.ship_img.get_height()  # 14 will be defined here, for use on enemy ship also, and inheriting players


class Player(Ship):  # 12 new class, inherits from "Ship", and takes Ships draw function as well
    def __init__(self, x, y, health=100):  # 12c we define our own initialization method
        super().__init__(x, y, health)  # 12cc we use super method from Ship class to inherit all methods we'll reuse
        self.ship_img = YELLOW_SPACE_SHIP  # 12ccc we create an extension
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(
            self.ship_img)  # 13 we define "mask" which will allow pixel-perfect collisions, rather than hit-box cols.
        self.max_health = health  # 13


class Enemy(Ship):  # 15 inherit from parent class: Ship
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),  # if we hit "red", it'll access whatever we've linked/mapped to "red"
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }  # 16 we map our images to keywords, thus gaining access to them, when we call on them

    def __init__(self, x, y, color, health=100):  # 15c new initialization, we have added color since it's new
        super().__init__(  # 15cc calling super constructor, already defined under "Ship" class, meaning we reuse what
            x, y, health)  # we already have set and defined earlier
        self.ship_img, self.laser_img = self.COLOR_MAP[color]  # 16 ship/laser img is linked to our dictionary, and we
        # pass in the "color" argument, that we've created in our function
        self.mask = pygame.mask.from_surface(self.ship_img)  # 16c we create mask, and pass in ship img

    def move(self, vel):  # 17 making enemy ships move
        self.y += vel  # 17 since they will only move from top to bottom, we only need y pos, and += velocity


def main():  # 3
    run = True  # 3
    FPS = 60  # 4
    level = 0
    lives = 6
    main_font = pygame.font.SysFont('linuxlibertinegsemibold', 50)  # 6 pass in name and size of our desired font
    lost_font = pygame.font.SysFont('linuxlibertinegsemibold', 90)  # 22cc we create a "lost" font to display when loss

    enemies = []  # 18 will store all of our enemies
    wave_length = 5  # 18c every lvl we complete, we generate a new wave, and new waves of enemies
    enemy_vel = 1  # 18

    player = Player(200, 900)  # 9 call in player from class Ship, at position - must then be drawn inside redraw func

    clock = pygame.time.Clock()  # 4 sets up the FPS, and checks for collisions, movement, shooting etc

    lost = False  # 22cc
    lost_count = 0  # 22ccc c

    def redraw_window():  # 5 new function inside main func, to draw on screen and etc
        WIN.blit(BACKGROUND, (0, 0))  # 5 WIN.blit = draw a surface of "BACKGROUND", at pos x=0 and y=0
        lives_label = main_font.render(f'Lives: {lives}', 1, WHITE)  # 6 1=antialiasing, is always 1
        level_label = main_font.render(f'Level: {level}', 1, WHITE)

        WIN.blit(lives_label, (10, 10))  # 6 we blit(draw) lives on screen, at the pos of x=10 and y=10
        WIN.blit(level_label, (WIDTH - level_label.get_width(), 10))  # 6 use .get_width to get the width of level text

        for enemy in enemies:  # 19 we've already drawn ships and lasers in Ship class and Enemy class, so we can just
            enemy.draw(WIN)  # use draw method and draw them on the WINdow here

        player.draw(WIN)  # 9 call player, draw it, on the window (WIN)
        if lost:  # 22cc if "lost" turns True, we access this line
            lost_label = lost_font.render('You lost, kyni!', 1, PINK)
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 650))  # center of screen will be width/2 minus
            # the width of the label which is also divided by 2, and 2nd argument is y pos

        pygame.display.update()  # 5

    while run:  # 3
        clock.tick(FPS)  # 4 we call the "clock" object here, and pass in how often to check it: which is FPS

        redraw_window()  # 5 call it here

        if lives <= 0 or player.health <= 0:  # 22
            lost = True  # 22c
            lost_count += 1  # 22ccc cc

        if lost:  # 22ccc cc
            if lost_count > FPS * 5:  # this is how many seconds we want to display our lost screen, before breaking
                run = False  # this will quit the game, after we've lost
            else:
                continue  # this will allow the screen to run, until we've quit the game, but won't allow movements

        if len(enemies) == 0:  # 20 when no more enemies are on screen, increment lvl by 1
            level += 1
            wave_length += 5  # 20  # we add this many more enemies with every wave
            for i in range(wave_length):  # 20c we're using random.randrange to make enemies spawn at random locations
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(  # from off the screen from above
                    -500, -100), random.choice(  # we pass in x pos, y pos, and let it choose from a random color
                    ["red", "green", "blue"]))  # we can change the positions of ships to spawn dynamically as we reach
                # higher levels if we want to, i.e. "-1500*level*2" or whatever we may find balanced
                enemies.append(enemy)  # 20cc we add enemies to the enemy list, using append

        for event in pygame.event.get():  # 5 allows us to quit the game, when X button is pressed
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()  # 10 allows several keys to be pressed at same time
        if keys[pygame.K_a] and player.x - VEL + 20 > 0:
            player.x -= VEL  # -= on x axis, since it's left movement
        if keys[pygame.K_d] and player.x + VEL + player.get_width() < WIDTH:  # 14c get_width and height from class
            player.x += VEL  # += also on x axis, since we're moving right
        if keys[pygame.K_w] and player.y - VEL + 20 > 0:  # if we are greater than 0, we can move, so until edge of
            player.y -= VEL  # -= HEIGHT on y axis, since we're moving up
        if keys[pygame.K_s] and player.y + VEL + player.get_height()< HEIGHT:  # move, if player.y position is less
            player.y += VEL  # than height, if VEL += is added on y axis, and need to + the velocity

        for enemy in enemies[:]:  # 21 our enemies move down now by calling them here - we make a copy of list with [:]
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:  # 21c we check the enemies height pos, to remove them from our
                lives -= 1  # list, and remove 1 hp from our lives, in order to be able to spawn new enemies
                enemies.remove(enemy)  # removes object "enemy" from the "enemies" list




main()
