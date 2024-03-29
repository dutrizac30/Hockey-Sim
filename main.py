import pygame
import hockey
import time
from hockey.constants import *

# To do list:

# - Return puck to center after goal
# - Fall down when hitting boards too fast/ gettting hit with puck
# - Add goalie
# - Fill all positions on ice
# - Create the AI
# - Add icing/offside

clock = pygame.time.Clock()

class HockeyGame():
    def __init__(self, dis):
        self.game = hockey.Game(dis)
        self.player = self.game.player
        self.puck = self.game.puck

    def run_manual_game(self):
        game_over = False
        pygame.key.set_repeat(0, 0)
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.puck, self.player.get_direction())
                    if event.key == pygame.K_LEFT:
                        self.player.accelerate(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.player.accelerate(1, 0)
                    if event.key == pygame.K_UP:
                        self.player.accelerate(0, -1)
                    if event.key == pygame.K_DOWN:
                        self.player.accelerate(0, 1)
                    if event.key == pygame.K_p:
                        self.player.passing(self.puck, self.player.get_direction())

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.coast()
                    if event.key == pygame.K_RIGHT:
                        self.player.coast()
                    if event.key == pygame.K_UP:
                        self.player.coast()
                    if event.key == pygame.K_DOWN:
                        self.player.coast()
                if event.type == LEFT_GOAL_EVENT:
                    self.game.get_game_state().left_score += 1
                if event.type == RIGHT_GOAL_EVENT:
                    self.game.get_game_state().right_score += 1

            self.game.update(event)
            self.game.draw()
            clock.tick(FRAME_RATE)
        pygame.quit()
        quit()

def run_game():
    pygame.init()
    pygame.font.init() 
    dis = pygame.display.set_mode((hockey.SCREEN_WIDTH, hockey.SCREEN_HEIGHT))
    pygame.display.set_caption('Hockey Sim')
    game = HockeyGame(dis)
    game.run_manual_game()

run_game()

