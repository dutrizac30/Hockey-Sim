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
 
dis = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hockey Sim')
 
clock = pygame.time.Clock()

def drawRink(display):
    display.fill(white)
    big_line_width = 2
    thin_line_width = 0.5
    pygame.draw.circle(dis, blue, [10 * rink_scale, 85 * rink_scale / 2], 6 * rink_scale, draw_top_right = True, draw_bottom_right= True)
    pygame.draw.circle(dis, blue, [190 * rink_scale, 85 * rink_scale / 2], 6 * rink_scale, draw_top_left = True, draw_bottom_left= True)
    pygame.draw.rect(dis, red, [(10 - 4 )* rink_scale, (85 - 6) / 2 *rink_scale, 4 * rink_scale, 6 * rink_scale], border_top_left_radius= 1 * rink_scale, border_bottom_left_radius= 1 * rink_scale,)
    pygame.draw.rect(dis, red, [190* rink_scale, (85 - 6) / 2 *rink_scale, 4 * rink_scale, 6 * rink_scale], border_top_right_radius= 1 * rink_scale, border_bottom_right_radius= 1 * rink_scale,)
    pygame.draw.rect(dis, red, [(100 * rink_scale) - big_line_width * rink_scale / 2, 0, big_line_width * rink_scale, 85 * rink_scale])
    pygame.draw.rect(dis, blue, [(70 * rink_scale) - big_line_width * rink_scale / 2, 0, big_line_width * rink_scale, 85 * rink_scale])
    pygame.draw.rect(dis, blue, [(130 * rink_scale) - big_line_width * rink_scale / 2, 0, big_line_width * rink_scale, 85 * rink_scale])
    pygame.draw.rect(dis, red, [(10 * rink_scale) - thin_line_width * rink_scale / 2, 0, thin_line_width * rink_scale, 85 * rink_scale])
    pygame.draw.rect(dis, red, [(190 * rink_scale) - thin_line_width * rink_scale / 2, 0, thin_line_width * rink_scale, 85 * rink_scale])
    pygame.draw.rect(dis, red, [(10 * rink_scale) - thin_line_width * rink_scale / 2, 0, thin_line_width * rink_scale, 85 * rink_scale])

def gameLoop():
    game_over = False
   
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
 
        drawRink(dis)
        pygame.display.update()
        clock.tick(30)
 
    pygame.quit()
    quit()
 
 
gameLoop()