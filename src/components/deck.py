import random
from .card import Card


class Deck:
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        # Create a deck of 52 cards
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    # Shuffle the deck to ensure randomness on each session
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal the top card from the deck and remove it from the deck
    # TODO deal with empty deck
    def deal_card(self) -> Card:
        return self.cards.pop()

    def reset(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def custom_deck(self, cards):
        self.cards = cards

    # Debug string to print out all the cards in the deck
    def __repr__(self) -> str:
        return ', '.join(str(card) for card in self.cards)