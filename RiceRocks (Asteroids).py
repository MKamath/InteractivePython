# Title :- RiceRocks (Asteroids)

# Description :-
# In our last two mini-projects, we will build a 2D space game RiceRocks that is inspired by the
# classic arcade game Asteroids (1979). Asteroids is a relatively simple game by today's
# standards, but was still immensely popular during its time. In the game, the player controls a
# spaceship via four buttons: two buttons that rotate the spaceship clockwise or counterclockwise
# (independent of its current velocity), a thrust button that accelerates the ship in its forward
# direction and a fire button that shoots missiles. Large asteroids spawn randomly on the screen
# with random velocities. The player's goal is to destroy these asteroids before they strike the
# player's ship. In the arcade version, a large rock hit by a missile split into several fast
# moving small asteroids that themselves must be destroyed. Occasionally, a flying saucer also
# crosses the screen and attempts to destroy the player's spaceship. Searching for "asteroids
# arcade" yields links to multiple versions of Asteroids that are available on the web
# (including an updated version by Atari, the original creator of Asteroids).
# 
# For this mini-project, we will complete the implementation of RiceRocks, an updated version of
# Asteroids,  that we began last week (Spaceship).

import simplegui
import math
import random

# globals for user interface
EXPLOSION_DIM = [9, 9]
EXPLOSION_SIZE = [100, 100]
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
trip = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        self.animated = animated
        if lifespan:
            self.lifespan = lifespan
        
        else:
            self.lifespan = float('inf')

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.explode = False
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99
    
    def shoot(self):
        global a_missile  
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], 
                       self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        missile_sound.play()
    
    def get_radius(self):
        return self.radius
    
    def get_vel(self):
        return self.vel
    
    def get_pos(self):
        return self.pos
    
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
        
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
    
    def set_explode(self, yes):
        self.explode = yes

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.explode = False
        if sound:
            sound.rewind()
            sound.play()
    
    def draw(self, canvas):        
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + (self.image_size[0] * self.age),
                                            self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.age += 1
        self.angle += self.angle_vel 
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        if self.age < self.lifespan:
            return False
        else:
            return True
    
    def get_radius(self):
        return self.radius
    
    def get_vel(self):
        return self.vel
    
    def get_pos(self):
        return self.pos
    
    def collide(self, other_object):
        pos = other_object.get_pos()
        radius = other_object.get_radius()
        distance = dist(self.pos, pos)
        if distance < self.radius + radius:
            return True
        else:
            return False

def new_game(pos):
    global started, score, lives
    
    if not started:
        score = 0
        lives = 3
        started = True
        timer.start()
        soundtrack.play()

def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, my_ship, trip
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                      [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # update & draw ship and sprites
    my_ship.update()
    decrement = group_collide(rock_group, my_ship)
    if decrement:
        lives -= 1
    increment = group_group_collide(missile_group, rock_group)
    if increment > 0:
        score += increment
    
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    if my_ship.explode:
        if trip == 20:
            trip = 0
            my_ship.set_explode(False)
        
        else:
            trip += 1
            
    else:
        my_ship.draw(canvas)
    
    # update scores and lives
    canvas.draw_text("Lives " + str(lives), [50, 50], 22, "White")
    canvas.draw_text("Score " + str(score), [680, 50], 22, "White")
    
    if lives == 0:
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        rock_group = set()
        missile_group = set()
        started = False
        timer.stop()
        soundtrack.rewind()
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], 
                          splash_info.get_size())

def group_collide(group, other_object):
    global lives, ship_explode
    tmp = set(group)
    to_do = False
    for sprite in tmp:
            if sprite.collide(other_object):
                group.remove(sprite)
                if type(other_object) == Ship:
                    other_object.set_explode(True)
                    explosion_group.add(Sprite(other_object.get_pos(), other_object.get_vel(), 0, 0, explosion_image,
                                        explosion_info, explosion_sound))
                explosion_group.add(Sprite(sprite.get_pos(), sprite.get_vel(), 0, 0, explosion_image, explosion_info,
                                    explosion_sound))
                to_do = True
    return to_do

def group_group_collide(group1, group2):
    tmp = set(group1)
    to_do = 0
    for sprite in tmp:
        remove = group_collide(group2, sprite)
        if remove:
            group1.remove(sprite)
            to_do += 1
    return to_do

def process_sprite_group(group, canvas):
    tmp = set(group)
    for sprite in tmp:
        sprite.draw(canvas)
        remove = sprite.update()
        if remove:
            group.remove(sprite)

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    if len(rock_group) < 12:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        pos = my_ship.get_pos()
        radius = my_ship.get_radius()
        distance = dist(rock.pos, pos)
        if distance > (rock.radius + radius + 10):
            rock_group.add(rock)

def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False) 

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(new_game)
timer = simplegui.create_timer(1000.0, rock_spawner)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
missile_group = set()
explosion_group = set()

# get things rolling
frame.start()
