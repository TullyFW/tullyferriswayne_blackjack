from itertools import product as prod
import random as rand
from time import sleep

class Card:
    def __init__(self,rank,suit,value):
        self.rank = rank
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"[{self.suit}{self.rank}]"
    
    def __repr__(self):
        return f"{str(self)}"
    


class Deck:
    def __init__(self,ranks,suits,values):
        self.cards = [Card(r,s,v) for (s,(r,v)) in prod(suits,zip(ranks,values))]
    
    def shuffle(self):
        rand.shuffle(self.cards)
        
    def deal(self,hand):
        hand.cards.append(self.get_top_card)
    
    def get_top_card(self):
        return self.cards.pop(0)
    
    def __str__(self):
        return str(self.cards)
    
    def __len__(self):
        return len(self.cards)

class Hand():
    '''Class that stores the cards a player is holding'''
    def __init__(self,name,deck):
        self.cards = [deck.get_top_card(),deck.get_top_card()]
        self.name = name
        self.money = 100
        self.bet = 0
    
    @property
    def value(self):
        card_sum  = sum([card.value for card in self.cards])
        if card_sum > 21 and "A" in [card.rank for card in self.cards]:
            return card_sum - 10
        return card_sum
        
    
    def reset(self,deck):
        self.cards = [deck.get_top_card(),deck.get_top_card()]
        
    def check_bust(self):
            '''returns True or False based on whether the tally is greater than 21'''
            return self.value > 21
    
    def check_blackjack(self):
        return self.tally == 21
    
    def __str__(self):
        return f"{self.name}'s hand: {self.cards}"
    
    def __iadd__(self,card):
        self.cards.append(card)
        return self
    


class Blackjack:
    def make_players(self,deck):
        how_many = int(input("How many players? "))
        players = []
        for p in range(1,how_many + 1):
            name = input(f"Player {p} name: ")
            players.append(Hand(name,deck))
        return players
    
    def make_bets(self,players,deck):
        for player in players:
            player.reset(deck)
            print(f"{player.name}'s turn to bet")
            print(f"Your current money: {player.money}")
            while True:
                try: 
                    player.bet = abs(int(input("How much do you want to bet? ")))
                except ValueError:
                    print("Invalid input (must be integer)")
                if player.bet <= player.money:
                    break
                print("You don't have that amount of money")
    
    def turn(self,hand,deck):
        print(f"{hand.name}'s Turn: ")
        while True:
            print(f"\n{hand}")
            hit = input("hit (h) or stay (s): ")
            print("\n")
            if hit == "s":
                break
            elif hit == "h":
                print(hand)
                hand += deck.get_top_card()
                print(hand)
                if hand.check_bust():
                    print("Bust!")
                    break
                continue
            print("Invalid input")
        
    
    def comp_turn(self,hand,deck):
        print(f"Dealer's turn: \n\n{hand}")
        while hand.value < 17:
            print("Computer hits")
            hand += deck.get_top_card()
            print(hand)
        if hand.check_bust():
            print("Bust!\n")
        else:
            print("Computer stays\n")
            print(hand)
    
    def round_scores(self,players,dealer):
        dealer_pts = dealer.value if not dealer.check_bust() else 0
        print(f"Dealer total: {dealer.value}")
        for player in players:
            print(f"{player.name} bet {player.bet}")
            print(f"{player.name}'s round total: {player.value}")
            if player.value > dealer_pts and not player.check_bust():
                print(f"You beat the dealer and gained {player.bet}!")
                player.money += player.bet
                print(f"Current money: {player}.money")
            else:
                print(f"You lost the round and lost {player.bet}!")
                player.money -= player.bet
                print(f"Current money: {player.money}")
            

def main():
    game = Blackjack()
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    suits = ['♦', '♦', '♥', '♠']
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10 , 11]
    deck = Deck(ranks,suits,values)
    deck.shuffle()
    players = game.make_players(deck)
    dealer = Hand("Dealer",deck)
    while True:
        dealer.reset(deck)
        game.make_bets(players,deck)
        print(f"Dealer first card: {dealer.cards[0]}")
        for player in players:
            game.turn(player,deck)
        game.comp_turn(dealer,deck)
        sleep(3)
        game.round_scores(players,dealer)
        if input("do you want to play another round? Type nothing for yes: "):
            break
    for player in players:
        print(f"{player.name}'s final score: {player.money}")
    winner = max(players,key = lambda x:x.money)
    print(f"{winner.name.upper()} WINS!!!")

if __name__ == "__main__":
    main()

