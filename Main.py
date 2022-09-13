import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
blue = (50, 153, 213)
 
screen_width = 800
screen_height = 400
 
dis = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hockey Sim')
 
clock = pygame.time.Clock()
 
def gameLoop():
    game_over = False
   
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
 
        dis.fill(white)
        pygame.display.update()
        clock.tick(30)
 
    pygame.quit()
    quit()
 
 
gameLoop()