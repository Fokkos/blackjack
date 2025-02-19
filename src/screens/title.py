import pygame
from ..utils.constraints import *
from ..components.input_box import InputBox
from ..components.dropdown import Dropdown
from ..components.button import Button
from ..utils.settings import Settings


def title_screen(window_surface, settings: Settings) -> str:
    """
    Display the title screen and handle user input for the game settings
    :param window_surface: The surface used to render the title screen
    :param settings: The game settings object to store the user input
    :return: The next screen to display
    """
    global num_players, num_rounds, ace_value

    # Load the title image
    title_image = pygame.image.load('img/logo.jpg')
    title_image = pygame.transform.scale(title_image, (WINDOW_WIDTH, 150))

    # Create UI components
    players_input = Dropdown(MENU_INPUT_X_START, ["1", "2", "3"], "Players:")
    rounds_input = InputBox(MENU_INPUT_X_START + MENU_INPUT_WIDTH + MENU_INPUT_X_SPACING, "3", "Rounds:")
    stake_input = InputBox(MENU_INPUT_X_START + (2 * (MENU_INPUT_WIDTH + MENU_INPUT_X_SPACING)), "10", "Stake:")
    start_button = Button(MENU_INPUT_X, START_BTN_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, BLUE, "Start")

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit game

            # Handle input box events
            rounds_input.handle_event(event)
            stake_input.handle_event(event)

            # Handle dropdown events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if players_input.rect.collidepoint(event.pos):
                    players_input.toggle()
                else:
                    players_input.select_option(event.pos)

            # Check if start button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_clicked(event.pos):
                    # Assign the selected values to variables
                    settings.num_players = int(players_input.selected_option) if players_input.selected_option else 2
                    settings.num_rounds = int(rounds_input.text) if rounds_input.text.isdigit() else 0
                    settings.stake = int(stake_input.text) if stake_input.text.isdigit() else 0

                    # Proceed to the game screen
                    return "game_screen"

        # Draw title screen
        window_surface.fill(WHITE)
        window_surface.blit(title_image, (0, 0))

        players_input.draw(window_surface)
        rounds_input.draw(window_surface)
        stake_input.draw(window_surface)
        start_button.draw(window_surface)

        pygame.display.update()