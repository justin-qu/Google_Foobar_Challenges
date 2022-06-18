/*
Gearing Up for Destruction
==========================

As Commander Lambda's personal assistant, you've been assigned the task of 
configuring the LAMBCHOP doomsday device's axial orientation gears. It should 
be pretty simple -- just add gears to create the appropriate rotation ratio. 
But the problem is, due to the layout of the LAMBCHOP and the complicated 
system of beams and pipes supporting it, the pegs that will support the gears 
are fixed in place. The LAMBCHOP's engineers have given you lists identifying 
the placement of groups of pegs along various support beams. You need to place 
a gear on each peg (otherwise the gears will collide with unoccupied pegs). The 
engineers have plenty of gears in all different sizes stocked up, so you can 
choose gears of any size, from a radius of 1 on up. Your goal is to build a 
system where the last gear rotates at twice the rate (in revolutions per minute, 
or rpm) of the first gear, no matter the direction. Each gear (except the last) 
touches and turns the gear on the next peg to the right.

Given a list of distinct positive integers named pegs representing the location 
of each peg along the support beam, write a function solution(pegs) which, if there
is a solution, returns a list of two positive integers a and b representing the 
numerator and denominator of the first gear's radius in its simplest form in order to 
achieve the goal above, such that radius = a/b. The ratio a/b should be greater than 
or equal to 1. Not all support configurations will necessarily be capable of creating 
the proper rotation ratio, so if the task is impossible, the function solution(pegs) 
should return the list [-1, -1].

For example, if the pegs are placed at [4, 30, 50], then the first gear could have a 
radius of 12, the second gear could have a radius of 14, and the last one a radius of 6. 
Thus, the last gear would rotate twice as fast as the first one. In this case, pegs 
would be [4, 30, 50] and solution(pegs) should return [12, 1].

The list pegs will be given sorted in ascending order and will contain at least 2 and no 
more than 20 distinct positive integers, all between 1 and 10000 inclusive.

Test cases
==========

Input:
Solution.solution({4, 17, 50})
Output:
    -1,-1

Input:
Solution.solution({4, 30, 50})
Output:
    12,1
*/

public class Solution 
{
    public static int[] solution(int[] pegs) 
    {
        int N = pegs.length;
        int[] gears = new int[N];
        int[] ret = {-1, -1};
        int offset = 0;
        int upp_limit = 0;
        int bot_limit = 0;
        
        for (int i = 1; i < N; i++)
        {
            if (pegs[i] - pegs[i - 1] < 2)
            {
                return ret;
            }
        }
        
        gears[0] = (pegs[1] - pegs[0]) / 2;
        upp_limit = pegs[1] - pegs[0] - gears[0] - 1;
        bot_limit = 1 - gears[0];
        
        for (int i = 1; i < N; i++)
        {
            gears[i] = pegs[i] - pegs[i - 1] - gears[i - 1];
            if (i % 2 == 0)
            {
                bot_limit = Math.max(bot_limit, 1 - gears[i]);
            }
            else
            {
                upp_limit = Math.min(upp_limit, gears[i] - 1);
            }
            
            if (bot_limit > upp_limit)
            {
                return ret;
            }
        }
        
        if (N % 2 == 0)
        {
            offset = -(gears[0] - (2 * gears[N - 1]));
            if ((float) offset / 3 < bot_limit || (float) offset / 3 > upp_limit)
            {
                return ret;
            }
            
            if (offset % 3 == 0)
            {
                ret[0] = gears[0] + offset / 3;
                ret[1] = 1;
                return ret;
            }
            else
            {
                ret[0] = 3 * gears[0] + offset;
                ret[1] = 3;
                return ret;
            }
        }
        else
        {
            offset = gears[0] - (2 * gears[N - 1]);
            if (offset < bot_limit || offset > upp_limit)
            {
                return ret;
            }
            
            ret[0] = gears[0] + offset;
            ret[1] = 1;
            return ret;
        }
    }
}