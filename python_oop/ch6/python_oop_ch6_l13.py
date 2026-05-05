SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.rank_index = RANKS.index(rank)
        self.suit_index = SUITS.index(suit)

    def __eq__(self, other):
        return (
            self.rank_index == other.rank_index and self.suit_index == other.suit_index
        )

    def __lt__(self, other):
        if self.rank_index == other.rank_index:
            return self.suit_index < other.suit_index
        return self.rank_index < other.rank_index

    def __gt__(self, other):
        if self.rank_index == other.rank_index:
            return self.suit_index > other.suit_index
        return self.rank_index > other.rank_index

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Round():
    def resolve_round(self):
        raise NotImplementedError("Subclasses must implement resolve_round()")

class HighCardRound(Round):
    def __init__(self, card1, card2):
        # Store cards as instance variables
        self.card1 = card1
        self.card2 = card2

    def resolve_round(self):
        # 1 if card1 is higher than card2
        if self.card1 > self.card2:
            return 1
        # 2 if card2 is higher than card1
        if self.card2 > self.card1:
            return 2
        # 0 if the cards are equal
        return 0


class LowCardRound(Round):
    def __init__(self, card1, card2):
        # Store cards as instance variables[cite: 14]
        self.card1 = card1
        self.card2 = card2

    def resolve_round(self):
        # 1 if card1 is lower than card2[cite: 14]
        if self.card1 < self.card2:
            return 1
        # 2 if card2 is lower than card1[cite: 14]
        if self.card2 < self.card1:
            return 2
        # 0 if the cards are equal[cite: 14]
        return 0
