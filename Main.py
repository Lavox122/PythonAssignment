import pygame
import sys
import cv2
import numpy as np
import random

def convertIMG(img):
    if img is None:
        return None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = np.rot90(img)
    img = np.flipud(img)
    return pygame.surfarray.make_surface(img)

def resize(img, width, height):
    if img is None:
        return None
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    return convertIMG(img)

#Level 1 coding
#loading all the pictures
#Player
PlayerIdleIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Player\\Idle.png')
PlayerBlockIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Player\\Block.png')
PlayerPunchIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Player\\Punch.png')

#Enemy
EnemyIdleIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Enemy\\Level1\\Idle.png')
EnemyBlockIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Enemy\\Level1\\Block.png')
EnemyAttackWindUpIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Enemy\\Level1\\Attack_Wind-up.png')
EnemyAttackIMG = cv2.imread('D:\\PythonAssignments\\PythonAssignment\\Images\\Enemy\\Level1\\Attack.png')

#Resizing the images after conversion
PlayerIdleIMG = resize(PlayerIdleIMG, 400, 400)
PlayerBlockIMG = resize(PlayerBlockIMG, 450, 450)
PlayerPunchIMG = resize(PlayerPunchIMG, 600, 600)

EnemyIdleIMG = resize(EnemyIdleIMG, 350, 500)
EnemyBlockIMG = resize(EnemyBlockIMG, 400, 400)
EnemyAttackWindUpIMG = resize(EnemyAttackWindUpIMG, 350, 500)
EnemyAttackIMG = resize(EnemyAttackIMG, 600, 600)

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
idle_x = screen_width // 2 - 25
idle_y = screen_height - 350

punch_x = screen_width // 2 - 200
punch_y = screen_height - 600

block_x = screen_width // 2 - 250
block_y = screen_height - 450

#Enemy settings
EnemyIdle_x = screen_width // 2 - 200
EnemyIdle_y = screen_height - 500

EnemyAttackWindUp_x = screen_width // 2 - 200
EnemyAttackWindUp_y = screen_height - 500

EnemyAttack_x = screen_width // 2 - 200
EnemyAttack_y = screen_height - 500

#Punch settings (All numbers are in milliseconds)
punching = False
punch_timer = 0
punch_duration = 300
punch_cooldown = 1000
last_punch_time = 0

#Block settings
blocking = False

#Enemy AI system (pseudo-AI)
EnemyAttacking = False
EnemyAttackWindUp = False
Enemy_attack_timer = 0
EnemyAttackWindUp_timer = 0
EnemyAttackWindUp_duration = 1000
EnemyAttack_duration = 500
Enemy_attack_cooldown = random.randint(1000, 5000)
last_enemy_attack_time = pygame.time.get_ticks()

#The game coding
while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #Left click (for punching)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not punching and (current_time - last_punch_time > punch_cooldown):
                punching = True
                punch_timer = current_time

        #Right click (for blocking)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if not punching and (current_time - last_punch_time > punch_cooldown):
                blocking = True

        #Release Right click (for stopping blocking)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            blocking = False
    
    #Punching animation cooldown
    if punching and (current_time - punch_timer > punch_duration):
        punching = False
        last_punch_time = current_time

    #Stops player from blocking when recently punched or is punching
    if punching or (current_time - last_punch_time <= punch_cooldown):
        blocking = False

    #Enemy AI part 2
    if not EnemyAttacking and not EnemyAttackWindUp and (current_time - last_enemy_attack_time > Enemy_attack_cooldown):
        EnemyAttackWindUp = True
        EnemyAttackWindUp_timer = current_time

    if EnemyAttackWindUp and (current_time - EnemyAttackWindUp_timer > EnemyAttackWindUp_duration):
        EnemyAttackWindUp = False
        EnemyAttacking = True
        Enemy_attack_timer = current_time

    if EnemyAttacking and (current_time - Enemy_attack_timer > EnemyAttack_duration):
        EnemyAttacking = False
        last_enemy_attack_time = current_time
        Enemy_attack_cooldown = random.randint(1000, 5000)

    screen.fill((0, 0, 0))

    #Player images
    if punching:
        screen.blit(PlayerPunchIMG, (punch_x, punch_y))
    elif blocking:
        screen.blit(PlayerBlockIMG, (block_x, block_y))
    else:
        screen.blit(PlayerIdleIMG, (idle_x, idle_y))

    #Enemy images
    if EnemyAttackWindUp:
        screen.blit(EnemyAttackWindUpIMG, (EnemyAttackWindUp_x, EnemyAttackWindUp_y))
    elif EnemyAttacking:
        screen.blit(EnemyAttackIMG, (EnemyAttack_x, EnemyAttack_y))
    else:
        screen.blit(EnemyIdleIMG, (EnemyIdle_x, EnemyIdle_y))

    pygame.display.flip()
    clock.tick(60)
