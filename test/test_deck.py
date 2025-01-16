import unittest
import sys
from src.components import Deck, PlayerDeck, Card
sys.path.append("..") # Adds higher directory to python modules path.


class DeckTestCase(unittest.TestCase):

    def setUp(self):  # this method will be run before each test
        self.deck = Deck()
        self.deck.shuffle()

    def tearDown(self):  # this method will be run after each test
        pass

    def test_number_of_cards(self):  # any method beginning with 'test_' will be run by unittest
        number_of_cards = len(self.deck.cards)
        self.assertEqual(number_of_cards, 52)

    """
    Given I play a game of blackjack
    When I am dealt my opening hand
    Then I have two cards
    """
    def test_opening_hand(self):
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)
        number_of_cards = len(player.cards)
        self.assertEqual(number_of_cards, 2)

    """
    Given I have a valid hand of cards
    When I choose to ‘hit’
    Then I receive another card
    And my score is updated
    """
    def test_hit(self):
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)
        opening_score = player.total
        player.add_card(self.deck)
        number_of_cards = len(player.cards)
        # one more card is added
        self.assertEqual(number_of_cards, 3)
        # score is updated
        self.assertNotEqual(opening_score, player.total)

    """
    Given I have a valid hand of cards
    When I choose to ‘stand’
    Then I receive no further cards
    And my score is evaluated
    """
    # The stand functionality is done in the Pygame UI, so we can't test it here. It has been manually tested to work :)

    """
    Given my score is updated or evaluated
    When it is 21 or less
    Then I have a valid hand
    """
    # The players opening hand will ALWAYS be 21 or under
    def test_valid_hand_under_or_equal_to_21(self):
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)
        self.assertLessEqual(player.total, 21)
        self.assertFalse(player.is_bust)

    # Also do it by manually adding cards to the player deck
    def test_valid_hand_under_or_equal_to_21_manually(self):
        # Create custom deck for guaranteed right cards (7 + 3 + Queen = 20)
        sevenOfHearts = Card("7", "Hearts")
        threeOfHearts = Card("3", "Hearts")
        queenOfHearts = Card("Queen", "Hearts")
        self.deck.custom_deck([sevenOfHearts, threeOfHearts, queenOfHearts])

        # Initialise player
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)
        initial_total = player.total

        # Add third card
        player.add_card(self.deck)

        # Check that score has been updated
        self.assertNotEqual(player.total, initial_total)
        # Check that score is still under 21
        self.assertLessEqual(player.total, 21)
        # Check that hand is valid (not bust)
        self.assertFalse(player.is_bust)

    """
    Given my score is updated
    When it is 22 or more 
    Then I am ‘bust’ and do not have a valid hand
    """
    # This test is done by manually adding cards to the player deck that total over 21 (e.g. 9 + King + 3 = 22)
    def test_bust_hand_over_21(self):
        # Create custom deck for guaranteed right cards (9 + King + 3 = 22)
        nineOfHearts = Card("9", "Hearts")
        kingOfHearts = Card("King", "Hearts")
        threeOfHearts = Card("3", "Hearts")
        self.deck.custom_deck([nineOfHearts, kingOfHearts, threeOfHearts])

        # Initialise player
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)
        initial_total = player.total

        # Add third card
        player.add_card(self.deck)

        # Check that score has been updated
        self.assertNotEqual(player.total, initial_total)
        # Check that score is over 21
        self.assertGreater(player.total, 21)
        # Check that hand is invalid (bust)
        self.assertTrue(player.is_bust)

    """
    Given I have a king and an ace
    When my score is evaluated
    Then my score is 21
    """
    def test_natural_blackjack(self):
        # Create custom deck for guaranteed right cards (King + Ace = 21)
        kingOfHearts = Card("King", "Hearts")
        aceOfHearts = Card("Ace", "Hearts")
        self.deck.custom_deck([kingOfHearts, aceOfHearts])

        # Initialise player
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)

        # Check that score is 21
        self.assertEqual(player.total, 21)
        # Check that hand is valid (not bust)
        self.assertFalse(player.is_bust)

    """
    Given I have a king, a queen, and an ace
    When my score is evaluated
    Then my score is 21
    """
    def test_ace_evaluating_to_one(self):
        # Create custom deck for guaranteed right cards (King + Queen + Ace = 21)
        kingOfHearts = Card("King", "Hearts")
        queenOfHearts = Card("Queen", "Hearts")
        aceOfHearts = Card("Ace", "Hearts")

        # Ordering is reversed as drawing cards works by popping the array (last card is first card drawn)
        # This means that the ace will be drawn last and have a value of 1
        self.deck.custom_deck([aceOfHearts, queenOfHearts, kingOfHearts])

        # Initialise player
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)

        # Add third card
        player.add_card(self.deck)

        # Check that score is 21
        self.assertEqual(player.total, 21)
        # Check that hand is valid (not bust)
        self.assertFalse(player.is_bust)

    """
    Given that I have a nine, an ace, and another ace
    When my score is evaluated
    Then my score is 21
    """
    def test_dynamic_ace_value(self):
        # Create custom deck for guaranteed right cards (9 + Ace + Ace = 21)
        nineOfHearts = Card("9", "Hearts")
        aceOfHearts = Card("Ace", "Hearts")
        aceOfSpades = Card("Ace", "Spades")
        self.deck.custom_deck([aceOfSpades, aceOfHearts, nineOfHearts])

        # Initialise player
        player = PlayerDeck(0)
        player.add_first_cards(self.deck)

        # Add third card
        player.add_card(self.deck)

        # Check that score is 21
        self.assertEqual(player.total, 21)
        # Check that hand is valid (not bust)
        self.assertFalse(player.is_bust)


if __name__ == '__main__':
    unittest.main()
