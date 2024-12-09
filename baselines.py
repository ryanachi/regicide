# import random
from card import Suit
from rng import rng


# Random choice
def random_choice(castle, tavern, discard, player, opp_card):
    print(list(player.hand))
    return rng.choice(list(player.hand))

# Always play highest card
def highest_card(castle, tavern, discard, player, opp_card):
    return max([(card.attack, card) for card in player.hand], key=lambda tup: tup[0])[1]

# Always play lowest card
def lowest_card(castle, tavern, discard, player, opp_card):
    return min([(card.attack, card) for card in player.hand], key=lambda tup: tup[0])[1]

# Choose all diamonds, clubs, hearts, spades (highest to lowest)
def suit_order(castle, tavern, discard, player, opp_card):
    suit_to_priority = {
        Suit.SPADE : 4,
        Suit.DIAMOND: 3,
        Suit.CLUB : 2,
        Suit.HEART : 1
    }

    return max([(suit_to_priority[card.suit], card.rank, card) for card in player.hand], key=lambda tup: (tup[0], tup[1]))[2]