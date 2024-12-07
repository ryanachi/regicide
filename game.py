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
                player_card = strategy(self.castle_deck, self.tavern_deck, self.discard_deck, self.player, self.opp_card)

                # 1. Play a card from hand to attack the enemy
                self.player.hand.remove(player_card)

                # 2. Activate the played card’s suit power
                # I would normally use a `match` for this but that requires python3.10
                if self.card.suit == Suit.CLUB:
                    pass
                    # no action needed; already addressed in card.py
                elif self.card.suit == Suit.DIAMOND:
                    cards_to_draw = min([self.card.rank, len(self.tavern_deck), HAND_SIZE - len(self.player.hand)])
                    ... 
                    # draw from tavern
                elif self.card.suit == Suit.HEART:
                    ...
                    # refill tavern
                elif self.card.suit == Suit.SPADE:




                # 3. Deal damage and check to see if the enemy is defeated
                self.opp_card.health -= player_card.attack

                # 4. Suffer damage from the enemy by discarding cards


                # Attack the player: Do we want the player to choose which cards to discard??

                # Loss condition
                if not self.player.hand:
                    print("You Lose") 

            # If beaten, replace curr card and add royal to appropriate deck
            # Note that its health won't be used again, so we don't need to reset it
            if self.opp_card.health == 0:
                self.tavern_deck.insert(0, self.opp_card)
            else:
                self.discard_deck.append(self.opp_card)
            
        