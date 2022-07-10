"""
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous
escape pods full of bunnies. But -- oh no! -- one of the escape pods has flown
into a nearby nebula, causing you to lose track of it. You start monitoring the
nebula, but unfortunately, just a moment too late to find where the pod went.
However, you do find that the gas of the steadily expanding nebula follows a
simple pattern, meaning that you should be able to determine the previous state
of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and
distributed in distinct patches, so you can model it as a 2D grid. You find that
the current existence of gas in a cell of the grid is determined exactly by its
4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell
to the right of it, and (4) the cell below and to the right of it. If, in the
current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will
also have gas in the next state. Otherwise, the cell will be empty in the next
state.

For example, let's say the previous state of the grid (p) was:
.O..
..O.
...O
O...

To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
.O -> O
..

Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:
O. -> .
.O

Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
O.O
.O.
O.O

Note that the resulting output will have 1 fewer row and column, since the
bottom and rightmost cells do not have a cell below and to the right of them,
respectively.

Write a function solution(g) where g is an array of array of bools saying
whether there is gas in each cell (the current scan of the nebula), and return
an int with the number of possible previous states that could have resulted in
that grid after 1 time step.  For instance, if the function were given the
current state c above, it would deduce that the possible previous states were
p (given above) as well as its horizontal and vertical reflections, and would
return 4. The width of the grid will be between 3 and 50 inclusive, and the
height of the grid will be between 3 and 9 inclusive.  The solution will always
be less than one billion (10^9).

Test cases
==========

Input:
solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
Output:
    11567

Input:
solution.solution([[True, False, True], [False, True, False], [True, False, True]])
Output:
    4

Input:
solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
Output:
    254

"""
from itertools import product
from collections import defaultdict

def transpose(g):
    return tuple([tuple([g[j][i] for j in range(len(g))]) for i in range(len(g[0]))])
    
def step(g):
    H = len(g)
    W = len(g[0])

    next_g = [[False] * (W - 1) for _ in range(H - 1)]

    for i in range(H - 1):
        for j in range(W - 1):
            t = g[i][j] + g[i + 1][j] + g[i][j + 1] + g[i + 1][j + 1]
            if t == 1:
                next_g[i][j] = True

    return tuple([tuple(i) for i in next_g])

class Segment:
    def __init__(self):
        self.top = defaultdict(lambda: defaultdict(int))
        self.bot = defaultdict(lambda: defaultdict(int))
        
def solution(g):
    G = transpose(g)
    H = len(G) + 1
    W = len(G[0]) + 1

    arr = []
    for seq in product((False, True), repeat = W):
        arr.append(seq)

    row_to_segment = dict()
    curr_g = []

    for row in G:
        row_to_segment[row] = Segment()

    for row in G:
        curr_g.append(row_to_segment[row])

    for i, seqi in enumerate(arr):
        for j, seqj in enumerate(arr):
            result = step((seqi, seqj))

            if result[0] in row_to_segment:
                s = row_to_segment[result[0]]
                s.top[i][j] += 1
                s.bot[j][i] += 1

    next_g = []

    while len(curr_g) > 1:
        index = 0
        while index + 1 < len(curr_g):
            new_segment = Segment()
            next_g.append(new_segment)

            top_segment = curr_g[index]
            bot_segment = curr_g[index + 1]
            index += 2

# Python 2: for row in top_segment.bot.viewkeys() & bot_segment.top.viewkeys():
            for row in top_segment.bot.keys() & bot_segment.top.keys():
                possible_tops = top_segment.bot[row]
                possible_bots = bot_segment.top[row]

                for top_k, top_v in possible_tops.items():
                    for bot_k, bot_v in possible_bots.items():
                        new_segment.top[top_k][bot_k] += (top_v * bot_v)
                        new_segment.bot[bot_k][top_k] = new_segment.top[top_k][bot_k]

        if index < len(curr_g):
            next_g.append(curr_g[index])

        curr_g = next_g
        next_g = []

    return sum([sum(d.values()) for d in curr_g[0].top.values()])
