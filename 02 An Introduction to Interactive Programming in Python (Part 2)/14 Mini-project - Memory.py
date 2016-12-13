# implementation of card game - Memory

import simplegui
import random

deck = list()
counter = 0


# helper function to initialize globals
def new_game():
    global deck, exposed, state, card1, card2, counter
    deck = 2* range(0, 8)
    exposed = [False] * 16
    state = 0
    card1 = 0
    card2 = 0
    counter = 0
    random.shuffle(deck)
    label.set_text('Turns = ' + str(counter))
    
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1, card2, counter
    if state == 0 :
        exposed[pos[0] // 50] = True
        card1 = pos[0] // 50
        state = 1
    elif state == 1:
        if not exposed[pos[0] // 50] :
            exposed[pos[0] // 50] = True
            card2 = pos[0] // 50
            state = 2
            counter += 1
            label.set_text('Turns = ' + str(counter))
    else:
        if not exposed[pos[0] // 50] :
            exposed[pos[0] // 50] = True
            if deck[card1] != deck[card2] :
                exposed[card1] = False
                exposed[card2] = False
            card1 = pos[0] // 50
            state = 1
    
    return pos[0] // 50
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i, card in enumerate(deck) :
        if exposed[i] :
            canvas.draw_text(str(card), [50 * i + 5, 80], 80, "White")
        else:
            canvas.draw_polygon([[50 * i, 0], [50 * i + 50, 0],
            [50 * i + 50, 100], [50 * i, 100]], 1, "Grey", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric