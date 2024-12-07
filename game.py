from card import Suit, Royals, Card
from player import Player, Opp
from dataclasses import dataclass, default_factory

HAND_SIZE = 8

SUITS = {}

@dataclass
class Game():
    castle_deck: list[Card] = default_factory(list)
    tavern_deck: list[Card] = default_factory(list)
    discard_deck: list[Card] = default_factory(list)
    player: Player
    opp_card: Card
    # opp: Opp

    def __post_init__(self):

        # initialize tavern deck
        for rank in range(1, 10+1):
            for _, suit in enumerate(Suit):
                self.tavern_deck.append(Card(suit, rank))
        self.tavern_deck.shuffle()
        self.player.hand, self.tavern_deck = set(self.tavern_deck[:HAND_SIZE]), self.tavern_deck[HAND_SIZE:]

        # initialize castle deck
        for _, suit in enumerate(Suit):
            for _, royal in enumerate(Royals):
                new_Royal = Card(suit, royal)
                new_Royal.attack = Royals.royal.value
                new_Royal.health = Royals.royal.value * 2
                self.castle_deck.append(Card(suit, royal))
        self.castle_deck.shuffle()

    def main(self, strategy):
        while self.castle_deck:
            self.opp.opp_card = self.castle_deck.pop(0)

            while self.opp_card.health > 0:
                # Include all inputs for the sake of building a strategy later
                play_card = strategy(self.castle_deck, self.tavern_deck, self.discard_deck, self.player, self.opp_card)
                self.opp_card.health -= play_card.attack

                # Attack the player: Do we want the player to choose which cards to discard??

                # Loss condition
                if not self.player.hand:
                    print("You Lose") 

            # If beaten, replace curr card and add royal to appropriate deck
            new_R_Suit = self.opp_card.suit
            new_Royal = Card(new_R_Suit, Royals.new_R_Suit)
            if self.opp_card.health == 0:
                self.tavern_deck.insert(0, new_Royal)
            else:
                self.discard_deck.append(new_Royal)
            
        