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

def draw_rink_line(rink, horizontal, width, colour):
    pygame.draw.rect(rink, colour, [(horizontal * rink_scale) - width * rink_scale / 2, 0, width * rink_scale, 85 * rink_scale])

def draw_net(rink, horizontal, flip):
    size = width, height = ( 4 * rink_scale, 6 * rink_scale)
    net = pygame.Surface(size, pygame.SRCALPHA, 32) 
    net = net.convert_alpha()
    pygame.draw.rect(net, red, [0, 0, 4 * rink_scale, 6 * rink_scale], border_top_left_radius= 1 * rink_scale, border_bottom_left_radius= 1 * rink_scale,)
    if flip:
        net = pygame.transform.flip(net, True, False)
    rink.blit(net, (horizontal * rink_scale, (85 - 6) / 2 * rink_scale))

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
    #Left Net
    draw_net(rink, 10 - 4, False)
    #Right Net
    draw_net(rink, 190, True)
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