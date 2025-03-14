import pygame
import sys
import subprocess
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

#Player Low Health Sound Effects
PlayerLowAud = pygame.mixer.Sound('Audio\\Player\\LowHealth.mp3')
PlayerLowAud.set_volume(0.5)

#Enemy
EnemyIdleIMG = cv2.imread('Images\\Enemy\\Level1\\Idle.png', cv2.IMREAD_UNCHANGED)
EnemyBlockIMG = cv2.imread('Images\\Enemy\\Level1\\Block.png', cv2.IMREAD_UNCHANGED)
EnemyAttackWindUpIMG = cv2.imread('Images\\Enemy\\Level1\\Attack_Wind-up.png', cv2.IMREAD_UNCHANGED)
EnemyAttackIMG = cv2.imread('Images\\Enemy\\Level1\\Attack.png', cv2.IMREAD_UNCHANGED)

# Define the circle radius
circle_radius = 25  # Adjust this value as needed

# Load the EnemyIcon
EnemyIcon = cv2.imread('Images\\Enemy\\Level1\\EnemyIcon.png', cv2.IMREAD_UNCHANGED)

# Resize the EnemyIcon proportionally to fit inside the circle
icon_height, icon_width = EnemyIcon.shape[:2]
circle_diameter = 2 * circle_radius  # Diameter of the circle
scale = max(circle_diameter / icon_width, circle_diameter / icon_height)  # Scale to fill the circle more fully
new_width = int(icon_width * scale)
new_height = int(icon_height * scale)
EnemyIcon = resize(EnemyIcon, new_width, new_height)

#Enemy Sound Effects
EnemyPunchAud = pygame.mixer.Sound('Audio\\Enemy\\EnemyPunchingSound.mp3')
EnemyWindUpAud = pygame.mixer.Sound('Audio\\Enemy\\EnemyWindUpSound.ogg')
BoxingBellAud = pygame.mixer.Sound('Audio\\Enemy\\BoxingBellSound.mp3')

#Enemy Animation Effects
EnemyPunchGIF = GifLoading('Images\\Effect\\EnemyPunching\\EnemyPunching.gif', 400, 400)

#universal block effect
BlockGIF = GifLoading('Images\\Effect\\Blocking\\Blocking.gif', 400, 400)

#Background Image
BackgroundIMG = cv2.imread('Images\\Background\\BoxingRing.png', cv2.IMREAD_UNCHANGED)

#Background Ambience
BackgroundAud= pygame.mixer.Sound('Audio\\Background\\BackgroundAmbience.mp3')
BackgroundAud.set_volume(0.1)

#Resizing the images after conversion
PlayerIdleIMG = resize(PlayerIdleIMG, 400, 400, flip= True)
PlayerBlockIMG = resize(PlayerBlockIMG, 600, 600, flip= True)
PlayerPunchIMG = resize(PlayerPunchIMG, 600, 600, flip= True)

EnemyIdleIMG = resize(EnemyIdleIMG, 350, 600)
EnemyBlockIMG = resize(EnemyBlockIMG, 600, 600)
EnemyAttackWindUpIMG = resize(EnemyAttackWindUpIMG, 250, 600)
EnemyAttackIMG = resize(EnemyAttackIMG, 600, 600)

BackgroundIMG = resize(BackgroundIMG, 800, 600)

#Animation Settings
PlayerAttackFrame_index = 0
animation_speed = 100
PlayerAttackLast_update = pygame.time.get_ticks()

EnemyAttackFrame_index = 0
animation_speed = 100
EnemyAttackLast_update = pygame.time.get_ticks()

EnemyAttackGIF_duration = len(EnemyPunchGIF) * animation_speed
EnemyPunchGIF_start_time = 0

BlockFrame_index = 0
BlockLast_update = pygame.time.get_ticks()

#initialize the window
pygame.init()

#Window resolution and size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SRCALPHA)
pygame.display.set_caption("Fighting Game")

BackgroundAud.play(loops=-1)

#Health system
PlayerHealth = 3
EnemyHealth = 10
playerDamaged = False
LowHealth = False

#Controlling game over
GameOver = False
Victory = False

#frame rate
clock = pygame.time.Clock()

#Player settings
idle_x = screen_width // 2 + 10
idle_y = screen_height - 350

punch_x = screen_width // 2 - 200
punch_y = screen_height - 600

block_x = screen_width // 2 - 250
block_y = screen_height - 600

#Enemy settings
EnemyIdle_x = screen_width // 2 - 200
EnemyIdle_y = screen_height - 600

EnemyAttackWindUp_x = screen_width // 2 - 125
EnemyAttackWindUp_y = screen_height - 600

EnemyAttack_x = screen_width // 2 - 300
EnemyAttack_y = screen_height - 500

EnemyBlocking_x = screen_width // 2 - 300
EnemyBlocking_y = screen_height - 600

#Effect size settings
PunchEffect_x = screen_width // 2 - 125
PunchEffect_y = screen_height - 450

EnemyPunchEffect_x = screen_width // 2 - 175
EnemyPunchEffect_y = screen_height - 525

BlockGIF_x = screen_width // 2 - 150
BlockGIF_y = screen_height - 450

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
EnemyBlock_duration = random.randint(1000, 3000)
EnemyAttack_cooldown = random.randint(4000, 6000)
EnemyBlock_cooldown = 1500
last_enemy_attack_time = pygame.time.get_ticks()

#The game coding
while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not GameOver and not Victory:
        #Left click (for punching)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not punching and (current_time - last_punch_time > punch_cooldown):
                punching = True
                punch_timer = current_time
                PlayerAttackFrame_index = 0
                PlayerAttackLast_update = current_time
                if not EnemyBlocking:
                    PlayerPunchAud.play()
                elif EnemyBlocking:
                    PlayerBlockAud.play()

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
                

        #Stops player from blocking when recently punched or is punching
        if punching or (current_time - last_punch_time <= punch_cooldown):
            blocking = False

        #Enemy AI part 2
        if not EnemyBlocking:
            if not EnemyAttacking and not EnemyAttackWindUp and (current_time - last_enemy_attack_time > EnemyAttack_cooldown):
                action_choice = random.choice(["Attack", "Block"])
                if action_choice == "Attack":
                    EnemyAttackWindUp = True
                    EnemyAttackWindUp_timer = current_time
                    EnemyWindUpAud.play()
                elif action_choice == "Block":
                    EnemyBlocking = True
                    EnemyBlock_timer = current_time

            if EnemyAttackWindUp and (current_time - EnemyAttackWindUp_timer > EnemyAttackWindUp_duration):
                EnemyAttackWindUp = False
                EnemyAttacking = True
                EnemyAttack_timer = current_time
                if not blocking:
                    EnemyPunchAud.play()
                    EnemyPunchGIF_start_time = current_time
                    EnemyAttackFrame_index = 0
                elif blocking:
                    PlayerBlockAud.play()

            if EnemyAttacking and (current_time - EnemyAttack_timer > EnemyAttack_duration):
                if not blocking:
                    PlayerHealth -= 1
                    playerDamaged = True
                    print(f"Player Health: {PlayerHealth}") #this is only for debugging purposes
                
                
                EnemyAttacking = False
                last_enemy_attack_time = current_time
                EnemyAttack_cooldown = random.randint(1000, 5000)

        if EnemyBlocking and (current_time - EnemyBlock_timer > EnemyBlock_duration):
            EnemyBlocking = False
            last_enemy_attack_time = current_time
            EnemyAttack_cooldown = random.randint(5000, 7000)

        if PlayerHealth == 1 and not LowHealth:
            PlayerLowAud.play(loops=-1)
            LowHealth = True
        elif PlayerHealth != 1 and LowHealth:
            PlayerLowAud.stop()
            LowHealth = False

        #Set it so the game over runs
        if PlayerHealth <= 0:
            GameOver = True

        if EnemyHealth <= 0:
            Victory = True
            BoxingBellAud.play()  # Play the boxing bell sound effect
        
            # Fadeout effect
            font = pygame.font.Font(None, 72)
            text = font.render("You Win!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

            for alpha in range(0, 255, 5):  # Gradually increase opacity
                # Draw the background and "You Win!" text
                screen.blit(BackgroundIMG, (0, 0))
                screen.blit(text, text_rect)

                # Draw the fadeout overlay
                fade_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
                fade_surface.fill((0, 0, 0, alpha))  # Black fade
                screen.blit(fade_surface, (0, 0))

                pygame.display.flip()
                pygame.time.delay(50)  # Delay for smooth fadeout

        screen.fill((0, 0, 0, 0))

        #Background image
        screen.blit(BackgroundIMG, (0,0))
        
        # Draw the health bar
        health_bar_width = 200
        health_bar_height = 20
        health_bar_x = 20
        health_bar_y = 20
        health_bar_border_color = (255, 255, 255)
        health_bar_fill_color = (255, 0, 0)

        # Draw the border of the health bar
        pygame.draw.rect(screen, health_bar_border_color, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)

        # Calculate the width of the filled portion based on PlayerHealth
        filled_width = int((EnemyHealth / 10) * health_bar_width)

        # Draw the filled portion of the health bar
        pygame.draw.rect(screen, health_bar_fill_color, (health_bar_x, health_bar_y, filled_width, health_bar_height))
        
        # Add "Enemy HP" text with an outline below the health bar
        font = pygame.font.Font(None, 36)  # Font size 36

        # Render the outline by drawing the text multiple times with a slight offset
        outline_color = (0, 0, 0)  # Black outline
        enemy_hp_text_outline = font.render("Enemy HP", True, outline_color)
        for offset_x, offset_y in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Offsets for the outline
            outline_rect = enemy_hp_text_outline.get_rect(center=(health_bar_x + health_bar_width // 2 + offset_x, health_bar_y + health_bar_height + 20 + offset_y))
            screen.blit(enemy_hp_text_outline, outline_rect)

        # Render the main text on top of the outline
        text_color = (255, 255, 255)  # White text
        enemy_hp_text = font.render("Enemy HP", True, text_color)
        enemy_hp_text_rect = enemy_hp_text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y + health_bar_height + 20))
        screen.blit(enemy_hp_text, enemy_hp_text_rect)
        
        # Draw the circle for the EnemyIcon
        circle_x = health_bar_x + health_bar_width + 40  # Position next to the health bar
        circle_y = health_bar_y + health_bar_height // 2
        circle_radius = 25
        circle_color = (255, 255, 255)

        pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)

        # Create a circular mask for the EnemyIcon
        icon_surface = pygame.Surface((circle_diameter, circle_diameter), pygame.SRCALPHA)
        pygame.draw.circle(icon_surface, (255, 255, 255, 255), (circle_radius, circle_radius), circle_radius)
        icon_surface.blit(EnemyIcon, (circle_radius - new_width // 2 + 18, circle_radius - new_height // 2), special_flags=pygame.BLEND_RGBA_MIN)

        # Blit the masked EnemyIcon onto the screen
        screen.blit(icon_surface, (circle_x - circle_radius, circle_y - circle_radius))

        #Enemy images
        if EnemyAttackWindUp:
            screen.blit(EnemyAttackWindUpIMG, (EnemyAttackWindUp_x, EnemyAttackWindUp_y))
        elif EnemyAttacking:
            if current_time - EnemyAttackLast_update > animation_speed:
                EnemyAttackFrame_index = (EnemyAttackFrame_index + 1) % len(EnemyPunchGIF)
                EnemyAttackLast_update = current_time
            screen.blit(EnemyAttackIMG, (EnemyAttack_x, EnemyAttack_y))
            if playerDamaged:
                screen.blit(EnemyPunchGIF[EnemyAttackFrame_index], (EnemyPunchEffect_x, EnemyPunchEffect_y))
                if current_time - EnemyPunchGIF_start_time > EnemyAttackGIF_duration:
                    playerDamaged = False
        elif EnemyBlocking:
            screen.blit(EnemyBlockIMG, (EnemyBlocking_x, EnemyBlocking_y))
        else:
            screen.blit(EnemyIdleIMG, (EnemyIdle_x, EnemyIdle_y))
            

        #Player images
        if punching:
            if EnemyBlocking:
                if current_time - BlockLast_update > animation_speed:
                    BlockFrame_index = (BlockFrame_index + 1) % len(BlockGIF)
                    BlockLast_update = current_time
                screen.blit(BlockGIF[BlockFrame_index], (BlockGIF_x, BlockGIF_y))
                screen.blit(PlayerPunchIMG, (punch_x, punch_y))
            else:
                if current_time - PlayerAttackLast_update > animation_speed:
                    PlayerAttackFrame_index = (PlayerAttackFrame_index + 1) % len(PlayerPunchGIF)
                    PlayerAttackLast_update = current_time
                screen.blit(PlayerPunchGIF[PlayerAttackFrame_index], (PunchEffect_x, PunchEffect_y))
                screen.blit(PlayerPunchIMG, (punch_x, punch_y))
        elif blocking:
            screen.blit(PlayerBlockIMG, (block_x, block_y))
        else:
            screen.blit(PlayerIdleIMG, (idle_x, idle_y))

        if EnemyAttacking and blocking:
            if current_time - BlockLast_update > animation_speed:
                BlockFrame_index = (BlockFrame_index + 1) % len(BlockGIF)
                BlockLast_update = current_time
            screen.blit(BlockGIF[BlockFrame_index], (BlockGIF_x, BlockGIF_y))
            screen.blit(PlayerBlockIMG, (block_x, block_y))


        #Health effects
        if PlayerHealth < 3:
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            intensity = int(150 * (1 - (PlayerHealth / 3)))
            overlay.fill((255, 0, 0, intensity))
            screen.blit(overlay, (0, 0))

        #Game Over
    elif GameOver:
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
                
    elif Victory:
        # The "You Win!" text
        font = pygame.font.Font(None, 72)
        text = font.render("You Win!!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width//2, screen_height//2 - 100))
        screen.blit(text, text_rect)

        # Continue Button
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        button_y = screen_height // 2 - 10
        button_color = (255, 255, 255)
        button_text_color = (0, 0, 0)

        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 36)
        button_text = font.render("Continue", True, button_text_color)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
        screen.blit(button_text, text_rect)

        # Mouse position tracking
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        hover_color = (200, 200, 200)
        click_color = (150, 150, 150)

        # Continue button function
        continue_hover = button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height
        continue_click = continue_hover and mouse_pressed[0]
        continue_display_color = click_color if continue_click else hover_color if continue_hover else button_color

        pygame.draw.rect(screen, continue_display_color, (button_x, button_y, button_width, button_height))
        button_text = font.render("Continue", True, button_text_color)
        text_rect = button_text.get_rect(center=(button_x + button_width//2, button_y + button_height//2))
        screen.blit(button_text, text_rect)

        if continue_click:
            pygame.quit()
            subprocess.run(["python", "level2.py"])
            sys.exit()
        
        # Return to Main Menu Button
        menu_button_y = button_y + button_height + 20
        pygame.draw.rect(screen, button_color, (button_x, menu_button_y, button_width, button_height))
        menu_text = font.render("Main Menu", True, button_text_color)
        menu_text_rect = menu_text.get_rect(center=(button_x + button_width//2, menu_button_y + button_height//2))
        screen.blit(menu_text, menu_text_rect)

        menu_hover = button_x <= mouse_x <= button_x + button_width and menu_button_y <= mouse_y <= menu_button_y + button_height
        menu_click = menu_hover and mouse_pressed[0]
        menu_display_color = click_color if menu_click else hover_color if menu_hover else button_color

        pygame.draw.rect(screen, menu_display_color, (button_x, menu_button_y, button_width, button_height))
        menu_text = font.render("Main Menu", True, button_text_color)
        menu_text_rect = menu_text.get_rect(center=(button_x + button_width//2, menu_button_y + button_height//2))
        screen.blit(menu_text, menu_text_rect)

        if menu_click:
            pygame.quit()
            subprocess.run(["python", "Main_Menu.py"])  # Return to Main_Menu.py
            sys.exit()
    pygame.display.flip()
    clock.tick(60)
