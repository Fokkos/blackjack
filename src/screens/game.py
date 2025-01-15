import pygame
from ..components.deck import Deck
from ..components.button import Button
from ..utils.constraints import *
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
    next_round_button = Button(MENU_INPUT_X, NEXT_ROUND_BTN_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, pygame.Color('#00FF33'), "Next Round")

    game_round = 1
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
                        if players[turn].is_bust or players[turn].total == 21:
                            turn += 1
                    else:
                        # Draw for dealer
                        dealer.add_card(deck)
                        if dealer.is_bust or dealer.total >= 17:
                            turn += 1
                if stand_button.is_clicked(event.pos) and turn < settings.num_players:
                    turn += 1
                # if end of round, enable next round

        # Draw the game screen
        window_surface.fill((32, 128, 32))  # Green background

        # Display game settings
        font = pygame.font.SysFont(None, 36)
        settings_text = (
            f"Round {game_round}/{settings.num_rounds}"
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

            # If player draws a natural blackjack, move to the next player
            if players[turn].total == 21:
                turn += 1

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
            text_surface = font.render(f"Bust: {player.is_bust}", True, WHITE)
            window_surface.blit(text_surface, (5, 315 + i * 150))

            # Draw player deck
            for j, card in enumerate(player.cards):
                card.draw(window_surface, 150 + j * 60, 260 + i * 150)

        # Check if all players/dealer have played and handle the game ending
        if turn > settings.num_players:
            # Round is finished, find the winners and increment the turn so its only called once
            if turn == settings.num_players + 1:
                winners = find_winners(dealer, players)
                turn += 1

            # Draw the end screen
            draw_end_screen(window_surface, winners)
            next_round_button.draw(window_surface)

        pygame.display.update()


def find_winners(dealer: PlayerDeck, players: [PlayerDeck]) -> [PlayerDeck]:
    print("finding winners...")
    winners = []
    # If dealer is bust, all non-bust players win
    if dealer.is_bust:
        for player in players:
            if not player.is_bust:
                winners.append(player)
                print(f"Player {player.id + 1} wins as dealer is bust.")
    else:
        # Dealer is not bust
        for player in players:
            # Check if player is not bust and has a higher score than the dealer
            if not player.is_bust and player.total > dealer.total:
                winners.append(player)
                print(f"Player {player.id + 1} wins with a score of {player.total}.")
            # if both players have 21, player with natural blackjack wins, else no winner
            elif player.total == dealer.total == 21:
                if player.natural_blackjack() and not dealer.natural_blackjack():
                    print(f"Player {player.id + 1} wins with a natural blackjack.")
                    winners.append(player)
                # If both get a natural blackjack, it's a tie, so no winner
                elif player.natural_blackjack() and dealer.natural_blackjack():
                    pass
                # Don't declare the dealer as the winner yet, as there might be other players with a natural blackjack

    # If none of the above scenarios have happened, the dealer wins
    if not winners:
        print("No winners, so dealer wins.")
        winners.append(dealer)

    return winners


def draw_end_screen(surface, winners: [PlayerDeck]):
    pygame.draw.rect(surface, LIGHT_GRAY, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT))
    pygame.draw.rect(surface, BLACK, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT), 6)
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render("Winners:", True, BLACK)
    surface.blit(text_surface, (END_SCREEN_X + 5, END_SCREEN_Y + 5))
    for i, winner in enumerate(winners):
        if winner.id == -1:
            # Dealer's id is -1
            text_surface = font.render("Dealer", True, BLACK)
        else:
            text_surface = font.render(f"Player {winner.id + 1}", True, BLACK)
        surface.blit(text_surface, (END_SCREEN_X + 5, END_SCREEN_Y + 25 + i * 20))