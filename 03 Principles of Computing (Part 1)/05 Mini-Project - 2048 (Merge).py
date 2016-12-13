"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    new_line = [item for item in line if item] + [0]*line.count(0)
    for i in range(len(new_line)-1):
        if new_line[i] == new_line[i+1]:
            new_line[i] *= 2
            new_line[i+1] = 0
    new_line = [item for item in new_line if item] + [0]*new_line.count(0)
    return new_line


# print merge([2, 0, 2, 4])
# print "[4, 4, 0, 0]"
# print ""
# print merge([0, 0, 2, 2])
# print "[4, 0, 0, 0]"
# print ""
# print merge([2, 2, 0, 0])
# print "[4, 0, 0, 0]"
# print ""
# print merge([2, 2, 2, 2, 2])
# print "[4, 4, 2, 0, 0]"
# print ""
# print merge([8, 16, 16, 8])
# print "[8, 32, 8, 0]"
