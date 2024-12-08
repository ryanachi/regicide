import random
from card import Suit

# Random choice
def random_choice(castle, tavern, discard, player, opp_card):
    print(list(player.hand))
    return random.choice(list(player.hand))

# Always play highest card
def highest_card(castle, tavern, discard, player, opp_card):
    return max([(card.attack, card) for card in player.hand], key=lambda tup: tup[0])[1]

# Always play lowest card
def lowest_card(castle, tavern, discard, player, opp_card):
    return min([(card.attack, card) for card in player.hand], key=lambda tup: tup[0])[1]

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