from dataclasses import dataclass
from enum import Enum

class Suit(Enum):
    DIAMOND = "\u2666"
    CLUB = "\u2663"
    HEART = "\u2665"
    SPADE = "\u2660"
    # JOKER = 4  # I guess no jokers in solo

class Royals(Enum):
    JACK = 10
    QUEEN = 15
    KING = 20

@dataclass
class Card():
    suit: Suit | None
    rank: int
    health: int = None
    attack: int = None

    def __post_init__(self):
        self.health = self.rank
        self.attack = self.rank

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        return hash((self.suit, self.rank))
    
    def __repr__(self):
        return f"{self.rank}{self.suit.value.upper()}"