import pygame
from ..utils.constraints import GRAY, BLACK, BLUE, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, MENU_INPUT_Y


class InputBox:
    def __init__(self, x, default_value, name=""):
        self.rect = pygame.Rect(x, MENU_INPUT_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT)
        self.font = pygame.font.SysFont(None, 36)
        self.color = GRAY
        self.text = default_value
        self.name = name
        self.name_rect = pygame.Rect(self.rect.x, self.rect.y - 25, self.rect.width, 20)
        self.active = False

    def draw(self, surface):
        """
        Draw the input box on the surface, including the name of the input box above it
        :param surface: The surface to draw the input box on
        """
        # Draw the name above the input box
        name_surface = self.font.render(self.name, True, BLACK)
        surface.blit(name_surface, (self.name_rect.x + 10, self.name_rect.y))

        # Draw the input box
        pygame.draw.rect(surface, self.color, self.rect, 2)

        # If there is text, draw it inside the box
        text_surface = self.font.render(self.text if self.text else "", True, BLACK)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        """
        Handle events for the input box, including mouse clicks and key presses for entering numbers
        :param event: The event to handle
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = BLUE
            else:
                self.active = False
                self.color = GRAY

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                # Handle return press if needed
                pass
            else:
                # Only allow digits to be entered
                if event.unicode.isdigit():
                    self.text += event.unicode
