# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

remaining = 7
range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, remaining
    secret_number = random.randrange(0, range)
    if range == 100:
        remaining = 7
    else:
        remaining = 10
    
    print "----------------------------------"
    print "New game started"
    print "Range is from 0 to", range
    print "Number of remaining guesses is", remaining
    print ""

    # define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global range
    range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global range
    range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global remaining, num_guesses
    print "Guess was", int(guess)
    if int(guess) == secret_number:
        print "Correct"
        print ""
        new_game()
    elif int(guess) > secret_number:
        print "Lower"
        remaining -= 1
        print "Number of guesses remaining is", remaining
        print ""

    else:
        print "Higher"
        remaining -= 1
        print "Number of guesses remaining is", remaining
        print ""
    
    if remaining == 0:
        print "Sorry, you ran out of guesses"
        print "You lose. The secret number was", secret_number
        print "New game beginning"
        print ""
        new_game()

    
# create frame
f = simplegui.create_frame('Guess the Number', 300, 300)

# register event handlers for control elements and start frame
f.add_button("Range is [0,100)", range100, 200)
f.add_button("Range is [0,1000)", range1000, 200)
f.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
