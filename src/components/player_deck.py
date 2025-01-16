import pygame

from .deck import Deck
from ..utils.constraints import CARD_SPACING_X, CARD_SPACING_Y, FIRST_CARD_X, FIRST_CARD_Y, CARD_HEIGHT


class PlayerDeck:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.total = 0
        self.is_bust = False
        self.money = 0

    def add_card(self, deck: Deck):
        """
        Add a single card to the player's deck, updating the total and bust status
        :param deck: The deck to deal the card from
        """
        dealt_card = deck.deal_card()
        self.cards.append(dealt_card)
        self.total += dealt_card.value(self.total)
        if self.total > 21:
            self.is_bust = True

    def add_first_cards(self, deck: Deck):
        """
        Add the first two cards to the player's deck, done at the start of a round
        :param deck: The deck to deal the cards from
        """
        self.add_card(deck)
        self.add_card(deck)

    def natural_blackjack(self) -> bool:
        """
        Check if the player has a natural blackjack (21 with 2 cards)
        :return: True if the player has a natural blackjack, False otherwise
        """
        return self.total == 21 and len(self.cards) == 2

    def draw(self, surface, y):
        """
        Draw the player's deck on the surface
        :param surface: The surface to draw the deck on
        :param y: The row of the player (i.e. what order they are in, starting from 0 for the dealer)
        """
        for x, card in enumerate(self.cards):
            card.draw(surface, FIRST_CARD_X + x * CARD_SPACING_X, FIRST_CARD_Y + y * (CARD_HEIGHT + CARD_SPACING_Y))

    def clear(self):
        """
        Clear the player's deck and reset their total and bust status for start of new round
        """
        self.cards = []
        self.total = 0
        self.is_bust = False
