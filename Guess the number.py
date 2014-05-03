# Title :- Guess the Number
# Input :- Buttons and an input field
# Output :- Printed in the console
import simplegui
import random

# initialize global variables used in your code
answer = 0
range_value = 100
no_of_guess = 7
range_100 = True
range_1000 = False

# helper function to start and restart the game
def new_game():
    global answer
    global range_value
    global no_of_guess
    if range_100:
        answer = random.randrange(0, 100)
        range_value = 100
        no_of_guess = 7
    elif range_1000:
        answer = random.randrange(0, 1000)
        range_value = 1000
        no_of_guess = 10        
    print "New game. Range from 0 to", range_value
    print "Number of remaining guesses is", no_of_guess
    print " "

# define event handlers for control panel
def range100():
    """ button that changes range to range [0,100) 
    and restarts """
    global range_100
    global range_1000
    range_100 = True
    range_1000 = False
    new_game()

def range1000():
    """ button that changes range to range [0,1000) 
    and restarts """
    global range_100
    global range_1000
    range_100 = False
    range_1000 = True
    new_game()

def input_guess(guess):
    """ Main Game Logic """
    global no_of_guess
    player_guess = int(guess)
    no_of_guess -= 1
    if player_guess == answer:
        print "Correct!"
        print " "
        new_game()
    elif no_of_guess > 0:
        print "Guess was", player_guess
        print "Number of remaining guesses is", no_of_guess
        if player_guess > answer :
            print "Lower!"
            print " "
        else:
            print "Higher!"
            print " "
    elif no_of_guess == 0:
        print "You ran out of guesses. The answer is", answer
        print " "
        new_game()

# create frame
f = simplegui.create_frame("Guess the Number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0 to 100)", range100, 200)
f.add_button("Range is [0 to 1000)", range1000, 200)
f.add_input("Enter a guess:", input_guess, 200)

# call new_game and start frame
new_game()
f.start()