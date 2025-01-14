import random
from .card import Card


class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        # Create a deck of 52 cards
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]
        self.shuffle()

    # Shuffle the deck to ensure randomness on each session
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal the top card from the deck and remove it from the deck
    # TODO deal with empty deck
    def deal_card(self) -> Card:
        return self.cards.pop()

    # Debug string to print out all the cards in the deck
    def __repr__(self) -> str:
        return ', '.join(str(card) for card in self.cards)