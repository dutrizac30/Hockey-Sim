from pickle import FRAME
import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)

rink_scale = 5
 
screen_width = 200 * rink_scale
screen_height = 85 * rink_scale

NET_WIDTH = 4 * rink_scale
NET_HEIGHT = 6 * rink_scale

PUCK_WIDTH = 2 * rink_scale
PUCK_HEIGHT = 2 * rink_scale

PLAYER_WIDTH = 3 * rink_scale
PLAYER_HEIGHT = 3 * rink_scale

dis = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hockey Sim')
 
clock = pygame.time.Clock()

FRAME_RATE = 30

MAX_PLAYER_VELOCITY = 85 / FRAME_RATE

MAX_PUCK_VELOCITY = MAX_PLAYER_VELOCITY * 5

FRICTION = 0.01

SHOT_VELOCITY = 20

# To do list:

# - Detect puck in net
# - Keep score
# - Add second player
# - Pass puck
# - Player collision
# - Fall down when hitting boards too fast/ gettting hit with puck
# - Add goalie
# - Fill all positions on ice
# - Create the AI
# - Add icing/offside

class Net(pygame.sprite.Sprite):
    def __init__(self, x, y, flip = False):
        super().__init__()
        self.image = pygame.Surface([NET_WIDTH, NET_HEIGHT], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x * rink_scale
        self.rect.y = y * rink_scale
        pygame.draw.rect(self.image, red, [0, 0, self.rect.width, self.rect.height], border_top_left_radius= 1 * rink_scale, border_bottom_left_radius= 1 * rink_scale,)
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

    def update(self):
        self.velocity = self.velocity + self.acceleration - self.velocity * FRICTION
        if self.velocity.length() > 0:
            self.velocity.clamp_magnitude_ip(self.getMaxVelocity())
        self.pos = self.pos + self.velocity
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def getMaxVelocity(self):
        raise ValueError("NotImplemented")


class Player(PhysicsBase):

    def __init__(self, color, x, y):
       PhysicsBase.__init__(self, x, y)
       self.puck = None
       self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
       self.image.fill(color)
       self.rect = self.image.get_rect()

    def handle_collision(self, target):
        pass

    def have_posession(self):
        return self.puck != None
       
    def update(self):
        PhysicsBase.update(self)
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
        print("shoot")
        if self.have_posession():
            puck = self.puck
            self.lose_posession()
            puck.velocity = self.velocity + self.velocity.normalize() * SHOT_VELOCITY

    def getMaxVelocity(self):
        return MAX_PLAYER_VELOCITY


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

    def getMaxVelocity(self):
        return MAX_PUCK_VELOCITY

def RinkCollide(target):
    if target.pos.y + target.rect.height > screen_height:
        target.pos.y = (screen_height - target.rect.height) - (target.pos.y - (screen_height - target.rect.height))
        target.velocity.y = -target.velocity.y
    elif target.pos.y < 0:
        target.pos.y = -target.pos.y
        target.velocity.y = -target.velocity.y
    if target.pos.x + target.rect.width > screen_width:
        target.pos.x = (screen_width - target.rect.width) - (target.pos.x - (screen_width - target.rect.width))
        target.velocity.x = -target.velocity.x
    elif target.pos.x < 0:
        target.pos.x = -target.pos.x
        target.velocity.x = -target.velocity.x
    

def draw_rink_line(rink, horizontal, width, colour):
    pygame.draw.rect(rink, colour, [(horizontal * rink_scale) - width * rink_scale / 2, 0, width * rink_scale, 85 * rink_scale])

def drawRink(display):
    size = width, height = (200 * rink_scale, 85 * rink_scale)
    rink = pygame.Surface(size)
    rink.fill(white)
    big_line_width = 2
    thin_line_width = 0.5
    #Left Crease
    pygame.draw.circle(rink, blue, [10 * rink_scale, 85 * rink_scale / 2], 6 * rink_scale, draw_top_right = True, draw_bottom_right= True)
    #Right Crease
    pygame.draw.circle(rink, blue, [190 * rink_scale, 85 * rink_scale / 2], 6 * rink_scale, draw_top_left = True, draw_bottom_left= True)
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

player = Player(red, 150, 60)
puck = Puck(200, 80)
addMovingSprite(player)
addMovingSprite(puck)
addMovingSprite(Player(blue, 60, 70))
addFixedSprite(Net(6, (85 - 6) / 2))
addFixedSprite(Net(190, (85 - 6) / 2, True))
posession = None

# player.rect.x = screen_width / 2
# player.rect.y = screen_height / 2

def gameLoop():
    game_over = False
    pygame.key.set_repeat(0, 0)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    print("shot")
                if event.key == pygame.K_LEFT:
                    player.accelerate(-MAX_PLAYER_VELOCITY, 0)
                if event.key == pygame.K_RIGHT:
                    player.accelerate(MAX_PLAYER_VELOCITY, 0)
                if event.key == pygame.K_UP:
                    player.accelerate(0, -MAX_PLAYER_VELOCITY)
                if event.key == pygame.K_DOWN:
                    player.accelerate(0, MAX_PLAYER_VELOCITY)
                

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.coast()
                if event.key == pygame.K_RIGHT:
                    player.coast()
                if event.key == pygame.K_UP:
                    player.coast()
                if event.key == pygame.K_DOWN:
                    player.coast()

        drawRink(dis)
        all_sprites_list.update()
        RinkCollide(player)
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