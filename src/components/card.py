import pygame

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11   # TODO deal with Ace value of 1 or 11
        else:
            return int(self.rank)

    def draw(self, surface, x, y):
        # Draw white rectangle
        pygame.draw.rect(surface, (255, 255, 255), (x, y, 100, 150))
        # Draw black border
        pygame.draw.rect(surface, (0, 0, 0), (x, y, 100, 150), 2)
        # Draw text
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.rank, True, (0, 0, 0))
        surface.blit(text, (x + 10, y + 10))
        # Draw suit
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.suit, True, (0, 0, 0))
        surface.blit(text, (x + 10, y + 40))