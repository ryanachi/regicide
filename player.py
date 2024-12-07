from dataclasses import dataclass

from card import Card

@dataclass
class Player():
    hand: set[Card]
    num_jokers: int

# @dataclass
# class Opp():
#     curr_card: Card
#     hidden_cards: list[Card]
