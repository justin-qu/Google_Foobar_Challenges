"""
Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing
Commander Lambda's bunny workers, but once they're free of the work duties the
bunnies are going to need to escape Lambda's space station via the escape pods
as quickly as possible. Unfortunately, the halls of the space station are a maze
of corridors and dead ends that will be a deathtrap for the escaping bunnies.
Fortunately, Commander Lambda has put you in charge of a remodeling project that
will give you the opportunity to make things a little easier for the bunnies.
Unfortunately (again), you can't just remove all obstacles between the bunnies
and the escape pods - at most you can remove one wall per escape pod path, both
to maintain structural integrity of the station and to avoid arousing Commander
Lambda's suspicions. 

You have maps of parts of the space station, each starting at a work area exit
and ending at the door to an escape pod. The map is represented as a matrix of
0s and 1s, where 0s are passable space and 1s are impassable walls. The door out
of the station is at the top left (0,0) and the door into an escape pod is at
the bottom right (w-1,h-1). 

Write a function solution(map) that generates the length of the shortest path
from the station door to the escape pod, where you are allowed to remove one
wall as part of your remodeling plans. The path length is the total number of
nodes you pass through, counting both the entrance and exit nodes. The starting
and ending positions are always passable (0). The map will always be solvable,
though you may or may not need to remove a wall. The height and width of the map
can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal
moves are allowed.

Test cases
==========

Input:
solution.solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])
Output:
    7

Input:
solution.solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
Output:
    11
"""

def solution(_map):
    def get_adj_coords(y, x):
        adj_coords = set()

        if x > 0:
            adj_coords.add((y, x - 1))
        if x < W - 1:
            adj_coords.add((y, x + 1))

        if y > 0:
            adj_coords.add((y - 1, x))
        if y < H - 1:
            adj_coords.add((y + 1, x))

        return adj_coords
    
    H = len(_map)
    W = len(_map[0])

    dist = [[0] * W for h in range(H)]
    dist_break = [[0] * W for h in range(H)]
    visited = [[False] * W for h in range(H)]
    visited_break = [[False] * W for h in range(H)]

    dist[0][0] = 1
    dist_break[0][0] = -1
    visited[0][0] = True
    visited_break[0][0] = True

    stack = [(0, 0)]
    index = 0

    while index < len(stack):
        y, x = stack[index]
        index += 1
        
        adj_coords = get_adj_coords(y, x)
        
        for _y, _x in adj_coords:
            if dist[y][x] != 0:
                if _map[_y][_x] == 0 and visited[_y][_x] == False:
                    dist[_y][_x] = dist[y][x] + 1
                    visited[_y][_x] = True
                    if visited_break[_y][_x] == False or dist_break[_y][_x] == dist[_y][_x]:
                        dist_break[_y][_x] = -1
                        visited_break[_y][_x] = True
                    stack.append((_y, _x))
                elif _map[_y][_x] == 1 and visited_break[_y][_x] == False:
                    dist_break[_y][_x] = dist[y][x] + 1
                    visited_break[_y][_x] = True
                    stack.append((_y, _x))

            else:
                if _map[_y][_x] == 0 and visited_break[_y][_x] == False:
                    dist_break[_y][_x] = dist_break[y][x] + 1
                    visited_break[_y][_x] = True
                    if stack[-1] != (_y, _x):
                        stack.append((_y, _x))

        if (H - 1, W - 1) in adj_coords:
            for i in dist:
                print(i)
            print()
            for i in dist_break:
                print(i)
                
            if dist[H - 1][W - 1] == 0:
                return dist_break[H - 1][W - 1]
            elif dist_break[H - 1][W - 1] < 1:
                return dist[H - 1][W - 1]
            else:
                return min(dist[H - 1][W - 1], dist_break[H - 1][W - 1])
            
