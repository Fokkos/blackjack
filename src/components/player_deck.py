from .deck import Deck


class PlayerDeck:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.total = 0
        self.is_bust = False
        self.money = 0

    def add_card(self, deck: Deck):
        dealt_card = deck.deal_card()
        self.cards.append(dealt_card)
        self.total += dealt_card.value(self.total)
        if self.total > 21:
            self.is_bust = True

    def add_first_cards(self, deck: Deck):
        self.add_card(deck)
        self.add_card(deck)

    def natural_blackjack(self):
        return self.total == 21 and len(self.cards) == 2

    def draw(self, surface):
        x = 50
        y = 400
        for card in self.cards:
            card.draw(surface, x, y)
            x += 120

    def clear(self):
        self.cards = []
        self.total = 0
        self.is_bust = False

