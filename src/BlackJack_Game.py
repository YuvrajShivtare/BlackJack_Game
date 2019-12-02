# IMPORT STATEMENTS AND VARIABLE DECLARATIONS:

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True
new_player = True

# Stating Rules for the game:
print('\n***************Welcome to BlackJack**************\n'
      'Rules:\n--> Blackjack starts with players making bets\n'
      '--> Dealer deals 2 cards to the players and two to himself (1 card face up, the other face down)\n'
      '--> All cards count their face value in blackjack. Picture cards count as 10 and the ace can count as\n'
      '\teither 1 or 11. Card suits have no meaning in blackjack. '
      'The total of any hand is the sum of the card values in the hand\n'
      '--> Players must decide whether to stand or hit\n'
      '--> The dealer acts last and must hit on 16 or less and stand on 17 through 21\n'
      '--> Players win when their hand totals higher than dealer’s hand, or they have 21 or less when the dealer busts '
      '(i.e., exceeds 21)\n\nGame Begins!!\n')


# CLASS DEFINITIONS:

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck(object):

    def __init__(self):
        self.deck = []  # Empty deck
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''  # empty string
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand(object):

    def __init__(self):
        self.cards = []  # start with an empty list
        self.value = 0  # start with zero value
        self.aces = 0  # attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1  # add to self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips(object):

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# FUNCTION DEFINITIONS:

def take_bet(chips):
    while True:
        try:
            print("Total available chips", chips.total)
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!\n')
        else:
            if chips.bet <= 0:
                print("You can't bet 0 or less, try again!\n")
            elif chips.bet > chips.total:
                print("Sorry, your bet can't exceed", chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? (h/s) ")

        if x.lower() == 'h' or x.lower() == 'hit':
            hit(deck, hand)

        elif x.lower() == 's' or x.lower() == 'stand':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again. Expected value (h/s)\n")
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print("\t<card hidden>")
    print('\t', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n\t')
    print("Player's Hand =", player.value)


def show_all(player, dealer):
    print("Dealer's Hand:", *dealer.cards, sep='\n\t')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n\t')
    print("Player's Hand =", player.value)


def player_busts(chips):
    print("Player busts! Better luck next time")
    chips.lose_bet()


def player_wins(chips):
    print("Congratulations!! Player wins!")
    chips.win_bet()


def dealer_busts(chips):
    print("Congratulations!! Dealer busts!")
    chips.win_bet()


def dealer_wins(chips):
    print("Dealer wins! Better luck next time")
    chips.lose_bet()


def push():
    print("Dealer and Player tie! It's a push.")


def continue_play():
    while True:
        global playing
        global new_player
        new_game = input("Would you like to play another hand? Enter 'y' or 'n'?\n ")
        if new_game.lower() == 'y' or new_game.lower() == 'yes':
            playing = True
            if player_chips.total == 0:
                print("\nNo Coins left to play. Game reset!")
                new_player = True
            else:
                new_player = False
            return True
        elif new_game.lower() == 'n' or new_game.lower() == 'no':
            print("Thanks for playing!")
            return False
        else:
            print("Please enter valid input! Expected input(y/n)")
            continue

# GAME PLAY!


if __name__ == "__main__":
    while True:
        # Create & shuffle the deck, deal two cards to each player
        get_deck = Deck()
        get_deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(get_deck.deal())
        player_hand.add_card(get_deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(get_deck.deal())
        dealer_hand.add_card(get_deck.deal())

        if new_player:
            # Set up the Player's chips
            player_chips = Chips()  # default value is 100

        # Prompt the Player for their bet:
        take_bet(player_chips)

        # Show the cards:
        show_some(player_hand, dealer_hand)

        while playing:  # recall this variable from our hit_or_stand function

            # Prompt for Player to Hit or Stand
            hit_or_stand(get_deck, player_hand)
            show_some(player_hand, dealer_hand)

            if player_hand.value > 21:
                print("\nRESULTS: ")
                show_all(player_hand, dealer_hand)
                player_busts(player_chips)
                break

        # If Player hasn't busted, play Dealer's hand
        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(get_deck, dealer_hand)

            # Show all cards
            print("\nRESULTS: ")
            show_all(player_hand, dealer_hand)

            # Test different winning scenarios
            if dealer_hand.value > 21:
                # dealer_busts(player_hand, dealer_hand, player_chips)
                dealer_busts(player_chips)

            elif dealer_hand.value > player_hand.value:
                # dealer_wins(player_hand, dealer_hand, player_chips)
                dealer_wins(player_chips)

            elif dealer_hand.value < player_hand.value:
                player_wins(player_chips)

            else:
                push()

        # Inform Player of their chips total
        print("\nPlayer's winnings stand at", player_chips.total)

        if continue_play():
            continue
        else:
            break
