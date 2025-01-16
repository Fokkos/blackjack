import pygame

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def value(self, total):
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
        # Draw white rectangle
        pygame.draw.rect(surface, (255, 255, 255), (x, y, 100, 150))
        # Draw black border
        pygame.draw.rect(surface, (0, 0, 0), (x, y, 100, 150), 2)
        # Draw text in top left and bottom right
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.rank, True, (0, 0, 0))
        surface.blit(text, (x + 10, y + 10))
        # Draw suit
        suit_image = pygame.image.load(f"img/{self.suit.lower()}.jpg")
        suit_image = pygame.transform.scale(suit_image, (30, 30))
        # Draw image in top right and bottom left corner
        surface.blit(suit_image, (x + 65, y + 5))
        surface.blit(suit_image, (x + 5, y + 115))

