import pygame
from .card import Card
from .deck import Deck


class PlayerDeck:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.total = 0
        self.bust = False

    def add_card(self, deck: Deck):
        dealt_card = deck.deal_card()
        self.cards.append(dealt_card)
        self.total += dealt_card.value()
        if self.total > 21:
            self.bust = True

    def add_first_cards(self, deck: Deck):
        self.add_card(deck)
        self.add_card(deck)

    def draw(self, surface):
        x = 50
        y = 400
        for card in self.cards:
            card.draw(surface, x, y)
            x += 120

    def clear(self):
        self.cards = []
        self.total = 0