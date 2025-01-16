import pygame
from ..components.deck import Deck
from ..components.button import Button
from ..utils.constraints import *
from ..components.player_deck import PlayerDeck


def game_screen(window_surface, settings) -> str:
    """
    Main game screen for playing blackjack
    :param window_surface: The surface used to render the game
    :param settings: The game settings (player count, rounds and stake)
    :return: The next screen to display
    """
    game_font = pygame.font.SysFont(None, 36)

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

    # Game buttons
    hit_button = Button(HIT_BTN_X, GAME_BTN_Y, GAME_INPUT_WIDTH, GAME_INPUT_HEIGHT, BLUE, "Hit")
    stand_button = Button(STAND_BTN_X, GAME_BTN_Y, GAME_INPUT_WIDTH, GAME_INPUT_HEIGHT, RED, "Stand")
    next_round_button = Button(MENU_INPUT_X, NEXT_ROUND_BTN_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, GREEN, "Next Round")
    next_button = Button(MENU_INPUT_X, NEXT_ROUND_BTN_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, GREEN, "Next")
    end_game_button = Button(MENU_INPUT_X, NEXT_ROUND_BTN_Y, MENU_INPUT_WIDTH, MENU_INPUT_HEIGHT, RED, "End Game")

    game_round = 1
    turn = 0
    next_button_clicked = False

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
                    elif turn == settings.num_players:
                        # Draw for dealer
                        dealer.add_card(deck)
                        if dealer.is_bust or dealer.total >= 17:
                            turn += 1
                if stand_button.is_clicked(event.pos) and turn < settings.num_players:
                    turn += 1
                # if end of current round but not final overall round, enable next round
                if next_round_button.is_clicked(
                        event.pos) and turn > settings.num_players + 1 and game_round < settings.num_rounds:
                    # End game if all rounds are played
                    # Clear all player and dealer cards
                    for player in players:
                        player.clear()
                    dealer.clear()
                    deck.reset()
                    dealer.add_card(deck)
                    for player in players:
                        player.add_first_cards(deck)
                    game_round += 1
                    turn = 0
                elif next_button.is_clicked(
                        event.pos) and turn > settings.num_players + 1 and game_round == settings.num_rounds and \
                        not next_button_clicked:
                    next_button_clicked = True
                elif end_game_button.is_clicked(event.pos) and next_button_clicked:
                    return "title_screen"

        # Draw the game screen
        window_surface.fill((32, 128, 32))  # Green background

        # Display game settings
        settings_text = (
            f"Round {game_round}/{settings.num_rounds}  Stake: {settings.stake}"
        )
        text_surface = game_font.render(settings_text, True, WHITE)
        window_surface.blit(text_surface, (20, 20))

        # Display turn in top right corner
        turn_text = ("Dealer" if turn >= settings.num_players else f"Player {turn + 1}") + "'s turn"
        text_surface = game_font.render(turn_text, True, WHITE)
        window_surface.blit(text_surface, (WINDOW_WIDTH - 200, 20))

        # Draw the buttons
        hit_button.draw(window_surface)
        if turn < settings.num_players:
            stand_button.draw(window_surface)

            # If player draws a natural blackjack, move to the next player
            if players[turn].total == 21:
                turn += 1

        # Draw dealer
        text_surface = game_font.render("Dealer", True, WHITE)
        window_surface.blit(text_surface, (5, 125))

        # Draw dealer score
        text_surface = game_font.render(f"Score: {dealer.total}", True, WHITE)
        window_surface.blit(text_surface, (5, 145))

        # Draw dealer deck
        dealer.draw(window_surface, 0)

        # Draw players
        for i, player in enumerate(players):

            text_surface = game_font.render(f"Player {i + 1}", True, WHITE)
            window_surface.blit(text_surface, (5, 275 + i * 150))

            # Draw player score
            text_surface = game_font.render(f"Score: {player.total}", True, WHITE)
            window_surface.blit(text_surface, (5, 300 + i * 150))

            # Draw player status
            bust_colour = RED if player.is_bust else WHITE
            text_surface = game_font.render(f"Bust: {player.is_bust}", True, bust_colour)
            window_surface.blit(text_surface, (5, 325 + i * 150))

            # Draw player money
            # Using dollars instead of pounds as the £ symbol looks bad in pygame :P
            text_surface = game_font.render(f"{format_money(player.money)}", True, GOLD)
            window_surface.blit(text_surface, (5, 350 + i * 150))

            # Draw player deck (+1 as dealer is drawn first)
            player.draw(window_surface, i + 1)

        # Check if all players/dealer have played and handle the game ending
        if turn > settings.num_players:
            # Round is finished, find the winners and increment the turn so its only called once
            if turn == settings.num_players + 1:
                winners = find_winners(dealer, players, settings.stake)
                turn += 1

            # Draw the end screen
            if next_button_clicked:
                draw_game_end_screen(window_surface, players)
            else:
                draw_round_end_screen(window_surface, winners)

            # The next button is triggered by a boolean as it is in the same position as the next round button
            # Using a boolean makes the logic for displaying much simpler
            if game_round == settings.num_rounds:
                if next_button_clicked:
                    end_game_button.draw(window_surface)
                else:
                    next_button.draw(window_surface)
            else:
                next_round_button.draw(window_surface)

        pygame.display.update()


def find_winners(dealer: PlayerDeck, players: [PlayerDeck], stake: int) -> [PlayerDeck]:
    """
    Find the winners of the round and update their money
    :param dealer: The dealer's deck
    :param players: The list of player decks
    :param stake: The stake for the round
    :return: The list of winners
    """
    winners = []
    # If dealer is bust, all non-bust players win
    if dealer.is_bust:
        for player in players:
            if not player.is_bust:
                winners.append(player)
    else:
        # Dealer is not bust
        for player in players:
            # Check if player is not bust and has a higher score than the dealer
            if not player.is_bust and player.total > dealer.total:
                winners.append(player)
            # if both player and dealer have 21, player with natural blackjack wins, else no winner
            elif player.total == dealer.total == 21:
                if player.natural_blackjack() and not dealer.natural_blackjack():
                    winners.append(player)
                # If both get a natural blackjack, it's a tie, so no winner
                elif player.natural_blackjack() and dealer.natural_blackjack():
                    pass
                # Don't declare the dealer as the winner yet, as there might be other players with a natural blackjack

    # If none of the above scenarios have happened, the dealer wins
    if not winners:
        winners.append(dealer)

    # Calculate payouts - Dealer can be whatever as their money is not displayed
    for player in players:
        if player in winners:
            # Natural blackjack pays 1.5x the stake, normal win pays 2x the stake
            if player.natural_blackjack():
                player.money += stake * 1.5
            else:
                player.money += stake * 2
        else:
            # For a tie, the player gets their stake back (no change)
            if player.total == dealer.total and not player.is_bust:
                pass
            # If not a win or tie, then player loses their stake
            else:
                player.money -= stake

    return winners


def draw_round_end_screen(surface, winners: [PlayerDeck]):
    """
    Draw the end screen for a round
    :param surface: The surface to draw the end screen on
    :param winners: The list of winners
    """
    game_font = pygame.font.SysFont(None, 36)
    pygame.draw.rect(surface, LIGHT_GRAY, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT))
    pygame.draw.rect(surface, BLACK, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT), 6)
    # text surface should be winners if len(winners) > 1
    if len(winners) == 1:
        text_surface = game_font.render("Winner:", True, BLACK)
    else:
        text_surface = game_font.render("Winners:", True, BLACK)
    surface.blit(text_surface, (END_SCREEN_X + 10, END_SCREEN_Y + 10))
    for i, winner in enumerate(winners):
        if winner.id == -1:
            # Dealer's id is -1
            text_surface = game_font.render("Dealer", True, BLACK)
        else:
            text_surface = game_font.render(f"Player {winner.id + 1}", True, BLACK)
        surface.blit(text_surface, (END_SCREEN_X + 10, END_SCREEN_Y + 35 + i * 25))


def draw_game_end_screen(surface, players: [PlayerDeck]):
    """
    Draw the end screen for the game, including how much money each player has
    :param surface: The surface to draw the end screen on
    :param players: The list of all players
    """
    game_font = pygame.font.SysFont(None, 36)
    pygame.draw.rect(surface, LIGHT_GRAY, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT))
    pygame.draw.rect(surface, BLACK, (END_SCREEN_X, END_SCREEN_Y, END_SCREEN_WIDTH, END_SCREEN_HEIGHT), 6)

    text_surface = game_font.render("Final results:", True, BLACK)
    surface.blit(text_surface, (END_SCREEN_X + 10, END_SCREEN_Y + 10))

    for i, player in enumerate(players):
        text_surface = game_font.render(f"Player {player.id + 1}: {format_money(player.money)}", True, BLACK)
        surface.blit(text_surface, (END_SCREEN_X + 10, END_SCREEN_Y + 35 + i * 25))


def format_money(money) -> str:
    """
    Format the money as a string with a dollar sign and two decimal places for cents (e.g. $10.00)
    $ is used over £ as the £ symbol looks bad in pygame
    :param money: The money to format
    :return: The formatted money string
    """
    if money < 0:
        return f"-${format(-money, '.2f')}"
    else:
        return f"${format(money, '.2f')}"
