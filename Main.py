from pickle import FRAME
import pygame
import time
import random
import math
 
pygame.init()
 
FRAME_RATE = 30

MAX_PLAYER_VELOCITY = 85 / FRAME_RATE

MAX_PUCK_VELOCITY = MAX_PLAYER_VELOCITY * 5

FRICTION = 0.01

SHOT_VELOCITY = 20

PASS_VELOCITY = 5

ELASTICITY = 1

RINK_SCALE = 5
 
SCREEN_WIDTH = 200 * RINK_SCALE
SCREEN_HEIGHT = 85 * RINK_SCALE

NET_WIDTH = 4 * RINK_SCALE
NET_HEIGHT = 6 * RINK_SCALE

PUCK_WIDTH = 2 * RINK_SCALE
PUCK_HEIGHT = 2 * RINK_SCALE

PLAYER_WIDTH = 3 * RINK_SCALE
PLAYER_HEIGHT = 3 * RINK_SCALE

white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)

dis = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hockey Sim')
 
clock = pygame.time.Clock()

# To do list:

# - Make the boards a sprite
# - Detect puck in net
# - Add second player controls
# - Fall down when hitting boards too fast/ gettting hit with puck
# - Add goalie
# - Keep score
# - Fill all positions on ice
# - Create the AI
# - Add icing/offside

class Net(pygame.sprite.Sprite):
    def __init__(self, x, y, flip = False):
        super().__init__()
        self.image = pygame.Surface([NET_WIDTH, NET_HEIGHT], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x * RINK_SCALE
        self.rect.y = y * RINK_SCALE
        pygame.draw.rect(self.image, red, [0, 0, self.rect.width, self.rect.height], border_top_left_radius= 1 * RINK_SCALE, border_bottom_left_radius= 1 * RINK_SCALE,)
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def handle_collision(self, target):
        target.pos = target.pos - target.velocity
        target.velocity = -target.velocity
        
class PhysicsBase(pygame.sprite.Sprite):
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.velocity = pygame.math.Vector2(0, 0)
       self.acceleration = pygame.math.Vector2(0, 0)
       self.pos = pygame.math.Vector2(x, y)

    def update(self, game_state, event):
        self.velocity = self.velocity + self.acceleration - self.velocity * FRICTION
        if self.velocity.length() > 0:
            self.velocity.clamp_magnitude_ip(self.get_max_velocity())
        self.pos = self.pos + self.velocity
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def get_max_velocity(self):
        raise ValueError("NotImplemented")


class Player(PhysicsBase):

    def __init__(self, color, x, y, controller):
       PhysicsBase.__init__(self, x, y)
       self.puck = None
       self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
       self.image.fill(color)
       self.rect = self.image.get_rect()
       self.skipCollision = False
       self.controller = controller

    def handle_collision(self, target):
        if self.skipCollision:
            self.skipCollision = False
            return
        if type(target) is Player:
            target.skipCollision = True
            dx = self.pos.x - target.pos.x
            dy = self.pos.y - target.pos.y
            self_angle = math.atan2(self.velocity.y, self.velocity.x)
            target_angle = math.atan2(target.velocity.y, target.velocity.x)
            self_speed = self.velocity.length()
            target_speed = target.velocity.length()
            tangent = math.atan2(dy, dx)
            self_angle = 2 * tangent - self_angle
            target_angle = 2 * tangent - target_angle
            (self_speed, target_speed) = (target_speed, self_speed)
            self_speed *= ELASTICITY
            target_speed *= ELASTICITY
            self.velocity.x = self_speed * math.cos(self_angle)
            self.velocity.y = self_speed * math.sin(self_angle)
            target.velocity.x = target_speed * math.cos(target_angle)
            target.velocity.y = target_speed * math.sin(target_angle)  

    def have_posession(self):
        return self.puck != None
       
    def update(self, game_state, event):
        self.controller.update_controller(self, game_state, event)
        PhysicsBase.update(self, game_state, event)
        if self.have_posession():
            direction = self.velocity.copy()
            if direction.length() > 0:
                direction.normalize_ip()
            self.puck.pos.x = self.pos.x + PLAYER_WIDTH / 2 - PUCK_WIDTH / 2 + direction.x * 20
            self.puck.pos.y = self.pos.y + PLAYER_HEIGHT / 2 - PUCK_HEIGHT / 2 + direction.y * 20

    def accelerate(self, x, y):
        self.acceleration.update(x/5, y/5)

    def coast(self):
        self.acceleration.update(0, 0)
    
    def gain_posession(self, puck):
        global posession
        posession = self
        self.puck = puck

    def lose_posession(self):
        global posession
        posession = None
        self.puck = None

    def shoot(self):
        if self.have_posession():
            puck = self.puck
            self.lose_posession()
            puck.velocity = self.velocity + self.velocity.normalize() * SHOT_VELOCITY

    def pass_puck(self):
        if self.have_posession():
            puck = self.puck
            self.lose_posession()
            puck.velocity = self.velocity + self.velocity.normalize() * PASS_VELOCITY

    def get_max_velocity(self):
        return MAX_PLAYER_VELOCITY

class Controller:
    def update_controller(self, player, game_state, event):
        pass

class Manual_Controller(Controller):
    def update_controller(self, player, game_state, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_LEFT:
                player.accelerate(-MAX_PLAYER_VELOCITY, 0)
            if event.key == pygame.K_RIGHT:
                player.accelerate(MAX_PLAYER_VELOCITY, 0)
            if event.key == pygame.K_UP:
                player.accelerate(0, -MAX_PLAYER_VELOCITY)
            if event.key == pygame.K_DOWN:
                player.accelerate(0, MAX_PLAYER_VELOCITY)
            if event.key == pygame.K_p:
                player.pass_puck()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.coast()
            if event.key == pygame.K_RIGHT:
                player.coast()
            if event.key == pygame.K_UP:
                player.coast()
            if event.key == pygame.K_DOWN:
                player.coast()

class Chaser_Controller(Controller):
    def update_controller(self, player, game_state, event):
        puck = game_state["puck"]
        player.velocity = puck.pos - player.pos
        player.velocity.normalize

class Puck(PhysicsBase):
    def __init__(self, x, y):
        PhysicsBase.__init__(self, x, y)
        self.image = pygame.Surface([PUCK_WIDTH, PUCK_HEIGHT])
        self.image.fill(black)
        self.rect = self.image.get_rect()

    def handle_collision(self, target):
        global posession
        if not posession and type(target) is Player:
            target.gain_posession(self)

    def get_max_velocity(self):
        return MAX_PUCK_VELOCITY

def RinkCollide(target):
    if target.pos.y + target.rect.height > SCREEN_HEIGHT:
        target.pos.y = (SCREEN_HEIGHT - target.rect.height) - (target.pos.y - (SCREEN_HEIGHT - target.rect.height))
        target.velocity.y = -target.velocity.y
    elif target.pos.y < 0:
        target.pos.y = -target.pos.y
        target.velocity.y = -target.velocity.y
    if target.pos.x + target.rect.width > SCREEN_WIDTH:
        target.pos.x = (SCREEN_WIDTH - target.rect.width) - (target.pos.x - (SCREEN_WIDTH - target.rect.width))
        target.velocity.x = -target.velocity.x
    elif target.pos.x < 0:
        target.pos.x = -target.pos.x
        target.velocity.x = -target.velocity.x
    

def draw_rink_line(rink, horizontal, width, colour):
    pygame.draw.rect(rink, colour, [(horizontal * RINK_SCALE) - width * RINK_SCALE / 2, 0, width * RINK_SCALE, 85 * RINK_SCALE])

def drawRink(display):
    size = width, height = (200 * RINK_SCALE, 85 * RINK_SCALE)
    rink = pygame.Surface(size)
    rink.fill(white)
    big_line_width = 2
    thin_line_width = 0.5
    #Left Crease
    pygame.draw.circle(rink, blue, [10 * RINK_SCALE, 85 * RINK_SCALE / 2], 6 * RINK_SCALE, draw_top_right = True, draw_bottom_right= True)
    #Right Crease
    pygame.draw.circle(rink, blue, [190 * RINK_SCALE, 85 * RINK_SCALE / 2], 6 * RINK_SCALE, draw_top_left = True, draw_bottom_left= True)
    #Center line
    draw_rink_line(rink, 100, big_line_width, red)
    #Left Blueline
    draw_rink_line(rink, 70, big_line_width, blue)
    #Right Blueline
    draw_rink_line(rink, 130, big_line_width, blue)
    #Left Goalline
    draw_rink_line(rink, 10, thin_line_width, red)
    #Right Goalline
    draw_rink_line(rink, 190, thin_line_width, red)
    display.blit(rink, (0, 0))

def addMovingSprite(sprite):
    moving_sprites_list.add(sprite)
    all_sprites_list.add(sprite)

def addFixedSprite(sprite):
    all_sprites_list.add(sprite)


moving_sprites_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

player = Player(red, 150, 60, Manual_Controller())
player2 = Player(blue, 60, 70, Chaser_Controller())
puck = Puck(200, 80)
addMovingSprite(player)
addMovingSprite(puck)
addMovingSprite(player2)
addFixedSprite(Net(6, (85 - 6) / 2))
addFixedSprite(Net(190, (85 - 6) / 2, True))
posession = None

game_state = {
    "puck": puck
}

def gameLoop():
    game_over = False
    pygame.key.set_repeat(0, 0)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True


        drawRink(dis)
        all_sprites_list.update(game_state, event)
        RinkCollide(player)
        RinkCollide(player2)
        RinkCollide(puck)
        collisions_map = pygame.sprite.groupcollide(all_sprites_list, moving_sprites_list, False, False)
        for sprite in collisions_map.keys():
            collisions = collisions_map[sprite]
            for collided in collisions:
                if sprite != collided:
                    sprite.handle_collision(collided)
        all_sprites_list.draw(dis)
        pygame.display.update()
        clock.tick(FRAME_RATE)
        
 
    pygame.quit()
    quit()
 
 
gameLoop()