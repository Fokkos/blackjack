"""
This file contains all the constants used in the game, making it easier to change the values of these constants in one
place and keep a consistent and clean style and theme.
"""

# Colours used for inputs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DROPDOWN_COLOUR = (180, 180, 255)
BLUE = (37, 122, 253)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
BLUE = (0, 140, 186)
GREEN = (0, 255, 51)

# Other constants (e.g., window dimensions, font sizes)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Menu input box dimensions and position
MENU_INPUT_WIDTH = 300
MENU_INPUT_HEIGHT = 50
MENU_INPUT_X = (WINDOW_WIDTH // 2) - (MENU_INPUT_WIDTH // 2)
MENU_INPUT_Y = 200
MENU_INPUT_X_SPACING = 50
MENU_INPUT_X_START = (WINDOW_WIDTH // 2) - (MENU_INPUT_WIDTH * 3 // 2) - MENU_INPUT_X_SPACING
START_BTN_Y = 500

# GAME BUTTONS
GAME_INPUT_SPACING = 20
GAME_INPUT_WIDTH = 200
GAME_INPUT_HEIGHT = 50
HIT_BTN_X = MENU_INPUT_X
STAND_BTN_X = HIT_BTN_X + GAME_INPUT_WIDTH + GAME_INPUT_SPACING
GAME_BTN_Y = 10

# End screen dimensions and position
END_SCREEN_WIDTH = 600
END_SCREEN_HEIGHT = 200
END_SCREEN_X = WINDOW_WIDTH / 2 - END_SCREEN_WIDTH / 2
END_SCREEN_Y = 200
NEXT_ROUND_BTN_Y = END_SCREEN_Y + END_SCREEN_HEIGHT - 20 - MENU_INPUT_HEIGHT

# Card dimensions
CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_SPACING_X = 63
CARD_SPACING_Y = 4
FIRST_CARD_X = 150
FIRST_CARD_Y = 100
