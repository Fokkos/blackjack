import pygame
from ..utils.constraints import WHITE, BLACK, CARD_WIDTH, CARD_HEIGHT


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self, total):
        """
        Get the value of the card based on the total of the player's hand
        :param total: the total before adding the card (to account for aces)
        :return: The value of the card
        """
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        # Value of ace is 11 or 1 depending on if it would bust the player
        elif self.rank == 'Ace':
            if total + 11 > 21:
                return 1
            else:
                return 11
        else:
            return int(self.rank)

    def draw(self, surface, x, y):
        """
        Draw the card on the surface
        :param surface: Surface to draw the card on
        :param x: x-coordinate of the card (top left corner)
        :param y: y-coordinate of the card (top left corner)
        """
        # Draw card
        pygame.draw.rect(surface, WHITE, (x, y, CARD_WIDTH, CARD_HEIGHT))
        pygame.draw.rect(surface, BLACK, (x, y, CARD_WIDTH, CARD_HEIGHT), 2)
        # Draw text in top left
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.rank, True, BLACK)
        surface.blit(text, (x + 10, y + 10))
        # Prepare suit image
        suit_image = pygame.image.load(f"img/{self.suit.lower()}.jpg")
        suit_image = pygame.transform.scale(suit_image, (30, 30))
        # Draw suit image in top right and bottom left corner
        surface.blit(suit_image, (x + 65, y + 5))
        surface.blit(suit_image, (x + 5, y + 115))

    # Debug string to print out the card
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
