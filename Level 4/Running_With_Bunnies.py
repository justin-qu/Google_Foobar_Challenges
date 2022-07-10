"""
Running with Bunnies
====================

You and the bunny workers need to get out of this collapsing death trap of a
space station -- and fast! Unfortunately, some of the bunnies have been weakened
by their long work shifts and can't run very fast. Their friends are trying to
help them, but this escape would go a lot faster if you also pitched in. The
defensive bulkhead doors have begun to close, and if you don't make it through
in time, you'll be trapped! You need to grab as many bunnies as you can and get
through the bulkheads before they close. 

The time it takes to move from your starting point to all of the bunnies and to
the bulkhead will be given to you in a square matrix of integers. Each row will
tell you the time it takes to get to the start, first bunny, second bunny, ...,
last bunny, and the bulkhead in that order. The order of the rows follows the
same pattern (start, each bunny, bulkhead). The bunnies can jump into your arms,
so picking them up is instantaneous, and arriving at the bulkhead at the same
time as it seals still allows for a successful, if dramatic, escape. (Don't
worry, any bunnies you don't pick up will be able to escape with you since they
no longer have to carry the ones you did pick up.) You can revisit different
spots if you wish, and moving to the bulkhead doesn't mean you have to immediate
ly leave -- you can move to and from the bulkhead to pick up additional bunnies
if time permits.

In addition to spending time traveling between bunnies, some paths interact
with the space station's security checkpoints and add time back to the clock.
Adding time to the clock will delay the closing of the bulkhead doors, and if
the time goes back up to 0 or a positive number after the doors have already
closed, it triggers the bulkhead to reopen. Therefore, it might be possible to
walk in a circle and keep gaining time: that is, each time a path is traversed,
the same amount of time is used or added.

Write a function of the form solution(times, time_limit) to calculate the most
bunnies you can pick up and which bunnies they are, while still escaping through
the bulkhead before the doors close for good. If there are multiple sets of
bunnies of the same size, return the set of bunnies with the lowest worker IDs
(as indexes) in sorted order. The bunnies are represented as a sorted list by
worker ID, with the first bunny being 0. There are at most 5 bunnies, and
time_limit is a non-negative integer that is at most 999.

For instance, in the case of
[
  [0, 2, 2, 2, -1],  # 0 = Start
  [9, 0, 2, 2, -1],  # 1 = Bunny 0
  [9, 3, 0, 2, -1],  # 2 = Bunny 1
  [9, 3, 2, 0, -1],  # 3 = Bunny 2
  [9, 3, 2, 2,  0],  # 4 = Bulkhead
]
and a time limit of 1, the five inner array rows designate the starting point,
bunny 0, bunny 1, bunny 2, and the bulkhead door exit respectively. You could
take the path:

Start End Delta Time Status
    -   0     -    1 Bulkhead initially open
    0   4    -1    2
    4   2     2    0
    2   4    -1    1
    4   3     2   -1 Bulkhead closes
    3   4    -1    0 Bulkhead reopens; you and the bunnies exit

With this solution, you would pick up bunnies 1 and 2. This is the best
combination for this space station hallway, so the solution is [1, 2].

Test cases
==========
Input:
solution.solution([[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]], 1)
Output:
    [1, 2]

Input:
solution.solution([[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]], 3)
Output:
    [0, 1]

"""
from itertools import permutations

def solution(times, times_limit):
    N = len(times)
    distance = [0] * N
    distance[0] = 0

    for _ in range(N - 2):
        for u in range(N):
            for v in range(N):
                if u == v:
                    continue

                distance[v] = min(distance[v], distance[u] + times[u][v])

    for u in range(N):
        for v in range(N):
            if u == v:
                continue

            if distance[u] + times[u][v] < distance[v]:
                return list(range(N - 2))

    apsp = [[10000000] * N for _ in range(N)]
    re_dist = [[0] * N for _ in range(N)]

    for u in range(N):
        for v in range(N):
            if u == v:
                continue

            re_dist[u][v] = times[u][v] + distance[u] - distance[v]

    def dijkstra(start, dist):
        ## nonlocal re_dist
        
        dist[start] = 0
        queue = set(range(N))

        while len(queue) > 0:
            min_dist = 10000000
            min_node = 0
            
            for node in queue:
                if dist[node] < min_dist:
                    min_dist = dist[node]
                    min_node = node
                    
            queue.remove(min_node)

            for v in range(N):
                dist[v] = min(dist[v], dist[min_node] + re_dist[min_node][v])

    for s in range(N):
        dijkstra(s, apsp[s])

    best_perm = ()

    for i in range(1, N - 1):
        for perm in permutations(range(1, N - 1), i):
            total_time = apsp[0][perm[0]] - distance[0]
            
            for j in range(1, len(perm)):
                total_time += apsp[perm[j-1]][perm[j]]

            total_time += apsp[perm[-1]][N - 1] + distance[N - 1]

            if total_time > times_limit:
                continue
            elif len(perm) > len(best_perm):
                best_perm = perm
                break
                
    return sorted([x-1 for x in best_perm])
