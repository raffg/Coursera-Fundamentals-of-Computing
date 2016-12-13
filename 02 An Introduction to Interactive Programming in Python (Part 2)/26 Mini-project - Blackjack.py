# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
deck = []
in_play = False
outcome = ""
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
            # create Hand object
        self.hand = []

    def __str__(self):
            # return a string representation of a hand
        string = "Hand Contains "
        for cards in self.hand:
            string += str(cards) + " "
        return string

    def add_card(self, card):
            # add a card object to a hand
        self.hand.append(card)       

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
            # compute the value of the hand, see Blackjack video
        hand_value = 0
        has_ace = False
        for card in self.hand:
            if card.get_rank() == 'A':
                has_ace = True 
        
        for card in self.hand :
            hand_value += VALUES[card.get_rank()]
        
        if has_ace and hand_value <= 11 :
            hand_value += 10
        return hand_value
        
   
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards
        for card in self.hand :
            card.draw(canvas, pos)
            pos[0] += 100
        
# define deck class 
class Deck:
    def __init__(self):
            # create a Deck object
        self.deck = []
        for suit in SUITS :
            for rank in RANKS :
                self.deck.append(Card(suit, rank))
           
    def shuffle(self):
        # shuffle the deck 
            # use random.shuffle()
        return (random.shuffle(self.deck))
            
    def deal_card(self):
            # deal a card object from the deck
        return self.deck.pop(random.choice(range(len(self.deck))))
    
    def __str__(self):
            # return a string representing the deck
        string = "Deck Contains "
        for cards in self.deck:
            string += str(cards) + " "
        return string


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, dealer_score
    
    deck = Deck()
    deck.shuffle()
        
    player_hand = Hand()
    dealer_hand = Hand()
        
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    if in_play :
        outcome = "Player forfeits and loses the round."
        dealer_score += 1
        in_play = True
    
    else:        
        outcome = "Hit or stand?"
        in_play = True
    
#    print "Player's", player_hand, ", value:", player_hand.get_value()
#    print "Dealer's", dealer_hand, ", value:", dealer_hand.get_value()
        

def hit():
    global outcome, in_play, player_score, dealer_score, player_hand
        # replace with your code below
 
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    if in_play :
        if player_hand.get_value() <= 21 :
            player_hand.add_card(deck.deal_card())
#            print "Player's", player_hand, ", value:", player_hand.get_value()
            
        if player_hand.get_value() > 21 :
            in_play = False
            outcome = "You have busted. Dealer wins. Deal again?"
            dealer_score += 1
#            print outcome
#            print ""
       
def stand():
    global outcome, in_play, player_score, dealer_score, player_hand, dealer_hand
        # replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    
    
    if player_hand.get_value() > 21 :
        outcome = "You have already busted. Deal again?"
#        print "You have already busted"
        in_play = False
        
    else :
        while dealer_hand.get_value() < 17 :
            dealer_hand.add_card(deck.deal_card())
#            print "Dealer's", dealer_hand, ", value:", dealer_hand.get_value()
        if in_play :
            if dealer_hand.get_value() > 21 :
                outcome = "Dealer has busted. You win! Deal again?"
                player_score += 1
                in_play = False
#                print "Dealer has busted"
#                print outcome
#                print ""
            elif player_hand.get_value() <= dealer_hand.get_value() :
                outcome = "Dealer wins. Deal again?"
                dealer_score += 1
                in_play = False
#                print outcome
#                print ""
            else :
                outcome = "You win! Deal again?"
                player_score += 1
                in_play = False
#                print outcome
#                print ""


# draw handler    
def draw(canvas):
    global player_score, dealer_score
    # test to make sure that card.draw works, replace with your code below
    
    canvas.draw_text('Blackjack', [100, 75], 50, 'White')
    
    canvas.draw_text('Dealer:' + str(dealer_score), [100, 180], 30, 'Black')
    dealer_hand.draw(canvas, [100, 200])
    
    canvas.draw_text('Player:' + str(player_score), [100, 380], 30, 'Black')
    player_hand.draw(canvas, [100, 400])
    
    canvas.draw_text(outcome, [10, 125], 30 ,"White")
    
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [136, 249], CARD_BACK_SIZE)


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


# remember to review the gradic rubric