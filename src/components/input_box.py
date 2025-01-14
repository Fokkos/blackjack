import pygame
from ..utils.constraints import GRAY, BLACK, BLUE, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, MENU_INPUT_Y


class InputBox:
    def __init__(self, x, placeholder=""):
        self.rect = pygame.Rect(x, MENU_INPUT_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT)
        self.font = pygame.font.SysFont(None, 36)
        self.color = GRAY
        self.text = '1'
        self.placeholder = placeholder
        self.active = False

        # Adjust the height of the placeholder text to be above the box
        self.placeholder_rect = pygame.Rect(self.rect.x, self.rect.y - 25, self.rect.width, 20)

    def draw(self, surface):
        # Draw the placeholder above the input box
        placeholder_surface = self.font.render(self.placeholder, True, BLACK)
        surface.blit(placeholder_surface, (self.placeholder_rect.x + 10, self.placeholder_rect.y))

        # Draw the input box
        pygame.draw.rect(surface, self.color, self.rect, 2)

        # If there is text, draw it inside the box, otherwise display the placeholder text inside the box
        text_surface = self.font.render(self.text if self.text else "", True, BLACK)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
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
                if event.unicode.isdigit():
                    self.text += event.unicode
