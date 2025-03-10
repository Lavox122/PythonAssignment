import pygame
import sys
from PIL import Image
import cv2
import numpy as np
import random

pygame.mixer.init()

def convertIMG(img):
    if img is None:
        return None
    
    if len(img.shape) == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    img = np.rot90(img)
    img = np.rot90(img)
    img = np.flipud(img)

    return pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "RGBA")


def resize(img, width, height, flip = False):
    if img is None:
        return None
    
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    if flip:
        img = cv2.flip(img, 1)

    return convertIMG(img)

def GifLoading(file_path, width, height):
    gif = Image.open(file_path)
    frames = []

    try:
        while True:
            frame = gif.convert("RGBA")
            frame = frame.resize((width, height), Image.LANCZOS)
            pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            frames.append(pygame_frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    return frames

#Level 1 coding
#loading all the pictures, sounds, and animation
#Player
PlayerIdleIMG = cv2.imread("Images\\Player\\Idle.png", cv2.IMREAD_UNCHANGED)
PlayerBlockIMG = cv2.imread('Images\\Player\\Block.png', cv2.IMREAD_UNCHANGED)
PlayerPunchIMG = cv2.imread('Images\\Player\\Punch.png', cv2.IMREAD_UNCHANGED)

#Player Sound Effects
PlayerPunchAud = pygame.mixer.Sound('Audio\\Player\\PlayerPunchingSound1.mp3')
PlayerBlockAud = pygame.mixer.Sound('Audio\\Player\\PlayerBlockingSound.mp3')

#Player Animation Effects
PlayerPunchGIF = GifLoading('Images\\Effect\\PunchingEnemy\\Punching_Enemy.gif', 350, 350)

#Enemy
EnemyIdleIMG = cv2.imread('Images\\Enemy\\Level1\\Idle.png', cv2.IMREAD_UNCHANGED)
EnemyBlockIMG = cv2.imread('Images\\Enemy\\Level1\\Block.png', cv2.IMREAD_UNCHANGED)
EnemyAttackWindUpIMG = cv2.imread('Images\\Enemy\\Level1\\Attack_Wind-up.png', cv2.IMREAD_UNCHANGED)
EnemyAttackIMG = cv2.imread('Images\\Enemy\\Level1\\Attack.png', cv2.IMREAD_UNCHANGED)

#Enemy Sound Effects
EnemyPunchAud = pygame.mixer.Sound('Audio\\Enemy\\EnemyPunchingSound.mp3')
EnemyWindUpAud = pygame.mixer.Sound('Audio\\Enemy\\EnemyWindUpSound.ogg')

#Enemy Animation Effects
EnemyPunchGIF = GifLoading('Images\\Effect\\EnemyPunching\\EnemyPunching.gif', 600, 600)

#Background Image
BackgroundIMG = cv2.imread('Images\\Background\\BoxingRing.png', cv2.IMREAD_UNCHANGED)

#Background Ambience
BackgroundAud= pygame.mixer.Sound('Audio\\Background\\BackgroundAmbience.mp3')

#Resizing the images after conversion
PlayerIdleIMG = resize(PlayerIdleIMG, 400, 400, flip= True)
PlayerBlockIMG = resize(PlayerBlockIMG, 450, 450, flip= True)
PlayerPunchIMG = resize(PlayerPunchIMG, 600, 600, flip= True)

EnemyIdleIMG = resize(EnemyIdleIMG, 350, 600)
EnemyBlockIMG = resize(EnemyBlockIMG, 400, 400)
EnemyAttackWindUpIMG = resize(EnemyAttackWindUpIMG, 250, 600)
EnemyAttackIMG = resize(EnemyAttackIMG, 600, 600)

BackgroundIMG = resize(BackgroundIMG, 800, 600)

#Animation Settings
frame_index = 0
animation_speed = 5
last_update = pygame.time.get_ticks()

#initialize the window
pygame.init()

#Window resolution and size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Fighting Game")

#Health system
PlayerHealth = 3
EnemyHealth = 10

#Controlling game over
GameOver = False

#frame rate
clock = pygame.time.Clock()

#Player settings
idle_x = screen_width // 2 + 10
idle_y = screen_height - 350

punch_x = screen_width // 2 - 200
punch_y = screen_height - 600

block_x = screen_width // 2 - 250
block_y = screen_height - 450

#Enemy settings
EnemyIdle_x = screen_width // 2 - 200
EnemyIdle_y = screen_height - 600

EnemyAttackWindUp_x = screen_width // 2 - 125
EnemyAttackWindUp_y = screen_height - 600

EnemyAttack_x = screen_width // 2 - 300
EnemyAttack_y = screen_height - 500

EnemyBlocking_x = screen_width // 2 - 200
EnemyBlocking_y = screen_height - 600

#Effect size settings
PunchEffect_x = screen_width // 2 - 125
PunchEffect_y = screen_height - 450

#Punch settings (All numbers are in milliseconds)
punching = False
punch_timer = 0
punch_duration = 300
punch_cooldown = 1200
last_punch_time = 0

#Block settings
blocking = False

#Enemy AI system (pseudo-AI)
EnemyAttacking = False
EnemyAttackWindUp = False
EnemyBlocking = False
EnemyAttack_timer = 0
EnemyAttackWindUp_timer = 0
EnemyAttackWindUp_duration = 1000
EnemyAttack_duration = 500
EnemyBlock_duration = random.randint(5000, 10000)
EnemyAttack_cooldown = random.randint(4000, 6000)
EnemyBlock_cooldown = 2000
last_enemy_attack_time = pygame.time.get_ticks()

#The game coding
while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not GameOver:
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

        #Reduce enemy health when punching (doesn't work when enemy blocking)
            if not EnemyBlocking:
                EnemyHealth -= 1
                print(f"Enemy Health: {EnemyHealth}") #this is only for debugging purposes

                PlayerPunchAud.play()

                for frame in PlayerPunchGIF:
                    screen.fill((0, 0, 0, 0))  # Clear the screen
                    screen.blit(BackgroundIMG, (0, 0))  # Draw the background
                    screen.blit(EnemyIdleIMG, (EnemyIdle_x, EnemyIdle_y))  # Draw the enemy idle image
                    screen.blit(frame, (PunchEffect_x, PunchEffect_y))  # Draw the punch effect behind the player
                    screen.blit(PlayerPunchIMG, (punch_x, punch_y))  # Draw the player punch image
                    pygame.display.flip()
                    pygame.time.delay(50)

        #Stops player from blocking when recently punched or is punching
        if punching or (current_time - last_punch_time <= punch_cooldown):
            blocking = False

        #Enemy AI part 2
        if not EnemyAttacking and not EnemyAttackWindUp and (current_time - last_enemy_attack_time > EnemyAttack_cooldown):
            action_choice = random.choice(["Attack", "Block"])
            if action_choice == "Attack":
                EnemyAttackWindUp = True
                EnemyAttackWindUp_timer = current_time
            elif action_choice == "Block":
                EnemyBlocking = True
                EnemyBlock_timer = current_time

        if EnemyAttackWindUp and (current_time - EnemyAttackWindUp_timer > EnemyAttackWindUp_duration):
            EnemyAttackWindUp = False
            EnemyAttacking = True
            EnemyAttack_timer = current_time

        if EnemyAttacking and (current_time - EnemyAttack_timer > EnemyAttack_duration):
            if not blocking:
                PlayerHealth -= 1
                print(f"Player Health: {PlayerHealth}") #this is only for debugging purposes
            
            EnemyAttacking = False
            last_enemy_attack_time = current_time
            EnemyAttack_cooldown = random.randint(1000, 5000)

        if EnemyBlocking and (current_time - EnemyBlock_timer > EnemyBlock_duration):
            EnemyBlocking = False
            last_enemy_attack_time = current_time
            EnemyAttack_cooldown = random.randint(5000, 7000)

        #Set it so the game over runs
        if PlayerHealth <= 0:
            GameOver = True

        screen.fill((0, 0, 0, 0))

        #Background image
        screen.blit(BackgroundIMG, (0,0))

        #Enemy images
        if EnemyAttackWindUp:
            screen.blit(EnemyAttackWindUpIMG, (EnemyAttackWindUp_x, EnemyAttackWindUp_y))
        elif EnemyAttacking:
            screen.blit(EnemyAttackIMG, (EnemyAttack_x, EnemyAttack_y))
        elif EnemyBlocking:
            screen.blit(EnemyBlockIMG, (EnemyBlocking_x, EnemyBlocking_y))
        else:
            screen.blit(EnemyIdleIMG, (EnemyIdle_x, EnemyIdle_y))

        #Player images
        if punching:
            screen.blit(PlayerPunchIMG, (punch_x, punch_y))
        elif blocking:
            screen.blit(PlayerBlockIMG, (block_x, block_y))
        else:
            screen.blit(PlayerIdleIMG, (idle_x, idle_y))

        #Health effects
        if PlayerHealth < 3:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            intensity = int(150 * (1 - (PlayerHealth / 3)))
            overlay.fill((255, 0, 0, intensity))
            screen.blit(overlay, (0, 0))

        #Game Over
    else:
        #The "You Fainted" text
        font = pygame.font.Font(None, 72)
        text = font.render("You fainted", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width//2, screen_height//2 - 100))
        screen.blit(text, text_rect)

        #Retry Button
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        button_y = screen_height // 2 - 10
        button_color = (255, 255, 255)
        button_text_color = (0, 0, 0)

        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        button_text = font.render("Retry", True, button_text_color)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
        screen.blit(button_text, text_rect)

        #Quit Button
        quit_button_y = button_y + button_height + 20
        pygame.draw.rect(screen, button_color, (button_x, quit_button_y, button_width, button_height))
        quit_text = font.render("Quit", True, button_text_color)
        quit_text_rect = quit_text.get_rect(center=(button_x + button_width//2, quit_button_y + button_height//2))
        screen.blit(quit_text, quit_text_rect)

        #Mouse position tracking
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        hover_color = (200, 200, 200)
        click_color = (150, 150, 150)

        #Retry button function
        retry_hover = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
        retry_click = retry_hover and mouse_pressed[0]
        retry_display_color = click_color if retry_click else hover_color if retry_hover else button_color
        
        pygame.draw.rect(screen, retry_display_color, (button_x, button_y, button_width, button_height))
        button_text = font.render("Retry", True, button_text_color)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
        screen.blit(button_text, text_rect)

        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
            if mouse_pressed[0]:
                PlayerHealth = 3
                EnemyHealth = 11
                GameOver = False
                last_punch_time = 0
                last_enemy_attack_time = pygame.time.get_ticks()
                EnemyAttacking = False
                EnemyAttackWindUp = False

        #Quit button function
        quit_hover = button_x <= mouse_x <= button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height
        quit_click = quit_hover and mouse_pressed[0]
        quit_display_color = click_color if quit_click else hover_color if quit_hover else button_color
        
        pygame.draw.rect(screen, quit_display_color, (button_x, quit_button_y, button_width, button_height))
        quit_text = font.render("Quit", True, button_text_color)
        quit_text_rect = quit_text.get_rect(center=(button_x + button_width//2, quit_button_y + button_height//2))
        screen.blit(quit_text, quit_text_rect)
        
        if button_x <= mouse_x <= button_x + button_width and quit_button_y <= mouse_y <= quit_button_y + button_height:
            if mouse_pressed[0]:
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    clock.tick(60)
