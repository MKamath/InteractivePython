# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 
          'T':10, 'J':10, 'Q':10, 'K':10}

def game_over(winner, reason):
    global in_play, outcome, score
    if winner == "Dealer":
        if reason == "busted":
            outcome = "Player busted! New Deal?"
        else:
            outcome = "Dealer Wins! New Deal?"
        score -= 1
    else:
        if reason == "busted":
            outcome = "Dealer busted! New Deal?"
        else:
            outcome = "Player Wins! New Deal?"
        score += 1
    in_play = False

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, 
                          [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.handValue = 0
        self.handCards = []
        self.busted = False
        self.removed = False

    def __str__(self):
        if self.handCards == []:
            return "Hand contains "
        else:
            string = ""
            for card in self.handCards:
                string += card + " "
            return "Hand contains " + string

    def add_card(self, card):
        self.handCards.append(card)
        self.handValue += VALUES.get(card.rank)
        if card.rank == "A":
            if self.handValue + 10 > 21:
                self.handValue += 10
        if self.handValue > 21:
            self.busted = True

    def get_value(self):
        return self.handValue

    def draw(self, canvas, pos):
        for card in self.handCards:
            if self.handCards.index(card) <= 4:
                card.draw(canvas, pos)
                pos[0] += 100
            else:
                self.removed = True

# define deck class 
class Deck:
    def __init__(self):
        self.deckCards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deckCards.append(card) 

    def shuffle(self):
        random.shuffle(self.deckCards)

    def deal_card(self):
        self.shuffle()
        suit = random.choice(SUITS)
        rank = random.choice(RANKS)
        card = Card(suit, rank)
        for element in self.deckCards:
            tmp = str(element)
            if tmp[0] == suit:
                if tmp[-1] == rank:
                    self.deckCards.remove(element)
        return card

    def __str__(self):
        string = ""
        for card in self.deckCards:
            string += card + " "
        return "Deck contains " + string

#define event handlers for buttons
def deal():
    global outcome, in_play
    global Player, Dealer, cardDeck
    if in_play:
        game_over("Dealer","")
    cardDeck = Deck()
    Player = Hand()
    Dealer = Hand()
    for i in range(2):
        Player.add_card(cardDeck.deal_card())
        Dealer.add_card(cardDeck.deal_card())
    outcome = "Hit or Stand?"
    in_play = True

def hit():
    if in_play:
        if not Player.busted:
            Player.add_card(cardDeck.deal_card())
        if Player.busted:
            game_over("Dealer","busted")
       
def stand():
    if in_play:
        if Player.busted:
            game_over("Dealer", "busted")
        else:
            while Dealer.handValue < 17:
                Dealer.add_card(cardDeck.deal_card())
            if Dealer.busted:
                game_over("Player", "busted")
            else:
                if Dealer.handValue >= Player.handValue:
                    game_over("Dealer","")
                else:
                    game_over("Player","")

# draw handler    
def draw(canvas):
    canvas.draw_text('Blackjack', (50, 100), 60, '00FFFF')
    canvas.draw_text('Score  ' + str(score), (375, 100), 40, 'Black')
    canvas.draw_text('Dealer', (50, 200), 40, 'Black')
    Dealer.draw(canvas,[50, 225])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [50 + CARD_BACK_CENTER[0], 225 + CARD_BACK_CENTER[1]], 
                          CARD_BACK_SIZE)
    if Dealer.removed:
        canvas.draw_text('Only first 5 cards shown', 
                         (175, 350), 20, 'Black')
    canvas.draw_text('Player', (50, 400), 40, 'Black')
    canvas.draw_text(outcome, (175, 400), 40, 'Black')
    Player.draw(canvas,[50, 425])
    if Player.removed:
        canvas.draw_text('Only first 5 cards shown', (175, 550), 20, 'Black')

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
