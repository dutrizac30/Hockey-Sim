import pygame
import hockey

class HockeyGame():
    def __init__(self, dis):
        self.game = hockey.Game(dis)
        self.player = self.game.player
    
    def run_manual_game(self):
        game_over = False
        pygame.key.set_repeat(0, 0)
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(self.player.get_direction())
                    if event.key == pygame.K_LEFT:
                        self.player.accelerate(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        self.player.accelerate(1, 0)
                    if event.key == pygame.K_UP:
                        self.player.accelerate(0, -1)
                    if event.key == pygame.K_DOWN:
                        self.player.accelerate(0, 1)
                    if event.key == pygame.K_p:
                        self.player.passing(self.player.get_direction())

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.coast()
                    if event.key == pygame.K_RIGHT:
                        self.player.coast()
                    if event.key == pygame.K_UP:
                        self.player.coast()
                    if event.key == pygame.K_DOWN:
                        self.player.coast()
        pygame.quit()
        quit()



def run_game():

    pygame.init()

    dis = pygame.display.set_mode((hockey.SCREEN_WIDTH, hockey.SCREEN_HEIGHT))
    pygame.display.set_caption('Hockey Sim')
    game = HockeyGame(dis)

run_game()