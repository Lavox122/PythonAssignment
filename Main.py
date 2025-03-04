import pygame
import sys
import cv2


#Level 1 coding
#loading all the pictures
#Player
PlayerIdleIMG = cv2.imread('PythonAssignment\\Images\\Player\\Idle.png')
PlayerBlockIMG = cv2.imread('PythonAssignment\\Images\\Player\\Block.png')
PlayerPunchIMG = cv2.imread('PythonAssignment\\Image\\Player\\Punch.png')

#Enemy
EnemyIdleIMG = cv2.imread('PythonAssignment\\Images\\Enemy\\Level1\\Idle.png')
EnemyBlockIMG = cv2.imread('PythonAssignment\\Images\\Enemy\\Level1\\Block.png')
EnemyAttackWindUpIMG = cv2.imread('PythonAssignment\\Images\\Enemy\\Level1\\Attack_Wind-up.png')
EnemyAttackIMG = cv2.imread('PythonAssignment\\Images\\Enemy\\Level1\\Attack.png')

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

    cv2.imshow('Test', PlayerIdleIMG)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)