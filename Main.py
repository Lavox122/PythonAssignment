import pygame
import sys

#initialize the window
pygame.init()

#Window resolution and size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fighting Game")

#frame rate
clock = pygame.time.Clock()

#Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width //2
player_y = screen_height - player_height - 10

#The game coding
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)