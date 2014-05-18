# Title - Memory

# Description :- 
# This is an implementation of the card game Memory, in which we use numbers in place of
# actual cards

import simplegui
import random

# helper function to initialize globals
def new_game():
    """ Initializes a new game """
    global state, deck_of_cards, exposed, turns, choice
    
    state = 0
    turns = 0
    deck_of_cards = range(16)
    random.shuffle(deck_of_cards)
    exposed = []
    choice = []
    
    for i in range(len(deck_of_cards)):
        exposed.append(False)
        
        if deck_of_cards[i] >= 8:
            deck_of_cards[i] -= 8

# event handlers
def mouseclick(pos):
    """ Mouse Click Handler """
    global state, turns, choice, exposed
    
    if pos[0]//50 not in choice: 
    
        if state == 0:
            """ Initially, no cards are exposed yet """
            choice.append(pos[0]//50)
            exposed[pos[0]//50] = True
            state += 1
        
        elif state == 1:
            """ One card has been exposed, so we add that to the list """
            choice.append(pos[0]//50)
            exposed[pos[0]//50] = True
            state += 1
        
        else:
            """ Two cards are exposed, we check if those cards are the same """
            if deck_of_cards[choice[-1]] != deck_of_cards[choice[-2]]:
                exposed[choice[-1]] = False
                exposed[choice[-2]] = False
                choice.pop()
                choice.pop()
            
            state = 1
            turns += 1
            exposed[pos[0]//50] = True
            choice.append(pos[0]//50)

# cards are logically 50x100 pixels in size    
def draw(canvas):
    """ Draw the exposed numbers and cards """
    label.set_text("Turns = " + str(turns))
    
    for i in range(len(deck_of_cards)):
    
        if exposed[i] == False:
            canvas.draw_polygon([(50*i, 0), (50*(i + 1), 0), 
                                 (50*(i + 1), 100),(50*i, 100)], 3, "White", "Blue");
        
        else:
            canvas.draw_text(str(deck_of_cards[i]),[(50*i) + 5, 75], 60, "White");
    
    if exposed.count(True) == len(exposed):
        label.set_text("You win! Turns required = " + str(turns))

# creating the frame and adding button & labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# registering the event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()