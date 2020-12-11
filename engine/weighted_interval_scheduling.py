
import collections
import bisect
from functools import cmp_to_key

"""
Weighted Interval scheduling algorithm.
Runtime complexity: O(n log n)
"""

class Interval(object):
    '''Date weighted interval'''

    def __init__(self, title, start, finish):
        self.title = title
        self.start = start
        self.finish = finish
        self.weight = weight_socre(finish - start + 1)

    def __repr__(self):
        return str((self.title, self.start, self.finish, self.weight))

def weight_socre(w):
    # 长度越长分数会越高
    return w + (w-1) / 10

def list2Intervals(lst):
    I = []
    for l in lst:
        I.append(Interval(l[0], l[1], l[2]))
    return I

def compute_best_cover(lst):
    I = list2Intervals(lst)
    return schedule_weighted_intervals(I)

def custom_cmp(left, right):
    if left.finish == right.finish:
        return left.weight - right.weight
    else:
        return left.finish - right.finish

def search_rightmost_valid(finish, s, j):
    for i in range(j-1, -1, -1):
        if finish[i] < s: return i
    return -1

def compute_previous_intervals(I):
    '''For every interval j, compute the rightmost mutually compatible interval i, where i < j
    I is a sorted list of Interval objects (sorted by finish time)
    '''
    # extract start and finish times
    start = [i.start for i in I]
    finish = [i.finish for i in I]

    p = []
    for j in range(len(I)):
        #i = bisect.bisect_left(finish, start[j]) - 1  # rightmost interval f_i <= s_j
        i = search_rightmost_valid(finish, start[j], j)
        p.append(i)

    return p

def schedule_weighted_intervals(I):
    '''Use dynamic algorithm to schedule weighted intervals
    sorting is O(n log n),
    finding p[1..n] is O(n log n),
    finding OPT[1..n] is O(n),
    selecting is O(n)
    whole operation is dominated by O(n log n)
    '''

    I.sort(key = cmp_to_key(custom_cmp))  # f_1 <= f_2 <= .. <= f_n
    p = compute_previous_intervals(I)

    # compute OPTs iteratively in O(n), here we use DP
    OPT = collections.defaultdict(int)
    OPT[-1] = 0
    #OPT[0] = I[0].weight
    for j in range(0, len(I)):
        OPT[j] = max(I[j].weight + OPT[p[j]], OPT[j - 1])

    # given OPT and p, find actual solution intervals in O(n)
    O = []
    def compute_solution(j):
        if j >= 0:  # will halt on OPT[-1]
            if I[j].weight + OPT[p[j]] > OPT[j - 1]:
                O.append(I[j])
                compute_solution(p[j])
            else:
                compute_solution(j - 1)

    compute_solution(len(I) - 1)
    # resort, as our O is in reverse order (OPTIONAL)
    O.sort(key = lambda x: x.finish)
    return O

def test():
    I = []
    I.append(Interval("A" , 0, 0))
    I.append(Interval("AB" , 0,1))
    I.append(Interval("B" , 1,1))
    I.append(Interval("CD" , 2,3))
    I.append(Interval("D" , 3,3))
    """
    0 0 播 播 OP
    0 1 播放 播放 OP
    1 1 放 放 OP
    2 3 文爱 文爱 GQM
    3 3 爱 爱 GQM
    I.append(Interval("A" , 2, 3))
    I.append(Interval("Semester 2" , 3,3))
    I.append(Interval("Semester 2" , 4,4))
    I.append(Interval("Trimester 1" , 6,8))
    I.append(Interval("Trimester 3" , 9,10))
    """
    O = schedule_weighted_intervals(I)
    print(O)

if __name__ == '__main__':
    test()
