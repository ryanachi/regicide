from dataclasses import dataclass
from enum import Enum

class Suit(Enum):
    DIAMOND = 0
    CLUB = 1
    HEART = 2
    SPADE = 3
    # JOKER = 4

class Royals(Enum):
    JACK = 10
    QUEEN = 15
    KING = 20

@dataclass
class Card():
    suit: Suit | None
    rank: int | Royals
    health: int = None
    attack: int = None

    def __post_init__(self):
        self.health = self.rank
        self.attack = self.rank * (2 if self.suit == Suit.CLUB else 1)