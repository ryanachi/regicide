from itertools import combinations
from baselines import (
    random_choice,
    highest_card,
    lowest_card,
)
from card import Suit, Royals, Card
from player import Player
from dataclasses import dataclass, field
from rng import rng


HAND_SIZE = 10

SUITS = {}

@dataclass
class Game():
    # player: Player  -> defined in __post_init__
    # opp_card: Card  -> defined in __post_init__
    castle_deck: list[Card] = field(default_factory=list)
    tavern_deck: list[Card] = field(default_factory=list)
    discard_deck: list[Card] = field(default_factory=list)

    def __post_init__(self):
        self.player = Player(set())
        # initialize tavern deck
        for rank in range(4, 12+1):
            for _, suit in enumerate(Suit):
                self.tavern_deck.append(Card(suit, rank))
        rng.shuffle(self.tavern_deck)
        self.player.hand, self.tavern_deck = set(self.tavern_deck[:HAND_SIZE]), self.tavern_deck[HAND_SIZE:]

        # initialize castle deck
        for _, royal in enumerate(Royals):
            mini_castle = []
            for _, suit in enumerate(Suit):
                new_Royal = Card(suit=suit, rank=royal.value, is_royal=True)
                new_Royal.attack = new_Royal.rank
                new_Royal.health = new_Royal.rank * 2
                mini_castle.append(new_Royal)
            rng.shuffle(mini_castle)
            self.castle_deck.extend(mini_castle)

        self.opp_card = self.castle_deck.pop(0)


    def discard(self, player_hand: set[Card], attack_pow: int):
        # Heuristic: Automatically select cards that add up to the attack power (Done), 
        # with penalties for too many of a single suit discarded (Done)

        

        exact_match_weight = 12.824111
        diversity_weight = 3.03
        spades_penalty = 4.371
        diamonds_penalty = 5.2991
        hearts_penalty = 1.2651
        royal_penalty = 2.01010101
        card_count_penalty = 2.1

        best_subset = None
        best_score = float('-inf')


        player_hand = sorted(list(player_hand), key=lambda x: (x.rank, x.suit.value, x.is_royal))
        # Check all possible subsets
        for r in range(1, len(player_hand) + 1):
            for subset in combinations(player_hand, r):
                subset_attack = sum(card.rank or 0 for card in subset)
                if subset_attack < attack_pow:
                    continue  # Skip subsets that don't meet the attack power threshold

                # Calculate scores
                score = 0

                # Weight for exact match
                if subset_attack == attack_pow:
                    score += exact_match_weight

                # Weight for suit diversity
                unique_suits = {card.suit for card in subset}
                score += diversity_weight * len(unique_suits)

                # Penalty for including spades
                spades_count = sum(1 for card in subset if card.suit == Suit.SPADE)
                score -= spades_penalty * spades_count

                # Penalty for including diamonds
                diamonds_count = sum(1 for card in subset if card.suit == Suit.DIAMOND)
                score -= diamonds_penalty * diamonds_count

                # Penalty for including hearts
                hearts_count = sum(1 for card in subset if card.suit == Suit.HEART)
                score -= hearts_count * hearts_penalty

                # Penalty for including royal
                royal_count = sum(1 for card in subset if card.is_royal)
                score -= royal_count * royal_penalty

                # Penalty for number of cards discarded
                score -= card_count_penalty * len(subset)

                # Update best subset
                if score > best_score:
                    best_score = score
                    best_subset = subset

        # Remove the chosen cards from the hand
        if best_subset:
            return set(best_subset)
        return None



        # best_hand = []
        # best_score = -11

        # if not player_hand and attack_pow > 0:
        #     best_score = -10  # Arbitrary bad score that beats the initialization
        # elif attack_pow <= 0:
        #     best_score = sum([c.rank for c in player_hand]) + (attack_pow / 2)  # Penalize for over-attacking
        #     hand_suits = [c.suit for c in player_hand]
        #     best_score -= hand_suits.count(hand_suits)  # Penalize for not leaving a good mix of cards

        # # whats the fastest and most efficient way of doing this :(
        # for card in player_hand:
        #     player_hand.remove(card)
        #     i_score, i_hand = self.discard(player_hand, attack_pow - card.rank)  # Include
        #     e_score, e_hand = self.discard(player_hand, attack_pow)  # Exclude

        #     if max(i_score, e_score) > best_score:
        #         best_score, best_hand = i_score, (i_hand + [card]) if i_score > e_score else e_score, e_hand

        # return best_score, best_hand

    def one_step(self, strategy, action=None):
        #print(f"HAND: {self.player.hand}")

        # Include all inputs for the sake of building a strategy later
        if action:
            player_card = action
        else:
            player_card = strategy(self.castle_deck, self.tavern_deck, self.discard_deck, self.player, self.opp_card)
        #print(f"CARD: {player_card}")
        #print(f"")

        # 1. Play a card from hand to attack the enemy
        self.player.hand.remove(player_card)

        # 2. Activate the played card’s suit power
        # I would normally use a `match` for this but that requires python3.10
        if player_card.suit == Suit.CLUB and self.opp_card.suit != Suit.CLUB:
            # double attack
            self.opp_card.health -= player_card.attack
        elif player_card.suit == Suit.DIAMOND and self.opp_card.suit != Suit.DIAMOND:
            # draw from tavern
            n = min([player_card.rank, len(self.tavern_deck), HAND_SIZE - len(self.player.hand)])
            cards_to_draw, self.tavern_deck = self.tavern_deck[:n], self.tavern_deck[n:]
            self.player.hand |= set(cards_to_draw)
        elif player_card.suit == Suit.HEART and self.opp_card.suit != Suit.HEART:
            # refill tavern
            n = min(player_card.rank, len(self.discard_deck))
            self.tavern_deck, self.discard_deck = self.tavern_deck + self.discard_deck[:n], self.discard_deck[n:]
        elif player_card.suit == Suit.SPADE and self.opp_card.suit != Suit.SPADE:
            # decrease enemy attack
            self.opp_card.attack -= min([player_card.rank, self.opp_card.attack])

        # 3. Deal damage, add card to discard, and check to see if the enemy is defeated
        self.opp_card.health -= player_card.attack
        #print(f"{self.opp_card}'s health={self.opp_card.health}, attack={self.opp_card.attack}")
        self.discard_deck.append(player_card)
        if self.opp_card.health <= 0:
            # If beaten, replace curr card and add royal to appropriate deck
            # Note that its health won't be used again, so we don't need to reset it
            # Reset the attack power, since Royal clubs do not have double damage
            self.opp_card.attack = self.opp_card.rank
            if self.opp_card.health == 0:
                self.tavern_deck.insert(0, self.opp_card)
            else:
                self.discard_deck.append(self.opp_card)

            if self.castle_deck:
                self.opp_card = self.castle_deck.pop(0)
            else:
                return (10_000, True)  # reward for winning
        elif self.opp_card.attack > 0:
            # 4. Suffer damage from the enemy by discarding cards ONLY if enemy is not defeated
            discard_set = self.discard(self.player.hand, self.opp_card.attack)
            # empty set means nothing needed to discard
            # None means insufficient cards to discard
            if discard_set is None:
                return (-100 * len(self.castle_deck), True)
            #print(f"{discard_set=}")
            for c in discard_set:
                self.player.hand.remove(c)
                self.discard_deck.append(c)

        if not self.player.hand:
            return (-100 * len(self.castle_deck), True)
        else:
            return (0, False)


    def main(self, strategy):
        # Already popped off first card

        _cnt = 0
        while self.castle_deck or self.opp_card.health > 0:
            _cnt += 1
            #print(f"\n======STEP {_cnt}======")
            res, done = self.one_step(strategy)
            if res < 0:
                #print("You Lose :(")
                return res
            if done:
                return res
            
if __name__ == "__main__":
    g = Game()
    g.main(random_choice)