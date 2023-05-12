import pygame
import time
import random
import math
import types

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
        self.score_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.player = Player(red, 150, 60, Manual_Controller())
        self.puck = Puck(200, 80)
        self.addMovingSprite(self.player)
        self.addMovingSprite(self.puck)
        # self.addMovingSprite(Player(blue, 60, 70, Chaser_Controller()))
        self.addFixedSprite(Net(6, (85 - 6) / 2))
        self.addFixedSprite(Net(190, (85 - 6) / 2, True))
        self.addFixedSprite(GoalBox(9 * RINK_SCALE, (85 - 4) / 2 * RINK_SCALE, LEFT_GOAL_EVENT))
        self.addFixedSprite(GoalBox(190 * RINK_SCALE - 1, (85 - 4) / 2 * RINK_SCALE, RIGHT_GOAL_EVENT))
        self.posession = None

        self.game_state = types.SimpleNamespace()
        self.game_state.puck = self.puck
        self.game_state.left_score = 0
        self.game_state.right_score = 0
        print(self.game_state)

        self.addFixedSprite(TopBoard())
        self.addFixedSprite(BottomBoard())
        self.addFixedSprite(LeftBoard())
        self.addFixedSprite(RightBoard())

    def draw(self):
        drawRink(self.dis)
        self.all_sprites_list.draw(self.dis)
        self.draw_score()
        pygame.display.update()
        
    def get_game_state(self):
        return self.game_state

    def draw_score(self):
        score_string = '{} - {}'.format(self.game_state.left_score, self.game_state.right_score)
        text_surface = self.score_font.render(score_string, True, black)
        x = RINK_WIDTH / 2 - text_surface.get_width() / 2 + BOARD_THICKNESS
        self.dis.blit(text_surface, (x, 0))


    def update(self, event):
        self.all_sprites_list.update(self.game_state, event)
        collisions_map = pygame.sprite.groupcollide(self.all_sprites_list, self.moving_sprites_list, False, False, collider)
        for sprite in collisions_map.keys():
            collisions = collisions_map[sprite]
            for collided in collisions:
                if sprite != collided:
                    sprite.handle_collision(collided)
        # if self.is_out_of_bounds(self.puck):
        #     self.puck.pos.update(RINK_WIDTH / 2, RINK_HEIGHT / 2)
        #     self.puck.velocity.update(0, 0)
    
    def is_out_of_bounds(self, sprite):
        rink = pygame.Rect(0, 0, RINK_WIDTH, RINK_HEIGHT)
        return not rink.contains(sprite.rect)
    
def collider(a, b):
    if isinstance(a, Board):
        custom_collider = a.get_collider()
        return custom_collider(a, b)
    if isinstance(b, Board):
        custom_collider = b.get_collider()
        return custom_collider(b, a)
    
    return pygame.sprite.collide_rect(a, b)


