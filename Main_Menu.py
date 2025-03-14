import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Marvel Boxing")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fonts
title_font = pygame.font.Font(None, 74)  # Title font
button_font = pygame.font.Font(None, 50)  # Button font

# Button dimensions
button_width = 200
button_height = 60
start_button_x = (screen_width - button_width) // 2
start_button_y = 300
exit_button_x = (screen_width - button_width) // 2
exit_button_y = 400

# Load the background image
# background_image = pygame.image.load("Images\\Background\\Main_Menu_Background.jpg")
# background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale to fit the screen

# Main menu loop
def main_menu():
    while True:
        # Draw the background image
        #screen.blit(background_image, (0, 0))

        # Draw the title
        title_text = title_font.render("Underground Arena", True, black)
        title_rect = title_text.get_rect(center=(screen_width // 2, 150))
        screen.blit(title_text, title_rect)

        # Draw the Start Game button
        pygame.draw.rect(screen, blue, (start_button_x, start_button_y, button_width, button_height))
        start_text = button_font.render("Start Game", True, white)
        start_text_rect = start_text.get_rect(center=(start_button_x + button_width // 2, start_button_y + button_height // 2))
        screen.blit(start_text, start_text_rect)

        # Draw the Exit button
        pygame.draw.rect(screen, red, (exit_button_x, exit_button_y, button_width, button_height))
        exit_text = button_font.render("Exit", True, white)
        exit_text_rect = exit_text.get_rect(center=(exit_button_x + button_width // 2, exit_button_y + button_height // 2))
        screen.blit(exit_text, exit_text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if Start Game button is clicked
                if start_button_x <= mouse_x <= start_button_x + button_width and start_button_y <= mouse_y <= start_button_y + button_height:
                    pygame.quit()
                    subprocess.run(["python", "Main.py"])  # Launch Main.py
                    sys.exit()

                # Check if Exit button is clicked
                if exit_button_x <= mouse_x <= exit_button_x + button_width and exit_button_y <= mouse_y <= exit_button_y + button_height:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Run the main menu
if __name__ == "__main__":
    main_menu()