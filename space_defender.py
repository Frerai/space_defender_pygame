import pygame
import os
import time
import random

pygame.mixer.init()  # 36 sound library
pygame.font.init()  # 6 allows us to access fonts, and start writing on the screen

WIDTH, HEIGHT = 1600, 1300  # 1
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # 1
pygame.display.set_caption("Invasion of Kynis!")  # 1c

VEL = 25

RED_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_red_small.png'))  # 2
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_blue_small.png'))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('material', 'pixel_ship_yellow.png'))

pygame.mixer.music.load(os.path.join('material', 'music.mp3'))  # 36ccc c background music
pygame.mixer.music.play(-1, 0.0)  # -1 is parameter for forever loop, 0.0 is what second you want the music to play from
ENEMY_LASER_SOUND = pygame.mixer.Sound(os.path.join('material', 'enemy_laser.wav'))  # 36cc loading sounds
PLAYER_LASER_SOUND = pygame.mixer.Sound(os.path.join('material', 'player_laser.wav'))
SHIP_COLLISION_SOUND = pygame.mixer.Sound(os.path.join('material', 'collision_ships.wav'))  # collision with ships
NEXT_LEVEL = pygame.mixer.Sound(os.path.join('material', 'next_level.wav'))
pygame.mixer.Sound.set_volume(PLAYER_LASER_SOUND, 0.5)  # 36ccc adjusting volume
pygame.mixer.Sound.set_volume(ENEMY_LASER_SOUND, 0.3)
pygame.mixer.Sound.set_volume(NEXT_LEVEL, 1)


RED_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_green.png'))
YELLOW_LASER = pygame.image.load(os.path.join('material', 'pixel_laser_yellow.png'))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (204, 102, 255)
LEMON = (255, 250, 205)

BACKGROUND = pygame.transform.scale(
    pygame.image.load(os.path.join(
        'material', 'background-black.png')), (
        WIDTH, HEIGHT))  # 2 rescale first argument, second argument are dimensions of our rescaling = width, height


class Laser:  # 23
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)  # this will be colliding with different things, so we need mask

    def draw(self, window):  # 23c draws on window, takes img, x pos and y pos
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):  # 23cc movement of the lasers, takes velocity from down to up, and up to down
        self.y += vel  # if we want to go down, we pass in a positive vel, if the lasers goes up we pass in negative vel

    def off_screen(self, height):  # 23ccc whenever lasers are off screen, based of the height of the screen
        return not (
                self.y <= height and self.y >= 0)  # if it's off the screen, then True, if not off screen, then False

    def collision(self, obj):  # 23ccc returns whether we've collided with anything or not
        return collide(obj, self)  # must create function for "collide"


class Ship:  # 7 we create ship class, to inherit from later
    COOLDOWN = 30  # 25c relative to FPS - i.e since 60 frames per second, cooldown of 30 would be 2 shots per second

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
        for laser in self.lasers:  # 27c drawing the lasers here
            laser.draw(window)

    def move_lasers(self, vel, obj):  # 28 self, velocity and objects - we want to check for collision with all objects
        self.cooldown()  # incrementing cooldown counter by calling cooldown
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):  # if the laser is off screen, we can delete the laser from the list
                self.lasers.remove(laser)  # remove laser from list, so we can use laser again
            elif laser.collision(obj):  # obj is player, that we've have passed in
                obj.health -= 10  # if we collide with an object, subtract health from the player
                self.lasers.remove(laser)

    def cooldown(self):  # 26
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):  # 25
        if self.cool_down_counter == 0:  # when laser is at 0 cd we'll create a new laser
            laser = Laser(self.x, self.y, self.laser_img)  # new laser created
            self.lasers.append(laser)  # laser added to "lasers" list
            self.cool_down_counter = 1

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

    def move_lasers(self, vel, objs):  # 29 self, velocity and objects
        self.cooldown()
        for laser in self.lasers:  # for each laser, move the laser with a given velocity
            laser.move(vel)
            if laser.off_screen(HEIGHT):  # if the laser is off screen, we can delete the laser from the list
                self.lasers.remove(laser)  # remove laser from list, so we can use laser again
            else:  # if laser is not off the screen
                for obj in objs:  # for each object in the object list
                    if laser.collision(obj):  # if laser has collided with object remove it
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):  # 34 drawing health bars here
        super().draw(window)  # we call the super of draw method from the parent class Ship
        self.health_bar(window)

    def health_bar(self, window):  # 33 drawing rectangles, red and green will be overlapping
        pygame.draw.rect(window, RED, (self.x, self.y + self.ship_img.get_height() + 10,
                                       self.ship_img.get_width(), 10))  # adding 10 pixels to the pos, to make the bar
        # appear a bit below the spaceship, rather than right on it
        pygame.draw.rect(window, GREEN, (self.x, self.y + self.ship_img.get_height() + 10,
                                         self.ship_img.get_width() * (self.health / self.max_health), 10))  # making
        # green bar on top of red bar, subtracting by percentage of health divided by max health


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

    def shoot(self):  # 30 overriding shoot method here, since we want to adjust lasers on the enemy
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img)  # subtract any desired pixels, to center the lasers
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):  # 24 function for when two masks have pixels overlapping another, meaning they've collided
    offset_x = obj2.x - obj1.x  # will tell us the distance from object 2 to 1, and let us know whether we've collided
    offset_y = obj2.y - obj1.y  # this offset allows us to count whether we have overlapping pixels or not, meaning
    # there is a collision, and not just depending on hitbox
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None  # does not equal None, if objects are not over-
# lapping, then the entire phrase will return False/None, and if they are overlapping it will return a tuple with coords
# is object 1 overlapping object 2, with the offset of offset_x and offset_y - both objects needs to have mask


def main():  # 3
    run = True  # 3
    FPS = 60  # 4
    level = 0
    lives = 10
    main_font = pygame.font.SysFont('linuxlibertinegsemibold', 50)  # 6 pass in name and size of our desired font
    lost_font = pygame.font.SysFont('linuxlibertinegsemibold', 90)  # 22cc we create a "lost" font to display when loss

    enemies = []  # 18 will store all of our enemies
    wave_length = 3  # 18c every lvl we complete, we generate a new wave, and new waves of enemies
    enemy_vel = 1  # 18
    laser_vel = 10

    player = Player(750, 900)  # 9 call in player from class Ship, at position - must then be drawn inside redraw func

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
            WIN.blit(lost_label,
                     (WIDTH / 2 - lost_label.get_width() / 2, 650))  # center of screen will be width/2 minus
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
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(  # from off the screen from above
                    -500, -100), random.choice(  # we pass in x pos, y pos, and let it choose from a random color
                    ["red", "green", "blue"]))  # we can change the positions of ships to spawn dynamically as we reach
                # higher levels if we want to, i.e. "-1500*level*2" or whatever we may find balanced
                enemies.append(enemy)  # 20cc we add enemies to the enemy list, using append
                NEXT_LEVEL.play()

        for event in pygame.event.get():  # 5 allows us to quit the game, when X button is pressed
            if event.type == pygame.QUIT:
                quit()  # may be replaced by "run = False" if double x click is desired before quitting game

        keys = pygame.key.get_pressed()  # 10 allows several keys to be pressed at same time
        if keys[pygame.K_a] and player.x - VEL + 20 > 0:
            player.x -= VEL  # -= on x axis, since it's left movement
        if keys[pygame.K_d] and player.x + VEL + player.get_width() < WIDTH:  # 14c get_width and height from class
            player.x += VEL  # += also on x axis, since we're moving right
        if keys[pygame.K_w] and player.y - VEL + 20 > 0:  # if we are greater than 0, we can move, so until edge of
            player.y -= VEL  # -= HEIGHT on y axis, since we're moving up
        if keys[pygame.K_s] and player.y + VEL + player.get_height() + 10 < HEIGHT:  # move down, if player.y position
            player.y += VEL  # is less than height, if VEL += is added on y axis, and need to + the velocity
        if keys[pygame.K_SPACE]:
            player.shoot()  # 27 we call the shoot method here, and will create a laser if the CD is 0
            PLAYER_LASER_SOUND.play()  # 36 play laser sound

        for enemy in enemies[:]:  # 21 our enemies move down now by calling them here - we make a copy of list with [:]
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)  # 30 move lasers here, check if we hit player object as 2nd argument
            if random.randrange(0, 2 * 60) == 1:  # 31 the probability for enemy to shoot for each frame, from 0 to
                enemy.shoot()  # whatever we want - multiply by 60, would make them shoot x times per second
                ENEMY_LASER_SOUND.play()
            if collide(enemy, player):  # 32 if there's a collision, parameters are enemy and player
                player.health -= 10  # then subtract 10 health from player
                enemies.remove(enemy)  # remove enemy from enemies list
                SHIP_COLLISION_SOUND.play()  # if we collide our ship with enemy ships
            elif enemy.y + enemy.get_height() > HEIGHT:  # 21c we check the enemies height pos, to remove them from our
                lives -= 1  # list, and remove 1 hp from our lives, in order to be able to spawn new enemies
                enemies.remove(enemy)  # removes object "enemy" from the "enemies" list

        player.move_lasers(-laser_vel, enemies)  # 30c move players laser, and see if we hit any enemies as 2nd argument
        # laser_vel must be negative, to shoot from bottom to top as the player


def main_menu():  # 35
    title_font = pygame.font.SysFont("linuxlibertinegsemibold", 90)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0, 0))  # making the background appear at x pos 0 and y pos 0
        title_label = title_font.render("Kyni, press the mouse to begin...", 1, LEMON)
        WIN.blit(title_label,
                 (WIDTH / 2 - title_label.get_width() / 2, 150))  # appear at width/2 minus titles width/2, y
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # if x is clicked, then quit the game
            if event.type == pygame.MOUSEBUTTONDOWN:  # if we press any of the mouse buttons, enter main loop -->
                main()  # and start playing the game - calling main here, we keep returning to menu unless x is pressed
    pygame.quit()


main_menu()
