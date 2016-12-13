"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list2 = []
    idx = 1
    if len(list1) > 0:
        list2.append(list1[0])
        while idx < len(list1):
            if list1[idx] != list1[idx-1]:
                if list1[idx] < list1[idx-1]:
                    return
                list2.append(list1[idx])
            idx += 1
    return list2

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list3 = []
    copy2 = list(list2)
    idx = 0
    while idx < len(list1):
        if list1[idx] in copy2:
            list3.append(list1[idx])
            copy2.remove(list1[idx])
        idx += 1    
    return list3

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    list3 = []
    copy1 = list(list1)
    copy2 = list(list2)
    while len(copy1 + copy2) > 0:
        if copy1 == []:
            list3.extend(copy2)
            return list3
        if copy2 == []:
            list3.extend(copy1)
            return list3
        if copy1[0] < copy2[0]:
            list3.append(copy1[0])
            del copy1[0]
        else:
            list3.append(copy2[0])
            del copy2[0]
    return list3
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    
    mid = len(list1) / 2
    
    return merge(merge_sort(list1[:mid]), merge_sort(list1[mid:]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if not word:
        return [""]
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    new_strings = [string[:position] + first + string[position:] 
                   for string in rest_strings 
                   for position in range(len(string) + 1)]
    rest_strings.extend(new_strings)
    return rest_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    net_file = urllib2.urlopen(codeskulptor.file2url(filename))
    return net_file.read().split('\n')

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

# TESTS
# Test remove_duplicates(list1)
print remove_duplicates([1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8])
print remove_duplicates([1])
print remove_duplicates([])
print remove_duplicates([1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3])
print remove_duplicates([1, 1, 2, 2, 1])
print remove_duplicates([1, 1, 2, 2])
print ""

# Test intersect(list1, list2)
print intersect([1, 2, 3, 4], [2, 4, 5])
print intersect([1, 2, 3, 4, 4], [2, 4, 5])
print intersect([1, 2, 3, 4, 4], [2, 2, 4, 5])
print intersect([1, 2, 3, 4, 4], [2, 4, 4, 5])
print intersect([1, 3, 4, 4], [2, 5])
print intersect([], [1, 2, 3])
print ""

# Test merge(list1, list2)
print merge([1, 2, 3, 4], [2, 4, 5])
print merge([1, 2, 3, 4, 4], [2, 4, 5])
print merge([1, 2, 3, 4, 4], [2, 2, 4, 5])
print merge([1, 2, 3, 4, 4], [2, 4, 4, 5])
print merge([1, 3, 4, 4], [2, 5])
print merge([], [1, 2, 3])
print merge([], [])
print ""

# Test merge_sort(list1)
print merge_sort([1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 7, 8])
print merge_sort([1])
print merge_sort([])
print merge_sort([1, 1, 1, 1, 1, 2, 3, 3, 3, 3, 3])
print merge_sort([1, 1, 2, 2, 1])
print merge_sort([1, 1, 2, 2])
print ""

# Test gen_all_strings(word)
print gen_all_strings("")
print gen_all_strings("a")
print gen_all_strings("ab")
print gen_all_strings("abc")