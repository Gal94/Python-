import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
signs = {'Hearts': '\u2665', 'Diamonds': '\u2666', 'Spades': '\u2663', 'Clubs': '\u2660'}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "{} of {}".format(self.rank, self.suit)


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                card = Card(suit, rank) #create a card object
                self.deck.append(card) #add to deck

    def __str__(self):
        for piece in self.deck:
            print(piece)
        return "Deck has been printed out."

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        randCard = self.deck.pop()
        return randCard


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        if self.value > 21 and self.aces >= 1:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chip):
    '''
    assigns chips bet for current round
    '''
    while True:
        try:
            chip.bet = int(input("How much would you like to bet?"))
        except ValueError:
            print("Please provide the bet value as an integer.")
        else:
            if chip.total >= chip.bet > 0:
                print("Betting on {}".format(chip.bet))
                break
            else:
                print("Insufficient funds, Please enter a different amount.")


def hit(gameDeck, hand):
    card = gameDeck.deal()
    hand.add_card(card)
    if hand.value > 21:
        hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global gameRound  # to control an upcoming while loop

    while True:
        x = input("Would you like to Hit or Stand?\nEnter Hit or Stand: ")

        if x[0].lower() == 'h':
            hit(deck, hand)
            gameRound = True

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            gameRound = False

        else:
            print("Sorry, please try again.")
            continue
        break


def show_some(player, dealer):
    print("\n"* 10)
    #keep 1 dealer card hidden and show all player cards
    print("Dealer's Hand:")
    if values[dealer.cards[1].rank] < 10:
        print("   ----------    ----------\n "
              " |          |  |{}         |\n"
              "  |          |  |          |\n"
              "  |  hidden  |  |    {}     |\n"
              "  |          |  |          |\n"
              "  |          |  |        {} |\n"
              "   ----------    ----------\n".format(signs[dealer.cards[1].suit], values[dealer.cards[1].rank], signs[dealer.cards[1].suit]))
    else:
        print("   ----------    ----------\n "
              " |          |  |{}         |\n"
              "  |          |  |          |\n"
              "  |  hidden  |  |    {}    |\n"
              "  |          |  |          |\n"
              "  |          |  |        {} |\n"
              "   ----------    ----------\n".format(signs[dealer.cards[1].suit], values[dealer.cards[1].rank],
                                                     signs[dealer.cards[1].suit]))
    #print("Player's Hand:", *player.cards, sep='\n ')
    print_hand(player)


def show_all(player, dealer):
    #display all cards - at end of game
    print_hand(dealer)
    print_hand(player)


def player_busts(player, chip):
    print("Player busts!\nPlayer loses {} chips.".format(chip.bet))
    chip.lose_bet()


def player_wins(player, chip):
    print("Player wins!\nPlayer wins {} chips.".format(chip.bet))
    chip.win_bet()


def dealer_busts(player, chip):
    print("Dealer busts!\n"
          "Player wins {} chips.".format(chip.bet))
    chip.win_bet()


def dealer_wins(player, chip):
    print("Dealer wins!\nPlayer loses {} chips.".format(chip.bet))
    chip.lose_bet()


def push(player):
    print("Push!\n"
          "Dealer and Player tie with {}".format(player.value))


def print_hand(player):
    i = 0
    while i < len(player.cards):
        print("   ----------", end=" ", sep="    ")
        i += 1
    print("\n", end="")
    i = 0
    while i < len(player.cards):
        print("  |{}         |".format(signs[player.cards[i].suit]), end="", sep="  ")
        i += 1
    print("\n", end="")
    i = 0
    while i < len(player.cards):
        print("  |          |", end="", sep="  ")
        i += 1
    print("\n", end="")
    i = 0
    while i < len(player.cards):
        if values[player.cards[i].rank] >= 10:
            print("  |    {}    |".format(values[player.cards[i].rank]), end="", sep="  ")
        else:
            print("  |    {}     |".format(values[player.cards[i].rank]), end="", sep=" ")
        i += 1

    print("\n", end="")
    i = 0
    while i < len(player.cards):
        print("  |          |", end="", sep="  ")
        i += 1
    print("\n", end="")
    i = 0
    while i < len(player.cards):
        print("  |         {}|".format(signs[player.cards[i].suit]), end="", sep="  ")
        i += 1
    print("\n", end="")
    i = 0
    while i < len(player.cards):
        print("   ----------", end=" ", sep="  ")
        i += 1
    print("\n", end="")
    print("Hand's strength : {}\n".format(player.value))


def main():
    global gameRound
    gameRound = True
    chips = Chips()
    print("Welcome to Blackjack21.\n"
          "Dealer plays by the soft 17 rule.")
    while True:
        print("\nYou currently have {} chips.".format(chips.total))
        take_bet(chips)
        gameDeck = Deck()
        gameDeck.shuffle()
        gamePlayer = Hand()
        gameDealer = Hand()
        i = 0
        while i < 2:
            hit(gameDeck, gamePlayer)
            hit(gameDeck, gameDealer)
            i += 1
        print("\n" * 25)
        show_some(gamePlayer, gameDealer)

        while gameRound:  # game goes on until player stand

            hit_or_stand(gameDeck, gamePlayer)
            print("\n" * 25)
            show_some(gamePlayer, gameDealer)

            #checking for a player bust
            if gamePlayer.value > 21:
                player_busts(gamePlayer, chips)
                break
            elif gamePlayer.value == 21:
                player_wins(gamePlayer, chips)
                gameRound = False
                break

            #if dealer is above 17 check conditions
        if gameDealer.value> 17 and gamePlayer.value < 21:
            show_all(gamePlayer, gameDealer)
            if gameDealer.value > gamePlayer.value:
                dealer_wins(gamePlayer, chips)
            if gameDealer.value < gamePlayer.value:
                player_wins(gamePlayer, chips)
            else:
                push(gamePlayer)
        else: #else dealer keeps drawing cards
            #different winning conditions
            while gameDealer.value < 17 and gamePlayer.value < 21:
                hit(gameDeck, gameDealer)
                show_all(gamePlayer, gameDealer)
                if gameDealer.value > 21:
                    dealer_busts(gamePlayer, chips)
                    break
                elif gameDealer.value > gamePlayer.value:
                    dealer_wins(gamePlayer, chips)
                    break
                elif gameDealer.value < gamePlayer.value and gameDealer.value >= 17:
                    player_wins(gamePlayer, chips)
                    break
                elif gameDealer.value >=17 and gamePlayer.value == gameDealer.value:
                    break

        print("You currently have {} chips.".format(chips.total))

        if chips.total == 0:
            print("You lost, thank you for playing.\n")
            break

        answer = input("Would you like to play again?\nEnter Yes to start another round anything else"
                       " will close the game : ")
        if answer[0].lower() == 'y':
            gameRound = True
            continue
        else:
            break


if __name__ == '__main__':
    main()
