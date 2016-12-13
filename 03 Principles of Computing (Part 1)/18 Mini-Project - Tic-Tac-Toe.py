"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by 
    making random moves, alternating between players. The function 
    should return when the game is over. The modified board will 
    contain the state of the game, so the function does not return 
    anything. In other words, the function should modify the board input.
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        select_square = random.choice(empty_squares)
        board.move(select_square[0], select_square[1], player)
        player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the 
    same dimensions as the Tic-Tac-Toe board, a board from a completed 
    game, and which player the machine player is. The function should 
    score the completed board and update the scores grid. As the function 
    updates the scores grid directly, it does not return anything.
    """
    winner = board.check_win()
    dim = board.get_dim()
    # set score values depending upon the winner
    if player == winner:
        score_current = SCORE_CURRENT
        score_other = -SCORE_OTHER
    else:
        score_current = -SCORE_CURRENT
        score_other = SCORE_OTHER
    
    # score the board and update scores list
    if winner != provided.DRAW:
        for row in range(dim):
            for col in range(dim):
                if board.square(row, col) == player:
                    scores[row][col] += score_current
                elif board.square(row, col) == provided.switch_player(player):
                    scores[row][col] += score_other

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function 
    should find all of the empty squares with the maximum score and 
    randomly return one of them as a (row, column) tuple. It is an 
    error to call this function with a board that has no empty squares 
    (there is no possible next move), so your function may do whatever 
    it wants in that case. The case where the board is full will not be 
    tested.
    """
    empty_squares = board.get_empty_squares()
    score_list = list()
    
    # find the top score of all empty squares
    for square in empty_squares:
        score_list.append(scores[square[0]][square[1]])
    
    top_score = max(score_list)
    
    # find all squares with top score, randomly choose one
    best_moves = list()
    for square in empty_squares:
        if scores[square[0]][square[1]] == top_score:
            best_moves.append(square)
            
    if len(best_moves) > 1:
        move = random.choice(best_moves)
    elif len(best_moves) == 1:
        move = best_moves[0]
    else :
        pass
    
    return(move)


def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player 
    is, and the number of trials to run. The function should use the 
    Monte Carlo simulation described above to return a move for the 
    machine player in the form of a (row, column) tuple. Be sure to 
    use the other functions you have written!
    """
    # initialize empty scores list
    dim = board.get_dim()
    scores = [[0 for _col in range(dim)] 
                for _row in range(dim)]
    
    # run n number of trials, update scores list
    for _ in range(trials):
        trial = board.clone()
        mc_trial(trial, player)
        mc_update_scores(scores, trial, player)
    
    return get_best_move(board, scores)

# # Testing code
# test_game = provided.TTTBoard(3)
# test_dim = test_game.get_dim()
# test_scores = [[0 for emptycol in range(test_dim)] 
               # for emptyrow in range(test_dim)]

# # test mc_trial()
# mc_trial(test_game, provided.PLAYERX)
# print str(test_game)
# print "Winner:", test_game.check_win(), "\n"

# # test mc_update_scores
# mc_update_scores(test_scores, test_game, provided.PLAYERX)
# print "Scores:"
# for row in test_scores:
    # print row

# # test mc_get_best_move
# test_scores = [[-2.0, -1.0, -1.0], 
                # [-1.0, 2.0, -2.0], 
                # [2.0, 3.0, -2.0]]
# move = get_best_move(test_game, test_scores)
# print str(test_game)

# # test mc_move()
# mc_move(test_game, provided.PLAYERX, NTRIALS)
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
