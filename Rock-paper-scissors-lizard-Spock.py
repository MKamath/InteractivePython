# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

import random

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
    """ This calls various functions, and essentially 
        contains on the flow of the program """
    # Prints a blank line to separate consecutive games
    print " "
    
    # Prints out the message for the player's choice
    print "Player chooses", player_choice
    
    # Converts the player's choice to player_number 
    # using the function name_to_number()
    player_number = name_to_number(player_choice)
    
    # Computes random guess for comp_number 
    # using random.randrange()
    computer_number = random.randrange(0, 5)
    
    # Converts computer_number to computer_choice 
    # using the function number_to_name()
    computer_choice = number_to_name(computer_number)
    
    # Prints out the message for computer's choice
    print "Computer chooses", computer_choice
    
    # Computes difference of computer_number 
    # and player_number modulo five and uses it to
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

# test your code - LEAVE THESE CALLS IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
