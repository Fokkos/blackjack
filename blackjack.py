from src.utils.constraints import *
from src.screens.title import title_screen
from src.screens.game import game_screen
from src.utils.settings import Settings
import pygame


def play():
    # Load game settings
    settings = Settings()

    pygame.init()
    pygame.display.set_caption('Blackjack')
    window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Screen state
    current_screen = "title_screen"

    while True:
        if current_screen == "title_screen":
            current_screen = title_screen(window_surface, settings)
        elif current_screen == "game_screen":
            current_screen = game_screen(window_surface, settings)
        else:
            break  # Exit game

if __name__ == '__main__':
    play()
