# CARD_DICTIONARY = {
#        "SUITS": ["Clubs","Diamonds", "Hearts", "Spades"],
#        "SUITS_VALUES": [j+1 for j in range(0, N_SUITS, 1)], # 1-4
#        "RANKS": ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"],
#        "RANKS_VALUES": [i+1 for i in range(0, len(N_CARDS_PER_SUIT), 1)] #1-13 
# }

SUITS = ["Clubs", "Diamonds", "Hearts", "Spades"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

class Card():
    def __init__(self, rank, suit):
        self.__rank = rank
        self.__suit = suit

    def __lt__(self, other):
        # Find the numerical index of the strings to compare power
        if self.__rank != other.__rank:
            return RANKS.index(self.__rank) < RANKS.index(other.__rank)
        return SUITS.index(self.__suit) < SUITS.index(other.__suit)

    def __gt__(self, other):
        # Use the same index-based comparison for 'greater than'[cite: 12]
        if self.__rank != other.__rank:
            return RANKS.index(self.__rank) > RANKS.index(other.__rank)
        return SUITS.index(self.__suit) > SUITS.index(other.__suit)

    def __eq__(self, other):
        return (self.__rank == other.__rank) and (self.__suit == other.__suit)

    # don't touch below this line
    def __str__(self):
        return f"{self.__rank} of {self.__suit}"
