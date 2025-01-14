import pygame
from ..utils.constraints import DROPDOWN_COLOUR, GRAY, BLACK, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, MENU_INPUT_Y

class Dropdown:

    def __init__(self, x, options, title):
        self.rect = pygame.Rect(x, MENU_INPUT_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT)
        self.font = pygame.font.SysFont(None, 36)
        self.options = options
        self.is_open = False
        self.selected_option = options[0] if options else None
        self.option_rects = []

        self.title = title
        self.title_rect = pygame.Rect(self.rect.x, self.rect.y - 25, self.rect.width, 20)

    def draw(self, surface):
        # Draw the placeholder above the input box
        title_surface = self.font.render(self.title, True, BLACK)
        surface.blit(title_surface, (self.title_rect.x + 10, self.title_rect.y))

        # Reset the option_rects list each time the dropdown is drawn
        self.option_rects = []

        # Draw the dropdown box
        pygame.draw.rect(surface, DROPDOWN_COLOUR, self.rect)
        text_surface = self.font.render(self.selected_option if self.selected_option else "", True, BLACK)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

        if self.is_open:
            # Draw the options if the dropdown is open
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * MENU_INPUT_HEIGHT, self.rect.width, MENU_INPUT_HEIGHT)
                self.option_rects.append(option_rect)
                pygame.draw.rect(surface, GRAY, option_rect)
                text_surface = self.font.render(option, True, BLACK)
                surface.blit(text_surface, (option_rect.x + 10, option_rect.y + 10))

    def toggle(self):
        self.is_open = not self.is_open

    def select_option(self, mouse_pos):
        for i, option_rect in enumerate(self.option_rects):
            if option_rect.collidepoint(mouse_pos):
                self.selected_option = self.options[i]
                self.is_open = False
