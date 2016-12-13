# implementation of Spaceship - program template for RiceRocks
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
collisions = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("https://www.dropbox.com/s/0uk5o4k4bhznybw/TrumpRoids.png?dl=1")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

#tomato image
tomato_info = ImageInfo([15, 15], [30, 30], 10, 100)
tomato_image = simplegui.load_image("https://www.dropbox.com/s/xfisgncg84ju5jw/tomato.png?dl=1")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# Trump image
trump_info = ImageInfo([45, 45], [90, 90], 40)
trump_image = simplegui.load_image("https://www.dropbox.com/s/eso7ezfdae57t5h/Trump.png?dl=1")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


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
        
    def draw(self,canvas):
        center = self.image_center
        if self.thrust :
            center = [self.image_center[0] + self.image_size[0], 
            self.image_center[1]]
        canvas.draw_image(self.image, center, self.image_size, 
        self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        if self.thrust :
            self.vel[0] += .1 * angle_to_vector(self.angle)[0]
            self.vel[1] += .1 * angle_to_vector(self.angle)[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.vel[0] = .995 * self.vel[0]
        self.vel[1] = .995 * self.vel[1]
        
    def spin_right(self):
        self.angle_vel += .1
        
    def spin_left(self):
        self.angle_vel -= .1

    def i_feel_the_need__the_need_for_speed(self, thrusters) :
        self.thrust = thrusters
        if self.thrust :
            ship_thrust_sound.play()
        if not self.thrust :
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
    
    def shoot(self) :
        global missile_group
        missile_group.add(Sprite([self.pos[0] + self.radius * angle_to_vector(self.angle)[0], 
        self.pos[1] + self.radius * angle_to_vector(self.angle)[1]], 
        [self.vel[0] + 3 * angle_to_vector(self.angle)[0], 
        self.vel[1] + 3 * angle_to_vector(self.angle)[1]], 0, 0, 
        tomato_image, tomato_info, missile_sound))
    
    
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
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        center = list(self.image_center)
        if self.animated :
            center[0] = self.image_center[0] + (self.age * self.image_size[0])
        canvas.draw_image(self.image, center, self.image_size, 
        self.pos, self.image_size, self.angle)
            

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.age += 1
        return self.age > self.lifespan
    
    def collide(self, other_object) :
        return dist(self.pos, other_object.pos) < (self.radius + other_object.radius)

           
def draw(canvas):
    global time, lives, score, started, collisions, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship
    my_ship.update()
    
    # detect ship/rock collisions
    if group_collide(rock_group, my_ship) :
        lives -= 1
        
    # detect missile/rock collisions
    if group_group_collide(missile_group, rock_group) :
        score = collisions
    
    # draw user interface
    canvas.draw_text("Lives " + str(lives), [50, 50], 22, "White", "sans-serif")
    canvas.draw_text("Score " + str(score), [680, 50], 22, "White", "sans-serif")
    
    # graw splash screen if not started
    if not started :
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), 
                          [WIDTH / 2, HEIGHT / 2], [WIDTH / 2, HEIGHT / 2])
    if lives == 0 :
        started = False
        rock_group = set([])
        timer.stop()
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), 
                          [WIDTH / 2, HEIGHT / 2], [WIDTH / 2, HEIGHT / 2])

def process_sprite_group(group, canvas):
    for sprite in set(group) :
        sprite.draw(canvas)
        sprite.update()
        if sprite.update() :
            group.remove(sprite)
        
def group_collide(group, other_object) :
    collision = False
    for object in set(group) :
        if object.collide(other_object) :
            group.remove(object)
            collision = True
            explosion_group.add(Sprite(object.pos, [0, 0], 0, 0, 
                                       explosion_image, explosion_info, 
                                       explosion_sound))
    return collision

def group_group_collide(group, other_group) :
    global collisions
    for object in set(group) :
        if group_collide(other_group, object) :
            collisions += 1
            group.discard(object)
    return collisions
    
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    if len(list(rock_group)) < 12 and started and dist(rock_pos, my_ship.pos) > 200 :
        rock_group.add(Sprite(rock_pos, [.01 * random.randrange(-100, 100), 
        .01 * random.randrange(-100, 100)], 2 * math.pi * random.randrange(-100, 100), 
        .0001 * random.randrange(-100, 100), trump_image, trump_info))
    
    
# keydown and keyup handlers
def keydown(key) :
    if key == simplegui.KEY_MAP["left"] :
        my_ship.spin_left()
    if key == simplegui.KEY_MAP["right"] :
        my_ship.spin_right()
    if key == simplegui.KEY_MAP["up"] :
        my_ship.i_feel_the_need__the_need_for_speed(True)
    if key == simplegui.KEY_MAP["space"] :
        my_ship.shoot()
        
def keyup(key) :
    if key == simplegui.KEY_MAP["left"] :
        my_ship.spin_right()
    if key == simplegui.KEY_MAP["right"] :
        my_ship.spin_left()
    if key == simplegui.KEY_MAP["up"] :
        my_ship.i_feel_the_need__the_need_for_speed(False)

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos) :
    global started, lives, collisions, score
    if not started :
        started = True
        lives = 3
        collisions = 0
        score = 0
        timer.start()
        soundtrack.rewind()
        soundtrack.play()
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprite groups
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 3 * math.pi / 2, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()