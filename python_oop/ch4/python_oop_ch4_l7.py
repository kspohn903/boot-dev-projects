import random

class DeckOfCards():
    SUITS = [ "Hearts", "Diamonds", "Clubs", "Spades" ]
    RANKS = [ 
               "Ace", "2", "3", "4", "5", "6", "7", 
               "8", "9", "10", "Jack", "Queen", "King"
    ]

    def __init__(self):
        self.__cards = []
        # Call create_deck here so the list isn't empty!
        self.create_deck()

    def create_deck(self):
        # Access class variables using 'self.' or 'DeckOfCards.'
        for suit in self.SUITS:
            for rank in self.RANKS:
                self.__cards.append((rank, suit))
                print(f"{rank} of {suit}")

    def shuffle_deck(self):
        random.shuffle(self.__cards)

    def deal_card(self):
        return None if (len(self.__cards) <= 0) else self.__cards.pop()

    def __str__(self):
        return f"The deck has {len(self.__cards)} cards"
