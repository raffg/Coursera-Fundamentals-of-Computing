"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(40)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    return max([item * hand.count(item) for item in hand])

#    scores = list()
#	 for item in hand:
#        scores.append(item * hand.count(item))
#    return max(scores)

#    scores = list()
#    for idx in range(len(hand)):
#        value = 0
#        for die in hand:
#            if die == hand[idx]:
#                value += die
#        if value > max:
#            max = value
#    
#    return max

def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """

    permutations = list(gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)) 
    hands = [held_dice + permutation for permutation in permutations]
    scores = [score(hand) for hand in hands]
        
    return sum(scores) / float(len(hands))


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    
    answer_set = set([()])
    temp_set = set()
    for dummy_idx in range(len(hand)):
        for partial_sequence in answer_set:
            for item in hand:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                if new_sequence.count(item) <= hand.count(item):
                    temp_set.add(tuple(new_sequence))
        answer_set = set(temp_set)
    answer_set.add(tuple())
    
    return set([tuple(sorted(sequence)) for sequence in answer_set])


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    hands = gen_all_holds(hand)
    max_score = 0
    max_hand = tuple()
    for permutation in hands:
        if expected_value(permutation, num_die_sides, len(hand) - len(permutation)) > max_score:
            max_score = expected_value(permutation, num_die_sides, len(hand) - len(permutation))
            max_hand = permutation
    
    return (max_score, max_hand)

# # Testing area
# #
# # Testing score(hand)
# print score((1, 1, 2, 3, 4))
# print score((1, 1, 1, 1, 2))
# print score((1, 1, 2, 3, 1))
# print score((6, 4, 5, 4, 3))
# print score((6, 6, 6, 6, 6))
# print ""

# # Testing gen_all_holds(hand)
# import poc_holds_testsuite
# poc_holds_testsuite.run_suite(gen_all_holds)
# print ""

# # Testing expected_value(held_dice, num_die_sides, num_free_dice)
# print expected_value((1, 2, 3, 4), 6, 1)
# print expected_value((1, 1, 1, 1, 1), 6, 0)
# print expected_value((1, 1, 1, 1), 6, 1)
# print expected_value((1, 1, 1), 6, 2)
# print ""

# # Testing strategy(hand, num_die_sides)
# print strategy((6, 6, 6, 6, 6), 6)
# print strategy((1, 2, 3, 4, 5), 6)
# print strategy((1, 1, 1, 2, 2), 6)
# print strategy((2, 2, 2, 2, 2), 6)
# print ""


# def run_example(hand):
    # """
    # Compute the dice to hold and expected score for an example hand
    # """
    # num_die_sides = 6
    # hand_score, hold = strategy(hand, num_die_sides)
    # print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    
# run_example((1, 1, 1, 5, 6))
# run_example((1, 2, 3, 4, 5))
