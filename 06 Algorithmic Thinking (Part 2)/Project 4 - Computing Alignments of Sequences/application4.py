# Application #4 - Applications to Genomics and Beyond
'''
In Project 4, you implemented dynamic programming algorithms for determining 
both global and local alignments of pairs of sequences. In this Application, we 
will demonstrate the utility of these algorithms in two domains. In the first 
part of the Application, we examine an interesting problem from genomics. 
(This is based on "Introduction to Computational Genomics", by Nello 
Cristianini and Matthew W. Hahn). We will compare two sequences that have 
diverged from a common ancestor sequence due to mutation. (Mutation here 
includes base-pair substitution, which changes the sequence content, and 
insertion/deletion, which change the sequence lengths.) In the second part of 
the Application, we consider words that have spelling mistakes.
'''


import project4
import alg_application4_provided as provided
import random
import matplotlib.pyplot as plt
import urllib2



def question_1():
    '''
    First, load the files HumanEyelessProtein and FruitflyEyelessProtein using 
    the provided code. These files contain the amino acid sequences that form 
    the eyeless proteins in the human and fruit fly genomes, respectively. Then 
    load the scoring matrix PAM50 for sequences of amino acids. This scoring 
    matrix is defined over the alphabet {A,R,N,D,C,Q,E,G,H,I,L,K,M,F,P,S,T,W,Y,
    V,B,Z,X,-} which represents all possible amino acids and gaps (the "dashes" 
    in the alignment).

    Next, compute the local alignments of the sequences of HumanEyelessProtein 
    and FruitflyEyelessProtein using the PAM50 scoring matrix and enter the 
    score and local alignments for these two sequences below. Be sure to 
    clearly distinguish which alignment is which and include any dashes ('-') 
    that might appear in the local alignment.
    '''
    
    human_protein = provided.read_protein(provided.HUMAN_EYELESS_URL)
    fruitfly_protein = provided.read_protein(provided.FRUITFLY_EYELESS_URL)
    scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
    
    alignment_matrix = project4.compute_alignment_matrix(human_protein,
                                                         fruitfly_protein,
                                                         scoring_matrix,
                                                         False)
    
    local_alignment = project4.compute_local_alignment(human_protein, 
                                                       fruitfly_protein,
                                                       scoring_matrix, 
                                                       alignment_matrix)
    return local_alignment
    

def compute_similarity(str1, str2):
    '''
    Helper function for Question 2
    '''
    
    count = 0
    length = len(str1)
    for idx in range(length):
        if str1[idx] == str2[idx]:
            count += 1
    
    return 100* float(count) / length

    
    
def question_2():
    '''
    To continue our investigation, we next consider the similarity of the two 
    sequences in the local alignment computed in Question 1 to a third 
    sequence. The file ConsensusPAXDomain contains a "consensus" sequence of 
    the PAX domain; that is, the sequence of amino acids in the PAX domain in 
    any organism. In this problem, we will compare each of the two sequences of 
    the local alignment computed in Question 1 to this consensus sequence to 
    determine whether they correspond to the PAX domain.
    '''
    
    consensus = provided.read_protein(provided.CONSENSUS_PAX_URL)
    score, human_alignment, fruitfly_alignment = question_1()
    scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
    
    # Delete any dashes '-' present in the sequence
    human = human_alignment.replace('-', '')
    fruitfly = fruitfly_alignment.replace('-', '')
    
    # Compute the global alignment of this dash-less sequence with the 
    # ConsensusPAXDomain sequence.
    alignment_matrix_human = project4.compute_alignment_matrix(human,
                                                         consensus,
                                                         scoring_matrix,
                                                         True)
    human_global = project4.compute_global_alignment(human,
                                                     consensus,
                                                     scoring_matrix,
                                                     alignment_matrix_human)
    
    alignment_matrix_fruitfly = project4.compute_alignment_matrix(fruitfly, 
                                                                  consensus,
                                                                  scoring_matrix,
                                                                  True)
    fruitfly_global = project4.compute_global_alignment(fruitfly,
                                                        consensus,
                                                        scoring_matrix,
                                                        alignment_matrix_fruitfly)
    
    # Compare corresponding elements of these two globally-aligned sequences 
    # (local vs. consensus) and compute the percentage of elements in these two 
    # sequences that agree.
    human_similarity = compute_similarity(human_global[1], human_global[2])
    fruitfly_similarity = compute_similarity(fruitfly_global[1], fruitfly_global[2])
    
    
    return 'Human:',  human_similarity, 'Fruitfly:', fruitfly_similarity
    
    
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    '''
    Helper function for Question 4
    Takes as input two sequences seq_x and seq_y, a scoring matrix 
    scoring_matrix, and a number of trials num_trials. This function should 
    return a dictionary scoring_distribution that represents an un-normalized 
    distribution generated by performing the following process num_trials times:

    Generate a random permutation rand_y of the sequence seq_y using 
    random.shuffle().
    Compute the maximum value score for the local alignment of seq_x and rand_y 
    using the score matrix scoring_matrix.
    Increment the entry score in the dictionary scoring_distribution by one.
    '''
    
    scoring_distribution = {}
    trial = 0
        
    while trial < num_trials:
        seq_y_list = list(seq_y)
        random.shuffle(seq_y_list)
        rand_y = ''.join(seq_y_list)
        alignment_matrix = project4.compute_alignment_matrix(seq_x, rand_y, 
                                                             scoring_matrix, 
                                                             False)
        score = project4.compute_local_alignment(seq_x, 
                                                 rand_y, 
                                                 scoring_matrix, 
                                                 alignment_matrix)
        if score[0] not in scoring_distribution:
            scoring_distribution[score[0]] = 1
        else:
            scoring_distribution[score[0]] += 1
        trial += 1
        print trial

    return scoring_distribution
    
    
def question_4():
    '''
    We will take an approach known as statistical hypothesis testing to 
    determine whether the local alignments computed in Question 1 are 
    statistically significant (that is, that the probability that they could 
    have arisen by chance is extremely small).
    '''
    
    # Use the function generate_null_distribution to create a distribution with 
    # 1000 trials using the protein sequences HumanEyelessProtein and 
    # FruitflyEyelessProtein (using the PAM50 scoring matrix). 
    
    human_protein = provided.read_protein(provided.HUMAN_EYELESS_URL)
    fruitfly_protein = provided.read_protein(provided.FRUITFLY_EYELESS_URL)
    scoring_matrix = provided.read_scoring_matrix(provided.PAM50_URL)
    
    num_trials = 1000
    
    distribution = generate_null_distribution(human_protein, fruitfly_protein,
                                              scoring_matrix, num_trials)
    
    # Next, create a bar plot of the normalized version of this distribution. 
    # The horizontal axis should be the scores and the vertical axis should be 
    # the fraction of total trials corresponding to each score. As usual, 
    # choose reasonable labels for the axes and title. 
    
    normalized_dist = {}
    for score in distribution:
        normalized_dist[score] = float(distribution[score])/num_trials
    
    plt.bar(normalized_dist.keys(), normalized_dist.values())
    plt.title('Null Distribution for Hypothesis Testing using 1000 Trials')
    plt.xlabel('Local Alignment Scores')
    plt.ylabel('Fraction of Total Trials')
    plt.show()
    
    return distribution
    
    
def question_5():
    '''
    Given the distribution computed in Question 4, we can do some very basic 
    statistical analysis of this distribution to help us understand how likely 
    the local alignment score from Question 1 is.
    '''
    
    # compute mean
    sum_scores = 0
    count_scores = 0
    for score in distribution:        
        sum_scores += score * distribution[score]
        count_scores += distribution[score]
    mean = float(sum_scores) / count_scores
    print "mean", mean
    
    # compute standard deviation
    sum_scores = 0
    for score in distribution:
        sum_scores += distribution[score] * ((score - mean) ** 2) 
    std_dev = float(sum_scores / count_scores) ** (0.5)
    print "standard deviation", std_dev
    
    # compute z-score for the human eyeless protein vs the fruitfly eyeless protein
    local_alignment = question_1()
    z_score = (local_alignment[0] - mean) / std_dev

    return "Mean:", mean, "Standard Deviation:", std_dev, "Z-score:", z_score
    
    
def edit_dist(xs, ys):
    '''
    Helper function for Question 8
    '''
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    scoring = project4.build_scoring_matrix(alphabet, 2, 1, 0)
    align = project4.compute_alignment_matrix(xs, ys, scoring, True)
    score, x, y = project4.compute_global_alignment(xs, ys, scoring, align)
    return len(xs) + len(ys) - score
    
    
def check_spelling(checked_word, dist, word_list):
    '''
    Helper function for Question 8
    '''
    
    return set([word for word in word_list
                if edit_dist(checked_word, word) <= dist])


def question_8():
    #dist = edit_dist('abb', 'aa')
    #print(dist)
    word_list = urllib2.urlopen('http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt')
    words = [x.strip() for x in word_list.readlines()]
    humble = check_spelling('humble', 1, words)
    firefly = check_spelling('firefly', 2, words)
    print(len(humble), humble)
    print(len(firefly), firefly)
    
    
    
#print question_1()
#print question_2()
distribution = question_4()
print distribution
print question_5()
#print question_8()