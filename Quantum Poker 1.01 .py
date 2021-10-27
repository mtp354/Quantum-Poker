# An interactive simulator for a quantum version of Texas Hold'em Poker

import numpy as np
from numpy import random

# All quantum cards are a superposition of two classical cards

Cards = {0: "2♣", 1: "2♦", 2: "2♥", 3: "2♠", 4: "3♣", 5: "3♦", 6: "3♥", 7: "3♠", 8: "4♣", 9: "4♦", 10: "4♥",
         11: "4♠", 12: "5♣", 13: "5♦", 14: "5♥", 15: "5♠", 16: "6♣", 17: "6♦", 18: "6♥", 19: "6♠", 20: "7♣",
         21: "7♦", 22: "7♥", 23: "7♠", 24: "8♣", 25: "8♦", 26: "8♥", 27: "8♠", 28: "9♣", 29: "9♦", 30: "9♥",
         31: "9♠", 32: "10♣", 33: "10♦",34: "10♥", 35: "10♠", 36: "J♣", 37: "J♦", 38: "J♥", 39: "J♠", 40: "Q♣",
         41: "Q♦", 42: "Q♥", 43: "Q♠", 44: "K♣", 45: "K♦", 46: "K♥", 47: "K♠", 48: "A♣", 49: "A♦", 50: "A♥",
         51: "A♠"}


def tensor_product(list1, list2):
    output = []
    if not list1:
        return list2
    for item1 in list1:
        for item2 in list2:
            output.append([item1, item2])
    for i in range(len(output)):
        output[i] = sorted(flatten(output[i]))
    return output


def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


class Quantum_Card:
    def __init__(self, value1, value2):  # value is int from 0 to 51
        self.v1 = value1
        self.v2 = value2

    def __str__(self):
        return "|" + Cards[self.v1] + ">" + " + " + "|" + Cards[self.v2] + ">"


class Quantum_Hand:
    def __init__(self):  # suit and number are ints
        self.cards = []
        self.values = []

    def add_card(self, card):
        self.cards.append(card)
        self.values = tensor_product(self.values, [card.v1, card.v2])

    def __str__(self):
        printable = ""
        for i in range(len(self.values)):
            printable += "|"
            for j in range(len(self.values[i])):
                printable += Cards[self.values[i][j]]
                if j != len(self.values[i])-1:
                    printable += ", "
            printable += ">"
            if i != len(self.values)-1:
                printable += " + "
        return printable

    def measure(self):
        outcome = self.values[random.randint(0, len(self.values))]
        if len(self.values) != 7:
            self.values = outcome


class Player:
    def __init__(self, name, wallet=100):
        self.name = name
        self.hand = Quantum_Hand()
        self.wallet = wallet

    def __str__(self):
        return self.name + " - " + str(self.wallet)


class Game:
    def __init__(self, players):
        self.deck = list(range(0, 51))
        self.players = players
        self.round_number = 0
        self.pot = 0

    def kick_inactive(self):
        for i in range(len(self.players)):
            if self.players[i].wallet < 2:
                self.players.pop(i)

    def play_round(self):
        self.kick_inactive()
        self.pot = np.zeros((1, len(self.players)))
        self.round_number += 1
        # BLINDS
        dealer_position = (self.round_number % len(self.players))

        lucky_numbers = np.random.choice(self.deck, 4*len(self.players)+10, replace=False)
        list_of_cards = []
        i = 0
        while i < len(lucky_numbers):
            list_of_cards.append(Quantum_Card(lucky_numbers[i], lucky_numbers[i+1]))
            i += 2
        # DEALING
        i = 5
        for player in self.players:
            player.hand.add_card(list_of_cards[i])
            player.hand.add_card(list_of_cards[i+1])
            i += 2
        # FLOP
        for player in self.players:
            player.hand.add_card(list_of_cards[0])
            player.hand.add_card(list_of_cards[1])
            player.hand.add_card(list_of_cards[2])
        # TURN
        for player in self.players:
            player.hand.add_card(list_of_cards[3])
        # RIVER
        for player in self.players:
            player.hand.add_card(list_of_cards[4])
        # REVEAL
        for player in self.players:
            player.hand.measure()
            print([Cards[item] for item in player.hand.values])


Cai = Player("Cai")
Andrew = Player("Andrew")
Phil = Player("Phil")
Elias = Player("Elias")
Matt = Player("Matt")
squad = [Cai, Andrew, Phil, Elias, Matt]
game = Game(squad)
game.play_round()


