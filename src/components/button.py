# Reusable button class for creating buttons in Pygame
import pygame
from ..utils.constraints import BLACK


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(None, 36)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        """
        Draw the button on the surface
        :param surface: The surface to draw the button on
        """
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 4)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos: tuple[int, int]):
        """
        Check if the button is clicked by comparing the mouse position to the button's rectangle
        :param mouse_pos: The position of the mouse (done automatically by Pygame)
        :return: True if the button is clicked, False otherwise
        """
        return self.rect.collidepoint(mouse_pos)
