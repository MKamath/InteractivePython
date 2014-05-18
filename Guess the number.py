# Title :- Guess the Number

# Description :- 
# One of the simplest two-player games is “Guess the number”. The first player thinks of a secret
# number in some known range while the second player attempts to guess the number. After each
# guess, the first player answers either “Higher”, “Lower” or “Correct!” depending on whether
# the secret number is higher, lower or equal to the guess. In this project, you will build a
# simple interactive program in Python where the computer will take the role of the first player
# while you play as the second player.
# 
# You will interact with your program using an input field and several buttons. For this project, 
# we will ignore the canvas and print the computer's responses in the console. Building an initial
# version of your project that prints information in the console is a development strategy that
# you should use in later projects as well. Focusing on getting the logic of the program correct
# before trying to make it display the information in some “nice” way on the canvas usually saves
# lots of time since debugging logic errors in graphical output can be tricky.

import simplegui
import random

# initialing global variables
answer = 0
range_value = 100
no_of_guess = 7
range_100 = True
range_1000 = False

# helper function to start and restart the game
def new_game():
    """ This will start a new game """
    global answer, range_value, no_of_guess
    
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

# event handlers for control panel
def range100():
    """ Event handler for button that changes range to range [0,100) and restarts """
    global range_100, range_1000
    
    range_100 = True
    range_1000 = False
    
    new_game()

def range1000():
    """ Event handler for button that changes range to range [0,1000) and restarts """
    global range_100, range_1000
    
    range_100 = False
    range_1000 = True
    
    new_game()

def input_guess(guess):
    """ This will compare the input given against the actual number, and decrement the counter
        for number of guesses for each wrong guess """
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

# creating a frame
f = simplegui.create_frame("Guess the Number", 200, 200)

# registering the event handlers for control elements
f.add_button("Range is [0 to 100)", range100, 200)
f.add_button("Range is [0 to 1000)", range1000, 200)
f.add_input("Enter a guess:", input_guess, 200)

# calling new_game and starting frame
new_game()
f.start()