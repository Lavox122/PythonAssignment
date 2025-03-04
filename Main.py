import pygame
import sys
import cv2
import numpy as np

#Level 1 coding
#loading all the pictures
#Player
PlayerIdleIMG = cv2.imread('D:\\PythonAssignment\\PythonAssignment\\Images\\Player\\Idle.png')
PlayerIdleIMG = cv2.cvtColor(PlayerIdleIMG, cv2.COLOR_BGR2RGB)

PlayerBlockIMG = cv2.imread('D\\PythonAssignment\\PythonAssignment\\Images\\Player\\Block.png')
PlayerBlockIMG = cv2.cvtColor(PlayerBlockIMG, cv2.COLOR_BGR2RGB)

PlayerPunchIMG = cv2.imread('D\\PythonAssignment\\PythonAssignment\\Image\\Player\\Punch.png')
PlayerPunchIMG = cv2.cvtColor(PlayerPunchIMG, cv2.COLOR_BGR2RGB)

#Enemy
EnemyIdleIMG = cv2.imread('D\\PythonAssignment\\PythonAssignment\\Images\\Enemy\\Level1\\Idle.png')
EnemyIdleIMG = cv2.cvtColor(EnemyIdleIMG, cv2.COLOR_BGR2RGB)

EnemyBlockIMG = cv2.imread('D\\PythonAssignment\\PythonAssignment\\Images\\Enemy\\Level1\\Block.png')
EnemyBlockIMG = cv2.cvtColor(EnemyBlockIMG, cv2.COLOR_BGR2RGB)

EnemyAttackWindUpIMG = cv2.imread('D\\PythonAssignment\\PythonAssignment\\Images\\Enemy\\Level1\\Attack_Wind-up.png')
EnemyAttackWindUpIMG = cv2.cvtColor(EnemyAttackWindUpIMG, cv2.COLOR_BGR2RGB)

EnemyAttackIMG = cv2.imread('D\\PythonAssignment\\PythonAssignment\\Images\\Enemy\\Level1\\Attack.png')
EnemyAttackIMG = cv2.cvtColor(EnemyAttackIMG, cv2.COLOR_BGR2RGB)

#initialize the window
pygame.init()

#Window resolution and size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fighting Game")

#frame rate
clock = pygame.time.Clock()

#Converting Images
#Player
PlayerIdleIMG = pygame.image.frombuffer(PlayerIdleIMG.tobytes(), PlayerIdleIMG.shape[1::-1], "RGB")
PlayerBlockIMG = pygame.image.frombuffer(PlayerBlockIMG.tobytes(), PlayerBlockIMG.shape[1::-1], "RGB")
PlayerPunchIMG = pygame.image.frombuffer(PlayerPunchIMG.tobytes(), PlayerPunchIMG.shape[1::-1], "RGB")

#Enemy
EnemyIdleIMG = pygame.image.frombuffer(EnemyIdleIMG.tobytes(), EnemyIdleIMG.shape[1::-1], "RGB")
EnemyBlockIMG = pygame.image.frombuffer(EnemyBlockIMG.tobytes(), EnemyBlockIMG.shape[1::-1], "RGB")
EnemyAttackWindUpIMG = pygame.image.frombuffer(EnemyAttackWindUpIMG.tobytes(), EnemyAttackWindUpIMG.shape[1::-1], "RGB")
EnemyAttackIMG = pygame.image.frombuffer(EnemyAttackIMG.tobytes(), EnemyAttackIMG.shape[1::-1], "RGB")

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
    screen.blit(PlayerIdleIMG, (player_x, player_y))
    pygame.display.flip()
    clock.tick(60)
