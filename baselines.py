import random
from card import Suit

# Random choice
def random_choice(castle, tavern, discard, player, opp_card):
    return random.choice(player.hand)

# Always play highest card
def highest_card(castle, tavern, discard, player, opp_card):
    highest_card = None
    for card in player.hand:
        if highest_card == None or card.attack > highest_card.attack:
            highest_card = card

    return highest_card

# Always play lowest card
def lowest_card(castle, tavern, discard, player, opp_card):
    lowest_card = None
    for card in player.hand:
        if lowest_card == None or card.attack > lowest_card.attack:
            lowest_card = card

    return lowest_card

# Choose all diamonds, clubs, hearts, spades (highest to lowest)
def suit_order(castle, tavern, discard, player, opp_card):
    curr_card = None
    curr_suit = None
    for card in player.hand:
        card_suit = card.suit
        if curr_card == None or (Suit.card_suit.value > Suit.curr_suit.value and card.attack > curr_card.attack):
            curr_card = card
            curr_suit = card_suit

    return curr_card