from pickle import FRAME
import pygame
import random
import math

from .colors import *
from .constants import *

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

    def get_direction(self):
        return math.atan2(self.velocity.y, self.velocity.x)

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

    def have_posession(self, puck):
        return puck.posession == self

    def update(self, game_state, event):
        self.controller.update_controller(self, game_state, event)
        PhysicsBase.update(self, game_state, event)
        if self.have_posession(game_state.puck):
            direction = self.velocity.copy()
            if direction.length() > 0:
                direction.normalize_ip()
            game_state.puck.pos.x = self.pos.x + PLAYER_WIDTH / 2 - PUCK_WIDTH / 2 + direction.x * 20
            game_state.puck.pos.y = self.pos.y + PLAYER_HEIGHT / 2 - PUCK_HEIGHT / 2 + direction.y * 20

    def accelerate(self, x, y):
        self.acceleration.update(x/5 * MAX_PLAYER_VELOCITY, y/5 * MAX_PLAYER_VELOCITY)

    def coast(self):
        self.acceleration.update(0, 0)

    def _shoot(self, puck, direction, velocity):
        if self.have_posession(puck):
            puck.posession = None
            puck.velocity.x = math.cos(direction) * velocity
            puck.velocity.y = math.sin(direction) * velocity

    def passing(self, puck, direction):
        self._shoot(puck, direction, PASS_VELOCITY)

    def shoot(self, puck, direction):
        self._shoot(puck, direction, SHOT_VELOCITY)

    def get_max_velocity(self):
        return MAX_PLAYER_VELOCITY

class Controller:
    def update_controller(self, player, game_state, event):
        pass

class Manual_Controller(Controller):
    def update_controller(self, player, game_state, event):
        pass

class Chaser_Controller(Controller):
    def update_controller(self, player, game_state, event):
        puck = game_state.puck
        player.acceleration = puck.pos - player.pos
        player.acceleration.scale_to_length(.1)
        if player.have_posession(puck):
            player.shoot(puck, random.uniform(0.0, 2 * math.pi))

class Puck(PhysicsBase):
    def __init__(self, x, y):
        PhysicsBase.__init__(self, x, y)
        self.image = pygame.Surface([PUCK_WIDTH, PUCK_HEIGHT])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.posession = None

    def handle_collision(self, target):
        if not self.posession and type(target) is Player:
            self.posession = target

    def get_max_velocity(self):
        return MAX_PUCK_VELOCITY

class TopBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([RINK_WIDTH, BOARD_THICKNESS])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.x = BOARD_THICKNESS
        self.rect.y = 0

    def handle_collision(self, target):
        target.pos.y = 0
        target.velocity.y = -target.velocity.y


class BottomBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([RINK_WIDTH, BOARD_THICKNESS])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.x = BOARD_THICKNESS
        self.rect.y = RINK_HEIGHT + BOARD_THICKNESS

    def handle_collision(self, target):
        target.pos.y = (RINK_HEIGHT - target.rect.height) - (target.pos.y - (RINK_HEIGHT - target.rect.height))
        target.velocity.y = -target.velocity.y

class LeftBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BOARD_THICKNESS, RINK_HEIGHT])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = BOARD_THICKNESS

    def handle_collision(self, target):
        target.pos.x = 0
        target.velocity.x = -target.velocity.x
        print(target.pos)

class RightBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([BOARD_THICKNESS, RINK_HEIGHT])
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.x = RINK_WIDTH + BOARD_THICKNESS
        self.rect.y = BOARD_THICKNESS

    def handle_collision(self, target):
        target.pos.x = (RINK_WIDTH - target.rect.width)
        print(target.pos)
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
    display.blit(rink, (BOARD_THICKNESS, BOARD_THICKNESS))
