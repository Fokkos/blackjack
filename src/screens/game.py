import pygame
from ..utils.constraints import WHITE
from ..components.deck import Deck
from ..components.button import Button
from ..utils.constraints import MENU_INPUT_X, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, WINDOW_WIDTH
from ..components.player_deck import PlayerDeck

def game_screen(window_surface, settings):
    # Create a shuffled deck
    deck = Deck()
    deck.shuffle()

    # Draw first card for dealer
    dealer = PlayerDeck(-1)
    dealer.add_card(deck)

    # Initialise player cards
    players = []
    for i in range(settings.num_players):
        player_deck = PlayerDeck(i)
        player_deck.add_first_cards(deck)
        players.append(player_deck)

    hit_button = Button(MENU_INPUT_X, 10, 200, MENU_INPUT_HEIGHT, pygame.Color('#008CBA'), "Hit")
    stand_button = Button(MENU_INPUT_X + 220, 10, 200, MENU_INPUT_HEIGHT, pygame.Color('#AA0033'), "Stand")

    # TODO deal with player drawing 21 initially
    turn = 0

    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit game
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hit_button.is_clicked(event.pos):
                    if turn < settings.num_players:
                        # Draw for players
                        players[turn].add_card(deck)
                        if players[turn].bust or players[turn].total == 21:
                            turn += 1
                    else:
                        # Draw for dealer
                        dealer.add_card(deck)
                        if dealer.bust or dealer.total >= 17:
                            turn += 1
                if stand_button.is_clicked(event.pos) and turn < settings.num_players:
                    turn += 1

        # Draw the game screen
        window_surface.fill((32, 128, 32))  # Green background

        # Display game settings
        font = pygame.font.SysFont(None, 36)
        settings_text = (
            f"Players: {settings.num_players}, Rounds: {settings.num_rounds}, Ace Value: {settings.ace_value}"
        )
        text_surface = font.render(settings_text, True, WHITE)
        window_surface.blit(text_surface, (20, 20))

        # Display turn in top right corner
        turn_text = ("Dealer" if turn >= settings.num_players else f"Player {turn + 1}") + "'s turn"
        text_surface = font.render(turn_text, True, WHITE)
        window_surface.blit(text_surface, (WINDOW_WIDTH - 200, 20))

        # Draw the buttons
        hit_button.draw(window_surface)
        if turn < settings.num_players:
            stand_button.draw(window_surface)

        # Draw dealer
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render("Dealer", True, WHITE)
        window_surface.blit(text_surface, (5, 125))

        # Draw dealer score
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(f"Score: {dealer.total}", True, WHITE)
        window_surface.blit(text_surface, (5, 145))

        # Draw dealer deck
        for j, card in enumerate(dealer.cards):
            card.draw(window_surface, 150 + j * 120, 110)

        # Draw players
        for i, player in enumerate(players):
            # Draw player id
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(f"Player {i + 1}", True, WHITE)
            window_surface.blit(text_surface, (5, 275 + i * 150))

            # Draw player score
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(f"Score: {player.total}", True, WHITE)
            window_surface.blit(text_surface, (5, 295 + i * 150))

            # Draw player status
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(f"Bust: {player.bust}", True, WHITE)
            window_surface.blit(text_surface, (5, 315 + i * 150))

            # Draw player deck
            for j, card in enumerate(player.cards):
                card.draw(window_surface, 150 + j * 120, 260 + i * 150)

        # Check if all players/dealer have played and handle the game ending
        if turn > settings.num_players:
            # TODO Add endgame logic
            # TODO for now when the game ends, it just displays GAME OVER
            font = pygame.font.SysFont(None, 72)
            text_surface = font.render("Game Over", True, ('#FF0000'))
            window_surface.blit(text_surface, (WINDOW_WIDTH // 2 - 150, 20))


        pygame.display.update()