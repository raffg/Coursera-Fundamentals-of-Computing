'''
In Project 4, we will implement four functions. The first pair of functions 
will return matrices that we will use in computing the alignment of two 
sequences. The second pair of functions will return global and local 
alignments of two input sequences based on a provided alignment matrix. You 
will then use these functions in Application 4 to analyze two problems 
involving comparison of similar sequences.
'''


def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    Takes as input a set of characters alphabet and three scores diag_score, 
    off_diag_score, and dash_score. The function returns a dictionary of 
    dictionaries whose entries are indexed by pairs of characters in alphabet 
    plus '-'. The score for any entry indexed by one or more dashes is 
    dash_score. The score for the remaining diagonal entries is diag_score. 
    Finally, the score for the remaining off-diagonal entries is 
    off_diag_score.
    '''

    scoring_matrix = {'-': {'-': dash_score}}

    for let_a in alphabet:
        if let_a not in scoring_matrix:
            scoring_matrix[let_a] = {}
        scoring_matrix[let_a]['-'] = dash_score
        scoring_matrix['-'][let_a] = dash_score

        for let_b in alphabet:
            if let_a == let_b:
                scoring_matrix[let_a][let_b] = diag_score
            else:
                scoring_matrix[let_a][let_b] = off_diag_score

    return scoring_matrix

    
def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common 
    alphabet with the scoring matrix scoring_matrix. The function computes and 
    returns the alignment matrix for seq_x and seq_y as described in the 
    Homework. If global_flag is True, each entry of the alignment matrix is 
    computed using the method described in Question 8 of the Homework. If 
    global_flag is False, each entry is computed using the method described in 
    Question 12 of the Homework.
    '''

    alignment = [[0 for dummycol in range(len(seq_y) + 1)] 
                    for dummyrow in range(len(seq_x) + 1)]
    
    for idx in range(1, len(seq_x) + 1):
        alignment[idx][0] = alignment[idx-1][0] + scoring_matrix[seq_x[idx-1]]['-']
        if global_flag == False and alignment[idx][0] < 0:
            alignment[idx][0] = 0
    for jdx in range(1, len(seq_y)+1):
        alignment[0][jdx] = alignment[0][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]]
        if global_flag == False and alignment[0][jdx] < 0:
            alignment[0][jdx] = 0
    for idx in range(1, len(seq_x)+1):
        for jdx in range(1, len(seq_y)+1):
            alignment[idx][jdx] = max(
                                      alignment[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]],
                                      alignment[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-'],
                                      alignment[idx][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]])
            if global_flag == False and alignment[idx][jdx] < 0:
                alignment[idx][jdx] = 0
    
    return alignment


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common 
    alphabet with the scoring matrix scoring_matrix. This function computes a 
    global alignment of seq_x and seq_y using the global alignment matrix 
    alignment_matrix.The function returns a tuple of the form (score, align_x, 
    align_y) where score is the score of the global alignment align_x and 
    align_y. Note that align_x and align_y should have the same length and may 
    include the padding character '-'.
    '''
    
    idx = len(seq_x)
    jdx = len(seq_y)
    seq_x_align = ''
    seq_y_align = ''
    
    while idx != 0 and jdx != 0:
        if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]]:
            seq_x_align = seq_x[idx-1] + seq_x_align
            seq_y_align = seq_y[jdx-1] + seq_y_align
            idx = idx - 1
            jdx = jdx - 1
        else:
            if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-']:
                seq_x_align = seq_x[idx-1] + seq_x_align
                seq_y_align = '-' + seq_y_align
                idx = idx - 1
            else:
                seq_x_align = '-' + seq_x_align
                seq_y_align = seq_y[jdx-1] + seq_y_align
                jdx = jdx - 1
    while idx != 0:
        seq_x_align = seq_x[idx-1] + seq_x_align
        seq_y_align = '-' + seq_y_align
        idx = idx - 1
    while jdx != 0:
        seq_x_align = '-' + seq_x_align
        seq_y_align = seq_y[jdx-1] + seq_y_align
        jdx = jdx -1
    return (alignment_matrix[len(seq_x)][len(seq_y)], seq_x_align, seq_y_align)

               
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    Takes as input two sequences seq_x and seq_y whose elements share a common 
    alphabet with the scoring matrix scoring_matrix. This function computes a 
    local alignment of seq_x and seq_y using the local alignment matrix 
    alignment_matrix.The function returns a tuple of the form (score, align_x, 
    align_y) where score is the score of the optimal local alignment align_x 
    and align_y. Note that align_x and align_y should have the same length and 
        may include the padding character '-'.
    '''
    
    # find location of maximum value in alignment matrix
    max_value = 0
    x_coord, y_coord = (0,0)
    for idx in range(1, len(seq_x)+1):
        for jdx in range(1, len(seq_y)+1):
            if alignment_matrix[idx][jdx] > max_value:
                max_value = alignment_matrix[idx][jdx]
                x_coord, y_coord = idx, jdx
    
    idx = x_coord
    jdx = y_coord
    seq_x_align = ''
    seq_y_align = ''
    while alignment_matrix[idx][jdx] != 0:
        if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]]:
            seq_x_align = seq_x[idx-1] + seq_x_align
            seq_y_align = seq_y[jdx-1] + seq_y_align
            idx = idx - 1
            jdx = jdx - 1
        else:
            if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-']:
                seq_x_align = seq_x[idx-1] + seq_x_align
                seq_y_align = '-' + seq_y_align
                idx = idx - 1
            else:
                seq_x_align = '-' + seq_x_align
                seq_y_align = seq_y[jdx-1] + seq_y_align
                jdx = jdx - 1
    
    return (max_value, seq_x_align, seq_y_align)         
    
def test1():
    """
    Test functions
    """
    testset = set(['a' ,'c', 't', 'g'])
    scoring_matrix = build_scoring_matrix(testset, 10, 4, -4)
    print 'Scoring Matrix'
    print scoring_matrix
    print ""
    alignment_matrix = compute_alignment_matrix("taat", "aa", scoring_matrix, True)
    print 'Alignment Matrix'
    print alignment_matrix
    print ""
    print 'Global Alignment'
    print compute_global_alignment('taat', 'aa', scoring_matrix, alignment_matrix)
    print ""
    alignment_matrix = compute_alignment_matrix("taat", "aa", scoring_matrix, False)
    print 'Alignment Matrix'
    print alignment_matrix
    print ""
    print 'Local Alignment'
    print compute_local_alignment('taat', 'aa', scoring_matrix, alignment_matrix)


def test2():
    """
    Test functions
    """
    testset = set(['a' ,'c', 't', 'g'])
    scoring_matrix = build_scoring_matrix(testset, 10, 4, -4)
    print scoring_matrix
    print ""
    alignment_matrix = compute_alignment_matrix("a", "a", scoring_matrix, True)
    print alignment_matrix
    print ""
    print compute_global_alignment("a", "a", scoring_matrix, alignment_matrix)
    print ""
    alignment_matrix = compute_alignment_matrix("ac", "ac", scoring_matrix, True)
    print alignment_matrix
    print ""
    print compute_global_alignment("ac", "ac", scoring_matrix, alignment_matrix)
    
#test1()
#test2()