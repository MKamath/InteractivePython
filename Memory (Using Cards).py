# Title - Memory (Using Cards)

# Description :- 
# This is an implementation of the card game Memory.

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initializing global variables
state = ""
turns = 0

# defining globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')

# defining card class
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
    
    def draw(self, canvas, pos, n):
        if n in cardSelected:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], 
                              CARD_SIZE)
        else:
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                              [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

# defining hand class
class Hand:
    def __init__(self):
        self.handCards = []
        
    def __str__(self):
        string = ""
        
        if self.handCards != []:
            for card in self.handCards:
                string += str(card) + " "
                
        return "Cards in deck are " + string

    def add_cards(self, cardList):
        for card in cardList:
            self.handCards.append(card)
        
    def shuffle(self):
        random.shuffle(self.handCards)

    def draw(self, canvas, pos):
        n = 0
        for card in self.handCards:
            n += 1
            card.draw(canvas, pos, n)
            if n%4 == 0:
                pos[0] = 10
                pos[1] += 110
            else:
                pos[0] += 100
                

class Deck:
    def __init__(self):
        self.deckCards = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deckCards.append(card) 

    def __str__(self):
        string = ""
        
        for card in self.deckCards:
            string += str(card) + " "
        
        return "Deck contains " + string
    
    def deal_cards(self):
        card = random.choice(self.deckCards)
        cardList = []
        cardList.append(card)
        cardList.append(card)
        self.deckCards.remove(card)
        return cardList

#defining event handlers for buttons
def create_deck():
    global Player, cardDict
    
    Player = Hand()
    cardDeck = Deck()
    cardDict = {}
    
    while len(Player.handCards) < 16:
        Player.add_cards(cardDeck.deal_cards())
     
    Player.shuffle()
    Player.shuffle()
    
    i = 1
    for card in Player.handCards:
        cardDict[i] = [str(card), 0]
        i += 1

def new_game():
    """ Event Handler for button :- Reset """
    global state, turns, cardSelected
    
    create_deck()
    state = 0
    turns = 0
    cardSelected = []
    frame.start()
    
def exposer(click_loc):
    pos = [10, 10]
    n = 1
    added_card = False
    
    for i in range(4):
        if not added_card:
            if (click_loc[1] > pos[1]) and (click_loc[1] < (pos[1] + 98)):
                for j in range(4):
                    if (click_loc[0] > pos[0]) and (click_loc[0] < (pos[0] + 73)):
                        if n not in cardSelected:
                            new_choice = n
                            added_card = True
                            break
                    else:
                        pos[0] += 100
                        n += 1
            else:
                n += 4
                pos[1] += 110
        else:
            break
    
    if added_card:
        game_logic(new_choice)
    
def game_logic(new_choice):
    global state, turns, cardSelected
    
    if state <= 1:
        cardSelected.append(new_choice)
        state += 1
        
    else:
        """ Two cards are exposed, we check if those cards are the same """
        if cardDict[cardSelected[-1]] != cardDict[cardSelected[-2]]:
            cardSelected.pop()
            cardSelected.pop()
            
        cardSelected.append(new_choice)
        state = 1
        turns += 1

def draw(canvas):
    """ This is the draw handler """
    if len(cardSelected) == 16:
        label.set_text("You Win! Turns taken = " + str(turns))
    else:
        label.set_text("Turns = " + str(turns))
    Player.draw(canvas, [10, 10])

# initializing the frame
frame = simplegui.create_frame("Blackjack", 395, 450)
label = frame.add_label("Turns = 0")

#creating buttons and canvas callback
frame.set_mouseclick_handler(exposer)
frame.add_button("Reset", new_game, 200)
frame.set_draw_handler(draw)

# get things rolling
new_game()
