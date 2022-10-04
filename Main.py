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

# To do list:
# - Add velocity to control (Accelerate, deccelerate)
# - Collision with the boards
# - Collision with the net
# - Arbitrary direction
# - Add puck
# - Collision with puck
# - Add second player
# - Shoot puck
# - Pass puck
# - Detect puck in the net
# - Keep score
# - Player collision
# - Fall down when hitting boards too fast/ gettting hit with puck
# - Add goalie
# - Fill all positions on ice
# - Create the AI
# - Add icing/offside


class Player(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

       pygame.sprite.Sprite.__init__(self)

       self.velocity = 1
       self.direction = (1, 0)

       self.image = pygame.Surface([width * rink_scale, height * rink_scale])
       self.image.fill(color)

       self.rect = self.image.get_rect()
       
    def update(self):
        self.rect.x = self.rect.x + self.direction[0] * self.velocity 
        self.rect.y = self.rect.y + self.direction[1] * self.velocity 

    def control(self, x, y):
        self.direction = (x, y)


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

all_players_list = pygame.sprite.Group()

player = Player(red, 3, 3)

player.rect.x = screen_width / 2
player.rect.y = screen_height / 2

all_players_list.add(player)

def gameLoop():
    game_over = False
   
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.control(-1, 0)
            if event.key == pygame.K_RIGHT:
                player.control(1, 0)
            if event.key == pygame.K_UP:
                player.control(0, -1)
            if event.key == pygame.K_DOWN:
                player.control(0, 1)
            if event.key == pygame.K_SPACE:
                print("Shoot!")

        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT:
        #         player.control(1, 0)
        #     if event.key == pygame.K_RIGHT:
        #         player.control(-1, 0)

        drawRink(dis)
        all_players_list.update()
        all_players_list.draw(dis)
        pygame.display.update()
        clock.tick(30)
        
 
    pygame.quit()
    quit()
 
 
gameLoop()