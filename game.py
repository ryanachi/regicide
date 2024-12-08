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
                new_Royal = Card(suit, Royals.royal.value)
                new_Royal.attack = new_Royal.rank
                new_Royal.health = new_Royal.rank * 2
                self.castle_deck.append(new_Royal)
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
                    n = min([self.card.rank, len(self.tavern_deck), HAND_SIZE - len(self.player.hand)])
                    cards_to_draw, self.tavern_deck = self.tavern_deck[:n], self.tavern_deck[n:]
                    self.player.hand |= set(cards_to_draw)
                    # draw from tavern
                elif self.card.suit == Suit.HEART:
                    n = min([self.card.rank, len(self.discard_deck)])
                    self.tavern_deck.append(c for c in self.discard_deck[:n])
                    self.discard_deck = self.discard_deck[n:]
                    # refill tavern
                elif self.card.suit == Suit.SPADE:
                    self.opp_card.attack -= min([self.card.rank, self.opp_card.attack])
                    # decrease enemy attack

                # 3. Deal damage and check to see if the enemy is defeated
                self.opp_card.health -= player_card.attack

                # 4. Suffer damage from the enemy by discarding cards 
                # Heuristic: Automatically select cards that add up to the attack power, 
                # with penalties for too many of a single suit discarded
                

                # Loss condition
                if not self.player.hand:
                    print("You Lose") 

            # If beaten, replace curr card and add royal to appropriate deck
            # Note that its health won't be used again, so we don't need to reset it
            # Reset the attack power, since Royal clubs do not have double damage
            self.opp_card.attack = self.rank * (2 if self.suit == Suit.CLUB else 1)
            if self.opp_card.health == 0:
                self.tavern_deck.insert(0, self.opp_card)
            else:
                self.discard_deck.append(self.opp_card)
            
        