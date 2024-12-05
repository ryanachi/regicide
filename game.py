from card import Suit, Card
from player import Player, Opp
from dataclasses import dataclass, default_factory

HAND_SIZE = 8

SUITS = {}

@dataclass
class Game():
    castle_deck: list[Card] = default_factory(list)
    tavern_deck: list[Card] = default_factory(list)
    # discard_deck: list[Card] = 
    player: Player
    opp_card: Card
    # opp: Opp

    def __post_init__(self):

        # initialize tavern deck
        for rank in range(1, 10+1):
            for i, suit in enumerate(Suit):
                self.tavern_deck.append(Card(suit, rank))
        self.tavern_deck.shuffle()
        self.player.hand, self.tavern_deck = set(self.tavern_deck[:HAND_SIZE]), self.tavern_deck[HAND_SIZE:]

        # initialize castle deck
        for _, suit in enumerate(Suit):
            # for _, royal in enumerate

    def main(self):
        while self.castle_deck:
            self.opp.opp_card = self.castle_deck.pop(0)

            # while self.opp_card

            # if kill
            # replace curr card
            
        