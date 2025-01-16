import random
from .card import Card


class Deck:
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        # Create a deck of 52 cards
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        """
        Deal a card from the deck
        :return:
        """
        # If deck is empty, reset the deck (reshuffle)
        if len(self.cards) == 0:
            self.reset()
        return self.cards.pop()

    def reset(self):
        """
        Reset the deck to a new deck of 52 shuffled cards
        """
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def custom_deck(self, cards: [Card]):
        """
        Custom deck for testing purposes
        :param cards: List of cards to be used in the deck
        """
        self.cards = cards

    # Debug string to print out all the cards in the deck
    def __repr__(self) -> str:
        return ', '.join(str(card) for card in self.cards)
