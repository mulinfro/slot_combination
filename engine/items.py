
from collections import namedtuple
ParamItem = namedtuple('ParamItem', ['tp', 'val'])
TNode = namedtuple('TNode', ['name', 'slices', 'permutation'])

# SpecialRulePost = namedtuple('SpecialRulePost', ['tag', 'start', 'end'])

"""
tag_type: str
   0: atom
   1: ref
   2: plus
   3: 需要特殊处理的atom或变量
"""
AcMatchedGroup = namedtuple('AcMatchedGroup', ['start', 'end', 'tag', 'tag_type'])

class AnyPat:

    def __init__(self, min_span, max_span):
        self.min_span = min_span
        self.max_span = max_span

    def is_valid(self, n):
        if n >= self.min_span:
            if self.max_span < 0:
                return True
            else:
                return n <= self.max_span

    def to_pat(self):
        return "__ANY__:%d:%d"%(self.min_span, self.max_span)

    def equal(self, min_s, max_s):
        return self.min_span == min_s and self.max_span == max_s

    def get_max_dist(self, cur, maxl):
        if self.max_span < 0:
            return maxl
        else:
            return min(cur + self.max_span, maxl)

class MatchedItem:

    def __init__(self, tagkey, fragments, tnodes):
        self.tagkey = tagkey
        self.fragments = fragments
        self.tnodes = tnodes
        self.matched = ""
        self.match_score = 0
        self.fuzzy_degree = 0
        self.begin = 0
        self.end = 0

    def __repr__(self):
        return "(%s,%d,%d)"%(self.matched, self.begin, self.end)

    def score(self):
        matched_length = len(self.fragments)
        for t in self.fragments:
            matched_length += t[3] - t[2]
        miss_length = self.end - self.begin + 1 - matched_length
        return (matched_length, miss_length)

    def cal_index(self):
        self.begin =  self.fragments[0][0] 
        self.end   =  self.fragments[-1][1] 

    def cal_match_score(self, dialog):
        eles = self.tagkey.strip("#").split("#")
        assert len(eles) == len(self.fragments), "Need match"
        self.cal_index()

        frags = []
        for i, idx in enumerate(self.fragments):
            bi, ei = idx[0], idx[1]
            frags.append((dialog[bi: ei + 1], eles[i], bi, ei))
        self.fragments = frags

        self.matched = dialog[self.begin: self.end + 1]
        sv = self.score()
        self.match_score = sv[0] / len(dialog)
        self.fuzzy_degree = sv[1] / sv[0]
