import pygame
import time
import random
import math

from .components import *
from .colors import *
from .constants import *

class Game:

    def addMovingSprite(self, sprite):
        self.moving_sprites_list.add(sprite)
        self.all_sprites_list.add(sprite)

    def addFixedSprite(self, sprite):
        self.all_sprites_list.add(sprite)

    def __init__(self, dis):
        self.dis = dis
        self.moving_sprites_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        self.player = Player(red, 150, 60, Manual_Controller())
        self.puck = Puck(200, 80)
        self.addMovingSprite(self.player)
        self.addMovingSprite(self.puck)
        self.addMovingSprite(Player(blue, 60, 70, Chaser_Controller()))
        self.addFixedSprite(Net(6, (85 - 6) / 2))
        self.addFixedSprite(Net(190, (85 - 6) / 2, True))
        self.posession = None

        self.game_state = {
            "puck": self.puck
        }

        self.addFixedSprite(TopBoard())
        self.addFixedSprite(BottomBoard())
        self.addFixedSprite(LeftBoard())
        self.addFixedSprite(RightBoard())

    def draw(self):
        drawRink(self.dis)
        self.all_sprites_list.draw(self.dis)
        pygame.display.update()

    def update(self, event):
        self.all_sprites_list.update(self.game_state, event)
        collisions_map = pygame.sprite.groupcollide(self.all_sprites_list, self.moving_sprites_list, False, False)
        for sprite in collisions_map.keys():
            collisions = collisions_map[sprite]
            for collided in collisions:
                if sprite != collided:
                    sprite.handle_collision(collided)

