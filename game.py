from baselines import (
    random_choice,
    highest_card,
    lowest_card,
)
from card import Suit, Royals, Card
from player import Player
from dataclasses import dataclass, field
import random


HAND_SIZE = 8

SUITS = {}

@dataclass
class Game():
    # player: Player = field(default_factory=Player(set()))
    castle_deck: list[Card] = field(default_factory=list)
    tavern_deck: list[Card] = field(default_factory=list)
    discard_deck: list[Card] = field(default_factory=list)
    # opp: Opp

    def __post_init__(self):
        self.player = Player(set())
        # initialize tavern deck
        for rank in range(1, 10+1):
            for _, suit in enumerate(Suit):
                self.tavern_deck.append(Card(suit, rank))
        random.shuffle(self.tavern_deck)
        self.player.hand, self.tavern_deck = set(self.tavern_deck[:HAND_SIZE]), self.tavern_deck[HAND_SIZE:]

        # initialize castle deck
        for _, suit in enumerate(Suit):
            for _, royal in enumerate(Royals):
                new_Royal = Card(suit, royal.value)
                new_Royal.attack = new_Royal.rank
                new_Royal.health = new_Royal.rank * 2
                self.castle_deck.append(new_Royal)
        # TODO: shuffling is wrong. Needs to only shuffle across each level.
        random.shuffle(self.castle_deck)

        self.opp_card = self.castle_deck.pop(0)

    def discard(self, player_hand, attack_pow):
        # Heuristic: Automatically select cards that add up to the attack power (Done), 
        # with penalties for too many of a single suit discarded (TODO)
        best_hand = []
        best_score = -11

        if not player_hand and attack_pow > 0:
            best_score = -10  # Arbitrary bad score that beats the initialization
        elif attack_pow <= 0:
            best_score = sum([c.rank for c in player_hand]) + (attack_pow / 2)  # Penalize for over-attacking
            hand_suits = [c.suit for c in player_hand]
            best_score -= hand_suits.count(hand_suits)  # Penalize for not leaving a good mix of cards

        # whats the fastest and most efficient way of doing this :(
        for card in player_hand:
            player_hand.remove(card)
            i_score, i_hand = self.discard(player_hand, attack_pow - card.rank)  # Include
            e_score, e_hand = self.discard(player_hand, attack_pow)  # Exclude

            if max(i_score, e_score) > best_score:
                best_score, best_hand = i_score, (i_hand + [card]) if i_score > e_score else e_score, e_hand

        return best_score, best_hand

    def main(self, strategy):
        self.opp_card = self.castle_deck.pop(0)
        while self.castle_deck:
            while self.opp_card.health > 0:
                # Include all inputs for the sake of building a strategy later
                player_card = strategy(self.castle_deck, self.tavern_deck, self.discard_deck, self.player, self.opp_card)

                # 1. Play a card from hand to attack the enemy
                self.player.hand.remove(player_card)

                # 2. Activate the played card’s suit power
                # I would normally use a `match` for this but that requires python3.10
                if player_card.suit == Suit.CLUB:
                    pass
                    # no action needed; already addressed in card.py
                elif player_card.suit == Suit.DIAMOND:
                    # draw from tavern
                    n = min([self.card.rank, len(self.tavern_deck), HAND_SIZE - len(self.player.hand)])
                    cards_to_draw, self.tavern_deck = self.tavern_deck[:n], self.tavern_deck[n:]
                    self.player.hand |= set(cards_to_draw)
                elif player_card.suit == Suit.HEART:
                    # refill tavern
                    n = min(self.card.rank, len(self.discard_deck))
                    self.tavern_deck, self.discard_deck = self.tavern_deck + self.discard_deck[:n], self.discard_deck[n:]
                elif player_card.suit == Suit.SPADE:
                    # decrease enemy attack
                    self.opp_card.attack -= min([player_card.rank, self.opp_card.attack])

                # 3. Deal damage and check to see if the enemy is defeated
                self.opp_card.health -= player_card.attack

                # 4. Suffer damage from the enemy by discarding cards
                _, discard_hand = self.discard(self.player.hand, self.opp_card.attack)
                for c in discard_hand:
                    self.player.hand.remove(c)

                # Loss condition
                if not self.player.hand:
                    print("You Lose") 
                    return 0

            # If beaten, replace curr card and add royal to appropriate deck
            # Note that its health won't be used again, so we don't need to reset it
            # Reset the attack power, since Royal clubs do not have double damage
            self.opp_card.attack = self.rank * (2 if self.suit == Suit.CLUB else 1)
            if self.opp_card.health == 0:
                self.tavern_deck.insert(0, self.opp_card)
            else:
                self.discard_deck.append(self.opp_card)

        print("You Win!")
        return 100
            
if __name__ == "__main__":
    g = Game()
    g.main(random_choice)