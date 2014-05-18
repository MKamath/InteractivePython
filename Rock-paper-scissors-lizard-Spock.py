# Title:- Rock-paper-scissors-lizard-Spock

# Description :- 
# Rock-paper-scissors is a hand game that is played by two people. The players count to three
# in unison and simultaneously "throw” one of three hand signals that correspond to rock, paper
# or scissors. The winner is determined by the rules:
# 
# 1. Rock smashes scissors
# 2. Scissors cuts paper
# 3. Paper covers rock
#
# Rock-paper-scissors is a surprisingly popular game that many people play seriously. Due to
# the fact that a tie happens around 1/3 of the time, several variants of Rock-Paper-Scissors
# exist that include more choices to make ties less likely.
# 
# Rock-paper-scissors-lizard-Spock (RPSLS) is a variant of Rock-paper-scissors that allows five
# choices. Each choice wins against two other choices, loses against two other choices and ties
# against itself. Much of RPSLS's popularity is that it has been featured in 3 episodes of the 
# TV series "The Big Bang Theory". 
# 
# In our first mini-project, we will build a Python function rpsls(name) that takes as input
# the string name, which is one of "rock", "paper", "scissors", "lizard", or "Spock". 
# The function then simulates playing a round of Rock-paper-scissors-lizard-Spock by generating
# its own random choice from these alternatives and then determining the winner using a
# simple rule that we will next describe.
# 
# While Rock-paper-scissor-lizard-Spock has a set of ten rules that logically determine who wins
# a round of RPSLS, coding up these rules would require a large number (5x5=25) of if/elif/else
# clauses in your mini-project code. A simpler method for determining the winner is to assign
# each of the five choices a number:
# 
# 0 — rock
# 1 — Spock
# 2 — paper
# 3 — lizard
# 4 — scissors
#
# In this expanded list, each choice wins against the preceding two choices and loses against 
# the following two choices (if rock and scissors are thought of as being adjacent using modular
# arithmetic).

import random

# helper functions
def name_to_number(name):
    """ This returns the number equated to the string """
    if name == 'rock':
        return 0
   
    elif name == 'Spock':
        return 1
    
    elif name == 'paper':
        return 2
    
    elif name == 'lizard':
        return 3
    
    elif name == 'scissors':
        return 4
    
    else:
        print "Error in function: name_to_number"
        print "name:", name
        return None

def number_to_name(number):
    """ This returns the number equated to the string """
    if number == 0:
        return 'rock'
    
    elif number == 1:
        return 'Spock'
    
    elif number == 2:
        return 'paper'
    
    elif number == 3:
        return 'lizard'
    
    elif number == 4:
        return 'scissors'
    
    else:
        print "Error in function: number_to_name"
        print "number:", number
        return None

def rpsls(player_choice): 
    """ This calls various functions, and essentially contains the flow of the program """
    # Prints a blank line to separate consecutive games
    print " "
    
    # Prints out the message for the player's choice
    print "Player chooses", player_choice
    
    # Converts the player's choice to player_number 
    # using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # Computes random guess for comp_number using random.randrange()
    computer_number = random.randrange(0, 5)
    
    # Converts computer_number to computer_choice using the function number_to_name()
    computer_choice = number_to_name(computer_number)
    
    # Prints out the message for computer's choice
    print "Computer chooses", computer_choice
    
    # Computes difference of computer_number and player_number modulo five and uses it to
    # determine winner and print winner message
    if (player_number - computer_number) % 5  == 0:
        print "Player and computer tie!"
    
    elif (player_number - computer_number) % 5 <= 2:
        print "Player wins!"
    
    elif (player_number - computer_number) % 5 >= 3:
        print "Computer wins!"
    
    else:
        print "Error in function: rpsls"
        print "player_number:", player_number
        print "computer_number:", computer_number    

# Test for code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
